FROM python:3.11-slim

# Set working directory
WORKDIR /src

# Copy requirements
COPY requirements.txt .

# Install dependencies and SSH
RUN apt-get update && \
    apt-get install -y openssh-server libexpat1 && \
    mkdir /var/run/sshd && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Configure SSH
RUN echo 'root:Docker!' | chpasswd && \
    sed -i 's/^#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose the SSH port and app port
EXPOSE 2222 5101

# Copy application files
COPY . .

# Set environment variable
ENV PYTHONPATH=/src

# Start SSH and the app
CMD ["/bin/bash", "-c", "/usr/sbin/sshd -D & python /src/src/app.py"]
