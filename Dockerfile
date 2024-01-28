FROM python:3.10.12

ENV PYTHONUNBUFFERED 1

WORKDIR /adigabza_api

RUN ["/bin/bash", "-c", "python3 -m venv venv"]
ADD . /adigabza_api
RUN ["/bin/bash", "-c", "source venv/bin/activate"]
RUN ["/bin/bash", "-c", "pip install -r requirements.txt"]
RUN ["/bin/bash", "-c", "python3 manage.py runserver 8000"]