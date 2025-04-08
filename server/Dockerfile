FROM node:23-bookworm-slim

WORKDIR /app/

COPY ./package.json ./package-lock.json ./

RUN npm install 

COPY src ./

CMD ["npm", "run", "serve"]
