FROM python:3

WORKDIR /app
ENV PYTHONUNBEFFERED=0

ADD . .

RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["./wait-for-it.sh", "db:3306", "-s", "-t", "30", "--"]
CMD ["python3",  "app.py"]