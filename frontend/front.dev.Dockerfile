FROM node:15.5.1
MAINTAINER ajh508@naver.com
WORKDIR /app
ADD . .
CMD yarn install && yarn run serve
