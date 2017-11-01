FROM python:alpine3.6

EXPOSE 8080

# COPY will take from local -> container
COPY . /cmps128

# Basically cd
WORKDIR /cmps128

# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install sanic

CMD python hw2.py