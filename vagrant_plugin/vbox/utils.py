def parse_additional_settings(additional_settings, indents):
    string_buffer = ''
    for key, value in additional_settings.items():
        string_buffer += '\n{0}{1}= "{2}"'.format('\t'*indents, key, value)
    return string_buffer


def gen_ip(ip):
    raise NotImplementedError
