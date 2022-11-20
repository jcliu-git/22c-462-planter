FROM python:3.10-slim

WORKDIR /hub

#Install all required dependencies for hub
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install psycopg2 Flask

#Copy main files to container
COPY main.py network462.py ./
COPY ./contract/contract.py ./contract/

# Add wait-for-it - This is to make sure db is ready before connecting to it
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh

# -u flag (unbuffered output) shows output of python file even when the container is running in detached mode 
CMD ["./wait-for-it.sh", "db:5432", "--", "python","-u", "main.py"] 

