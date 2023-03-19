FROM python:3.10
WORKDIR /app
COPY requirements.txt .
COPY /orders .
RUN pip install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "orders.wsgi:application", "--bind", "0:8000" ]
