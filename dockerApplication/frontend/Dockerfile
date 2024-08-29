FROM node:20-alpine

WORKDIR /app

COPY package*.json /app/

RUN npm i --save 
RUN npm i -g react-scripts@5.0.0

COPY . /app

CMD ["npm", "start"]
