FROM python:3.12.9
ENV PYTHONUNBUFFERED=1
WORKDIR /home/dawid/PycharmProjects/PythonProject1
COPY requirements.txt ./
RUN pip install -r requirements.txt