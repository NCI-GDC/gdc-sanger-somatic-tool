FROM python:3.12.10

# Installing dependencies
COPY requirements.txt /opt/
RUN pip install -r /opt/requirements.txt

# Copy over source
COPY scripts/ /opt/ 

WORKDIR /opt
