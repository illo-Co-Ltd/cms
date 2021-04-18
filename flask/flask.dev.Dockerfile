FROM python:3

WORKDIR /app
ENV PYTHONUNBEFFERED=0

ADD . .

#RUN apt-get update && apt-get install software-properties-common -y
#RUN add-apt-repository -y ppa:otto-kesselgulasch/gimp
#RUN apt-get update && apt-get install libgl1-mesa-glx libturbojpeg -y
RUN apt-get update && apt-get install libgl1-mesa-glx -y
RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["./wait-for-it.sh", "db:3306", "-s", "-t", "30", "--"]
CMD ["python3",  "app.py"]