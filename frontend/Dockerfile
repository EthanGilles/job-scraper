# Base image
FROM node:20-alpine

WORKDIR /app

# Copy package.json and install deps
COPY frontend/package*.json ./
RUN npm install

# Copy all frontend code
COPY frontend/ .

RUN npm run build

# Use nginx to serve built frontend
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80

# Default command
CMD ["nginx", "-g", "daemon off;"]
