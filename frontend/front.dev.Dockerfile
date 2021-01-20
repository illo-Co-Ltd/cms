FROM node
MAINTAINER ajh508@naver.com
WORKDIR /app
ADD . .
CMD yarn install && yarn run serve