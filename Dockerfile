FROM apify/actor-python:3.13

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . ./

# Specify the main script to run
CMD python src/main.py