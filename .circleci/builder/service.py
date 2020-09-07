import glob
import os
import shutil
import types
import typing

from builder.constants import BUILD_BASE_DIR, ARTIFACT_DEST_DIR
from builder.utils import filter_gitignore_entry__as_string, Collection, BuildJob, Category, Notebook, load_gitignore_data, run_command

def build_categories(start_path: str, rebuild: bool = True) -> types.GeneratorType:
    gitignore_data = load_gitignore_data(os.path.join(start_path, '.gitignore'))
    for root, dirnames, filenames in os.walk(start_path):
        for dirname in dirnames:
            dirpath = os.path.join(root, dirname)
            if filter_gitignore_entry__as_string(dirname, gitignore_data, dirpath):
                # Reassigning dirnames[:] removes the dir from being scaned
                dirnames[:] = [dname for dname in dirnames if dname == dirname]
                continue

            books = []
            for filepath in glob.glob(f'{dirpath}/*.ipynb'):
                name = os.path.basename(filepath).rsplit('.', 1)[0]
                rel_filepath = os.path.relpath(filepath)
                filename = os.path.basename(filepath)

                books.append([name, filename, rel_filepath])

            notebooks = []
            for idx, (name, filename, rel_filepath) in enumerate(sorted(books, key=lambda x: x[1])):
                notebooks.append(Notebook(name, filename, rel_filepath, idx))

            if notebooks:
                requirements_path = os.path.relpath(os.path.join(dirpath, 'requirements.txt'))
                if not os.path.exists(requirements_path):
                    raise NotImplementedError(f'Category missing Requirements File[{requirements_path}]')

                build_dir = os.path.join(BUILD_BASE_DIR, dirname)
                if os.path.exists(build_dir) and rebuild:
                    shutil.rmtree(build_dir)

                artifact_dir = os.path.join(ARTIFACT_DEST_DIR, dirname)
                if os.path.exists(artifact_dir) and rebuild:
                    shutil.rmtree(artifact_dir)

                yield Category(dirname, notebooks, dirpath, build_dir, artifact_dir)

            else:
                for category in build_categories(dirpath, rebuild):
                    yield category

def find_collections(notebook_collection_paths: typing.List[str], rebuild: bool = True) -> types.GeneratorType:
    for name in notebook_collection_paths:
        c_path = os.path.join(os.getcwd(), name)
        yield Collection(name, [cate for cate in build_categories(c_path, rebuild)])

def find_build_jobs(notebook_collection_paths: typing.List[str], rebuild: bool = True):
    for collection in find_collections(notebook_collection_paths, rebuild):
        for category in collection.categories:
            # category.setup_build_env()
            # category.inject_extra_files()
            build_scripts = []
            for notebook in category.notebooks:
            #     notebook.create_build_script([collection.name, category.name], category.build_dir, category.artifact_dir)
                build_scripts.append(os.path.join(category.build_dir, f'{notebook.filename}-builder.sh'))

            yield BuildJob(collection, category, build_scripts)

def setup_build(job: BuildJob) -> None:
    job.category.setup_build_env()
    job.category.inject_extra_files()
    for notebook in job.category.notebooks:
        notebook.create_build_script([job.collection.name, job.category.name], job.category.build_dir, job.category.artifact_dir)

def build_website(job: BuildJob) -> None:
    import pdb; pdb.set_trace()
# def consolidate_artifacts(job: BuildJob) -> None:
#     dest_dir = os.path.join(ARTIFACT_DEST_DIR, 'html-files')
#     if not os.path.exists(dest_dir):
#         os.makedirs(dest_dir)
# 
#     for notebook in job.category.notebooks:
#         filename = notebook.filename.rsplit('.', 1)[0]
#         filename = f'{filename}.html'
#         filepath = f'{ARTIFACT_DEST_DIR}/{job.collection.name}/{job.category.name}/{filename}'
#         dest_filepath = os.path.join(dest_dir, filename)
#         shutil.copyfile(filepath, dest_filepath)

def run_build(job: BuildJob) -> None:
    for script in job.scripts:
        command = f'bash "{script}"'
        run_command(command)

