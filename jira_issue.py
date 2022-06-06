# https://jira.readthedocs.io/

from jira import JIRA
import yaml

# Load YAML file secrets
with open('./access.yml', 'r') as file:
    credentials = yaml.safe_load(file)

# Store the values
username = credentials['jira_api']['username']
api_key = credentials['jira_api']['secret']
url = credentials['jira_api']['URL']

def create_issue(username, api_key, server):
    jira_connection = JIRA(
        basic_auth = (username, api_key),
        server = url
    )

    issue_dict = {
        'project': {'key': 'INFOSEC'},
        'assignee': 'Unassigned',
        'summary': 'This item was added via API - ncanino',
        'description': "Some junk JSON for validating passing JSON: \n\n {'status_code': 200, 'headers': {'Server': 'nginx', 'Date': 'Mon, 06 Jun 2022 17:10:09 GMT', 'Content-Type': 'application/json', 'Content-Length': '245', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Strict-Transport-Security': 'max-age=15724800; includeSubDomains, max-age=31536000; includeSubDomains', 'X-Cs-Region': 'us-2', 'X-Cs-Traceid': '17f1d4cf-99b1-468a-a94f-0dffaf63431f', 'X-Ratelimit-Limit': '6000', 'X-Ratelimit-Remaining': '5999'}, 'body': {'meta': {'query_time': 0.030592986, 'pagination': {'offset': 0, 'limit': 100, 'total': 2}, 'powered_by': 'reports', 'trace_id': '17f1d4cf-99b1-468a-a94f-0dffaf63431f'}, 'resources': ['86aeca6409544c2995f23b51363e6090', '47ae4e42fa924b59a940eba3decd3f0d'], 'errors': []}}",
        'issuetype': {'name': 'Bug'},
    }
    # Create a new issue
    new_issue = jira_connection.create_issue(fields=issue_dict)
    print(f'The new JIRA ticket is: {new_issue}.')
    return new_issue
    
create_issue(username, api_key, url)