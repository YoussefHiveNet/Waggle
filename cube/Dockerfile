FROM node:20-slim

WORKDIR /cube

# Install Cube CLI globally (this is the missing piece)
RUN npm install -g cubejs-cli

COPY package.json ./
RUN npm install

COPY . .

ENV NODE_ENV=production
EXPOSE 4000

CMD ["cubejs", "server"]
