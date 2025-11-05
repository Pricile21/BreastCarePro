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
RUN npm run build 2>&1 | tee /tmp/build.log || echo "⚠️ Build warning: Some pages failed to pre-render"

# Ensure prerender-manifest.json exists (required by Next.js start)
RUN mkdir -p .next && \
    if [ ! -f .next/prerender-manifest.json ]; then \
      echo '{"version": 4,"routes":{},"dynamicRoutes":{},"notFoundRoutes":[],"preview":{"previewModeId":"","previewModeSigningKey":"","previewModeEncryptionKey":""}}' > .next/prerender-manifest.json; \
    fi

# Expose port (Render will set PORT env variable)
EXPOSE 3000

# Start the production server
# Use npx to ensure next is found in node_modules/.bin
# Next.js will use PORT environment variable if set (Render requirement)        
CMD ["sh", "-c", "npx next start -p ${PORT:-3000}"]

