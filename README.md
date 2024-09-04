
### 1. 重設 `admin` 用戶密碼

如果你只是想重設 `admin` 用戶的密碼，可以使用以下命令：

```bash
python manage.py changepassword <admin-username>
```

將 `<admin-username>` 替換為你的管理員用戶名。

### 2. 刪除並重新創建 `admin` 用戶

如果你需要刪除並重新創建 `admin` 用戶，可以按照以下步驟操作：

1. **刪除 `admin` 用戶**

   首先，進入 Django shell：

   ```bash
   python manage.py shell
   ```

   然後執行以下代碼：

   ```python
   from django.contrib.auth.models import User
   User.objects.filter(username='<admin-username>').delete()
   ```

   將 `<admin-username>` 替換為你想要刪除的管理員用戶名。

2. **重新創建 `admin` 用戶**

   使用以下命令來重新創建管理員用戶：

   ```bash
   python manage.py createsuperuser
   ```

   按提示輸入用戶名、電子郵件和密碼。

### 3. 重設 `admin` 預設設置

如果你想要重設 `admin` 預設設置，可以刪除 `admin` 相關的數據表，並重新創建遷移檔。注意，這將刪除所有 `admin` 相關的數據：

1. **刪除 `admin` 數據表**

   在你的數據庫中，刪除 `django_admin_log` 和 `auth_user` 表（依你的數據庫而定）。

2. **重新創建遷移檔**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### 4. 刪除並重新安裝 `admin` 應用

如果你想要徹底重新安裝 `admin` 應用，可以嘗試以下步驟：

1. **卸載 Django**

   ```bash
   pip uninstall django
   ```

2. **重新安裝 Django**

   ```bash
   pip install django
   ```

3. **重新設置專案**

   創建一個新的 Django 專案，然後將你的應用程式遷移到新的專案中。

這些步驟應該能夠幫助你根據不同的需求重設 `admin`。如果有更具體的需求或問題，隨時告訴我！