import os
import shutil
import typing

BUILD_BASE_DIR = '/tmp/nbcollection-ci-build-base-dir'
ARTIFACT_DEST_DIR: str = '/tmp/artifacts'
PWN = typing.TypeVar('PWN')
IPYDB_REQUIRED_FILES: typing.List[str] = ['requirements.txt']
REQUIREMENTS_FILE_NAMES = ['requirements.txt', 'requirements']
ENCODING: str = 'utf-8'
FILTER_STRIP = '/'
if os.path.exists(ARTIFACT_DEST_DIR):
    shutil.rmtree(ARTIFACT_DEST_DIR)

os.makedirs(ARTIFACT_DEST_DIR)
