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

## KNOWN ISSUES
#### Sometimes the database does not run the schema file. 
RUN: psql -h 0.0.0.0 -p 5432 -d delta -U postgres
and add the schema manually with \i SCHEMA\_NAME\_HERE

(Visit 0.0.0.0 to see if everything went alrite)
(And   0.0.0.0:5000 to see if server is up)

---

## API

#### PATH: /
#### TYPE: GET
#### PURPOSE
serve static files

---


#### PATH: /posts/create
#### TYPE: POST
#### PURPOSE
create posts
#### BODY
{
  "token": "...",
  "post" : "..."
}
#### RETURNS
STATUS

---


#### PATH: /posts/....
#### TYPE: GET
#### PURPOSE
get posts located at path ....
#### BODY
EMPTY
#### RETURNS
POST (Nothing atm)

---


#### PATH: /user/login
#### TYPE: POST
#### PURPOSE
login and recieve a session token
#### BODY
{
  "user": "...",
  "password": "..."
}
#### RETURNS
SESSION TOKEN

---


#### PATH: /user/logout
#### TYPE: POST
#### PURPOSE
logout and invalidate session token
#### BODY
{
  "token": "..."
}
#### RETURNS
STATUS

---

#### PATH: /like
#### TYPE: POST
#### PURPOSE
Like something, a post or a comment
#### BODY
UNDEFINED
#### RETURNS
STATUS

---

#### PATH: /annotate
#### TYPE: POST
#### PURPOSE
Annotate a post
#### BODY
UNDEFINED
#### RETURNS
STATUS

---

#### PATH: /comment
#### TYPE: POST
#### PURPOSE
Comment something, a post or a comment
#### BODY
UNDEFINED
#### RETURNS
STATUS


---


#### PATH /logs/server.log
#### TYPE: GET
#### PURPOSE
monitor server health and general debug
#### BODY
EMPTY
#### RETURNS
server log text

----

#### PATH /logs/
#### TYPE: GET
#### PURPOSE
debuggin / info
#### BODY
EMPTY
#### RETURNS
Logging information




