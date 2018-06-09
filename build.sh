docker rm delta_server
docker build -t delta_server .
docker create --name delta_server -p 8080:8080  delta_server
