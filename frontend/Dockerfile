# ---- Stage 1: Build the frontend ----
FROM node:20-alpine AS build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

# Copy all source files from frontend folder
COPY frontend/ ./
RUN npm run build   # Build output will go to /app/build

# ---- Stage 2: Serve with nginx ----
FROM nginx:stable-alpine

COPY --from=build /app/build /usr/share/nginx/html

COPY frontend/resources/nginx.conf /etc/nginx/nginx.conf

COPY frontend/resources/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY frontend/resources/homelab-ca.crt /usr/local/share/ca-certificates/homelab-ca.crt
RUN apk add --no-cache ca-certificates && update-ca-certificates

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
