from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import ThirdParty, PaymentMode, Expense

from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter

class ExpenseListView(ListView):
    """
    Display a list of expenses
    """
    
    model = Expense
    context_object_name = 'expenses'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExpenseListView, self).dispatch(*args, **kwargs)
    
def print_it(request):
    """
    Create de pdf file with the list of all expenses
    """
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = SimpleDocTemplate(response, pagesize=letter)
        
    expenses = Expense.objects.all()
    
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
    
    expense_table.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                        ]))
    
    elements.append(expense_table)
    
    p.build(elements)
    
    return response