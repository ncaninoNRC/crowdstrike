from falconpy import ReportExecutions
import yaml

# Load YAML file secrets
with open('./access.yml', 'r') as file:
    credentials = yaml.safe_load(file)

# Store the values
access_secret = credentials['api']['secret']
client_key = credentials['api']['client']

# Put the things in a function this time I suppose...
def get_report_id(client, access):
    # Connect to the api
    falcon = ReportExecutions(client_id=client,
                             client_secret=access
                            )

    # Get reports limited to 100 results by created on date
    print("[-] Getting reports....")
    response = falcon.query_reports(sort="created_on",
                                    limit=100,
                                    )
    print(response)
    return response

# Call said function
get_report_id(client_key, access_secret)



