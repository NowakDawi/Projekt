FROM python:3.12.9
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 8000
