import flask
import json
import config 
import delta.db.connection as connection
import datetime
from psycopg2.extras import Json as psycopg2Json


DB = connection.Connection("Content")
content = flask.Blueprint("Content Blueprint", __name__)

INSERT_POST       = "INSERT INTO POST (TIME, TITLE, CONTENT, OWNER) VALUES (%s, %s, %s, %s) RETURNING ID;"

INSERT_COMMENT    = "INSERT INTO COMMENT (TARGET_POST, PARENT, OWNER, CONTENT, TIME) VALUES (%s, %s, %s, %s, %s) RETURNING ID;"

INSERT_ANNO       = "INSERT INTO ANNOTATION (TARGET_POST, TARGET_COMMENT, BEGINING, ENDING, COLOR) VALUES (%s, %s, %s, %s, %s) RETURNING ID;"

INSERT_TAG        = "INSERT INTO TAG (NAME, TARGET_POST) VALUES (%s, %s);"

GET_POST          = "SELECT TIME, TITLE, CONTENT, OWNER FROM POST WHERE POST.ID = %s;"

LIKE_POST         = "INSERT INTO POST_OPINION (TARGET, OWNER, STATE) VALUES (%s, %s, %s);"

LIKE_COMMENT      = "INSERT INTO COMMENT_OPINION (TARGET, OWNER, STATE) VALUES (%s, %s, %s);"

GET_POSTS_TIME    = "SELECT * FROM POST WHERE POST.TIME <= %s ORDER BY POST.TIME LIMIT %s;"

GET_POSTS_TIME_T  = "SELECT POST.ID, POST.TIME, POST.TITLE, POST.CONTENT, POST.OWNER"\
                  + " FROM POST JOIN TAG ON TAG.TARGET_POST = POST.ID"\
                  + " WHERE POST.TIME <= %s AND TAG.NAME IN %s ORDER BY POST.TIME LIMIT %s;"

GET_LIKES_POST    = "SELECT * FROM POST_OPINION WHERE TARGET = %s;"

GET_LIKES_COMMENT = "SELECT * FROM COMMENT_OPINION WHERE TARGET = %s;"

GET_COMMENTS_POST = "SELECT * FROM COMMENT WHERE TARGET_POST = %s;"

GET_ANNO_POST     = "SELECT * FROM ANNOTATION WHERE TARGET_POST = %s;"


@content.route("/feed", methods=["POST"])
def get_feed():
    LIMIT = None
    TIME  = None
    TAGS  = None

    try:
        request_data = flask.request.get_data().decode("utf-8")
        request_data = json.loads(request_data)

        LIMIT = request_data["limit"]
        TIME  = request_data["time"]
        TAGS  = request_data["tags"]
    except Exception as e:
        config.write_server_log("Unable to parse posts request: {}".format(str(e)))

        response = { "success": False
                   , "limit": LIMIT
                   , "time": str(TIME)
                   , "feed": None
                   }

        response = json.dumps(response)
        return flask.Response(response, status=200, mimetype="application/json")



    if TAGS is None:
        query = connection.Request( "get_posts"
                                  , GET_POSTS_TIME
                                  , (TIME, LIMIT)
                                  , lambda c: c.fetchall())
    else:
        query = connection.Request( "get_posts"
                                  , GET_POSTS_TIME_T
                                  , (TIME, tuple(TAGS), LIMIT)
                                  , lambda c: c.fetchall())
        
    feed = None
    try:
        feed = DB.request(query).data
    except Exception as e:
        config.write_server_log("Unable to fetch posts from DB: {}".format(str(e)))
        response = { "success": False
                   , "limit": LIMIT
                   , "time": TIME
                   , "feed": None
                   }

        response = json.dumps(response)
        return flask.Response(response, status=200, mimetype="application/json")


    response = { "success": True
               , "limit": LIMIT
               , "time": TIME
               , "feed": feed
               }

    response = json.dumps(response, default=config.default_json_serial)
    return flask.Response(response, status=200, mimetype="application/json")

    
@content.route("/like", methods=["GET"])
def get_likes():
    ID      = None
    TYPE    = None

    try:
        request_data = flask.request.get_data().decode("utf-8")
        request_data = json.loads(request_data)

        ID   = request_data["id"]
        TYPE = request_data["type"]

    except Exception as e:
        config.write_server_log("Unable to parse likes request: {}".format(str(e)))

        response = { "success": False
                   , "id": None
                   , "type": None
                   , "likes": None
                   }
        response = json.dumps(response)
        return flask.Response(response, status=200, mimetype="application/json")

    likeables = { "post": GET_LIKES_POST
                , "comment": GET_LIKES_COMMENT
                }


    if TYPE not in likeables:
        config.write_server_log("No likes on type {}".format(TYPE))

        response = { "success": False
                   , "id": ID
                   , "type": TYPE
                   , "likes": None
                   }
        response = json.dumps(response)
        return flask.Response(response, status=200, mimetype="application/json")



    query = connection.Request( "likes"
                              , likeables[TYPE]
                              , (ID,)
                              , fetcher=lambda c: c.fetchall())

    likes = None
    try: 
        likes = DB.request(query).data
    except Exception as e:
        config.write_server_log("Could not fetch likes from database: {}".format(str(e)))

        response = { "success": False
                   , "id": ID
                   , "type": TYPE
                   , "likes": None
                   }
        response = json.dumps(response)
        return flask.Response(response, status=200, mimetype="application/json")

    response = { "success": True
               , "id": ID
               , "type": TYPE
               , "likes": likes
               }

    response = json.dumps(response)
    return flask.Response(response, status=200, mimetype="application/json")


@content.route("/comment", methods=["GET"])
def get_comments():
    POST_ID    = None

    try:
        request_data = flask.request.get_data().decode("utf-8")
        request_data = json.loads(request_data)

        POST_ID = request_data["post_id"]
    except Exception as e:
        config.write_server_log("Could not parse comments request.")

        response = { "success": False
                   , "post_id": None
                   , "comments": None
                   }
        response = json.dumps(response)
        return flask.Response(response, status=200, mimetype="application/json")

    query = connection.Request( "comments"
                              , GET_COMMENTS_POST
                              , (POST_ID, )
                              , fetcher=lambda c: c.fetchall())

    comments = None
    try:
        comments = DB.request(query).data
    except Exception as e:
        config.write_server_log("Could not fetch comments from DB.")

        response = { "success": False
                   , "post_id": POST_ID
                   , "comments": None
                   }
        response = json.dumps(response)
        return flask.Response(response, status=200, mimetype="application/json")

    response = { "success": True
               , "post_id": POST_ID
               , "comments": comments
               }

    response = json.dumps(response, default=config.default_json_serial)
    return flask.Response(response, status=200, mimetype="application/json")


@content.route("/annotate", methods=["GET"])
def get_annotations():
    POST_ID    = None
    try:
        request_data = flask.request.get_data().decode("utf-8")
        request_data = json.loads(request_data)

        POST_ID = request_data["post_id"]
    except Exception as e:
        config.write_server_log("Could not parse get annotations request.")

        response = { "success": False
                   , "post_id": None
                   , "annotations": None
                   }
        response = json.dumps(response)
        return flask.Response(response, status=200, mimetype="application/json")

    query = connection.Request( "annotations"
                              , GET_ANNO_POST
                              , (POST_ID, )
                              , fetcher=lambda c: c.fetchall())

    annotations = None
    try:
        annotations = DB.request(query).data
    except Exception as e:
        config.write_server_log("Could not fetch annotations from DB.")

        response = { "success": False
                   , "post_id": POST_ID
                   , "annotations": None
                   }
        response = json.dumps(response)
        return flask.Response(response, status=200, mimetype="application/json")

    response = { "success": True
               , "post_id": POST_ID
               , "annotations": annotations
               }

    response = json.dumps(response)
    return flask.Response(response, status=200, mimetype="application/json")




@content.route("/posts/create", methods=["POST"])
def create_post():
    session_token    = None
    post_information = None

    TIME             = str(datetime.datetime.now())
    TITLE            = None
    CONTENT          = None
    OWNER            = None
    TAGS             = None

    try:
        request_data = flask.request.get_data().decode("utf-8")
        request_data = json.loads(request_data)

        session_token     = request_data["token"]
        post_information  = request_data["post"]

        TITLE             = request_data["post"]["title"]
        CONTENT           = request_data["post"]["content"]
        TAGS              = request_data["post"]["tags"]
    except Exception as e:
        config.write_server_log("Unable to parse post request: {}".format(str(e)))

        response = { "success": False
                   , "expired": None
                   , "post": None
                   , "id": None }

        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    try: 
        OWNER, expired = config.decode_token(session_token)


        if expired:
            response = { "success": False
                       , "expired": True
                       , "post": post_information
                       , "id": None }

            response = json.dumps(response)
            return flask.Response(response, status=500, mimetype="application/json")
    except Exception as e:
        config.write_server_log("Unable to decode token {}".format(str(e)))

        response = { "success": False
                   , "expired": None
                   , "post": post_information
                   , "id": None }

        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")



    query = connection.Request( "create_post"
                              , INSERT_POST
                              , (TIME, TITLE, psycopg2Json(CONTENT), OWNER)
                              , lambda c: c.fetchone())
    post_id = None
    try:
        post_id = DB.request(query).data[0]

        for tag in TAGS:
            query = connection.Request( "create_tag"
                                      , INSERT_TAG
                                      , (tag, post_id))
            DB.request(query)
    except Exception as e:
        config.write_server_log("Unable to create post, error: {}".format(str(e)))

        response = { "success": False
                   , "expired": False
                   , "post": post_information
                   , "id": None }

        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")
        
    response = { "success": True
               , "expired": False
               , "post": post_information 
               , "id": post_id}

    response = json.dumps(response)
    return flask.Response(response, status=200, mimetype="application/json")


@content.route("/posts/<id>", methods=["GET"])
def get_post(id):
    query = connection.Request( "get_post"
                              , GET_POST
                              , (id, )
                              , lambda c: c.fetchone())
    
    TIME    = None
    TITLE   = None
    CONTENT = None
    OWNER   = None

    try:
        TIME, TITLE, CONTENT, OWNER = DB.request(query).data
    except Exception as e:
        config.write_server_log("Unable to fetch post with id {} reason: {}"\
                .format(id, str(e)))

        response = { "success": False
                   , "time": None
                   , "title": None
                   , "content": None
                   , "owner": None
                   }

        response = json.dumps(response)
        return flask.Response(response, status=200, mimetype="application/json")

    response = { "success": True
               , "time": str(TIME)
               , "title": TITLE
               , "content": CONTENT
               , "owner": OWNER
               }

    response = json.dumps(response)
    return flask.Response(response, status=200, mimetype="application/json")


@content.route("/like", methods=["POST"])
def like():
    session_token   = None
    like_request    = None

    TARGET_ID       = None
    TYPE            = None
    OWNER           = None
    STATE           = None
    
    try:
        request_data = flask.request.get_data().decode("utf-8")
        request_data = json.loads(request_data)

        session_token = request_data["token"]
        like_request  = request_data["like"]

        TARGET_ID     = request_data["like"]["target_id"]
        TYPE          = request_data["like"]["type"]
        STATE         = request_data["like"]["state"]

    except Exception as e:
        config.write_server_log("Unable to parse like request: {}".format(str(e)))

        response = {"success": False, "expired": False, "like": None}
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    try:
        OWNER, expired = config.decode_token(session_token)

        if expired:
            config.write_server_log("Unable to like because session token expired")
            
            response = { "success": False, "expired": True, "like": like_request }
            response = json.dumps(response)

            return flask.Response(response, status=500, mimetype="application/json")
    except Exception as e:
        config.write_server_log("Unable to decode token: {}".format(str(e)))

        response = { "success": False, "expired": None, "like": like_request }
        response = json.dumps(response)

        return flask.Response(response, status=500, mimetype="application/json")


    likeables = { "comment": connection.Request( "comment_like"
                                               , LIKE_COMMENT 
                                               , (TARGET_ID, OWNER, STATE))
                , "post": connection.Request( "post_like"
                                            , LIKE_POST
                                            , (TARGET_ID, OWNER, STATE))
                }

    if TYPE not in likeables:
        config.write_server_log("{} is not likeable".format(TYPE))

        response = { "success": False, "expired": False, "like": like_request }
        response = json.dumps(response)

        return flask.Response(response, status=500, mimetype="application/json")

    query = likeables[TYPE]
    try:
        DB.request(query)
    except Exception as e:
        config.write_server_log("Unable to like, error: {}".format(str(e)))

        response = { "success": False , "expired": False , "like": like_request }
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    response = { "success": True, "expired": False, "like": like_request }
    response = json.dumps(response)
    return flask.Response(response, status=200, mimetype="application/json")


@content.route("/comment", methods=["POST"])
def comment():
    session_token   = None
    comment_request = None

    TARGET_POST     = None
    PARENT_COMMENT  = None
    OWNER           = None
    CONTENT         = None
    TIME            = str(datetime.datetime.now())

    try:
        request_data = flask.request.get_data().decode("utf-8")
        request_data = json.loads(request_data)

        session_token    = request_data["token"]
        comment_request  = request_data["comment"]

        TARGET_POST      = request_data["comment"]["target"]
        PARENT_COMMENT   = request_data["comment"]["parent"]
        CONTENT          = request_data["comment"]["content"]

    except Exception as e:
        config.write_server_log("Unable to parse comment request: {}".format(str(e)))

        response = { "success": False
                   , "expired": False
                   , "comment": None
                   , "id": None}
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    try:
        OWNER, expired = config.decode_token(session_token)

        if expired:
            config.write_server_log("Unable to insert comment, expired token")

            response = { "success": False
                       , "expired": True
                       , "comment": comment_request
                       , "id": None}
            response = json.dumps(response)
            return flask.Response(response, status=500, mimetype="application/json")

    except Exception as e:
        config.write_server_log("Unable to decode token: {}".format(str(e)))

        response = { "success": False
                   , "expired": None
                   , "comment": comment_request
                   , "id": None}
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    query = connection.Request("insert_comment"
                              , INSERT_COMMENT
                              , ( TARGET_POST
                                , PARENT_COMMENT
                                , OWNER
                                , psycopg2Json(CONTENT)
                                , TIME)
                              , fetcher=lambda c: c.fetchone())

    comment_id = None
    try:
        comment_id = DB.request(query).data[0]
    except Exception as e:
        config.write_server_log("Unable to insert comment: {}".format(str(e)))

        response = { "success": False
                   , "expired": False
                   , "comment": comment_request
                   , "id": None}
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    response = { "success": True
               , "expired": False
               , "comment": comment_request
               , "id": comment_id }


    response = json.dumps(response)
    return flask.Response(response, status=200, mimetype="application/json")


@content.route("/annotate", methods=["POST"])
def annotate():
    session_token    = None
    annotate_request = None

    TARGET_POST      = None
    TARGET_COMMENT   = None
    BEGINING         = None
    ENDING           = None
    COLOR            = None
    try:
        request_data = flask.request.get_data().decode("utf-8")
        request_data = json.loads(request_data)

        session_token     = request_data["token"]
        annotate_request  = request_data["annotation"]

        TARGET_POST       = request_data["annotation"]["target_post"]
        TARGET_COMMENT    = request_data["annotation"]["target_comment"]
        BEGINING          = request_data["annotation"]["begining"]
        ENDING            = request_data["annotation"]["ending"]
        COLOR             = request_data["annotation"]["color"]

    except Exception as e:
        config.write_server_log("Unable to parse annotation request: {}".format(str(e)))
        response = { "success": False
                   , "expired": False
                   , "annotation": None
                   , "id": None}
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    try:
        OWNER, expired = config.decode_token(session_token)

        if expired:
            config.write_server_log("Unable to insert annotation, expired token")

            response = { "success": False
                       , "expired": True
                       , "annotation": annotate_request
                       , "id": None}
            response = json.dumps(response)
            return flask.Response(response, status=500, mimetype="application/json")

    except Exception as e:
        config.write_server_log("Unable to decode token: {}".format(str(e)))

        response = { "success": False
                   , "expired": None
                   , "annotation": annotate_request
                   , "id": None}
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")

    query = connection.Request( "insert_annotation"
                              , INSERT_ANNO
                              , ( TARGET_POST
                                , TARGET_COMMENT
                                , BEGINING
                                , ENDING
                                , COLOR)
                              , fetcher=lambda c: c.fetchone())

    anno_id = None
    try:
        anno_id = DB.request(query).data[0]
    except Exception as e:
        config.write_server_log("Unable to insert annotation: {}".format(str(e)))

        response = { "success": False
                   , "expired": False
                   , "annotate_request": annotate_request
                   , "id": None}
        response = json.dumps(response)
        return flask.Response(response, status=500, mimetype="application/json")


    response = { "success": True
               , "expired": False
               , "annotation": annotate_request
               , "id": anno_id}

    response = json.dumps(response)
    return flask.Response(response, status=200, mimetype="application/json")

