# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /src

# Copy application requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install SSH server
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "root:Docker!" | chpasswd \
    && mkdir /var/run/sshd

# Copy configuration files
COPY sshd_config /etc/ssh/sshd_config
COPY entrypoint.sh /src/

# Make the entrypoint script executable
RUN chmod +x /src/entrypoint.sh

# Expose necessary ports
EXPOSE 5101 2222

# Configure entrypoint
ENTRYPOINT ["/src/entrypoint.sh"]
