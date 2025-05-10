FROM python:latest

# Installing dependencies
COPY requirements.txt /opt/
RUN pip install -r /opt/requirements.txt

# Copy over source
COPY scripts/ /opt/ 

WORKDIR /opt
