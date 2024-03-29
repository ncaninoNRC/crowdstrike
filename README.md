# Crowdstrike Tools for NRC

This repo contains scripts and functions for accessing the Crowdstrike API.

## Installation
These scripts require Python 3.9 or above. To install the requirements run the following:

`pip3 install -r requirements.txt`

## YAML File
This tooling requires an `access.yml` file with a Crowdstrike API keypair and a JIRA API key. The YAML file is in the following structure:
```
api:
  secret: <CROWDSTRIKE API SECRET KEY>
  client: <CROWDSTRIKE CLIENT KEY>

jira_api:
  secret: <JIRA API KEY>
  username: <NRC EMAIL>
  URL: https://nrc-eng.atlassian.net
```
## Tools

### cs_create_user.py
This tool is meant to streamline the user creation process. The exe is also available in the root of this repo. *YOU MUST RUN THE EXE FROM A CONSOLE*.

Usage: `cs_create_user.py --apikey APIKEYHERE`

### cs_hostcheck.py
This tool will accept a singular argument and search our Crowdstrike tenant and return any matches for the system.

Usage: `cs_hostcheck.py --host MACHINEHOSTNAME` or `cs_hostcheck.py -fh MACHINEHOSTNAME`

Example: `python3 cs_hostcheck.py -fh nbncanino`

### bulk_user.py
This tool accepts commands for bulk user management. `users.json` is provided as a template for the users data structure.

Usage: `bulk_user.py -h` will display a help output. `bulk_user.py -d DATAFILE -c COMMAND -k CLIENT_ID -s CLIENT_SECRET` will perfom the `COMMAND` on the data provided via `DATAFILE`.

### get_report_id.py
This tool will all the current reports within the Crowdstrike Tenant that are queriable via `download_report.py`

### download_report.py
This tool will download the report specified from `get_report_id.py` as a format specified.

### spotlight_vulnerabilites.py
This tool has multiple functions within. It can export a list of all items in the matching filter criteria. The output is a .json file meant to be ingested via another toolset - `jira.py`.

### jira.py
This tool will create an automatic ticket based on variables within. Meant to be used a basic bootstrap for automating data output from other tools.

### Resources
[Official Crowdstrike Python Documentation](https://falconpy.io/)
