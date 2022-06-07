# Crowdstrike Tools for NRC

This repo contains scripts and functions for accessing the Crowdstrike API.

## Installation
These scripts require Python 3.9 or above. To install the requirements run the following:

`pip3 install -r requirements.txt`

## YAML File
This tooling requires an `access.yml` file with a Crowdstrike API keypair. The YAML file is in the following structure:
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

### cs_hostcheck.py
This tool will accept a singular argument and search our Crowdstrike tenant and return any matches for the system.

Usage: `cs_hostcheck.py --host MACHINEHOSTNAME` or `cs_hostcheck.py -fh MACHINEHOSTNAME`

Example: `python3 cs_hostcheck.py -fh nbncanino`
 
### get_report_id.py
This tool will all the current reports within the Crowdstrike Tenant that are queriable via `download_report.py`

### download_report.py
This tool will download the report specified from `get_report_id.py` as a format specified.

### spotlight_vulnerabilites.py
This tool will export a list of all items in the matching filter criteria. The output is a .json file meant to be ingested via another toolset.

### Resources
[Official Crowdstrike Python Documentation](https://falconpy.io/)