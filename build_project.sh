
# Build Database
echo "Building database image and container..."

cd database/
sh build.sh

cd ..

echo "\n\n\n"

echo "Building Scraper image and container..."

cd delta_scraper/
sh build.sh

cd ..

echo "\n\n\n"

echo "Building proxy image and container ..."
cd www/
sh build.sh
cd ..

echo "\n\n\n"

echo "Building server image and container ..."
sh build.sh


echo "\n\n\n"

docker swarm init

echo "Ignore This error if there is one... :)"

echo "\n\n\n"
echo "All Done."

