#!/usr/bin/python
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../third-party/jsonschema")
import jsonschema
import jsonschema.exceptions

def main(argv):
    if len(argv) < 3:
        print "Usage: "
        print "\t" + os.path.basename(__file__) + " <json file> <schema file>"
        sys.exit(-1)

    jsonFile = open(argv[1])
    jsonContents = jsonFile.read()
    jsonFile.close()

    schemaFile = open(argv[2])
    jsonSchema = schemaFile.read()
    schemaFile.close()

    try:
        jsonschema.validate(eval(jsonContents), eval(jsonSchema))
        print "Provided JSON is valid against the schema."
    except jsonschema.ValidationError as e:
        print e

if (__name__ == "__main__"):
    sys.exit(main(sys.argv))
