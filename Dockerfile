FROM python:3.8-slim-bullseye

RUN pip install --upgrade pip
COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 80

ENTRYPOINT [ "./gunicorn.sh" ]