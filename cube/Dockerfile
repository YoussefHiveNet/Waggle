FROM node:22-alpine

WORKDIR /cube

RUN npm install -g cubejs-cli

COPY package.json ./
RUN npm install

COPY . .

EXPOSE 4000

CMD ["npx", "cubejs", "server"]
