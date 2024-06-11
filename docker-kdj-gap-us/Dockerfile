FROM python:3.9.6-slim-buster

# Install cron
RUN apt-get update
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime


# Build Python Env
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt


# COPY the script
#COPY scripts/ /scripts/

CMD ["python", "scripts/main.py"]