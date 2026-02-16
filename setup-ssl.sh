#!/bin/bash

# Create directory if it doesn't exist
mkdir -p ./nginx/ssl

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ./nginx/ssl/nginx.key \
  -out ./nginx/ssl/nginx.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

echo "Self-signed SSL certificates generated in ./nginx/ssl/"
