FROM python:3.5

# Copy over source
COPY scripts/ /opt/ 
COPY requirements.txt /opt/
WORKDIR /opt

# Installing dependencies
RUN pip install -r requirements.txt
