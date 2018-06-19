# Delta

Working with submodules: https://git-scm.com/book/en/v2/Git-Tools-Submodules

## Requirements 
1. Docker

## Installation
### Mac
https://docs.docker.com/docker-for-mac/install/

### Linux
https://docs.docker.com/install/linux/docker-ce/ubuntu/

### Windows
https://docs.docker.com/docker-for-windows/install/

## Building
1. sh devops.sh -b all

## Deploying
1. sh devops.sh -d

(Visit 0.0.0.0 to see if everything went alrite)

---

## API

#### PATH: /
#### PURPOSE
serve static files

---


#### PATH: /posts/create
#### PURPOSE
create posts

---


#### PATH: /posts/....
#### PURPOSE
get posts located at path ....

---


#### PATH: /user/login
#### PURPOSE
login and recieve a session token

---


#### PATH: /user/logout
#### PURPOSE
logout and invalidate session token

---


#### PATH /logs/server.log
#### PURPOSE
monitor server health and general debug



