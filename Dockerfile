FROM python:3.6

RUN mkdir /www
RUN mkdir static
WORKDIR /www

COPY ./project /www/project/
COPY ./requirements.txt /www/
RUN ls
RUN ls project

ARG DJANGO_ENV=${DJANGO_ENV}
ENV DJANGO_ENV=${DJANGO_ENV}

ENV PYTHONUNBUFFERED 1

### install crontab #####
ENV TZ=Asia/Bangkok
RUN apt-get update \
    && apt-get install -y cron \
    && apt-get autoremove -y
RUN apt-get install -y \
    vim

# to prevent issue when installing dependency
RUN pip install -r requirements.txt
RUN mkdir static

ADD ./docker/conf/crontab /etc/cron.d/healtcheck-cron
RUN chmod 0644 /etc/cron.d/healtcheck-cron
RUN touch /var/log/cron.log

#COPY ./docker/conf/crontab /etc/cron.d/crontab

RUN python --version
RUN cd project
RUN mkdir -p project/static
RUN mkdir -p /www/log
RUN touch /www/log/app.log

RUN echo 'yes' | project/manage.py collectstatic
RUN cp -rf /www/static project/

RUN mkdir /www/project/temp

ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"
#ENTRYPOINT [ "gunicorn", "-t", "300", "--workers", "3", "--chdir", "/www/project", "project.wsgi:application", "--bind", "0.0.0.0:8080"  ]
RUN service cron start
RUN /usr/bin/crontab /etc/cron.d/healtcheck-cron
#CMD cron
COPY ./docker/conf/executable.sh /www/
RUN chmod +x /www/executable.sh
CMD /www/executable.sh

#### RUN CRONTAB ####
#RUN /usr/bin/crontab /etc/cron.d/healtcheck