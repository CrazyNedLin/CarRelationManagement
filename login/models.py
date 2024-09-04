from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    _time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-_time']
        verbose_name = '用戶資料庫'
        verbose_name_plural = '用戶資料庫'


class Attendance(models.Model):
    account = models.CharField(max_length=255)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.account} - Check-in: {self.check_in_time}, Check-out: {self.check_out_time}"