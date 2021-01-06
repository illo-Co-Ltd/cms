FROM mysql:8.0

MAINTAINER ajh508@naver.com

ADD schema.sql /docker-entrypoint-initdb.d

EXPOSE 3306
