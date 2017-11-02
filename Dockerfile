FROM python:alpine3.6

EXPOSE 8080

# COPY will take from local -> container
COPY . /cmps128

# Basically cd
WORKDIR /cmps128

# Add GCC
RUN apk update && apk add gcc g++ make 

# Install app dependencies
RUN pip install -r requirements.txt

CMD python hw2.py