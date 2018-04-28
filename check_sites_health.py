import requests as re
import whois
import sys
from datetime import datetime


def load_urls4check(path):
    with open(path) as file:
        return file.read()


def get_list_urls(list_urls):
    return list_urls.split()


def is_server_respond_with_200(url):
    try:
        status_code = re.get(url).status_code
    except re.ConnectionError:
        return False
    return True if status_code == 200 else False


def get_domain_expiration_date(url):
    exp_date = whois.whois(url)['expiration_date']
    return exp_date if exp_date else None


def not_expire_in_month(exp_date):
    if exp_date is None:
        return False
    datediff = abs((exp_date - datetime.utcnow()).days)
    return True if datediff > 30 else False


def combined_check(list_urls):
    check_list = {}
    for url in list_urls:
        status_code = is_server_respond_with_200(url)
        exp_date = get_domain_expiration_date(url)
        check_list[url] = {
                'status code': 'OK'
                if status_code else 'NOT OK',
                'expiration date': 'OK'
                if not_expire_in_month(exp_date)
                else 'NOT OK'
                }
    return check_list


def pprint_check_list(check_list):
    for url, checks in check_list.items():
        for check, result in checks.items():
            print(url, 'check for', check, ':', result)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('There\'s no file given')
    filepath = sys.argv[1]
    loaded_urls = load_urls4check(filepath)
    urls_list = get_list_urls(loaded_urls)
    check_list = combined_check(urls_list)
    pprint_check_list(check_list)
