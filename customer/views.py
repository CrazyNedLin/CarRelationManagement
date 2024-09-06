from django.shortcuts import render, get_object_or_404, redirect

from .forms import CustomerForm, VehicleFormSet, CustomerRecordForm
from .models import Customer, Vehicle, CustomerRecord


def customer_search(request):
  if request.method == 'POST':
    phone = request.POST.get('phone')
    plate_number = request.POST.get('plate_number')

    if phone:
      try:
        customer = Customer.objects.get(phone=phone)
        return redirect('customer_maintain', customer_id=customer.customer_id)
      except Customer.DoesNotExist:
        return redirect('customer_add')

    elif plate_number:
      try:
        vehicle = Vehicle.objects.get(plate_number=plate_number)
        customer = vehicle.customer
        return redirect('customer_maintain', customer_id=customer.customer_id)
      except Vehicle.DoesNotExist:
        return redirect('customer_add')

  return render(request, './customer/customer_search.html')


def customer_add(request):
  referral_customers = Customer.objects.all()  # 可以作為介紹人的顧客清單

  if request.method == 'POST':
    form = CustomerForm(request.POST)
    vehicle_formset = VehicleFormSet(request.POST, request.FILES)
    if form.is_valid() and vehicle_formset.is_valid():
      # 先保存 customer，但不提交到數據庫
      customer = form.save(commit=False)

      # 設定介紹人
      referral_id = request.POST.get('referral_id')
      if referral_id:
        try:
          referral = Customer.objects.get(id=referral_id)
          customer.referral = referral
        except Customer.DoesNotExist:
          referral = None

      # 現在將 customer 保存到數據庫
      customer.save()

      # 將 vehicle_formset 與該 customer 關聯
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
    'referral_customers': referral_customers,
  })


def customer_maintain(request, customer_id):
  customer = get_object_or_404(Customer, customer_id=customer_id)
  referral_customers = Customer.objects.exclude(
      customer_id=customer.customer_id
  ).exclude(referral=customer)

  if request.method == 'POST':
    form = CustomerForm(request.POST, instance=customer)
    vehicle_formset = VehicleFormSet(request.POST, request.FILES,
                                     instance=customer)

    if form.is_valid() and vehicle_formset.is_valid():
      customer = form.save(commit=False)

      referral_id = request.POST.get('referral_id')
      if referral_id:
        try:
          referral = Customer.objects.get(id=referral_id)
          customer.referral = referral
        except Customer.DoesNotExist:
          referral = None

      customer.save()
      vehicle_formset.save()
      return redirect('customer_search')
  else:
    form = CustomerForm(instance=customer)
    vehicle_formset = VehicleFormSet(instance=customer)  # 初始化 formset

  return render(request, './customer/customer_form.html', {
    'form': form,
    'vehicle_formset': vehicle_formset,
    'customer': customer,
    'mode': 'maintain',
    'referral_customers': referral_customers,
  })


def customer_record_create_view(request):
  if request.method == 'POST':
    form = CustomerRecordForm(request.POST)
    if form.is_valid():
      vehicle = form.cleaned_data['vehicle']
      customer = vehicle.customer
      if customer:  # 確保 customer 存在
        print(f"Customer ID: {customer.customer_id}")  # 調試語句
        record = form.save(commit=False)
        record.customer = customer
        record.save()
        return redirect('customer_record_list',
                        customer_id=customer.customer_id)
      else:
        print("Vehicle does not have an associated customer.")  # 調試語句
        return redirect('customer_search')  # 或其他適當的處理
    else:
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
      customer = vehicle.customer
    except Vehicle.DoesNotExist:
      error_message = '找不到相關車輛信息'
      customer = None

  return render(request, './customer/customer_record_form.html',
                {'form': form, 'vehicle': vehicle, 'customer': customer,
                 'error_message': error_message})


def customer_recordlist_view(request):
  records = CustomerRecord.objects.all()
  return render(request, './customer/customer_record_list.html',
                {'records': records})
