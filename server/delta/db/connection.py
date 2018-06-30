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
        self.cursor.execute(request.query, request.params)

        """Need to add validation that request actually succeeded."""

        request.data = request.fetcher(self.cursor)

        return request


class Request(object):

    def __init__(self, type, query, params, fetcher=lambda _:_):
        self.__type     = type
        self.__query    = query
        self.__params   = params

        self.__data     = None
        self.fetcher    = fetcher

    @property
    def data(self):
        return self.__data

    @property
    def type(self):
        return self.__type

    @property
    def query(self):
        return self.__query

    @property
    def params(self):
        return self.__params

    @data.setter
    def data(self, data):
        if self.__data is None:
            self.__data = data
        else:
            raise Exception("Cannot set data that is already set.")

    @query.setter
    def query(self, query):
        if self.__query is None:
            self.__query = query
        else:
            raise Exception("Cannot set query that is already set.")

    @type.setter
    def type(self, type):
        if self.__type is None:
            self.__type = type
        else:
            raise Exception("Cannot set type that is already set.")

    @params.setter
    def params(self, params):
        if self.__params is None:
            self.__params = params
        else:
            raise Exception("Cannot set params that is already set.")

