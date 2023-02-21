From python:3.9

RUN pip3 freeze > requirements.txt

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./score_tracker /score_tracker

WORKDIR /score_tracker

ENV PORT 8080

CMD gunicorn --bind :$PORT score_tracker.wsgi:application