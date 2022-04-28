FROM python:3.7-alpine

COPY . /src

WORKDIR /src

# run locally
EXPOSE 8080
CMD python server.py 8080

#deploy
# CMD python3 server.py $PORT