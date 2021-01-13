FROM python:3

WORKDIR /app-back
ENV PYTHONUNBEFFERED=0

ADD . .

RUN apt update && apt install netcat -y
RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

CMD ["bash", "waitdb.sh"]
CMD ["python3",  "app.py"]