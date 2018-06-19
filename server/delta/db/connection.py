import psycopg2
import sys
import config 
import time



class Connection(object):
    """DB Connection handler."""
    
    def __init__(self, name):
        self.name   = name
        self.connection = None
        self.connection_string = "host={} dbname={} port={} user={} password={}"\
            .format( config.config["database"]["host"]
                   , config.config["database"]["dbname"]
                   , config.config["database"]["port"]
                   , config.config["database"]["user"]
                   , config.config["database"]["password"])

        self.cursor   = None
        self.handlers = {}

        self.connect()

    def connect(self):
        """Connect to database."""
        while True:
            try:
                self.connection = psycopg2.connect(self.connection_string)
                config.write_server_log("Connection to database successful! {}".format(self.name))
                break
            except Exception as e:
                config.write_server_log("Unable to connect to database from {}, reason: {}".format(self.name, str(e)))
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

        """Remove this later."""
        if not hasattr(request, "type"):
            raise Exception("requests should have a type.")

        if request.type in self.handlers:
            return self.handlers[request.type](self.cursor, request.data)
        else:
            raise NotImplementedError("Don't recognize request {}".format(self.type))

        return request




    

