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
(And   0.0.0.0:5000 to see if server is up)

## KNOWN ISSUES
#### Sometimes the database does not run the schema file. 
RUN: psql -h 0.0.0.0 -p 5432 -d delta -U postgres
and add the schema manually with \i SCHEMA\_NAME\_HERE


---

## API

Getting Tags given a post id

##### PATH: /tags/POST\_ID\_HERE
##### METHOD: GET
##### RETURNS
```javascript
{
  "success": IF\_REQ\_WENT\_GOOD,
  "tags": [TAG\_NAME, TAG\_NAME...]
}
```

---

Getting feed of posts

##### PATH: /feed
##### METHOD: POST
##### BODY
```javascript
{
  "limit": NUM\_OF\_POSTS,
  "time" : POSTS\_BEFORE\_TIME,
  "tags": [TAG\_NAME, TAG\_NAME...]
}
```
##### RETURNS
```javascript
{
  "success": IF\_REQ\_WENT\_GOOD,
  "limit": NUM\_OF\_POSTS,
  "time" : POSTS\_BEFORE\_TIME,
  "feed" : [POSTS...]

}
```

---

Get likes from post or comment

##### PATH: /like?id=ID\_HERE&type=TYPE\_HERE
##### METHOD: GET
##### RETURNS
```javascript
{
  "success": IF\_REQ\_WENT\_GOOD,
  "id": ID,
  "type": TYPE,
  "likes": LIKES
}
```

type is either "post" or "comment" and id is it's corresponding id

---

Get comments from post

##### PATH: /comment/id
##### METHOD: GET
##### RETURNS
```javascript
{
  "success": ..,
  "id": ID,
  "comments": COMMENTS
}
```

---

Get annotations from post

##### PATH: /annotate/id
##### METHOD: GET
##### RETURNS
```javascript
{ 
  "success": ..., 
  "post_id": POST_ID, 
  "annotations": annotations }
```

---

CREATE A POST

##### PATH: /posts/create
##### METHOD: POST
##### BODY
```javascript
{
  "token": TOKEN,
  "post": { 
            "title": TITLE,
            "content": {....},
            "tags": [....]
            }
}
```
##### RETURNS
```javascript
{
  "success": ...,
  "expired": IF TOKEN EXPIRED
  "post": SAME AS ABOVE,
  "id":  ID OF POST
}
```

---

Get a post from ID

##### PATH: /posts/id
##### METHOD: GET
##### RETURNS
```javascript
{ "success": ...,
  "time": ISO\_DATE,
  "title": ...,
  "content": {..},
  "owner": ...
}
```

---

Like something

##### PATH: /like
##### METHOD: POST
##### BODY
```javascript
{
  "token": ...,
  "like": {
     "target_id": ID OF TARGET,
     "type": "comment" or "post"
     "state": LIKE OR DISLIKE
  }
}
```
##### RETURNS
```javascript
{
  "success": ...,
  "expired": ...,
  "like": same as above
}
```


---

Comment on something
##### PATH /comment
##### METHOD: POST
##### BODY
```javascript
{
  "token": ...,
  "comment": {
    "target_id": ID OF TARGET,
    "parent": ID OF PARENT COMMENT, NULL IF ROOT,
    "content": {...}
  }
}
```
##### RETURNS
```javascript
{
  "success": ...,
  "expired": ...,
  "comment": ...,
  "id"     : ...
}
```


----

##### PATH /annotate/
##### METHOD: POST
##### BODY
```javascript
{
  "token": ...,
  "annotation": {
    "target_post": POST ID
    "target_comment": COMMENT ID,
    "begining": BEGINING OF ANNOTATION,
    "ending": ENDING OF ANNOTATION,
    "color": COLOR OF ANNOTATION
  }
}
```
##### RETURNS
```javascript
{
  "success": ...,
  "expired" ....,
  "annotation": same as above,
  "id": ANNOTATION ID
}
```

---

Login a user

##### PATH /profile/login
##### METHOD: POST
##### BODY
```javascript
{
  "user": username,
  "password": password
}
```
##### RETURNS
```javascript
{
  "success": ...,
  "token" ....,
  "message": Something Kind.
}
```

---

Logout a user

##### PATH /profile/logout
##### METHOD: POST
##### BODY
```javascript
{
  "token": ...
}
```
##### RETURNS
```javascript
{
  "success": ...,
  "token" ....,
  "message": Something Kind.
}
```

--- 

Create a user

##### PATH /profile/create
##### METHOD: POST
##### BODY
```javascript
{
  "user": ...,
  "password": ...,
  "email": ...
}
```
##### RETURNS
```javascript
{
  "success": ...,
  "message": Something Kind.
}
```









