from falconpy import APIHarness
import yaml
import json
import jmespath

# Load YAML file secrets
with open('./access.yml', 'r') as file:
    credentials = yaml.safe_load(file)

# Store the values
access_secret = credentials['api']['secret']
client_key = credentials['api']['client']

# Authenticate
print("[-] Authenticating against the Crowdstrike API...")
falcon = APIHarness(client_id=client_key,
                    client_secret=access_secret
                    )

filter_string = "cve.exprt_rating:'HIGH'+host_info.tags:['FalconGroupingTags/Production']"
#test_filter = "host_info.tags:['FalconGroupingTags/Production']"

def query_api(filter):
    print("[-] Running query...")
    response = falcon.command("combinedQueryVulnerabilities",
                            filter=filter,
                            limit=400,
                            facet="host_info",
                            sort="created_timestamp"
                            )["body"]

    # Make it pretty
    pretty_json = json.dumps(response, indent=4)
    vuln_data = json.loads(pretty_json)

    """
    Master Query
    hostname = jmespath.search("resources[*].[apps[].remediation.ids, host_info.hostname, host_info.local_ip, cve]", vuln_data)
    """

    full_query = "resources[*].[apps[].remediation.ids, host_info.hostname, host_info.local_ip, cve]"
    hostname = "resources[*].[host_info.hostname]"
    cve = "resources[*].[cve]"
    remediation = "resources[*].[apps[].remediation.ids]"

    print(jmespath.search(hostname, vuln_data))
    print(jmespath.search(remediation, vuln_data))
    
    """
    Save the file if we want
    Write the file
    print("[-] Writing results to vulnerability_list.json...")
    with open('vulnerability_list.json', 'w') as outfile:
         outfile.write(pretty_json)
    """


def get_remediation(remediation_id):
    print("Getting Remediation ID's...")
    response = falcon.command("getRemediationsV2", ids=remediation_id)
    
    print("[-] Geting Remediation Steps...")
    remediation_action = "body.resources[]"

    # Make it pretty
    pretty_json = json.dumps(response, indent=4)

    # Reload pretty json
    remediation_data = json.loads(pretty_json)

    # Debugging print
    print(remediation_data)

    # Reprint results we need
    pretty_results = json.dumps((jmespath.search(remediation_action, remediation_data)), indent=4)
    print(pretty_results)

    return pretty_results

# Call the functions
#query_api(filter_string)
get_remediation('677f0bf47a483832838d1ef064a7f1ce')

# Close session after running

print("[-] Closing our API session...")
falcon.deauthenticate()