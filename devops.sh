
BASE=`basename $(pwd)`


if [[ ! "$BASE" == "delta" ]]; then
  echo "You're in the wrong directory."
  echo "Please make sure delta is your base directory."
fi

function help {
  echo "Build Script For Delta\n\n"
  echo "-h help"
  echo "-b {build} [server, scraper, proxy, database, all]"
  echo "-r {run} [server, scraper, proxy, database, all]"
  echo "-d deploy stack"
  echo "-u update submodules"

  echo "\nIncase of extreme distress [-u force] will force update sub repos, use with great caution."
}

function build_server {
  echo "\nBuilding Server..."
  docker rm delta_server
  docker build -t delta_server .
  docker create --name delta_server -p 8080:8080 delta_server
}

function build_database {
  echo "\nBuilding Database..."
  docker rm delta_database
  docker build -t delta_database database/
  docker create --name delta_database -p 5432:5432 -v $(pwd)/database/volume:/var/lib/postgresql/data delta_database
}

function build_proxy {
  echo "\nBuilding Proxy..."
  docker rm delta_proxy
  docker build -t delta_proxy www/
  docker create --name delta_proxy -p 80:80 -v$(pwd)/www/nginx.conf:/etc/nginx/nginx.conf delta_proxy
}

function build_scraper {
  echo "\nBuilding Scraper..."
  docker rm delta_scraper
  docker build -t delta_scraper delta_scraper/
  docker create --name delta_scraper -p 8000:8000 delta_scraper
}

function run_server {
  echo "Starting Server..."
  docker start delta_server
}

function run_database {
  echo "Starting Database..."
  docker start delta_database
}

function run_proxy {
  echo "Starting Proxy..."
  docker start delta_proxy
}

function run_scraper {
  echo "Starting Scraper..."
  docker start delta_scraper
}

function update_submodules {
  git pull
  git submodule update --recursive --remote
}

function force_update_submodules {
  echo "There is no going back now..."
  if [ -d "delta_scraper" ]; then
    git rm delta_scraper -f
  fi

  git submodule add --force https://github.com/JonasRSV/delta_scraper.git 

  if [ -d "www/delta_frontend" ]; then
    git rm www/delta_frontend -f
  fi

  cd www
  git submodule add --force https://github.com/Pranz/delta_frontend.git 
  cd ..
}

BUILD_TARGETS=()
RUN_TARGETS=()
DEPLOY=0
while true ; do
    case "$1" in
        -b )
            BUILD_TARGETS+=($2)
            shift 2
        ;;
        -r )
            RUN_TARGETS+=($2)
            shift 2
        ;;
        -d )
            DEPLOY=1
            shift 1
        ;;
        -h )
            help
            shift 1
        ;;
        -u )
          if [ "${2}" == "force" ]
            then
              force_update_submodules
              shift 2
            else
              update_submodules
              shift 1
            fi
        ;;
        *)
            break
        ;;
    esac 
done;

for build_target in ${BUILD_TARGETS[*]}
  do
    case $build_target in
      server)
        build_server
      ;;
      scraper) 
        build_scraper
      ;;
      proxy)
        build_proxy
      ;;
      database)
        build_database
      ;;
      all)
        build_server
        build_proxy
        build_database
        build_scraper
      ;;
      *)
        echo "Unknown Build Option: ${build_target}" 
      ;;
    esac
  done

for run_target in ${RUN_TARGETS[*]}
  do
    case $run_target in
      server)
        run_server
      ;;
      scraper) 
        run_scraper
      ;;
      proxy)
        run_proxy
      ;;
      database)
        run_database
      ;;
      all)
        run_server
        run_proxy
        run_database
        run_scraper
      ;;
      *)
        echo "Unknown Run Target: ${run_target}" 
      ;;
    esac
  done;


if [[ "${DEPLOY}" == "1" ]]
then
  echo "Deploying on stack delta..."
  docker swarm init
  docker stack deploy --compose-file docker-compose.yml delta
  docker stack ps delta
fi

