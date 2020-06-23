#!/usr/bin/python3

import requests
import sys
from nslookup import Nslookup

# Connection Information for IP Geolocation, used to get geolocation
IPGEO_API_URL = "https://api.ipgeolocation.io/ipgeo"
IPGEO_API_KEY = "b2eb304fb75f4956b946a99ff022c5d2"

# Connection information for Auth0, used to get blacklist information
AUTH0_API_URL = "https://signals.api.auth0.com/v2.0/ip/"
AUTH0_API_KEY = "eed8ca8a-4678-40a3-98b7-d762f66fcf59"

# If we don't have at least 1 argument, len = 1 is just the script name
if len(sys.argv) < 2:
    print("Usage: nslookup-geo.py DOMAIN.TO.LOOKUP [DNS.SERVER.TO.USE]")
    sys.exit()

# The domain to lookup
lookup_domain = sys.argv[1]

# If the length of argv is more than 2, meaning we have the script name,
# a domain to lookup and a DNS server to use.
if len(sys.argv) > 2:
    #TODO: Why is this not returning?
    dns_query = Nslookup(dns_servers=sys.argv[2])
else:
    dns_query = Nslookup()

dns_resp = dns_query.dns_lookup(lookup_domain)

# had to do a length check, because nothing is returned if there is no result
if len(dns_resp.answer) > 0:
    lookup_ip = dns_resp.answer[0]
else:
    print(f"Unable to get IP Address for {lookup_domain}")
    sys.exit()


def ipgeo_lookup():
    """
    Gets the IP address associated with the domain, also gets the
    geolocation information. Prints the information to the console.
    :return: None
    """
    api_params = {"apiKey": IPGEO_API_KEY, "ip": lookup_ip}
    geo_ip = requests.get(IPGEO_API_URL, params=api_params)

    # If we got somekind of an error in response, show what it is
    if geo_ip.status_code != 200:
        print(f"Request Status Code: {geo_ip.status_code}")
        print(f"{geo_ip.text}")
        sys.exit()

    # Get the JSON object returned by the request
    answer = geo_ip.json()

    # Show the information we want to see
    print(f"          Domain: {lookup_domain}")
    print(f"              IP: {answer['ip']}")
    print(f"    Country Code: {answer['country_code2']}")
    print(f"         Country: {answer['country_name']}")


def auth0_lookup():
    """
    Queries Auth0 to determine any blacklists that the IP in question may be on, prints
    the results to the console.
    :return: None
    """
    auth0_headers = {"X-Auth-Token": AUTH0_API_KEY}
    geo_ip = requests.get(AUTH0_API_URL + lookup_ip, headers=auth0_headers)

    # Get the JSON object returned by the request
    full_ip = geo_ip.json()

    print(f"Domain Blacklist: {full_ip['fullip']['baddomain']['domain']['blacklist']}")
    print(f"    MX Blacklist: {full_ip['fullip']['baddomain']['domain']['blacklist']}")
    print(f"    NS Blacklist: {full_ip['fullip']['baddomain']['domain']['blacklist']}")
    print(f"    Domain Score: {full_ip['fullip']['baddomain']['domain']['score']}")
    print(f"    IP Blacklist: {full_ip['fullip']['baddomain']['ip']['blacklist']}")
    print(f"        IP Score: {full_ip['fullip']['baddomain']['ip']['blacklist']}")


ipgeo_lookup()
auth0_lookup()
