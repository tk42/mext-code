FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app


# Make port 80 available to the world outside this container
EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port", "8501"]
