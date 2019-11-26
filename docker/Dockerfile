# FROM php:7.2-apache

FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y php7.2 && \
    apt-get install -y apache2 && \
    apt-get install -y libapache2-mod-php

COPY file /file
RUN cp /file/000-default.conf /etc/apache2/sites-enabled/default.conf
RUN export WEBROOT=`echo -n $RANDOM | md5sum | cut -d ' ' -f1` && \
    rm -rf /var/www/html/index.html && \
    mv /file/apache2.conf /etc/apache2/apache2.conf && \
    printf "$(cat /file/000-default.conf)" $WEBROOT > /etc/apache2/sites-enabled/000-default.conf && \
    mkdir /var/www/html/$WEBROOT && \
    mv /file/index.php /var/www/html/$WEBROOT/index.php && \
    mv /file/run.sh /run.sh && \
    mv /file/php.ini /etc/php/7.2/apache2/php.ini && \
    mkdir /var/www/html/$WEBROOT/upload && \
    echo 'Options All -Indexes' > /var/www/html/$WEBROOT/upload/.htaccess && \
    echo 'd3ctf{C0n9rAtul4t1ons_Y0u_9ot_1t}' > /F1aG_1s_H4r4 && \
    rm -rf /file && \
    chmod 500 /run.sh && \
    chmod 777 /var/www/html/$WEBROOT/upload && \
    chmod 755 /var/www/html/$WEBROOT/upload/.htaccess && \
    chmod 755 /F1aG_1s_H4r4

WORKDIR /var/www/html/
CMD /bin/bash /run.sh
