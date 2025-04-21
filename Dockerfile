FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

## 配置 pip 镜像源
#RUN mkdir -p /root/.pip && \
#    echo "[global]" > /root/.pip/pip.conf && \
#    echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> /root/.pip/pip.conf && \
#    echo "trusted-host = pypi.tuna.tsinghua.edu.cn" >> /root/.pip/pip.conf \

# 创建数据库目录并设置权限
RUN mkdir -p /app/db && \
    touch /app/db/db.sqlite3 && \
    chmod 666 /app/db/db.sqlite3

# 安装git和其他依赖
RUN apt-get update && apt-get install -y git vim

# 复制项目文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "excel_site.wsgi"]