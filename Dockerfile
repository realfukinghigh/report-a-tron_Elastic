FROM ubuntu:18.04

RUN apt-get update && \
    apt-get -y install python3 python3-dev python3-pip && \
    apt-get -y install nginx

RUN pip3 install --upgrade pip

COPY . /reportatron

WORKDIR /reportatron

RUN pip3 install -r requirements.txt

COPY reportatron.conf /etc/nginx/conf.d/reportatron.conf

RUN rm /etc/nginx/sites-enabled/default

RUN rm /etc/nginx/sites-available/default

EXPOSE 80

RUN service nginx restart

RUN chmod a+x build.sh

ENTRYPOINT ["./build.sh"]
