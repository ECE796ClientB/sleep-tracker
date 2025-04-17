FROM hapiproject/hapi:latest

# Set environment variables
ENV HAPI_FHIR_CORS_ENABLED=true \
    HAPI_FHIR_CORS_ALLOWED_ORIGINS=http://localhost:3000 \
    HAPI_FHIR_CORS_ALLOWED_HEADERS=Content-Type,Authorization \
    HAPI_FHIR_CORS_ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS \
    HAPI_FHIR_CORS_MAX_AGE=3600

# Expose the port HAPI listens on
EXPOSE 8080