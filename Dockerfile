FROM puckel/docker-airflow:1.10.9
MAINTAINER WellsLu
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt