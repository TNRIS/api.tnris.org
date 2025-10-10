
FROM ubuntu:noble

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv nginx supervisor curl libpq-dev jq
RUN apt-get install -y binutils libproj-dev gdal-bin

# Setup pyenv dependencies
RUN apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git

# Upgrade ubuntu
RUN apt-get -y upgrade

# Download and install pyenv 
RUN curl -fsSL https://pyenv.run | bash
SHELL ["/bin/bash", "--login" , "-c"]

# Setup python 3 virtualenv and pyenv
RUN ~/.pyenv/bin/pyenv install 3.12

RUN mkdir /envs
WORKDIR /envs
RUN ~/.pyenv/bin/pyenv local 3.12
RUN python3 -m venv ./data_hub
WORKDIR /
# Cleanup pyenv dep 
RUN apt-get remove -y git

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
RUN pip3 install -r /src/requirements.txt
RUN pip3 install gunicorn

# install awscli
RUN pip3 install awscli --upgrade

# Setup Django environment
ENV PYTHONPATH $PYTHONPATH: /src/data_hub
ENV DJANGO_SETTINGS_MODULE data_hub.production_settings

# Setup staticfiles
RUN chmod -R 777 /src/data_hub/static

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
EXPOSE 1969

# Run entrypoint script
ENTRYPOINT ["/docker-entrypoint.sh"]
