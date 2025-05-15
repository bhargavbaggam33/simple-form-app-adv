# Stage 1: Builder
FROM python:3.9-alpine AS builder

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Reduce Python memory overhead and speed up startup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set permissions for the non-root user
RUN chown -R appuser:appuser /app

# Stage 2: Final Image
FROM python:3.9-alpine

# Create the same non-root user in the final stage
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Security configurations
RUN apk add --no-cache ca-certificates

# Set security options
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Use the non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

CMD ["python", "app.py"]





#flask-app      latest    1396b5571f4a   6 hours ago     251MB


#flask-app      v2        37db771da5e1   5 hours ago     242MB
# -changed the base image from latest to alpine


#flask-app      v3        028dd93999ea   9 seconds ago   232MB
# - removed multiple "copy . .", uswd --no-cache-dir flag to avoid caching packages


#flask-app    optimize4   1de8c431952c   3 seconds ago        47.8MB
#inluded .dockerignore file - ignored the environmental varialbles folder, .git metadata