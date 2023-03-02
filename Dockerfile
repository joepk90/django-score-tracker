FROM python:3.7 as build

# install utils/dubug tools
# RUN apt-get update
# RUN apt-get install vim -y

RUN pip install pipenv
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pipenv requirements > requirements.txt

From python:3.7

# install utils/dubug tools
# RUN apt-get update
# RUN apt-get install vim -y
# RUN apt-get -y install coreutils

COPY ./score_tracker /score_tracker

WORKDIR /score_tracker

COPY --from=build requirements.txt .

RUN pip install -r requirements.txt

ENV PORT 8080

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]