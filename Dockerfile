
FROM ubuntu:bionic

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-venv nginx supervisor curl

# Setup python 3 virtualenv
RUN mkdir /envs/
RUN python3 -m venv /envs/data_hub
ENV PATH /envs/data_hub/bin:$PATH
# upgrade pip
RUN pip3 install -U pip
RUN python3 --version
RUN pip3 --version
# install wheel
RUN pip3 install wheel

# set aws region
ENV AWS_REGION us-east-1

COPY /docker-entrypoint.sh /
COPY /docker-entrypoint.d/* /docker-entrypoint.d/
ONBUILD COPY /docker-entrypoint.d/* /docker-entrypoint.d/

RUN chmod +x docker-entrypoint.sh
RUN chmod +x docker-entrypoint.d/*.sh

# Setup app
COPY src /src/
RUN pip3 install -r /src/requirements.txt --upgrade
RUN pip3 install gunicorn

# install awscli
RUN pip3 install awscli --upgrade

# Setup Django environment
ENV PYTHONPATH $PYTHONPATH: /src/data_hub
ENV DJANGO_SETTINGS_MODULE data_hub.settings

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY django.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled/django.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

# Expose port
EXPOSE 1968

# Run entrypoint script
ENTRYPOINT ["/docker-entrypoint.sh"]
