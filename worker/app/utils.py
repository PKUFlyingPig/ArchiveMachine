import os
import time
import re
import logging

DATA_DIR = '/usr/src/app/data'
os.chdir(DATA_DIR)

def add_url(url, log_file="/tmp/log.txt"):
    """crawl the resource of the given url, return the filename
    @param url: target url
    @return (source_type, filename): the type (pdf, html, video) and the filename of the resource, None if crawl failed
    """
    logging.info("adding " + url + " into archivebox ...")
    # check arxiv pdf
    # match = re.match(r'^https://arxiv\.org/pdf/(.*\.pdf)$', url)
    match = re.match(r'.*/(.*\.pdf)$', url)
    if match != None:
        filename = str(time.time()) + ".pdf"
        cmd = f"wget --connect-timeout=5 -U NoSuchBrowser/1.0 '{url}' -O '{filename}'"
        source_type = "pdf"
    else: 
    # html
        filename = str(time.time()) + ".html"
        cmd = f"curl -m 30 -d 'url={url}' singlefile:80 > '{filename}'"
        source_type = "html"

    try:
        logging.info(cmd)
        os.system(cmd) # dangerous
    except:
        logging.info(f"!! Failed to run command : {cmd}!!")
        return None
    
    try:
        size = os.path.getsize(filename)
        if size == 0:
            logging.info("!! Failed to crawl the resource !!")
            return None
        else:
            return (source_type, filename)
    except:
        logging.info("!! Failed to crawl the resource !!")
        return None

def add_video(url):
    filename = f"{time.time()}.mp4"
    cmd = f"youtube-dl --socket-timeout 30 --exec 'mv {{}} {filename}' --recode-video mp4 {url}"
    try:
        logging.info(cmd)
        os.system(cmd)
        if os.path.exists(filename):
            return filename
        else:
            logging.info(filename)
            return None
    except Exception as e:
        logging.info(e)
        logging.info(f"!! not a video !!")
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
