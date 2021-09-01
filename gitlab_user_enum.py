import json
import time
import random
import urllib3
import argparse
from bs4 import BeautifulSoup
from urllib3 import Timeout, Retry
from multiprocessing import Pool, freeze_support

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--threads", help="number of threads (15)", type=int, default=15)
parser.add_argument("-o", "--timeout", help="timeout (5)", type=int, default=5)
parser.add_argument("-r", "--range", help="range of ids (500)", type=int, default=500)
parser.add_argument("-d", "--delay", help="delay between requests (1)", type=int, default=1)
parser.add_argument("-u", "--url", help="url (http://site.com)", type=str, required=True)
parser.add_argument("-f", "--file", help="file with usernames", type=str, default="usernames.txt")
parser.add_argument("-m", "--mode",
                    help="1-(/USERNAME);2-(/users/USERNAME/exists);3-(/api/v4/users/ID);4-(/explore/groups.json)",
                    choices=[1, 2, 3, 4], type=int, required=True)
parser.add_argument("-v", "--verbose", help="verbose", action="store_true")
args = parser.parse_args()

ua = ['Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; zh-cn) Opera 8.65',
      'Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.2)',
      'Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 6.0)',
      'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 5.2)',
      'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; el-GR)',
      'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533+ (KHTML, like Gecko)']


def header_gen():
    header = {
        'User-agent': random.choice(ua),
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive'}
    http = urllib3.PoolManager(headers=header, cert_reqs=False, num_pools=30, retries=Retry(3),
                               timeout=Timeout(args.timeout))
    return http


def enum1(login):
    time.sleep(args.delay)
    try:
        req = header_gen().request("GET", args.url + f"/{login}")
        if args.verbose:
            print(f"Trying: {login}")
        if "Member since" in req.data.decode("utf-8") or "Personal projects" in req.data.decode("utf-8"):
            parsing = BeautifulSoup(req.data.decode("utf-8"), features="html.parser")
            for text in parsing.find_all("div", class_="cover-title"):
                if "\n" in text.string:
                    username = text.string.split("\n")[1]
                else:
                    username = text.string
                print(f"Login: {login}\nUsername: {username}\nLink: {req.geturl()}\n")
    except Exception as ex:
        if "Max retries exceeded with url" in str(ex) or "NoneType" in str(ex):
            pass
        else:
            print(str(ex))


def enum2(login):
    time.sleep(args.delay)
    try:
        req = header_gen().request("GET", args.url + f"/users/{login}/exists")
        if args.verbose:
            print(f"Trying: {login}")
        if r'{"exists":true}' in req.data.decode("utf-8"):
            print(f"Username: {login}\nLink: {req.geturl()}\n")
    except Exception as ex:
        if "Max retries exceeded with url" in str(ex) or "NoneType" in str(ex):
            pass
        else:
            print(str(ex))


def enum3(number):
    time.sleep(args.delay)
    try:
        req = header_gen().request("GET", args.url + f"/api/v4/users/{number}")
        if args.verbose:
            print(f"Trying: {number}")
        if req.data.decode("utf-8") == '{"message":"404 User Not Found"}':
            pass
        else:
            info = json.loads(req.data.decode("utf-8"))
            print(f"\nFound user: {info['name']}")
            print(f"ID: {info['id']}")
            print(f"Username: {info['username']}")
            print(f"State: {info['state']}")
            print(f"Creation date: {info['created_at']}")
            print(f"Bio: {info['bio']}")
            print(f"Link: {info['web_url']}")
            print(f"API link: {args.url}/api/v4/users/{number}")
    except Exception as ex:
        if "Max retries exceeded with url" in str(ex) or "NoneType" in str(ex):
            pass
        else:
            print(str(ex))


def enum4():
    try:
        req = header_gen().request("GET", args.url + "/explore/groups.json")
        if len(req.data) > 1:
            json_groups = json.loads(req.data.decode("utf-8"))
            for group in json_groups:
                print(f"Found group: {group['relative_path']}")
    except Exception as ex:
        if "Max retries exceeded with url" in str(ex) or "NoneType" in str(ex):
            pass
        else:
            print(str(ex))


if __name__ == "__main__":
    print("GitLab user enumeration:\n")
    usernames = [username.split("\n")[0] for username in open(args.file, "r").readlines()]
    numbers = [str(number) for number in range(args.range)]
    if args.mode == 1:
        freeze_support()
        pool = Pool(args.threads)
        pool.map(enum1, usernames)
        pool.close()
        pool.join()
    elif args.mode == 2:
        freeze_support()
        pool = Pool(args.threads)
        pool.map(enum2, usernames)
        pool.close()
        pool.join()
    elif args.mode == 3:
        freeze_support()
        pool = Pool(args.threads)
        pool.map(enum3, numbers)
        pool.close()
        pool.join()
    elif args.mode == 4:
        enum4()
    else:
        print("-m 1 (/USERNAME)\n-m 2 (/users/USERNAME/exists)\n-m3 (/api/v4/users/ID)\n-m 4 (/explore/groups.json)")
        exit(1)
