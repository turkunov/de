FROM alpine:3.14

RUN apk --no-cache add nginx

ARG nginx_guid=1000
ARG nginx_uid=1000

# Create directories first (Nginx needs these to exist)
RUN mkdir -p /var/html_static \
    && mkdir -p /var/lib/nginx/tmp \
    && mkdir -p /run/nginx

# Create user and group with proper permissions
# first is group, next one - user 
# -D (passwordless)
# -u (userid)
# -g (GECOS field, additional identifier for user)
# Last chmod gives read+write+execute perms
RUN addgroup -g $nginx_guid nginx-demo-group \
    && adduser -D --ingroup nginx-demo-group \
    -u $nginx_uid -g 'Cat Enjoyer' nginx-demo-user \
    && chown -R nginx-demo-user:nginx-demo-group \
    /var/html_static /etc/nginx /var/lib/nginx /var/log/nginx /run/nginx \
    && chmod -R 755 /var/log/nginx /run/nginx

# Copy configuration files
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./conf.d/default.conf /etc/nginx/conf.d/default.conf

# explicitly define which user is going to execute a build command and maintain the container
USER nginx-demo-user

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]