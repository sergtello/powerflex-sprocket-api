import os
import sys
import argparse
from app import database
from fastapi import UploadFile
from app.modules.sprocket.service import upload_sprocket_file
from app.modules.factory.service import upload_factory_data_file
from app.modules.sprocket.models import Sprocket
from app.modules.factory.models import Factory
from pathlib import Path


parser = argparse.ArgumentParser(description='Seed files.')
parser.add_argument('sprocket_seed_file')
parser.add_argument('factory_seed_file')
args = parser.parse_args()

sprocket_seed_file = args.sprocket_seed_file
factory_seed_file = args.factory_seed_file

if not Path(sprocket_seed_file).exists():
    print(f'ERROR: {sprocket_seed_file} file does not exist')
    sys.exit(1)

if not Path(factory_seed_file).exists():
    print(f'ERROR: {factory_seed_file} file does not exist')
    sys.exit(1)


try:
    with open(sprocket_seed_file, 'rb') as sprocket_file:
        sprocket_f = UploadFile(file=sprocket_file)
        upload_sprocket_response = upload_sprocket_file(Sprocket, sprocket_f)

    if upload_sprocket_response.status == 'OK':
        print(f'Generating sprocket data from : {sprocket_seed_file}')
        print(upload_sprocket_response.msg)
    else:
        print('ERROR generating sprocket data')
        sys.exit(1)

except Exception as e:
    print(f'ERROR generating sprocket data, an exception occurred: {str(e)}')
    sys.exit(1)

try:
    with open(factory_seed_file, 'rb') as factory_file:
        factory_f = UploadFile(file=factory_file)
        upload_factory_response = upload_factory_data_file(Factory, factory_f)

    if upload_factory_response.status == 'OK':
        print(f'Generating factory data from : {factory_seed_file}')
        print(upload_factory_response.msg)
    else:
        print('ERROR generating factory data')
        sys.exit(1)

except Exception as e:
    print(f'ERROR generating factory data, an exception occurred: {str(e)}')
    sys.exit(1)
