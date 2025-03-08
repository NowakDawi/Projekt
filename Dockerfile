FROM python:3.12.9
ENV PYTHONUNBUFFERED=1
WORKDIR /home/dawid/Documents/GitHub/Projekt
COPY requirements.txt ./
RUN pip install -r requirements.txt
