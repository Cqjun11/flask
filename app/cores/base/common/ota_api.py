from app.cores.base.common.request import Post
from app.cores.base.common.request_util import handle_url

test_domain = '10.60.2.114'
test_port = 31893
pro_domain = '10.50.2.64'
pro_port = 32573


def get_device_data(pid):
    path = '/xconsole/v1/product/resource/list?productId'
    url = handle_url('https', 'aiot.aciga.com.cn', '', path)



def action():
    path = '/api/v1/internal/invoke-actions'
    url = handle_url('http', test_domain, test_port, path)



