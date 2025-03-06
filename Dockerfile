# Image
FROM python:3.9-slim

# DIR
WORKDIR /app

# Copy nescessary files
COPY requirements.txt
COPY network_scanner.py

# Install dependencies
RUN pip install -r requirements.txt

# Define comand to run
CMD ["python", "network_scanner.py"]
```