github update checker
===
This is a simple script written in python, used to check whether the projects you starred have new update(new commit or new release). <br>
You need to install Python3.x, beautifulsoup and requests. <br>
<b>Don't forget to change the username and password in github_ipdate_checker.py. </b> <br>
All the information is recorded in github_data.json. <br>

usage:
---
```
python .\github_update_checker.py
```
sample output:
---
```
AAAAAAAA has new commit!
AAAAAAAA has new release!
BBBBBBBB has new commit!
```
json file content:
---
There're lots of info.
```
{
    "AAAA": {
        "Project Author": "AA",
        "Latest Release Version": "146",
        "Latest Commit Version": "5,166",
        "Latest Release Date": "2017-05-17T15:03:31Z",
        "Latest Commit Date": "2017-08-30T13:25:36Z"
    },
    "BBBB": {
        "Project Author": "BB",
        "Latest Release Version": "15",
        "Latest Commit Version": "541",
        "Latest Release Date": "2017-05-30T15:12:46Z",
        "Latest Commit Date": "2017-08-31T22:10:51Z"
    }
}
```
