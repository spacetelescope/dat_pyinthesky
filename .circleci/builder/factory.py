#!/usr/bin/env python

import argparse
import enum
import logging
import os
import json
import shutil

from builder.constants import ARTIFACT_DEST_DIR, ENCODING, BUILD_LOG_DIR, CIRCLE_CI_CONFIG_PATH
from builder.github import scan_pull_requests_for_failures
from builder.service import find_build_jobs, run_build, setup_build, find_excluded_notebooks, is_excluded
from builder.notebook_sync import move_notebook

from nbpages import make_html_index

logger = logging.getLogger(__file__)
class Operation(enum.Enum):
    BuildNotebooks = 'build-notebooks'
    BuildWebsite = 'build-website'
    MultiBuild = 'multi-build'
    SyncNotebooks = 'sync-notebooks'
    ScanGithub = 'scan-github'
    MapNotebooks = 'map-notebooks'

def obtain_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--operation', type=Operation, default=Operation.BuildNotebooks)
    # Build Notebooks
    parser.add_argument('-c', '--notebook-collection-paths', type=str, default='')
    parser.add_argument('-n', '--notebook-category', type=str, default=None)
    parser.add_argument('-r', '--remote-names', type=str, default='master')
    # Build Website

    # Sync Notebooks
    parser.add_argument('-d', '--destination-path', type=str, default=None)

    # Map Notebooks

    options = parser.parse_args()
    options.notebook_collection_paths = [nb_path for nb_path in options.notebook_collection_paths.split(',')]
    return options

def validate(options: argparse.Namespace) -> None:
    operation_members = [member.value for member in Operation.__members__.values()]
    if not options.operation.value in operation_members:
        raise NotImplementedError(f'Operation[{options.operation.value}] does not exist. Available Operations: {",".join(operation_members)}')

def main(options: argparse.Namespace) -> None:
    if options.operation is Operation.ScanGithub:
        if options.remote_names == '':
            raise NotImplementedError

        options.remote_names == [name for name in options.remote_names.split(',')]
        for failure in scan_pull_requests_for_failures(options.remote_names):
            print(failure)

    elif options.operation is Operation.SyncNotebooks:
        if options.destination_path is None:
            raise NotImplementedError('Missing --destination-path input')

        formatted_collection_paths = ','.join(options.notebook_collection_paths)
        logger.info(f'Syncing Notebooks Collections to[{formatted_collection_paths}] to Destination[{options.destination_path}]')
        for build_job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths)):
            logger.info(f'Syncing Notebook: {build_job.category.name}')
            move_notebook(build_job, options.destination_path)

    elif options.operation is Operation.BuildNotebooks:
        if options.notebook_collection_paths == '':
            raise NotImplementedError

        if options.notebook_category is None:
            for build_job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths)):
                logger.info(f'Building Notebook: {build_job.collection.name}: {build_job.category.name}')
                setup_build(build_job)
                run_build(build_job)
        else:
            for build_job in find_build_jobs(options.notebook_collection_paths):
                if options.notebook_category != build_job.category.name:
                    continue

                logger.info(f'Building Notebook: {build_job.collection.name}: {build_job.category.name}')
                setup_build(build_job)
                run_build(build_job)

    elif options.operation is Operation.MultiBuild:
        import multiprocessing, time

        if os.path.exists(BUILD_LOG_DIR):
            shutil.rmtree(BUILD_LOG_DIR)

        os.makedirs(BUILD_LOG_DIR)
        def _build_category(collection_name: str, category_name: str) -> None:
            os.environ['CHANNEL_BUILD'] = 'true'
            for build_job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths, False)):
                if category_name != build_job.category.name:
                    continue

                setup_build(build_job)
                run_build(build_job)
            del os.environ['CHANNEL_BUILD']

        job_list = []
        for build_job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths)):
            job_list.append([build_job.collection.name, build_job.category.name])

        processes = []
        max_workers = 10
        while len(job_list) > 0 or len(processes) > 0:
            for proc_idx, proc in enumerate([proc for proc in processes if not proc.is_alive()]):
                processes.remove(proc)

            if len(processes) >= max_workers:
                time.sleep(1)
                continue

            try:
                collection_name, category_name = job_list.pop(0)
            except IndexError:
                continue

            logger.info(f'Starting new Build[{collection_name}, {category_name}]')
            proc = multiprocessing.Process(target=_build_category, args=(collection_name, category_name))
            proc.daemon = True
            proc.start()
            processes.append(proc)

    elif options.operation is Operation.BuildWebsite:
        artifact_dest_dir = 'pages'
        if os.path.exists(artifact_dest_dir):
            shutil.rmtree(artifact_dest_dir)

        os.makedirs(artifact_dest_dir)

        converted_pages = []
        for job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths, False)):
            for notebook in job.category.notebooks:
                filename = notebook.filename.rsplit('.', 1)[0]
                html_filename = f'{filename}.html'
                html_filepath = os.path.join(ARTIFACT_DEST_DIR, job.collection.name, job.category.name, html_filename)
                meta_filename = f'{filename}.metadata.json'
                meta_filepath = os.path.join(ARTIFACT_DEST_DIR, job.collection.name, job.category.name, meta_filename)
                with open(meta_filepath, 'rb') as stream:
                    metadata = json.loads(stream.read())

                group_dirpath = f'{artifact_dest_dir}/{job.collection.name}/{job.category.name}'
                if not os.path.exists(group_dirpath):
                    os.makedirs(group_dirpath)

                rel_filepath = f'{group_dirpath}/{filename}.html'
                shutil.copyfile(html_filepath, rel_filepath)
                html_rel_filepath = f'{job.collection.name}/{job.category.name}/{filename}.html'
                converted_pages.append({
                    'output_file_path': html_rel_filepath,
                    'name': metadata['title'],
                    'title': metadata['title'],
                })

        index_path = f'{artifact_dest_dir}/index.html'
        index_template_path = os.path.join(os.getcwd(), 'index.tpl')
        output = make_html_index(converted_pages, index_template_path, outfn=None, relpaths=True)
        with open(index_path, 'wb') as stream:
            stream.write(output.encode(ENCODING))

    elif options.operation is Operation.MapNotebooks:
        import copy
        import yaml
        config = {
            'version': 2.1,
            'executors': {
                'notebook-executor': {
                    'docker': [
                        {'image': 'continuumio/miniconda3'}
                    ],
                    'resource_class': 'medium',
                    'working_directory': '~/repo'
                }
            },
            'jobs': {},
            'workflows': {
                'version': '2.1',
                'Branch Build': {
                    'jobs': []
                },
                # 'PR Build': {
                #     'jobs': []
                # }
            }

        }
        job_template = {
            'executor': 'notebook-executor',
            'environment': {
                'PYTHONPATH': '.circleci',
            },
            'steps': [
                'checkout',
                {
                    'run': {
                        'name': 'Setup Environment',
                        'command': 'bash ./.circleci/setup_env.sh'
                    },
                },
                {
                    'run': {
                        'name': 'Build Notebook',
                        'no_output_timeout': '60m',
                        'command': None,
                    }
                },
                {
                    'store_artifacts': {
                        'path': './pages'
                    }
                }
            ]
        }
        for build_job in filter(is_excluded, find_build_jobs(options.notebook_collection_paths)):
            formatted_cat_name = ' '.join(build_job.category.name.split('_'))
            formatted_cat_name = formatted_cat_name.title()
            formatted_col_name = ' '.join(build_job.collection.name.split('_'))
            formatted_col_name = formatted_col_name.title()
            job_name = '-'.join([formatted_col_name, formatted_cat_name])
            job = copy.deepcopy(job_template)
            job['steps'][1]['run']['command'] = f'python ./.circleci/builder/factory.py -o build-notebooks -c {build_job.collection.name} -n {build_job.category.name}'
            config['jobs'][job_name] = job
            config['workflows']['Branch Build']['jobs'].append(job_name)

        with open(CIRCLE_CI_CONFIG_PATH, 'wb') as stream:
            stream.write(yaml.dump(config).encode('utf-8'))

    else:
        raise NotImplementedError

if __name__ == '__main__':
    options = obtain_options()
    validate(options)
    main(options)
