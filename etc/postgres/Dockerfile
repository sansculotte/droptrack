# vim:set ft=dockerfile:
#
# This setsup a database container to use for development.
# It creates the main database as well as the _testing database
# specifiy user and password according to your app config as
# outlined below.
#
# docker build -t droptrack/postgres .
# docker run -d --name droptrack-postgres \
#            -p 5432:5432 \
#            -e POSTGRES_USER=droptrack \
#            -e POSTGRES_PASSWORD=kcartpord \
#            -e POSTGRES_DB=droptrack \
#            droptrack/postgres
FROM postgres:13

COPY docker-entrypoint-initdb.d /docker-entrypoint-initdb.d
