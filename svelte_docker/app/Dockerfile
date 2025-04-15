# Stage 1: Build client
FROM node:18-alpine AS client-builder

WORKDIR /app/client
COPY client/package*.json ./
RUN npm install
COPY client/ .
RUN npm run build

# Stage 2: Build server
FROM node:18-alpine AS server-builder

WORKDIR /app/server
COPY server/package*.json ./
RUN npm install --production
COPY server/ .

# Stage 3: Runtime
FROM node:18-alpine

# Create unprivileged user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy built client
COPY --from=client-builder --chown=appuser:appgroup /app/client/public ./client
COPY --from=client-builder --chown=appuser:appgroup /app/client/index.html ./client

# Copy server
COPY --from=server-builder --chown=appuser:appgroup /app/server ./server

# Clean up cache
RUN npm cache clean --force && \
    rm -rf /var/cache/apk/* /tmp/*

# Switch to unprivileged user
USER appuser

# Application port
EXPOSE 3000

# Command to run
WORKDIR /app/server
ENV NODE_ENV=production
CMD ["node", "src/app.js"]