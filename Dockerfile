FROM python:3.8
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app
RUN chmod +x gunicorn.sh 
RUN python manage.py makemigrations && python manage.py migrate
ENTRYPOINT ["./gunicorn.sh"]
EXPOSE 8000