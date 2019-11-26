#!/bin/bash
service apache2 start
#tail -F /var/log/apache2/access.log

export MD5=`echo -n $RANDOM | md5sum | cut -d ' ' -f1`
export WEBROOT=${MD5:0:16}
printf "$(cat /etc/apache2/sites-enabled/default.conf)" $WEBROOT > /etc/apache2/sites-enabled/000-default.conf
mv /var/www//html/* /var/www/html/$WEBROOT
chmod 777 /var/www//html/$WEBROOT/upload
rm -rf /var/www/html/$WEBROOT/upload/*
service apache2 reload
echo -n "WEBROOT IS " && echo $WEBROOT
export OLDROOT=$WEBROOT

while true
	do export MD5=`echo -n $RANDOM | md5sum | cut -d ' ' -f1`
    export WEBROOT=${MD5:0:16}
    printf "$(cat /etc/apache2/sites-enabled/default.conf)" $WEBROOT > /etc/apache2/sites-enabled/000-default.conf
    cp -r /var/www//html/$OLDROOT /var/www/html/$WEBROOT
    chmod 777 /var/www//html/$WEBROOT/upload
    rm -rf /var/www/html/$WEBROOT/upload/*
    service apache2 reload
    sleep 1
    rm -rf /var/www//html/$OLDROOT
    echo -n "WEBROOT IS " && echo $WEBROOT
    export OLDROOT=$WEBROOT
	sleep 600
done