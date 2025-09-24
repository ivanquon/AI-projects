# Step 1: Build the application
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /src

# Copy dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the code
COPY . .

# Build the app for production
RUN npm run build

# Step 2: Serve with Nginx
FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy built assets from builder
COPY --from=builder /src/dist /usr/share/nginx/html

# Copy custom nginx config (optional)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
