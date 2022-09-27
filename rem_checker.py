from falconpy import APIHarness
import yaml
import json

# Load YAML file secrets
with open('./access.yml', 'r') as file:
    credentials = yaml.safe_load(file)

# Store the values
access_secret = credentials['api']['secret']
client_key = credentials['api']['client']

falcon = APIHarness(client_id=client_key,
                    client_secret=access_secret
                    )

id_list = '677f0bf47a483832838d1ef064a7f1ce'  # Can also pass a list here: ['ID1', 'ID2', 'ID3']

response = falcon.command("getRemediationsV2", ids=id_list)
print(response)