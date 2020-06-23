# py_geoip_nslookup
Get geolocation and blacklist information for a given domain using Python.

# REQUIREMENTS
This script relies on the following Python Packages:
- requests
- nslookup

The above requirements can be installed by using the following command:
```
sudo pip3 install requests nslookup
```

# USAGE
Usage is straight-forward, just run the script from the command line with the domain to lookup as an argument to the script.
```
python3 nslookup-geo.py www.google.com
```
The output will be similar to the following:
```
          Domain: www.google.com
              IP: 216.58.210.196
    Country Code: US
         Country: United States
Domain Blacklist: []
    MX Blacklist: []
    NS Blacklist: []
    Domain Score: 0
    IP Blacklist: []
        IP Score: []
```

# TODO
I need to look into why the script never returns when specifying a DNS server to query. This could be an issue with the nslookup package.
