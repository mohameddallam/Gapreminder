# Use an official minimal Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/ /app

# Expose the Streamlit default port
EXPOSE 8501

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]