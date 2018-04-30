from requests import get, ConnectionError
from whois import whois
import sys
from datetime import datetime


def load_urls4check(path):
    with open(path) as file:
        return file.read().split('\n')


def is_server_respond_with_ok(url):
    try:
        return get(url).ok
    except ConnectionError:
        return False


def get_domain_expiration_datediff(url):
    exp_date = whois(url)['expiration_date']
    if exp_date is None:
        return False
    if isinstance((exp_date), list):
        exp_date = exp_date[0]
    return abs((exp_date - datetime.utcnow()).days)


def is_not_expire_in_days(datediff, n_days):
    return datediff > n_days


def combine_checks(list_urls, n_days=30):
    checks_dict = {}
    for url in list_urls:
        if url:
            status_code = is_server_respond_with_ok(url)
            exp_date = get_domain_expiration_datediff(url)
            checks_dict[url] = {
                    'status code': 'OK'
                    if status_code else 'NOT OK',
                    'expiration date': 'OK'
                    if is_not_expire_in_days(exp_date, n_days)
                    else 'NOT OK'
                }
    return checks_dict


def pprint_check_list(checks_dict):
    for url, checks in checks_dict.items():
        for check, result in checks.items():
            print(url, 'check for', check, ':', result)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("There's no file given")
    filepath = sys.argv[1]
    loaded_urls_list = load_urls4check(filepath)
    checks = combine_checks(loaded_urls_list)
    pprint_check_list(checks)
