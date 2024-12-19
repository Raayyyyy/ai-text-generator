FROM python:3.9-slim

# 使用阿里云的 pip 镜像源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "run.py"] 