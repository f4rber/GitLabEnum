# GitLabEnum
Enumerate GitLab users in FOUR ways!

```
usage: gitlab_user_enum.py [-h] [-t THREADS] [-o TIMEOUT] [-r RANGE] [-d DELAY] -u URL [-f FILE] -m {1,2,3,4} [-v]

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        number of threads (15)
  -o TIMEOUT, --timeout TIMEOUT
                        timeout (5)
  -r RANGE, --range RANGE
                        range of ids (500)
  -d DELAY, --delay DELAY
                        delay between requests (1)
  -u URL, --url URL     url (http://site.com)
  -f FILE, --file FILE  file with usernames
  -m {1,2,3,4}, --mode {1,2,3,4}
                        1 - site.com/USERNAME; 2 - site.com/users/USERNAME/exists
  -v, --verbose         verbose
```

# Examples:
```
python3 gitlab_user_enum.py -u https://gitlab.site.com -o 2 -t 2 -d 2 -f ./usernames.txt -m 1
GitLab user enumeration:

Login: root
Username: Administrator
Link: https:/gitlab.site.com/root

#

python3 gitlab_user_enum.py -u https://gitlab.site.com -o 2 -t 2 -d 2 -f ./usernames.txt -m 2
GitLab user enumeration:

Username: root
Link: https://gitlab.site.com/users/root/exists

Username: test
Link: https://gitlab.site.com/users/test/exists

Username: administrator
Link: https://gitlab.site.com/users/administrator/exists

#

python gitlab_user_enum.py -u https://git.site.com -m 3
GitLab user enumeration:

Found user: name name
ID: 9
Username: name
State: active
Creation date: 2021-02-12T11:18:17.607Z
Bio:
Link: https://git.site.com/name
API link: https://git.site.com/api/v4/users/9

#

python gitlab_user_enum.py -u https://git.site.com -m 4
GitLab user enumeration:

Found group: /local-users
Found group: /group1234
```
