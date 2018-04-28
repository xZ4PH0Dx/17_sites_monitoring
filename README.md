# Sites Monitoring Utility

This program is watching for your sites listed in text file and shows you does it have 200 status and is it isn't it expiring it a month.

# How to Install
Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

pip install -r requirements.txt # alternatively try pip3
Remember, it is recommended to use virtualenv/venv for better isolation.

# How to run
Example of running a script on a Linux with a Python3 interpreter. You should pass a path to your text file filled with urls as an argument.
```bash
$python3 check_sites_health.py /home/zap/git/misc/urls_list
http://dfsdlkf.cf check for status code : NOT OK
http://dfsdlkf.cf check for expiration date : NOT OK
http://ya.ru check for status code : OK
http://ya.ru check for expiration date : OK
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
