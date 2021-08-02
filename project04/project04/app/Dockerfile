FROM python:3.8

EXPOSE 8080

WORKDIR /app

COPY requirements.txt /app
RUN pip install  -r requirements.txt --upgrade pip

ENV MYSQL_DATABASE_HOST=db
ENV MYSQL_DATABASE_USER=root
ENV MYSQL_DATABASE_PASSWORD=root
ENV MYSQL_DATABASE_PORT=3306
ENV MYSQL_DATABASE_DB=addressBook

COPY . /app

CMD python app.py