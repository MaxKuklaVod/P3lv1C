FROM python:3.11
WORKDIR /app 
COPY . .
RUN pip install -r requirments.txt
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends firefox

CMD ["./main.py"]
