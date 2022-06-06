# Crowdstrike Tools for NRC

This repo is for tools made to leverage the Crowdstrike API.

This tooling requires an `access.yml` file with a Crowdstrike API keypair.

## Tools

### cs_hostcheck.py
This tool will accept a singular argument and search our Crowdstrike tenant and return any matches for the system.

Usage: `cs_hostcheck.py --host MACHINEHOSTNAME` or `cs_hostcheck.py -fh MACHINEHOSTNAME`

Example: `python3 cs_hostcheck.py -fh nbncanino`
 
 ### Resources
 [Official Crowdstrike Python Documentation](https://falconpy.io/)