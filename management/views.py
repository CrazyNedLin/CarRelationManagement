from datetime import datetime

from django.contrib import messages
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from customer.models import CustomerRecord
from login.models import Attendance  # 引入 Attendance 模型
from .form import CustomerRecordQueryForm, ExpenseForm, ExpenseQueryForm
from .models import Expense


@csrf_exempt
def attendance_query(request):
  # 獲取當前年份和月份的選項
  current_year = datetime.now().year
  year_choices = list(range(2020, current_year + 1))
  month_choices = list(range(1, 13))

  if request.method == "GET":
    return render(request, './management/attendance_query.html', {
      'year_choices': year_choices,
      'month_choices': month_choices
    })
  elif request.method == "POST":
    year = int(request.POST.get('year'))
    month = int(request.POST.get('month'))

    # 篩選當月的考勤紀錄
    attendance_records = Attendance.objects.filter(
        Q(check_in_time__year=year, check_in_time__month=month) |
        Q(check_out_time__year=year, check_out_time__month=month)
    )

    return render(request, './management/attendance_query.html', {
      'attendance_records': attendance_records,
      'year': year,
      'month': month,
      'year_choices': year_choices,
      'month_choices': month_choices
    })


def customer_record_query(request):
  form = CustomerRecordQueryForm(request.GET or None)
  results = CustomerRecord.objects.none()  # 預設為空的 QuerySet
  total_amount = 0  # 預設總金額為 0

  if form.is_valid():
    start_date = form.cleaned_data.get('start_date')
    end_date = form.cleaned_data.get('end_date')

    # 根據日期範圍過濾 CustomerRecord
    results = CustomerRecord.objects.filter(date__range=[start_date, end_date])

    # 計算 'amount' 的總和
    total_amount = results.aggregate(total=Sum('amount'))['total'] or 0

  return render(
      request,
      './management/customer_record_query.html',  # 注意這裡不需要 './'
      {
        'form': form,
        'results': results,
        'total_amount': total_amount,
      }
  )


def delete_customer_record(request, record_id):
  record = get_object_or_404(CustomerRecord, id=record_id)
  if request.method == 'POST':
    record.delete()
    messages.success(request, '記錄已成功刪除。')
  return redirect('customer_record_query')


def create_expense(request):
  if request.method == 'POST':
    form = ExpenseForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('expense_list')
  else:
    form = ExpenseForm()
  return render(request, './management/expense_form.html', {'form': form})


def expense_list(request):
  expenses = []
  if request.method == 'POST':
    form = ExpenseQueryForm(request.POST)
    if form.is_valid():
      year = form.cleaned_data['year']
      month = form.cleaned_data['month']
      expenses = Expense.objects.filter(date__year=year, date__month=month)
  else:
    form = ExpenseQueryForm()

  return render(request, './management/expense_list.html',
                {'form': form, 'expenses': expenses})


def view_receipt(request, pk):
  expense = get_object_or_404(Expense, pk=pk)
  return render(request, './management/view_receipt.html', {'expense': expense})
