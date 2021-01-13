FROM python:3

WORKDIR /app
ENV PYTHONUNBEFFERED=0

ADD . .

RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

CMD ["python3",  "tasks.py"]