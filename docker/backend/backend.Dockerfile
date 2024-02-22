FROM python:3.6
ENV PYTHONUNBUFFERED 1
WORKDIR /code
ADD requirements/base.txt .
ADD requirements/local.txt .
RUN pip install -U pip
RUN pip install -r base.txt
RUN pip install -r local.txt
COPY . .
ADD docker/entry.sh /code/docker/entry.sh
RUN chmod +x /code/docker/entry.sh


RUN chmod gu+x /code/docker/entry.sh
CMD ["./docker/wait-for-mysql.sh", "db", "3306", "dental_password", "dentalhub_db", "--", "./docker/entry.sh"]