# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the ports for Flask and Streamlit
EXPOSE 5000 8501

# Command to run both Flask and Streamlit using a process manager
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=5000 & streamlit run streamlit_app.py --server.port=8501 --server.headless true"]
