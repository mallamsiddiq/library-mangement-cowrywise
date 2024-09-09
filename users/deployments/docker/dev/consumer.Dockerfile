# consumer Dockerfile
FROM users_api_image:latest

# Use the explicit name and tag of the API image

# Set up the working directory
WORKDIR /app

# Copy the consumer-specific files
COPY ./app /app

# Run the consumer script

ENTRYPOINT ["python", "events/consumers/consumer.py"]
