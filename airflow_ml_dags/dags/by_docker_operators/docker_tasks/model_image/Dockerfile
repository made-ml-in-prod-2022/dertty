FROM python:3.10
USER root
RUN apt-get update && apt-get install git -y
RUN apt-get install python3-distutils -y
RUN apt-get install python3-apt -y
RUN pip install --upgrade pip
RUN mkdir /app
WORKDIR /app
ENV PYTHONUNBUFFERED 1

COPY . /app/
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "model.py"]