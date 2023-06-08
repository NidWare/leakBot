FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the bot code to the container
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y cron
RUN pip install --no-cache-dir telebot pytz beautifulsoup4 instaloader pillow

# Add crontab file
ADD crontab /etc/cron.d/bot-cron

# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/bot-cron

# Apply cron job
RUN crontab /etc/cron.d/bot-cron

# Run the command on container startup
CMD service cron start && python main.py
