import psycopg2
import sys


class Connection(object):
    """DB Connection handler."""
    
    DOC_ID_OR_TYPE =   "SELECT * FROM DOCUMENTS WHERE %s LIKE ID AND "\
                     + "TIME > %s LIMIT %s;"

    DOC_REGULAR    =   "SELECT * FROM DOCUMENTS WHERE TIME > %s LIMIT %s;"


    def __init__(self, config):
        self.config = config
        self.connection = None
        self.connection_string = "host={} dbname={} port={} user={} password={}"\
            .format( config["database"]["host"]
                   , config["database"]["dbname"]
                   , config["database"]["port"]
                   , config["database"]["user"]
                   , config["database"]["password"])

        self.cursor = None

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

    def request_documents(self, doc_request):
        """Get documents according to doc_request specification."""
        self.check_connection()

        limit = doc_request.limit
        if limit is None:
            limit = 10000

        try:
            if doc_request.id is None and doc_request.type is None:
                self.cursor.execute(  Connection.DOC_REGULAR
                                   , (doc_request.date, limit))

                return doc_request.set_payload(self.cursor.fetchall())

            if not doc_request.id is None:
                self.cursor.execute(  Connection.DOC_ID_OR_TYPE
                                   ,  (doc_request.id, doc_request.date, limit))

                return doc_request.set_payload(self.cursor.fetchall())

            self.cursor.execute(  Connection.DOC_ID_OR_TYPE
                               ,  (doc_request.type, doc_request.date, limit))

            return doc_request.set_payload(self.cursor.fetchall())
        except Exception as e:
            print(e)
            """Add error handling."""
            print("Failed to get requested document: {}".format(str(e)))
            sys.exit(1)

        return None




    

