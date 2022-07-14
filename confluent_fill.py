from pathlib import Path
import optparse
import os
import requests
import re
import json

def post_schema(confluentUrl: str, auth, subject: str, schemaType, schema, references):
    payload = {
            "schemaType": schemaType,
            "schema": schema,
    }

    if references is not None:
        payload["references"] = references
    
    response = requests.post(confluentUrl + "subjects/" + subject + "/versions", json=payload, auth=('Mirek', 'Mirek'))
    print(response.status_code)

def process_schemas(directory: str, schemaType: str):
    references_reg = re.compile('.*\.references$')

    for testName in sorted(os.listdir(directory)):
        print("Test:" + str(testName))
        #for all files
        for file in sorted(os.listdir(f"{directory}/{testName}")):
            file = re.sub(r"^[0-9]*_", "", file)
            if re.match(references_reg, str(file)):
                continue
            print("Schema:" + str(file))
            with open(f"{directory}/{testName}/{file}") as f:
                contents = f.read()
                references = None
                try:
                    with open(f"{directory}/{testName}/" + os.path.splitext(file)[0] + ".references") as refFile:
                        references = json.load(refFile)
                        print(str(file) + " has references.")
                except:
                    pass
                post_schema(confluentUrl, auth, re.sub(r"^[0-9]*_", "", testName), schemaType, contents, references)



parser = optparse.OptionParser()
parser.set_defaults(debug=False, json=False, avro=False, protobuf=False)
parser.add_option('--debug', action='store_true', dest='debug')
parser.add_option('--json', action='store_true', dest='json')
parser.add_option('--avro', action='store_true', dest='avro')
parser.add_option('--protobuf', action='store_true', dest='protobuf')
parser.add_option('--confluent', action='store', dest='confluentUrl')
parser.add_option('--username', action='store', dest='username')
parser.add_option('--password', action='store', dest='password')
(options, args) = parser.parse_args()

json_schema = options.json
avro = options.avro
protobuf = options.protobuf
confluentUrl = options.confluentUrl or "http://localhost:8081/"
auth = (options.username, options.password)

all = not json_schema and not avro and not protobuf

if json_schema or all:
    process_schemas("./schemas/jsonSchema", "JSON")

if avro or all:
    process_schemas("./schemas/avro", "AVRO")

if protobuf or all:
    process_schemas("./schemas/protobuf", "PROTOBUF")
