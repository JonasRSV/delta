import psycopg2
import sys
from delta.database.documents.motion import Motion
from delta.database.documents.document import Document
from delta.config import write_server_log
import time


class Request(object):

    def __init__(self, type, data):
        self.type = type
        self.data = data

    def set_type(self, type):
        self.type = type
        return self

    def set_data(self, data):
        self.data = data
        return self


class Connection(object):
    """DB Connection handler."""
    
    def __init__(self, config, name):
        self.config = config
        self.name   = name
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

        self.connect()

    def connect(self):
        """Connect to database."""
        while True:
            try:
                self.connection = psycopg2.connect(self.connection_string)
                write_server_log("Connection to database successful! {}".format(self.name))
                break
            except Exception as e:
                write_server_log("Unable to connect to database from {}, reason: {}".format(self.name, str(e)))
                time.sleep(5)



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
            raise NotImplementedError("Don't recognize request {}".format(self.type))

        return request




    

