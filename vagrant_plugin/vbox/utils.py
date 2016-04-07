from netaddr import IPNetwork
import random


def parse_additional_settings(additional_settings, indents):
    string_buffer = ''
    for key, value in additional_settings.items():
        string_buffer += '\n{0}{1}= "{2}"'.format('\t' * indents, key, value)
    return string_buffer


def set_ip(ip):
    if ip:
        # IPNetwork with an IP address returns the IP address
        return str(random.choice(IPNetwork(ip)))
    else:
        return gen_rand_ip()


def gen_rand_ip(seed=None):
    not_valid = [10, 127, 169, 172, 192]

    random.seed(seed)
    first = random.randrange(1, 256)
    while first in not_valid:
        first = random.randrange(1, 256)

    return ".".join(
        [str(first), str(random.randrange(1, 256)), str(randrange(1, 256)),
         str(random.randrange(1, 256))])
