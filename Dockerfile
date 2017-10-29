FROM alpine3.6

EXPOSE 8080

# COPY will take from local -> container
COPY . /cmps128
# Basically cd
WORKDIR /cmps128
RUN sh init.sh
CMD python hw2.py