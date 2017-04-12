from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.urlresolvers import reverse_lazy

import json

from datetime import date
from calendar import monthrange

from .models import ThirdParty, PaymentMode, Expense

from .forms import ExpenseForm

from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter

def quarter_range():
    """
    return the start date and the end date for the actual quarter of the year
    """
    quarter = [[1,3],[4,6],[7,9],[10,12]]
    
    start_date = date(date.today().year,quarter[date.today().month//3][0],1)
    
    end_date = date(date.today().year, quarter[date.today().month//3][1], monthrange(date.today().year,quarter[date.today().month//3][1])[1])

    return start_date, end_date


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
    The default queryset is all the values
    The user can filter values, his choice is store in a session's variable
    """
    
    model = Expense
    context_object_name = 'expenses'
    
    def get_queryset(self, *args, **kwargs):
        
        if not 'filterexpense' in self.request.session:
            self.request.session['filterexpense'] = 'All'
            self.request.session['filterexpensemonth'] = date.today().month
            self.request.session['filterexpenseyear'] = date.today().year
        
        if not self.request.GET.get("filter"):
            
            filter_expense = self.request.session['filterexpense']
        
        else:
            
            filter_expense = self.request.GET.get("filter")
        
        if filter_expense == "All":
                
            queryset = Expense.objects.filter(property_of=self.request.user).order_by('-date_expense')
            self.request.session['filterexpense'] = 'All'
            self.request.session['filterexpensemonth'] = date.today().month
            self.request.session['filterexpenseyear'] = date.today().year
            
        elif filter_expense == "This month":
            
            queryset = Expense.objects.filter(property_of=self.request.user,date_expense__year=date.today().year,date_expense__month=date.today().month).order_by('-date_expense')
            self.request.session['filterexpense'] = 'This month'
            self.request.session['filterexpensemonth'] = date.today().month
            self.request.session['filterexpenseyear'] = date.today().year
            
        elif filter_expense == "This quarter":
            
            queryset = Expense.objects.filter(property_of=self.request.user,date_expense__range=quarter_range()).order_by('-date_expense')
            self.request.session['filterexpense'] = 'This quarter'
            self.request.session['filterexpensemonth'] = date.today().month
            self.request.session['filterexpenseyear'] = date.today().year
        
        elif filter_expense == "Previous month":
            
            if not self.request.is_ajax():
                
                request_year = self.request.session['filterexpenseyear']
                request_month = self.request.session['filterexpensemonth']
            
            elif self.request.session['filterexpensemonth'] == 1:
                
                request_month = 12
                request_year = self.request.session['filterexpenseyear'] - 1
            
            else:
            
                request_year = self.request.session['filterexpenseyear']
                request_month = self.request.session['filterexpensemonth'] - 1
            
            queryset = Expense.objects.filter(property_of=self.request.user,date_expense__year=request_year,date_expense__month=request_month).order_by('-date_expense')
            self.request.session['filterexpense'] = 'Previous month'
            self.request.session['filterexpenseyear'] = request_year
            self.request.session['filterexpensemonth'] = request_month
            
        
        elif filter_expense == "Next month":
            
            if not self.request.is_ajax():
                
                request_year = self.request.session['filterexpenseyear']
                request_month = self.request.session['filterexpensemonth']
            
            elif self.request.session['filterexpensemonth'] == 12:
                
                request_month = 1
                request_year = self.request.session['filterexpenseyear'] + 1
            
            else:
            
                request_year = self.request.session['filterexpenseyear']
                request_month = self.request.session['filterexpensemonth'] + 1
            
            queryset = Expense.objects.filter(property_of=self.request.user,date_expense__year=request_year,date_expense__month=request_month).order_by('-date_expense')
            self.request.session['filterexpense'] = 'Next month'
            self.request.session['filterexpenseyear'] = request_year
            self.request.session['filterexpensemonth'] = request_month
        
        return queryset
    
    def get_template_names(self, *args, **kwargs):
        
        if self.request.method == 'GET' and self.request.is_ajax():
            
            template_name = 'simplecost/expense_list_table.html'

        else:
            
            template_name = 'simplecost/expense_list.html'
            
        return template_name
    
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

class ExpenseUpdate(AjaxableResponseMixin, UpdateView):
    """
    View to update an Expense. Works with ajax.
    Use default template expense_form.html
    """
    
    model = Expense
    form_class = ExpenseForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExpenseUpdate, self).dispatch(*args, **kwargs)
    
class ExpenseDelete(AjaxableResponseMixin, DeleteView):
    """
    View to delete an Expense. Works with ajax.
    Use default template expense_confirm_delete.html
    """
    
    model = Expense
    success_url = reverse_lazy('expense-list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExpenseDelete, self).dispatch(*args, **kwargs)
    
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