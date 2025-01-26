# 1. Add a base image
FROM python:3.12.0-slim-bookworm

# 2. Set environment variables
ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV APP=/app

# 3. Change the working directory
WORKDIR $APP

# 4. Add the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application files
COPY . .

# 6. Expose the port the application will use
EXPOSE 8000

# 7. Run the command to start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "djangoproj.wsgi"]
