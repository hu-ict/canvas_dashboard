# Start from the base Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install pip dependencies and system libraries
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get update \
    && apt-get install -y libexpat1 openssh-server

# Set up SSH
RUN mkdir /var/run/sshd \
    && echo 'root:iTHL5iaoUNAjOy3vTG+ACRAa7DKg' | chpasswd \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Ensure SSH runs on container start
RUN echo "PermitTunnel yes" >> /etc/ssh/sshd_config \
    && echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config \
    && echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# Copy the app code
COPY . .

# Expose the application port and SSH port
EXPOSE 5101 22

# Start both SSH and the application
CMD service ssh start && python app.py
