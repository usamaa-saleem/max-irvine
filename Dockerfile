# Base image
FROM runpod/pytorch:3.10-2.0.0-117

# Use bash shell with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set the working directory
WORKDIR /app

# Update and upgrade the system packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt install -y \
    fonts-dejavu-core rsync git jq moreutils aria2 wget \
    libgoogle-perftools-dev procps pkg-config libcairo2-dev \
    libgirepository1.0-dev gir1.2-gtk-3.0 libsystemd-dev cmake && \
    apt-get autoremove -y && rm -rf /var/lib/apt/lists/* && apt-get clean -y

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --upgrade -r /app/requirements.txt --no-cache-dir

# Expose the FastAPI port
EXPOSE 8000

# Ensure the start script is executable
RUN chmod +x /start.sh

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]