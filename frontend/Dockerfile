FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

COPY /app/.zshrc /root/.zshrc
RUN echo "source /root/.zshrc" >> /root/.bashrc

RUN npm run build

# Use serve to run the app
RUN npm install -g serve
EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]
