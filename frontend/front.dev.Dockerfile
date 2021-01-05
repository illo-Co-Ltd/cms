FROM node
MAINTAINER ajh508@naver.com
WORKDIR /app-front
ADD . ./
CMD yarn install && yarn run serve
EXPOSE 8080