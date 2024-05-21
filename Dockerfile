FROM python:3.10-alpine

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the default .env file into the container
# fixme: delete me if system env is used
COPY .env.example /app/server/.env

COPY server ./server

ENTRYPOINT [ "python", "/app/server/manage.py" ]
CMD [ "runserver" ]
