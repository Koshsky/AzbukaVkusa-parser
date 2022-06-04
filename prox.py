from random import choice


with open('proxies_IPv4.txt', 'r') as file:
    proxies_IPv4 = [line.strip() for line in file.readlines()]
    
def get_random_IPv4():
    ip = choice(proxies_IPv4)  # login:pass@ip:port
    proxies = {'http': f'http://{ip}',
               'https': f'http://{ip}'}
    return proxies
