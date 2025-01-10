# Use the official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app

# Set the working directory
WORKDIR $APP_HOME

# Install system dependencies for the app and tesseract
RUN apt-get update && apt-get install -y \
    libtesseract-dev \
    tesseract-ocr \
    build-essential \
    make \
    && apt-get clean

# Copy project files
COPY . .

# Install Python dependencies globally within the container
RUN make install

# Expose the application port
EXPOSE 5050

# Run the application using Makefile
CMD ["make", "run"]