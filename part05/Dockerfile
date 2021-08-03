FROM python:3.8

EXPOSE 5004

WORKDIR /app5

COPY requirements.txt /app5
RUN pip install  -r requirements.txt --upgrade pip

ENV SECRET_KEY=GDtfDCFYjD
ENV SESSION_COOKIE_NAME=my_cookie
ENV PROD_DATABASE_URI=my_prod_db
ENV DEV_DATABASE_URI=my_dev_db

COPY . /app5

CMD python app.py