FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 创建数据库目录并设置权限
RUN mkdir -p /app/db && \
    touch /app/db/db.sqlite3 && \
    chmod 666 /app/db/db.sqlite3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "excel_site.wsgi"]