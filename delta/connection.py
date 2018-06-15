import psycopg2
import sys
from delta.database.motion import Motion
from delta.database.document import Document



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




    

