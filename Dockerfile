FROM python:3.8.10
RUN pip3 install requests

COPY . /src

WORKDIR /src

# run locally
# EXPOSE 8080
# CMD python server.py 8080

#deploy
CMD python server.py $PORT