from falconpy import APIHarness
import yaml
import json

# Load YAML file secrets
with open('./access.yml', 'r') as file:
    credentials = yaml.safe_load(file)

# Store the values
access_secret = credentials['api']['secret']
client_key = credentials['api']['client']

filter_string = "cve.exprt_rating:'HIGH'+host_info.tags:['FalconGroupingTags/Production']"
#test_filter = "host_info.tags:['FalconGroupingTags/Production']"

def query_api(client,secret,filter):
    print("[-] Authenticating against the Crowdstrike API...")
    falcon = APIHarness(client_id=client,
                        client_secret=secret
                        )
    print("[-] Running query...")
    response = falcon.command("combinedQueryVulnerabilities",
                            filter=filter,
                            limit=400,
                            facet="host_info",
                            sort="created_timestamp"
                            )["body"]
                            
    # Make it pretty
    pretty_json = json.dumps(response, indent=4)

    # Write the file
    print("[-] Writing results to vulnerability_list.json...")
    with open('vulnerability_list.json', 'w') as outfile:
        outfile.write(pretty_json)

    print("[-] Closing our API session...")
    falcon.deauthenticate()


# Call the function
query_api(client_key,access_secret,filter_string)