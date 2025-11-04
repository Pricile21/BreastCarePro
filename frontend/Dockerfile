FROM node:20

WORKDIR /app

# Accept build-time argument for API URL
# Use localhost because browser makes requests from host machine, not container
ARG NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

# Copy package files
COPY package*.json ./

# Install dependencies with legacy peer deps to handle React 19 conflicts
RUN npm install --legacy-peer-deps

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Run development server
CMD ["npm", "run", "dev"]

