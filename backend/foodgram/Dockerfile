FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
CMD ["python3", "manage.py", "runserver", "0:8000"]
ENV SECRET_KEY=ab^&91hzhl%t$^v-=u7ut@@ad=_je3q9xsur#$0h=8j4rncdwy
ENV DEBUG=True