import os
import time
import re
from netifaces import interfaces, ifaddresses, AF_INET

def ip4_addresses():
    """
    return host's ipv4 addresses
    """
    ip_list = []
    for interface in interfaces():
        if AF_INET in ifaddresses(interface):
            for link in ifaddresses(interface)[AF_INET]:
                if link['addr'] != "127.0.0.1":
                    ip_list.append(link['addr'])
    if len(ip_list) == 0:
        return None
    return ip_list[0]

DATA_DIR = '/Users/apple/archivebox/data'
os.chdir(DATA_DIR)

def add_url(url, log_file="/tmp/log.txt"):
    """use archivebox API to crawl the html of the given url,
    return the path this file on the local filesystem
    @param url: target url
    @param log_file: where to save the archivebox log output
    @return path to the saved html, None if crawl failed
    """

    # dangerous method
    print("adding " + url + " into archivebox ...")
    add_cmd = "docker-compose run archivebox add "
    unique_url = url + "#" + str(time.time())
    log_suffix = " > " + log_file
    try:
        os.system(add_cmd + unique_url + log_suffix)
        print("adding " + url + " into archivebox successfully")
        path = catch_data_path(log_file)
        print("the path to the saved html is " + path)
        return path

    except:
        print("!! Failed to run 'archive add' command !!")
        return None

def catch_data_path(log_file):
    """use re to find the saved file path in the log output
    @param log_file: log file path
    @return saved file path
    """
    with open(log_file, "r") as f:
        log_content = f.read()
    m = re.search(r"\./archive/[0-9\.]+", log_content)
    return m.group()



if __name__ == '__main__':
    add_url("https://www.baidu.com")
