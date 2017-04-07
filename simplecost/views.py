from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.urlresolvers import reverse_lazy

import json

from .models import ThirdParty, PaymentMode, Expense

from .forms import ExpenseForm

from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class ExpenseListView(ListView):
    """
    Display a list of expenses for the request user
    """
    
    model = Expense
    context_object_name = 'expenses'
    
    def get_queryset(self):
        
        queryset = Expense.objects.filter(property_of=self.request.user).order_by('-date_expense')
        
        return queryset
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExpenseListView, self).dispatch(*args, **kwargs)

class ExpenseCreate(AjaxableResponseMixin, CreateView):
    """
    View to create an expense. Works with ajax.
    """
    
    model = Expense
    form_class = ExpenseForm
    template_name = 'simplecost/expense_create_form.html'
    
    def form_valid(self, form):
        form.instance.property_of = self.request.user
        return super(ExpenseCreate, self).form_valid(form)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExpenseCreate, self).dispatch(*args, **kwargs)
    
def print_it(request):
    """
    Create a pdf file with the list of all expenses
    ordered by oldest expenses
    """
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="expenses.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = SimpleDocTemplate(response, pagesize=letter)
        
    expenses = Expense.objects.filter(property_of=request.user).order_by('date_expense')
    
    # container for the 'Flowable' objects
    elements = []
    
    # container for the table content
    table_data = []
    
    table_data.append(['Date', 'Third party', 'Amount','Payment mode','Notes'])
    
    for i, expense in enumerate(expenses):
        # Add a row to the table
        table_data.append([expense.date_expense, expense.third_party, str(expense.amount) + ' €',expense.payment_mode,expense.notes])
    
    # Create the table
    expense_table = Table(table_data)
    
    # Add grid an font for table 
    expense_table.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                        ('FONTNAME',(0,0),(-1,-1),'Courier'),
                                        ]))
    
    elements.append(expense_table)
    
    p.build(elements)
    
    return response