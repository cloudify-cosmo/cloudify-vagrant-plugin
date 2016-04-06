from netaddr import IPNetwork
from random import choice, randrange


def parse_additional_settings(additional_settings, indents):
    string_buffer = ''
    for key, value in additional_settings.items():
        string_buffer += '\n{0}{1}= "{2}"'.format('\t' * indents, key, value)
    return string_buffer


def gen_ip(ip):
    if ip:
        return str(choice(IPNetwork(ip)))
    else:
        return gen_rand_ip()


def gen_rand_ip():
    not_valid = [10, 127, 169, 172, 192]

    first = randrange(1, 256)
    while first in not_valid:
        first = randrange(1, 256)

    return ".".join(
        [str(first), str(randrange(1, 256)), str(randrange(1, 256)),
         str(randrange(1, 256))])
