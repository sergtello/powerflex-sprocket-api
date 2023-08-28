import os
import sys
import requests

options = {
    'url': f'http://0.0.0.0:{os.environ.get("PORT")}',
    'timeout': 2
}

try:
    response = requests.get(options['url'], timeout=options['timeout'])

    print(f'HEALTHCHECK STATUS: {response.status_code}')

    if response.status_code == 200:
        sys.exit(0)
    else:
        sys.exit(1)

except requests.exceptions.RequestException as e:
    print('ERROR')
    sys.exit(1)
