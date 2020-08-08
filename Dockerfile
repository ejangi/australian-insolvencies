FROM google/cloud-sdk:alpine

WORKDIR /usr/src/app

ENV PORT 8080
EXPOSE $PORT

ENV DATAFILE https://data.gov.au/data/dataset/d1151a1d-2f4e-4519-9d6f-103032dae30d/resource/e182f36b-2dfd-402e-8c9e-5f95ff1a2589/download/total_business_related_debtors_quarterly_time_series.csv
# TABLE_ID_RAW = "your-project.your_dataset.your_table_name" 
#    — keep loading data into a "raw" table 
#    - then use a scheduled query to update a view that we read from
ENV TABLE_ID_RAW ""
ENV TABLE_ID ""
ENV LOAD_KEY ""

RUN apk --update add openssl ca-certificates py-openssl wget libffi-dev openssl-dev python3-dev build-base
RUN pip3 install --upgrade Flask gunicorn google-cloud-bigquery wget
RUN mkdir -p /usr/src/app

COPY src/app.py /usr/src/app/app.py
COPY src/templates /usr/src/app/templates

CMD PYTHONPATH=`pwd`/.. exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app