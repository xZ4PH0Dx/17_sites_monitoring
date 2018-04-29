import requests as r
import whois
import sys
from datetime import datetime


def load_urls4check(path):
    with open(path) as file:
        return file.read().split('\n')


def is_server_respond_with_200(url):
    try:
        return r.get(url).ok
    except r.ConnectionError:
        return False


def get_domain_expiration_date(url):
    exp_date = whois.whois(url)['expiration_date']
    if exp_date is None:
        return False
    return abs((exp_date - datetime.utcnow()).days)


def is_not_expire_in_month(datediff):
    return datediff > 30


def combine_checks(list_urls):
    check_list = {}
    for url in list_urls:
        if url:
            status_code = is_server_respond_with_200(url)
            exp_date = get_domain_expiration_date(url)
            check_list[url] = {
                    'status code': 'OK'
                    if status_code else 'NOT OK',
                    'expiration date': 'OK'
                    if is_not_expire_in_month(exp_date)
                    else 'NOT OK'
                }
    return check_list


def pprint_check_list(check_list):
    for url, checks in check_list.items():
        for check, result in checks.items():
            print(url, 'check for', check, ':', result)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("There's no file given")
    filepath = sys.argv[1]
    loaded_urls_list = load_urls4check(filepath)
    check_list = combine_checks(loaded_urls_list)
    pprint_check_list(check_list)
