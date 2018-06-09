import psycopg2
import sys


class Motion(object):

    ID      =   "SELECT * FROM DOCUMENT JOIN MOTION ON "\
            +   "DOCUMENT.ID = MOTION.ID WHERE %s LIKE DOCUMENT.ID "\
            +   "AND TIME > %s LIMIT %s;"

    TYPE    =   "SELECT * FROM DOCUMENT JOIN MOTION ON "\
            +   "DOCUMENT.ID = MOTION.ID WHERE %s LIKE DOCUMENT.TYPE "\
            +   "AND TIME > %s LIMIT %s;"

    REGULAR =   "SELECT * FROM DOCUMENT JOIN MOTION ON "\
            +   "DOCUMENT.ID = MOTION.ID AND TIME > %s LIMIT %s;"

    def request(cursor, request):
        limit = request.limit
        if limit is None:
            limit = 10000

        try:
            if request.id is not None:
                cursor.execute( Motion.ID
                              , (request.id, request.date, limit))

                return request.set_payload(cursor.fetchall())
            elif request.type is not None:
                cursor.execute( Motion.TYPE
                              , (request.type, request.date, limit))

                return request.set_payload(cursor.fetchall())
            else:
                cursor.execute( Motion.REGULAR
                              , (request.date, limit))

                return request.set_payload(self.cursor.fetchall())

        except Exception as e:
            print(e)
            """Add error handling."""
            print("Failed to get requested document: {}".format(str(e)))
            sys.exit(1)

        return request



class Document(object):
    ID      =   "SELECT * FROM DOCUMENT WHERE %s LIKE ID AND "\
            +   "TIME > %s LIMIT %s;"

    TYPE    =   "SELECT * FROM DOCUMENT where %s LIKE TYPE AND "\
            +   "TIME > %s LIMIT %s;"

    REGULAR =   "SELECT * FROM DOCUMENT WHERE TIME > %s LIMIT %s;"

    def request(cursor, request):
        limit = request.limit
        if limit is None:
            limit = 10000

        try:
            if request.id is not None:
                cursor.execute( Document.ID
                              , (request.id, request.date, limit))

                return request.set_payload(cursor.fetchall())
            elif request.type is not None:
                cursor.execute( Document.TYPE
                              , (request.type, request.date, limit))

                return request.set_payload(cursor.fetchall())
            else:
                cursor.execute( Document.REGULAR
                              , (request.date, limit))

                return request.set_payload(self.cursor.fetchall())

        except Exception as e:
            print(e)
            """Add error handling."""
            print("Failed to get requested document: {}".format(str(e)))
            sys.exit(1)

        return request


class Connection(object):
    """DB Connection handler."""
    
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.connection_string = "host={} dbname={} port={} user={} password={}"\
            .format( config["database"]["host"]
                   , config["database"]["dbname"]
                   , config["database"]["port"]
                   , config["database"]["user"]
                   , config["database"]["password"])

        self.cursor   = None

        self.handlers = { "document": Document.request
                        , "mot"  : Motion.request}

    def connect(self):
        """Connect to database."""
        try:
            self.connection = psycopg2.connect(self.connection_string)
        except Exception as e:
            """Need to add some error handling."""
            print("DB connection failed. {}".format(str(e)))
            sys.exit(1)

        """Commit after each command."""
        self.connection.set_session(autocommit=True)

        """Initialize curosor."""
        self.cursor = self.connection.cursor()

        return None

    def check_connection(self):
        if not self.cursor.closed:
            return None

        """Error handling issue applies here too."""
        self.connect()

        return None

    def request(self, request):
        """Get documents according to doc_request specification."""
        self.check_connection()

        if request.type in self.handlers:
            return self.handlers[request.type](self.cursor, request.data)
        else:
            raise NotImplementedError("Don't regonize request {}".format(self.type))

        return request




    

