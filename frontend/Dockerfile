FROM node:latest

# create destination directory
RUN mkdir -p /usr/src/clipis
WORKDIR /usr/src/clipis

# copy the app, note .dockerignore
COPY . .
RUN ls
RUN npm i
RUN npm install vue-masonry-css --save-dev
RUN npm install --save-dev pug pug-plain-loader
RUN npm install --save-dev sass sass-loader@10 fibers

# build necessary, even if no static files are needed,
# since it builds the server as well
RUN npm run build

# expose 5000 on container
EXPOSE 3000

# set app serving to permissive / assigned
ENV NUXT_HOST=0.0.0.0
# set app port
ENV NUXT_PORT=3000
