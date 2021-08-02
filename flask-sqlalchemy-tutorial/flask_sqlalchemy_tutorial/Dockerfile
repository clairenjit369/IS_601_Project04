FROM python:3.8

EXPOSE 5008

WORKDIR /flask_sqlalchemy_tutorial

COPY requirements.txt /flask_sqlalchemy_tutorial
RUN pip install -r requirements.txt --upgrade pip

COPY . /flask_sqlalchemy_tutorial

ENV SECRET_KEY=GDtfDCFYjD
ENV FLASK_APP=PartIX
ENV FLASK_ENV=development
ENV SQLALCHEMY_DATABASE_URI=TODO

CMD python routes.py