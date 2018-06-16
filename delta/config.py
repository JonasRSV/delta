import configparser
import sys
import datetime

config = None

try:
    config = configparser.ConfigParser()
    config.read("delta.config")
except Exception as e:
    sys.stderr.write("Unable to read config because: {}".format(str(e)))
    sys.stderr.write("\nTerminating Program...")
    sys.exit(1)


def write_server_log(message):
    timestamp = datetime.datetime.now()
    file_url  = config["logs"]["server"]

    with open(file_url, "a") as server_log:
        server_log.write("\n{}       --".format(message, str(timestamp)))


        server_log.flush()

    return None
        
