FROM node:22-slim

WORKDIR /app

ENV NODE_ENV=production

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/IMROVOID/Omnirush2API.git .

RUN npm ci && npm run build

ENV PORT=20129

EXPOSE 20129

CMD ["node", "dist/cli.js", "start", "--host", "0.0.0.0", "--port", "20129"]
