#
# Perform a authentication request
#

import sys
import json
import requests

###############################################################################
# MAIN
###############################################################################

if __name__ == '__main__':

    username = sys.argv[1]
    password = sys.argv[2]
    organization = sys.argv[3]
    url = "testsliderule.org"

    # Set URL
    if len(sys.argv) > 4:
        url = sys.argv[4]

    # Authentication Request
    url = "https://ps." + url + "/ps/api/org_token/"
    rqst = {"username": username, "password": password, "org_name": organization}
    headers = {'Content-Type': 'application/json'}
    rsps = requests.post(url, data=json.dumps(rqst), headers=headers, timeout=(60,10)).json()
    print("Login Response: ", rsps)
    refresh = rsps["refresh"]
    access = rsps["access"]

    # Organization Access Request
    url = "https://ps." + url + "/ps/api/get_membership_status/" + organization + "/"
    headers = {'Authorization': 'Bearer ' + access}
    rsps = requests.get(url, headers=headers, timeout=(60,10)).json()
    print("Validation Response: ", rsps)