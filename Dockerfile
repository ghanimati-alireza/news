FROM repos.divar.cloud/python:3.12

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app/

# Run migrations and collect static files
# You can customize this if you have more setup steps, like custom migration commands
RUN python manage.py migrate \
    && python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "news.wsgi:application"]
