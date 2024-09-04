import os
import uuid

from django.db import models


def upload_to(instance, filename):
  # 獲取文件的擴展名
  ext = filename.split('.')[-1]
  # 生成唯一的檔名
  filename = f'{uuid.uuid4()}.{ext}'
  # 返回保存的路徑
  return os.path.join('receipts', filename)


class Expense(models.Model):
  date = models.DateField()
  item = models.CharField(max_length=200)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  payment_method = models.CharField(max_length=50, choices=[('cash', '現金'), (
  'credit_card', '信用卡'), ('bank_transfer', '銀行轉帳')])
  receipt = models.ImageField(upload_to=upload_to, blank=True, null=True)
  category = models.CharField(max_length=50, choices=[('fixed', '固定支出'),
                                                      ('variable', '變動支出')])
  remarks = models.TextField(blank=True, null=True)

  def __str__(self):
    return f'{self.date} - {self.item}'
