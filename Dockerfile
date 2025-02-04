# Use the official Python image for Python 3.11
FROM python:3.11-slim

# Set environment variables to prevent Python from buffering output
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project files into the container
COPY . /app/

# Download the NLTK punkt and punkt_tab tokenizer resources
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader punkt_tab  # Add this line to download punkt_tab

# Expose port 8000 for the Django app
EXPOSE 8000

# Use Gunicorn to serve the app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "summar_ease.wsgi:application"]
