from jsonpath import jsonpath


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


def handle_version_and_path(data, version):
    '''
    遍历json数据,根据版本号筛选对应路径
    :param version: 版本号
    :param data:json数据
    :return: 升级数据
    '''
    data_list = jsonpath(data, f'$..resources[?(@.definition.versionName=="{version}")]')
    if data_list:
        file_url = data_list[0]['definition']['url']
        file_size = data_list[0]['definition']['size']
        md5 = data_list[0]['definition']['md5']
        sha256 = ''
        try:
            sha256 = data_list[0]['definition']['e_sha256']
            return file_url, file_size, md5, sha256
        except Exception as e:
            return file_url, file_size, md5, sha256
    else:
        print("输入版本号不符，请检查控制台版本号")
        return False


def handle_now_versionName(data):
    '''
    处理当前版本，兼容不同设备
    :return:
    '''
    now_version = jsonpath(data, "$..devices.[value]")
    if now_version:
        return now_version[0]
    else:
        print("输入版本号不符，请检查控制台版本号")
        return False
