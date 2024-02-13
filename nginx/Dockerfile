# Use the Nginx image as the base image
FROM nginx:1.21.1-alpine

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the configuration file from the local directory (this should be in the same directory as this Dockerfile)
COPY missions.conf /etc/nginx/conf.d