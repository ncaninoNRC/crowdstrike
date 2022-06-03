import yaml
from falconpy import Hosts

# Load YAML file secrets
with open('./access.yml', 'r') as file:
    credentials = yaml.safe_load(file)

# Store the values
access_secret = credentials['api']['secret']
client_key = credentials['api']['client']

hosts = Hosts(client_id=client_key, client_secret=access_secret)

SEARCH_FILTER = "Stuff Here"

# Retrieve a list of hosts that have a hostname that matches our search filter
hosts_search_result = hosts.query_devices_by_filter(filter=f"hostname:'{SEARCH_FILTER}'")

# Confirm we received a success response back from the CrowdStrike API
if hosts_search_result["status_code"] == 200:
    hosts_found = hosts_search_result["body"]["resources"]
    # Confirm our search produced results
    if hosts_found:
        # Retrieve the details for all matches
        hosts_detail = hosts.get_device_details(ids=hosts_found)["body"]["resources"]
        for detail in hosts_detail:
            # Display the AID and hostname for this match
            aid = detail["device_id"]
            hostname = detail["hostname"]
            print(f"{hostname} ({aid})")
    else:
        print("No hosts found matching that hostname within your Falcon tenant.")
else:
    # Retrieve the details of the error response
    error_detail = hosts_search_result["body"]["errors"]
    for error in error_detail:
        # Display the API error detail
        error_code = error["code"]
        error_message = error["message"]
        print(f"[Error {error_code}] {error_message}")