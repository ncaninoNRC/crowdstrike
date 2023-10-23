import requests
from falconpy import APIHarness
import yaml
from time import sleep
import json
import argparse

# Define groups
GROUPS = {
    "Systems": ["falcon_console_guest", "desktop_support", "help_desk", "vulnerability_manager", "identity_protection_admin", "overwatch_malware_submitter", "scheduled_report_analyst", "event_viewer", "falconhost_investigator", "idp_domain_admin_manager", "identity_protection_admin"],
    "Service Desk": ["falcon_console_guest", "desktop_support", "help_desk", "event_viewer", "identity_protection_admin", "overwatch_malware_submitter", "scheduled_report_analyst", "vulnerability_manager"],
    "DevOps": ["falcon_console_guest", "kubernetes_protection_admin", "horizon_analyst", "falconhost_analyst", "image_viewer"],
    "Developer": ["falcon_console_guest", "kubernetes_protection_read_only_analyst", "horizon_analyst", "image_viewer"]
}

# Client ID
CLIENT_ID = "5c1b024cdd8847cc8dea061da7a9c272"

# Argument function
def parse_arguments():
    parser = argparse.ArgumentParser(description='Crowdstrike user creation script.')
    parser.add_argument('--apikey', required=True, help='Required API key for user creation. If you do not have access to this, contact the Security Team.')
    return parser.parse_args()

# Load credentials from a YAML file
# def load_credentials_from_yaml(filename="config.yaml"):
#     with open(filename, 'r') as file:
#         config = yaml.safe_load(file)
#         return config["api_credentials"]["CLIENT_ID"], config["api_credentials"]["CLIENT_SECRET"]
    
# Fetch token using FalconPy SDK
def fetch_token(client_id, client_secret):
    print("Obtaining token from CrowdStrike API...")

    falcon = APIHarness(client_id=client_id, client_secret=client_secret)
    
    payload = {
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = falcon.command("oauth2AccessToken", data=payload)
    
    # Debugging: Print the response when fetching the token
    # print("Token Fetch Response:", json.dumps(response, indent=4))

    token = response['body']['access_token']
    # Debugging: Print the obtained token
    # print("Obtained Token:", token)
    return token

# Select grouping of roles
def select_roles_from_list(roles):
    for idx, role in enumerate(roles, 1):
        print(f"{idx}. {role['name']} (ID: {role['id']})")
    
    selected_indices = input("Enter the numbers of the roles you want to assign, separated by commas: ").split(',')
    return [roles[int(idx) - 1]['id'] for idx in selected_indices]

# Get user details
def get_user_details():
    print("Gathering user details...")
    print("\nEnter details for the new user:")

    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    uid = input("Email address: ").strip()

    return first_name, last_name, uid

# Make a person, like Zues!
def create_user(first_name, last_name, uid):
    print(f"Creating user: {first_name} {last_name} with UID: {uid}...")
    body = {
        "firstName": first_name,
        "lastName": last_name,
        "uid": uid
    }

    response = falcon.command("CreateUser", body=body)

    return response

# Fetch roles with requests because falconpy hates me
def fetch_roles_with_token(token):
    print("Fetching available roles from CrowdStrike API...")

    url = "https://api.us-2.crowdstrike.com/user-management/queries/roles/v1?action=grant"
    
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}"
    }
    
    # Debugging: Print the used token for the roles request
    # print("Used Token for Roles Request:", token)

    response = requests.get(url, headers=headers)
    
    # Debugging output
    # print("Roles Fetch Response Status:", response.status_code)
    # print("Roles Fetch Response JSON:", response.json())
    
    return response.json()

# Assign selected roles to a user using FalconPy SDK
def assign_roles_to_user(falcon_instance, client_id, client_secret, user_uuid, roles):
    print(f"Assigning roles to user with UUID: {user_uuid}...")
    
    body = {
        "roleIds": roles
    }

    response = falcon_instance.command("GrantUserRoleIds", user_uuid=user_uuid, body=body)
    
    # Debugging response
    # print("Role Assignment Response:", json.dumps(response, indent=4))
    
    if response["status_code"] == 200 :  # Updated this line to check for 200 or 201
        print(f"Successfully assigned roles to the user with UUID: {user_uuid}")
    else:
        print("Failed to assign roles to the user.")
        print(json.dumps(response, indent=4))
        
    
    return response

# Group selection
def prompt_group_selection():
    print("\nSelect a group for the user:")
    for index, group_name in enumerate(GROUPS.keys(), 1):
        print(f"{index}. {group_name}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the group: "))
            if 1 <= choice <= len(GROUPS):
                return list(GROUPS.keys())[choice-1]
            else:
                print("Invalid choice. Please select a valid group number.")
        except ValueError:
            print("Please enter a number.")

if __name__ == "__main__":
    print("Starting the user creation process...")
    #CLIENT_ID, CLIENT_SECRET = load_credentials_from_yaml()

    # Parse the command line arguments
    args = parse_arguments()
    CLIENT_SECRET = args.apikey
    
    # Authenticate
    falcon = APIHarness(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    token = fetch_token(CLIENT_ID, CLIENT_SECRET)

    sleep(1) # Rate limited?

    first_name, last_name, uid = get_user_details()

    sleep(1) # Rate limited?

    user_response = create_user(first_name, last_name, uid)

    sleep(1) # Rate limited?

    if user_response.get("status_code") == 201:
        print("User created successfully!")
        user_id = user_response["body"]["resources"][0]["uuid"]
    else:
        print("Failed to create user.")
        print(user_response)
        exit(1)

    available_roles = fetch_roles_with_token(token)
    sleep(1)

    if not available_roles:
        print("Failed to fetch roles.")
        exit(1)

    selected_group = prompt_group_selection()
    selected_roles = GROUPS[selected_group]

    role_assignment_response = assign_roles_to_user(falcon, CLIENT_ID, CLIENT_SECRET, user_id, selected_roles)

    if role_assignment_response.get("status_code") in [200, 201]:
        print(f"Roles assigned: {selected_roles}.")
    else:
        print(f"Failed to assign roles to the user.")