from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Vehicle, CustomerRecord
from .forms import CustomerForm, VehicleFormSet, CustomerRecordForm


def customer_search(request):
  if request.method == 'POST':
    phone = request.POST.get('phone')
    try:
      customer = Customer.objects.get(phone=phone)
      return redirect('customer_maintain', customer_id=customer.customer_id)
    except Customer.DoesNotExist:
      return redirect('customer_add')

  return render(request, './customer/customer_search.html')


def customer_add(request):
  if request.method == 'POST':
    form = CustomerForm(request.POST)
    vehicle_formset = VehicleFormSet(request.POST, request.FILES)
    if form.is_valid() and vehicle_formset.is_valid():
      customer = form.save()
      vehicle_formset.instance = customer
      vehicle_formset.save()
      return redirect('customer_search')
  else:
    form = CustomerForm()
    vehicle_formset = VehicleFormSet()

  return render(request, './customer/customer_form.html', {
    'form': form,
    'vehicle_formset': vehicle_formset,
    'mode': 'add',
  })


def customer_maintain(request, customer_id):
  customer = get_object_or_404(Customer, customer_id=customer_id)
  vehicle_formset = VehicleFormSet(instance=customer)
  if request.method == 'POST':
    form = CustomerForm(request.POST, instance=customer)
    vehicle_formset = VehicleFormSet(request.POST, request.FILES,
                                     instance=customer)
    if form.is_valid() and vehicle_formset.is_valid():
      form.save()
      vehicle_formset.save()
      return redirect('customer_search')
  else:
    form = CustomerForm(instance=customer)

  return render(request, './customer/customer_form.html', {
    'form': form,
    'vehicle_formset': vehicle_formset,
    'customer': customer,
    'mode': 'maintain',
  })


def customer_record_create_view(request):
  if request.method == 'POST':
    form = CustomerRecordForm(request.POST)
    if form.is_valid():
      vehicle = form.cleaned_data['vehicle']
      customer = vehicle.customer
      record = form.save(commit=False)
      record.customer = customer
      record.save()
      return redirect('customer_record_list')  # 保存成功後重定向到紀錄列表頁面
    else:
      # 如果表單未通過驗證，顯示表單錯誤
      print(form.errors)
  else:
    form = CustomerRecordForm()

  return render(request, './customer/customer_record_form.html', {'form': form})


def search_by_license_plate(request):
  license_plate = request.GET.get('license_plate')
  vehicle = None
  form = CustomerRecordForm()
  error_message = None

  if license_plate:
    try:
      vehicle = Vehicle.objects.get(plate_number=license_plate)
      form.fields['vehicle'].initial = vehicle.id
    except Vehicle.DoesNotExist:
      error_message = '找不到相關車輛信息'

  return render(request, './customer/customer_record_form.html',
                {'form': form, 'vehicle': vehicle,
                 'customer': vehicle.customer if vehicle else None,
                 'error_message': error_message})


def customer_recordlist_view(request):
  records = CustomerRecord.objects.all()
  return render(request, './customer/customer_record_list.html',
                {'records': records})
