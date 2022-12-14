import os
import requests
import IP2Location
import sys

def get_location(ip):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IPDB_PATH = os.path.join(BASE_DIR, 'ip2location_db')
    file = str(IPDB_PATH) + "/IP2LOCATION-LITE-DB1.BIN"
    # print("db_path = ", file)
    # ip = requests.get('http://ip.42.pl/raw').text
    IP2LocObj = IP2Location.IP2Location()
    IP2LocObj.open(file)
    rec = IP2LocObj.get_all(ip)
    print(rec)
    # return rec


if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = None

    return_val = get_location(arg)
