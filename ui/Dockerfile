FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy app source
COPY . .

# Install dependencies
RUN npm install

# Set environment variable
ENV CHOKIDAR_USEPOLLING=true

# Expose dev server port
EXPOSE 5173

# Run dev server
CMD ["npm", "run", "dev"]
