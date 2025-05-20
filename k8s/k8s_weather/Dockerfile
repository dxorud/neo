# Step 1 : Base Images
FROM node:18.16.0

# Step 2 : Package install
RUN apt -y update && apt -y upgrade; apt -y install vim git net-tools

# Step 3 : Specify a Working directory
WORKDIR /root

# Step 4 : Config file copy
COPY weather.tar.gz .

# Step 5 : Install express
RUN tar xzvf weather.tar.gz
WORKDIR '/root/weather'
RUN npm install
RUN npm install -g nodemon

# Step 6 : Open port
EXPOSE 8000

# Step 7 : Excution Program
CMD ["nodemon", "app.js"]
