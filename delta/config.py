import configparser
import sys

config = None

try:
    config = configparser.ConfigParser()
    config.read("delta.config")
except Exception as e:
    sys.stderr.write("Unable to read config because: {}".format(str(e)))
    sys.stderr.write("\nTerminating Program...")
    sys.exit(1)
