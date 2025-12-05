# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source files
COPY . .

# Build argument for API URL (used in production/Railway)
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Railway uses PORT env var, default to 80
EXPOSE 80

# Use shell form to allow PORT substitution
CMD sh -c "sed -i 's/listen 80/listen ${PORT:-80}/g' /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"

