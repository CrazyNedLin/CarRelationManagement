from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Customer(models.Model):
    customer_id = models.CharField(max_length=6, unique=True, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField()

    def save(self, *args, **kwargs):
        if not self.customer_id:
            # 生成會員編號
            last_customer = Customer.objects.all().order_by('customer_id').last()
            if last_customer:
                last_id = last_customer.customer_id
                letter_part = last_id[:2]
                number_part = int(last_id[2:])
                if number_part < 9999:
                    number_part += 1
                else:
                    letter_part = chr(ord(letter_part[0]) + (ord(letter_part[1]) == 'Z'), ord(letter_part[1]) + 1)
                    number_part = 1
                self.customer_id = f'{letter_part}{str(number_part).zfill(4)}'
            else:
                self.customer_id = 'AA0001'
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '顧客資料庫'
        verbose_name_plural = '顧客資料庫'

class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, related_name='vehicles', on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.brand} {self.model} ({self.plate_number})'


class CustomerRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="顧客")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="車輛")
    date = models.DateField(verbose_name="日期")
    service_content = models.TextField(verbose_name="服務內容")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金額")

    def __str__(self):
        return f"{self.customer.name} - {self.date} - {self.vehicle.plate_number}"