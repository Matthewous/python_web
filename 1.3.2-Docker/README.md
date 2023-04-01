docker build . --tag=image_sp
docker run -d -p 7998:6060 --name=container_sp image_sp