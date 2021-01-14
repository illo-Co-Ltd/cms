FROM redis:6

WORKDIR /data

ADD . .

CMD ["redis-server", "--requirepass", "$(REDIS_PASSWORD)"]