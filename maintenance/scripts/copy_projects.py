import omero
import subprocess
import toolbox

MAX_USERS = 12
PROJECTS_IDS = [15595, 15593, 15591]
SOURCE_HOST = None
DEST_HOST = None
TEMP_DIR = '/run/media/julio/DATA/OMERO_training_data'
OMERO_SERVER_DIR = '/opt/OMERO.server-5.6.3-ice36-b228'


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


def copy_image(source_conn, dest_conn, source_image, dest_dataset):
    pass


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


def run(source_host, dest_host, project_ids):
    source_conn = toolbox.open_connection(**source_host)
    dest_conn = toolbox.open_connection(**dest_host)

    for project_id in project_ids:
        project = toolbox.get_project(source_conn)
        copy_project(source_conn, dest_conn, project)


