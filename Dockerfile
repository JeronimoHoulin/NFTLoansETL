FROM python:3.10-slim-buster
WORKDIR /app
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    build-essential gcc

# required for psycopg2
RUN apt-get install -y libpq-dev 
RUN apt-get install -y git
RUN apt-get install -y libxml2-dev libxslt-dev python-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV AWS_ACCESS_KEY_ID="AKIATOQHIQBUUG7C346O"
ENV AWS_SECRET_ACCESS_KEY="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"
ENV AWS_DEFAULT_REGION="eu-west-1"
# this is overridden with entrypoint for individual images
CMD ["python", "main.py"]