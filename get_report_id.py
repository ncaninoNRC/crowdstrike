from falconpy import ReportExecutions
import yaml

# Load YAML file secrets
with open('./access.yml', 'r') as file:
    credentials = yaml.safe_load(file)

# Store the values
access_secret = credentials['api']['secret']
client_key = credentials['api']['client']

falcon = ReportExecutions(client_id=client_key,
                          client_secret=access_secret
                          )

# Put the things in a function this time I suppose...
def get_report_id(client, access):
    from falconpy import ReportExecutions

    falcon = ReportExecutions(client_id=client,
                             client_secret=access
                            )

    response = falcon.query_reports(sort="created_on",
                                    limit=100,
                                    )
    print(response)
    return response

# Call said function
get_report_id(client_key, access_secret)



