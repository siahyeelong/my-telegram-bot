FROM python:3.11-slim

# Create a working directory
WORKDIR /app

# Copy dependency list first (better for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your bot code
COPY ./word_of_the_week .

# Ensure logs are not buffered
ENV PYTHONUNBUFFERED=1

# Run your bot
CMD ["python", "main.py"]

