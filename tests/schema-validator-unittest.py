#!/usr/bin/python
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../third-party/jsonschema")
import jsonschema
import jsonschema.exceptions

class SchemaValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.schemaFileName = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../src/schema.json")
        schemaFile = open(self.schemaFileName)
        self.schema = eval(schemaFile.read())
        schemaFile.close()

    def validateJSONData(self, data, shouldThrow=True):
        try:
            jsonschema.validate(data, self.schema)
            self.assertTrue(not shouldThrow)
        except jsonschema.ValidationError as e:
            self.assertTrue(shouldThrow, e)

    def test_ValidJSONData(self):
        data = {
            "traceEvents": [
                {
                    "args": {
                        "sort_index": -5
                    },
                    "cat": "__metadata",
                    "name": "process_sort_index",
                    "ph": "M",
                    "pid": 29424,
                    "tid": 458,
                    "ts": 0
                }
            ]
        }
        self.validateJSONData(data, False)

    def test_TopLevelTraceEventsPropertyMissingShouldThrow(self):
        data = { "anythingElse": "" }
        self.validateJSONData(data, True)

    def test_InvalidNameForMetadataEventShouldThrow(self):
        data = {
            "traceEvents": [
                {
                    "args": {
                        "sort_index": -5
                    },
                    "cat": "__metadata",
                    "name": "oprocess_sort_index",
                    "ph": "M",
                    "pid": 29424,
                    "tid": 458,
                    "ts": 0
                }
            ]
        }
        self.validateJSONData(data, True)

    def test_InvalidPhaseNameShouldThrow(self):
        data = {
            "traceEvents": [
                {
                    "args": {
                        "sort_index": -5
                    },
                    "cat": "__metadata",
                    "name": "process_sort_index",
                    "ph": "k",
                    "pid": 29424,
                    "tid": 458,
                    "ts": 0
                }
            ]
        }
        self.validateJSONData(data, True)

    def test_ValidDataForDurationEventBegin(self):
        data = {
            "traceEvents": [
                {
                    "args": {
                        "sort_index": -5
                    },
                    "cat": "__metadata",
                    "name": "process_sort_index",
                    "ph": "B",
                    "pid": 29424,
                    "tid": 458,
                    "ts": 1
                }
            ]
        }
        self.validateJSONData(data, False)

    def test_InsufficientPropertiesForDurationEventEndPhaseNameShouldThrow(self):
        data = {
            "traceEvents": [
                {
                    "args": {
                        "sort_index": -5
                    },
                    "cat": "cat1, cat2",
                    "name": "some-name",
                    "ph": "B",
                    "pid": 29424,
                    "tid": 458
                }
            ]
        }
        self.validateJSONData(data, True)

if (__name__ == "__main__"):
    unittest.main(verbosity=2)
