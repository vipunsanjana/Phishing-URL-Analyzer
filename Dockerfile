# Use the official Playwright image with Python 3.9
FROM mcr.microsoft.com/playwright/python 

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies and upgrade pip and setuptools
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy the entire application code
COPY . .

# Create a new user with UID 10016 for security
RUN addgroup --gid 10016 choreo && \
    adduser --disabled-password --no-create-home --uid 10016 --ingroup choreo choreouser

# Change the ownership of the application code to the unprivileged user
RUN chown -R 10016:10016 /app

# Switch to the unprivileged user
USER choreouser

# Expose port 8000 (optional, if needed for debugging)
EXPOSE 8000

# Set the default command to run the script normally (modify script name as needed)
CMD ["python", "-m", "app.app.main"]
