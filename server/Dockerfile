FROM node:alpine

WORKDIR /app/

COPY ./package.json ./package-lock.json ./

RUN npm i

COPY src ./

CMD ["npm", "run", "serve"]
