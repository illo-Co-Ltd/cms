FROM mysql:8.0

MAINTAINER ajh508@naver.com

#COPY schema.sql /docker-entrypoint-initdb.d
COPY set_timezone.sql /docker-entrypoint-initdb.d
COPY create_users.sql /docker-entrypoint-initdb.d

# ENV init
# TODO
# 추후 외부 secret파일이나 db에서 읽어오도록 구현할 것
ENV MYSQL_DATABASE=cms \
    MYSQL_ROOT_PASSWORD=1010