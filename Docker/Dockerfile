FROM python:3.11.1-slim

# Install dependencies including MySQL client
RUN apt-get update && apt-get install -y \
    libgomp1 \
    build-essential \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*  # Clean up after installation to reduce image size

WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Command to run the Python script
CMD ["python", "real.py"]
