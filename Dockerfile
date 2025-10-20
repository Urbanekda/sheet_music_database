FROM python:3.13.3-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y 

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY django_project /app

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]



