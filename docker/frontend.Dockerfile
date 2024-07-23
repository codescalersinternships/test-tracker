# build stage
FROM node:18.18.2 as build-stage
WORKDIR /client

ENV SERVER_DOMAIN_NAME_API=$SERVER_DOMAIN_NAME_API

# Copy package.json and package-lock.json separately to leverage Docker cache
COPY ./client/package*.json /client
COPY ./docker/scripts/frontend/build-env.sh /client/scripts/

RUN npm i -g pnpm && pnpm install
RUN chmod +x /client/scripts/build-env.sh
COPY ./client /client
RUN pnpm build

FROM nginx:stable-alpine as production-stage
COPY ./nginx/prod.conf /temp/prod.conf

RUN envsubst '$SERVER_DOMAIN_NAME_API' < /temp/prod.conf > /etc/nginx/conf.d/default.conf

# Copy the build artifacts and build-env.sh from the build-stage
COPY --from=build-stage /client/dist /usr/share/nginx/html
COPY --from=build-stage /client/scripts/build-env.sh /usr/share/nginx/html

EXPOSE 80

CMD ["/bin/sh", "-c", "/usr/share/nginx/html/build-env.sh && nginx -g \"daemon off;\""]
