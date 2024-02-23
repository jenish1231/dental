FROM python:3.6
ENV PYTHONUNBUFFERED 1
WORKDIR /code
ADD requirements/base.txt .
ADD requirements/local.txt .
RUN pip install -U pip
RUN pip install -r base.txt
RUN pip install -r local.txt
COPY . .


CMD ["gunicorn", "dental.wsgi:application", "--bind 0.0.0.0:6061"]
