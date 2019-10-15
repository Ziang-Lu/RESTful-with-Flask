FROM nginx

# Delete the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf
# Instead, use our own
COPY nginx.conf /etc/nginx/conf.d/
