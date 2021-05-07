import omero
import subprocess
import toolbox
from os import path

import logging

logger = logging.Logger(name=__name__, level=logging.INFO)

MAX_USERS = 12
PROJECTS_IDS = [15595, 15593, 15591]
SOURCE_CONF = {'username': 'student_tournesol', 'password': 'student_tournesol_pw', 'group': 'prof_tournesol_lab', 'host': '192.168.56.107'}
DEST_CONF = {'username': 'user-1', 'password': 'ome', 'group': 'Lab1', 'host': '192.168.56.107'}
TEMP_DIR = '/run/media/julio/DATA/OMERO_training_data/'


def run_command(command):
    try:
        subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'Error: {e.output}')
        logger.error(f'Command: {e.cmd}')


def copy_annotations(source_object, dest_object):
    copy_tags(source_object, dest_object)
    copy_kvps(source_object, dest_object)
    copy_attachments(source_object, dest_object)


def copy_tags(source_object, dest_object):
    pass


def copy_kvps(source_object, dest_object):
    pass


def copy_attachments(source_object, dest_object):
    pass


def copy_rois(source_image, dest_image):
    pass


def copy_description():
    pass


def get_original_file_names(image):
    fileset = image.getFileset()

    return [f.getName() for f in fileset.listFiles()]


def copy_image(source_conn, dest_conn, source_image, dest_dataset):
    source_uuid = source_conn.getSession().getUuid().getValue()
    dest_uuid = dest_conn.getSession().getUuid().getValue()
    source_host = source_conn.host
    dest_host = dest_conn.host
    image_path = f'{TEMP_DIR}{get_original_file_names(source_image)[0].replace(" ", "")}'
    print(image_path)

    if not path.exists(f'{image_path}'):
        run_command(f"omero download -k {source_uuid} -s {source_host} Image:{source_image.getId()} {image_path}")
    print(f"omero import -k {dest_uuid} -s {dest_host} -d {dest_dataset.getId().getValue()} {image_path}")
    run_command(f"omero import -k {dest_uuid} -s {dest_host} -d {dest_dataset.getId().getValue()} {image_path}")


def copy_dataset(source_conn, dest_conn, source_dataset, dest_project):
    dest_dataset = toolbox.create_dataset(connection=dest_conn,
                                          dataset_name=source_dataset.getName(),
                                          dataset_description=source_dataset.getDescription(),
                                          parent_project=dest_project)

    images = source_dataset.listChildren()
    for image in images:
        copy_image(source_conn, dest_conn, image, dest_dataset)


def copy_project(source_conn, dest_conn, source_project):
    dest_project = toolbox.create_project(dest_conn, source_project.getName())

    datasets = source_project.listChildren()
    for dataset in datasets:
        copy_dataset(source_conn, dest_conn, dataset, dest_project)


def run(source_conf, dest_conf, project_ids):
    try:
        source_conn = toolbox.open_connection(**source_conf)
        dest_conn = toolbox.open_connection(**dest_conf)

        for project_id in project_ids:
            project = toolbox.get_project(source_conn, project_id)
            copy_project(source_conn, dest_conn, project)

    finally:
        source_conn.close()
        dest_conn.close()


