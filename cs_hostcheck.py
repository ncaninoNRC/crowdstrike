# Resources https://falconpy.io/Service-Collections/Hosts.html#getdevicedetails

import os
import resource
import string
import yaml
import argparse
from falconpy import Hosts

# Load YAML file secrets
with open('./access.yml', 'r') as file:
    credentials = yaml.safe_load(file)

# Store the values
access_secret = credentials['api']['secret']
client_key = credentials['api']['client']

hosts = Hosts(client_id=client_key, client_secret=access_secret)

# Modify help message 
helpM = "Help! Use the --host command to search for a host in our Crowdstrike tenant. Example: cs_hostcheck.py --host nbnanino"

# Init parser
parser = argparse.ArgumentParser(description = helpM)

# Add parser options
parser.add_argument("-fh", "--host", type = str, required = True, help = "Enter a hostname with the argument: --host HOSTNAME")

# Parse the given args
args = parser.parse_args()

SEARCH_FILTER = args.host

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
            # Display data on the query
            aid = detail["device_id"]
            hostname = detail["hostname"]
            os_version = detail["os_version"]
            external_ip = detail["external_ip"]
            first_seen = detail["first_seen"]
            last_seen = detail["last_seen"]
            print(f"Hostname: {hostname}\nAID: {aid}\nOS Version: {os_version}\nExternal IP: {external_ip}\nFirst seen: {first_seen}\nLast seen: {last_seen}")
    else:
        print(f"{SEARCH_FILTER} has no matching hostname within your Falcon tenant.")
else:
    # Retrieve the details of the error response
    error_detail = hosts_search_result["body"]["errors"]
    for error in error_detail:
        # Display the API error detail
        error_code = error["code"]
        error_message = error["message"]
        print(f"[Error {error_code}] {error_message}")