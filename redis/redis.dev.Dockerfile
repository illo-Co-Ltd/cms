FROM redis:6

MAINTAINER Jaehan Ahn <ajh508@naver.com>

WORKDIR /data

ADD redis.conf /data/redis.conf

#ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD [ "redis-server","/data/redis.conf" ]
