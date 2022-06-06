# Crowdstrike Tools for NRC

This repo is for tools made to leverage the Crowdstrike API.

This tooling requires an `access.yml` file with a Crowdstrike API keypair.

## Tools

### cs_hostcheck.py
This tool will accept a singular argument and search our Crowdstrike tenant and return any matches for the system.

Usage: `cs_hostcheck.py --host MACHINEHOSTNAME` or `cs_hostcheck.py -fh MACHINEHOSTNAME`

Example: `python3 cs_hostcheck.py -fh nbncanino`
 
### get_report_id.py
This tool will all the current reports within the Crowdstrike Tenant that are queriable via `download_report.py`

### download_report.py
This tool will download the report specified from `get_report_id.py` as a format specified.

### Resources
[Official Crowdstrike Python Documentation](https://falconpy.io/)