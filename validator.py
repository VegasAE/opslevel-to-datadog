import requests
import jsonschema

# Schema for the data dog service
schemaUrl = "https://raw.githubusercontent.com/DataDog/schema/main/service-catalog/v2.2/schema.json"

# Validate the passed yaml file against data dog schema
def validate(DataDogService) -> bool:

    # Get schema from online
    response = requests.get(schemaUrl)
    response.raise_for_status()
    schema = response.json()

    # Validate the data dog service
    try:
        jsonschema.validate(DataDogService, schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(e)
        return False

