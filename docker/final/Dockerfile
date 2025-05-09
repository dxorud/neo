# Step 1
FROM node:16

# Step2 
WORKDIR /usr/src/app

# Step3
RUN git clone https://github.com/dxorud/docker-publish
WORKDIR /usr/src/app/docker-publish/worldcup
RUN npm install

# Step 4
EXPOSE 8000

# Step 5
CMD ["node", "app.js"]