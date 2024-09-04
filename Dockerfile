# 使用官方的 Python 基礎鏡像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安装系统依赖和构建工具
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案所有檔案到容器中
COPY . /app/

# 暴露Django服務使用的端口
EXPOSE 8000

# 運行Django開發服務
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]