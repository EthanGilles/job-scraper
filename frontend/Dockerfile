# ---- Stage 1: Build the frontend ----
FROM node:20-alpine AS build

WORKDIR /app

# Copy dependency files from the frontend folder
COPY frontend/package*.json ./
RUN npm install

# Copy all source files from frontend folder
COPY frontend/ ./
RUN npm run build   # Build output will go to /app/build

# ---- Stage 2: Serve with nginx ----
FROM nginx:stable-alpine

# Copy built files from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy entrypoint script from frontend folder
COPY frontend/resources/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Add CA certificate
COPY frontend/reousrces/homelab-ca.crt /usr/local/share/ca-certificates/homelab-ca.crt
RUN apk add --no-cache ca-certificates && update-ca-certificates

# Expose port 80 for HTTP
EXPOSE 80

# Run entrypoint before nginx starts
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]

