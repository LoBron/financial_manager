FROM python:3.11.0-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./entrypoint.sh ./
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY ./src ./src

ENTRYPOINT ["/app/entrypoint.sh"]

#CMD [ "python3", "./src/manage.py", "runserver", "0.0.0.0:8000"]