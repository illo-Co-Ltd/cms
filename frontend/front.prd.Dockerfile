FROM node as build-stage
MAINTAINER ajh508@naver.com
WORKDIR /app
ADD . .
RUN yarn install
RUN yarn run build

FROM nginx:stable as production-stage
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]