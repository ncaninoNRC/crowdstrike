from falconpy import APIHarness
import yaml

# Load YAML file secrets
with open('./access.yml', 'r') as file:
    credentials = yaml.safe_load(file)

# Store the values
access_secret = credentials['api']['secret']
client_key = credentials['api']['client']

# You'll need to find the proper report ID and fill it in here use get_report_id.py
report_id = '86aeca6409544c2995f23b51363e6090'

# What to save the file as
save_file = "report.csv"

# Look another function...
def download(client, secret, report_ID, filename):
    # Connect to the API
    falcon = APIHarness(client_id=client,
                        client_secret=access_secret
                        )

    # We should note, don't ever print out the response unless its like... 10 lines.
    print("[-] Getting Report...")
    response = falcon.command("report_executions_download_get", ids=report_ID)
    print(f"[-] Saving report as {filename}...")
    open(filename, 'wb').write(response)

    # Close out our session
    print("[-] Closing our API session...")
    falcon.deauthenticate()
    print("[-] Complete.")


# Call the function
download(client_key, access_secret, report_id, "report.csv")