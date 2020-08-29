#!/usr/bin/env python

import argparse
from builder.service import find_build_jobs, run_build, setup_build

def obtain_options() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--notebook-collection-paths', type=str, required=True)
    options = parser.parse_args()
    options.notebook_collection_paths = [nb_path for nb_path in options.notebook_collection_paths.split(',')]
    return options

def main(options: argparse.Namespace) -> None:
    for build_job in find_build_jobs(options.notebook_collection_paths):
        print(build_job.collection.name, build_job.category.name)
        setup_build(build_job)
        run_build(build_job)

if __name__ == '__main__':
    options = obtain_options()
    main(options)
