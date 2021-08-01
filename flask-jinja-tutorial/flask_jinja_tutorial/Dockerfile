FROM python:3.8

EXPOSE 5001

WORKDIR /flask_jinja_tutorial

COPY requirements.txt /flask_jinja_tutorial
RUN pip install  -r requirements.txt --upgrade pip

COPY . /flask_jinja_tutorial

CMD python routes.py