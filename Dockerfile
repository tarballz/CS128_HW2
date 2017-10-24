FROM ubuntu

EXPOSE 8080

# COPY will take from local -> container
COPY . /cmps128
# Basically cd
WORKDIR /cmps128
RUN sh init.sh
CMD python hw1.py