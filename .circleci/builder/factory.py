#!/usr/bin/env python

import argparse

from builder.github import scan_pull_requests_for_failures
from builder.service import find_build_jobs, run_build, setup_build

def obtain_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--notebook-collection-paths', type=str, default='')
    parser.add_argument('-s', '--scan-for-failures', default=False, action='store_true')
    parser.add_argument('-r', '--remote-names', type=str, default='master')
    options = parser.parse_args()
    options.notebook_collection_paths = [nb_path for nb_path in options.notebook_collection_paths.split(',')]
    return options

def main(options: argparse.Namespace) -> None:
    if options.scan_for_failures:
        if options.remote_names == '':
            raise NotImplementedError

        options.remote_names == [name for name in options.remote_names.split(',')]
        for failure in scan_pull_requests_for_failures(options.remote_names):
            print(failure)

    else:
        if options.notebook_collection_paths == '':
            raise NotImplementedError

        for build_job in find_build_jobs(options.notebook_collection_paths):
            setup_build(build_job)
            run_build(build_job)

if __name__ == '__main__':
    options = obtain_options()
    main(options)
