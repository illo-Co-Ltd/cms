FROM python:3

WORKDIR /worker
ENV PYTHONUNBEFFERED=0

ADD . .

RUN apt-get update && apt-get install libgl1-mesa-glx -y
RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

CMD ["celery", "-A", "app", "worker", "-B", "-S", "redbeat.RedBeatScheduler", "--loglevel=info"]