FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=mysecretpassword
ENV MYSQL_DATABASE=OnlineBookstore
ENV MYSQL_USER=bookstore_user
ENV MYSQL_PASSWORD=bookstore_pass

COPY db.sql /docker-entrypoint-initdb.d/