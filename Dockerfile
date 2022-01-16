FROM python:3.8

WORKDIR /usr/src/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY req.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r req.txt

COPY . /usr/src/project

EXPOSE 8000

CMD [ "python", "manage.py", "makemigrations"]
CMD [ "python", "manage.py", "migrate"]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]