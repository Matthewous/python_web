docker build . --tag=homework_nginx
docker run -d -p 7998:6060 homework_nginx