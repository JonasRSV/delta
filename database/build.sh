docker rm delta_database
docker build -t delta_database .
docker create --name delta_database -p 5432:5432 -v $(pwd)/volume:/var/lib/postgresql/data delta_database:latest
