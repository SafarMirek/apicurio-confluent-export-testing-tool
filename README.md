# apicurio-confluent-export-testing-tool
Tool for testing Apicurio confluent export util

## Usage
To fill new Confluent instance with predefined schemas use:
```sh
python3 confluent_fill.py
```

## Schemas definition
Tool supports 3 types of schemas: AVRO, PROTOBUF and JSON SCHEMA.
You can see example of file structure below.

```
schemas
├── avro
│   └── [<optional_num>_]<subjectname>
│       ├── <schema_version>.json
│       └── <schema_version>.json
├── jsonSchema
│   └── person
│       ├── person_v1.json
│       ├── person_v2.json
│       └── person_v3.json
└── protobuf
    ├── 00_tutorial
    │   ├── tutorial_v1.proto
    │   └── tutorial_v2.proto
    └── 01_my_schema
        ├── my_schema.proto
        └── my_schema.references
```

To import schema with references you need to define references in second file with the same name as the schema and file extension `.references`.
