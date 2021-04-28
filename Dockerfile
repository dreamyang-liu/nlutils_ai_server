from python:3.7.9
RUN pip install nlutils flask flask-cors demjson gunicorn
COPY tmp/src /home/src
WORKDIR /home/src
CMD gunicorn -b 0.0.0.0:8000 main:app
ENTRYPOINT /bin/bash
