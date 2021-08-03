FROM python:3.8

EXPOSE 5006

WORKDIR /app

COPY requirements.txt /app
RUN pip install  -r requirements.txt --upgrade pip


COPY . /app
CMD python app.py