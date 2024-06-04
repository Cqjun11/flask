from typing import Iterable
from urllib.parse import urlencode


# def handle_headers(headers):
#     '''
#     :param headers:
#     :return:
#     '''
#     ret = {}
#     for header in headers:
#         ret[header.name_] = header.value_
#     print(ret)
#     return ret



# def handle_data_params(params):
#     '''
#     :param params:
#     :return:
#     '''
#     ret = {}
#     if isinstance(params, Iterable):
#         for param in params:
#
#         return {params.name : params.value for param in params}

def handle_url(protocol, domain, port, path):
    """预处理并返回url"""
    protocol = protocol.strip()
    domain = domain.strip()
    port = str(port).strip()
    path = path.strip()
    if port:
        return protocol + "://" + domain + ":" + port + path
    else:
        return protocol + "://" + domain + path
