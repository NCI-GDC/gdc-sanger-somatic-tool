FROM python:3.14.0rc1

# Installing dependencies
COPY requirements.txt /opt/
RUN pip install -r /opt/requirements.txt

# Copy over source
COPY scripts/ /opt/ 

WORKDIR /opt
