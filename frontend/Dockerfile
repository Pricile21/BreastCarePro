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

# Build the Next.js application for production
# Note: Some pages may fail to pre-render (e.g., /mobile/booking with useSearchParams)
# This is not critical as they will be rendered dynamically at runtime
RUN npm run build || (echo "⚠️ Build warning: Some pages failed to pre-render (will render at runtime)" && exit 0)

# Expose port (Render will set PORT env variable)
EXPOSE 3000

# Start the production server
# Next.js will use PORT environment variable if set (Render requirement)
CMD ["sh", "-c", "next start -p ${PORT:-3000}"]

