## Server for delta

Working with submodules: https://git-scm.com/book/en/v2/Git-Tools-Submodules


## Installing
1. Install Docker on your computer

## Building
1. sh devops.sh -b all

## Deploying
1. sh devops.sh -d




## API

#### PATH: /
#### PURPOSE
serve static files


#### PATH: /posts/create
#### PURPOSE
create posts


#### PATH: /posts/....
#### PURPOSE
get posts located at path ....


#### PATH: /profile/login
#### PURPOSE
login and recieve a session token


#### PATH: /profile/logout
#### PURPOSE
logout and invalidate session token


#### PATH: /documents
#### PURPOSE
get documents of all types
#### URL PARAMS: id (doc id) type (doc type) date (documents from) limit (max response)



