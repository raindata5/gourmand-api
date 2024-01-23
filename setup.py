from setuptools import setup

setup()
# docker build --tag raindata5/gourmand-api .
# docker images --quiet --filter=dangling=true | xargs --no-run-if-empty docker rmi
# docker push raindata5/gourmand-api

# INFO:root:{'type': 'http', 'asgi': {'version': '3.0', 'spec_version': '2.3'}, 'http_version': '1.1', 'server': ('172.18.0.4', 8000),
#  'client': ('172.18.0.1', 42402), 'scheme': 'http', 'method': 'GET', 'root_path': '', 'path': '/index_secure', 'raw_path': b'/index_secure',
# 'query_string': b'', 'headers': [(b'host', b'localhost:8000'), (b'connection', b'keep-alive'), 
# (b'sec-ch-ua', b'"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"'), (b'sec-ch-ua-mobile', b'?0'), (b'sec-ch-ua-platform', b'"Windows"'),
#  (b'upgrade-insecure-requests', b'1'), (b'user-agent',
#   b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46'),
#     (b'accept', b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'),
#       (b'sec-fetch-site', b'none'), (b'sec-fetch-mode', b'navigate'), (b'sec-fetch-user', b'?1'), (b'sec-fetch-dest', b'document'),
#         (b'accept-encoding', b'gzip, deflate, br'), (b'accept-language', b'fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6')], 'state': {},
# 'app': <fastapi.applications.FastAPI object at 0x7efcbab78d60>, 'fastapi_astack': <contextlib.AsyncExitStack object at 0x7efcba9ef250>,
# 'router': <fastapi.routing.APIRouter object at 0x7efcbab78d00>, 'endpoint': <function index at 0x7efcbab94c10>, 'path_params': {},
# 'route': APIRoute(path='/index_secure', name='index', methods=['GET'])}

# alembic --config alembic2.ini revision --autogenerate -m 'role creation'
# alembic --config alembic2.ini upgrade head\


# ERR_CERT_AUTHORITY_INVALID
# ERR_CERT_COMMON_NAME_INVALID