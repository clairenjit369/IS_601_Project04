FROM python:3.8

EXPOSE 5005

WORKDIR /app6

COPY requirements.txt /app6
RUN pip install  -r requirements.txt --upgrade pip

COPY . /app6

CMD python app.py