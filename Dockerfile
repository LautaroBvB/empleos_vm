FROM python:3.10-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "aplicacionmobile.wsgi:application", "--bind", "0.0.0.0:8000"]