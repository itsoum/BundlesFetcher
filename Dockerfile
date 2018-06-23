# Pull base images.
FROM ubuntu
FROM python:3

ADD main.py /
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app

# Define default command.
CMD ["bash"]

