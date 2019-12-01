import json
import sys

if len(sys.argv) is not 2:
    print("usage: python process-messages.py filename")
    exit()

filename = sys.argv[1]

with open(filename) as json_file:
    data = json.load(json_file)
    print("number of messages received:", len(data))
