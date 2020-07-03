import requests
import hashlib
import sys
import re

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    rspns = requests.get(url)
    if rspns.status_code != 200:
        raise  RuntimeError(f'Error fetching: {rspns.status_code}, check the api and try again')
    return rspns

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} found {count} times..You should change it.')
        else:
            print(f'{password} was not found. Carry on!')
    return 'checking complete.'


passinputs_list = []
file_list = sys.argv[1:]
for file in file_list:
    with open(file, mode = 'r') as my_file:
            passinputs = my_file.read().split()
            passinputs_list.extend(passinputs)

if __name__ == '__main__':
    sys.exit(main(passinputs_list))
