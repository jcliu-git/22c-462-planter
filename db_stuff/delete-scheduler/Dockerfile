FROM postgres:14.2

# Updating packages and installing cron
RUN apt-get update && apt-get install cron -y 

# Copying files into container
COPY deleteOldRows.sh deleteOldRows.sql /root/
COPY crontab /etc/cron.d/my-cron-file

# Give permisions 
RUN chmod 777 /root/deleteOldRows.sh
RUN chmod 644 /etc/cron.d/my-cron-file

# Running crontab
RUN crontab /etc/cron.d/my-cron-file

# Creating entry point for cron 
ENTRYPOINT ["cron", "-f"]