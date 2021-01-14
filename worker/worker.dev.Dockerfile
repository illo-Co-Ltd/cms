FROM python:3

WORKDIR /task
ENV PYTHONUNBEFFERED=0

ADD . .

RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["celery"]
CMD ["-A", "tasks.celery", "worker", "--loglevel=info"]