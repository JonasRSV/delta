docker rm delta_proxy
docker build -t delta_proxy .
docker create --name delta_proxy -p 80:80 -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf delta_proxy:latest

