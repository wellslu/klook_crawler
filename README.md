# klook_crawler
# docker
- docker pull selenium/standalone-chrome:latest
- docker pull mongo:latest
- docker build . -t klook/code:latest
- docker-compose -f compose.yml up
