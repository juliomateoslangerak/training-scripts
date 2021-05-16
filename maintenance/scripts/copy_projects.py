## known limitations
# Does not take into account images in multiple datasets


import omero
import subprocess
from random import choice
from string import ascii_letters
import csv
import toolbox
from os import path
import argh
# from . config import *

import logging

logger = logging.Logger(name=__name__, level=logging.INFO)

FULL_NAMES = ["Francis Crick",
                  "Linda Buck",
                  "Charles Darwin",
                  "Marie Curie",
                  "Alexander Fleming",
                  "Rosalind Franklin",
                  "Robert Hooke",
                  "Jane Goodall",
                  "Gregor Mendel",
                  "Barbara McClintock",
                  "Louis Pasteur",
                  "Ada Lovelace",
                  "Linus Pauling",
                  "Frances Kelsey",
                  "Maurice Wilkins",
                  "Florence Nightingale",
                  "John Sulston",
                  "Elizabeth Blackwell",
                  "Richard Dawkins",
                  "Caroline Dean",
                  "Stephen Reicher",
                  "Wendy Barclay",
                  "Paul Nurse",
                  "Jennifer Doudna",
                  "Adrian Thomas",
                  "Ann Clarke",
                  "Oswald Avery",
                  "Liz Sockett",
                  "Erwin Chargaff",
                  "Tracey Rogers",
                  "Ronald Fisher",
                  "Rachel Carson",
                  "William Harvey",
                  "Nettie Stevens",
                  "Jeffrey Hall",
                  "Youyou Tu",
                  "Michael Rosbash",
                  "Carol Greider",
                  "Yoshinori Ohsumi",
                  "Rosalyn Yalow",
                  "Amedeo Avogadro",
                  "Virginia Apgar",
                  "Kristian Birkeland",
                  "Mary Anning",
                  "Chen-Ning Yang",
                  "Stephanie Kwolek",
                  "Jagadish Bose",
                  "Rita Levi-Montalcini",
                  "Susumu Tonegawa",
                  "Irene Joliot-Curie",
                  ]


def create_users(admin_conn, save_dir: str, nb_users: int, nb_trainers: int):
    users = {}

    # creating trainer names and passwords
    for trainer_nb in range(nb_trainers):
        users[f'trainer-{trainer_nb}'] = "".join([choice(ascii_letters) for _ in range(8)])

    # creating user names and paswords
    for user_nb in range(nb_users):
        users[f'user-{user_nb}'] = "".join([choice(ascii_letters) for _ in range(8)])

    # save file with user names and passwords
    save_path = path.join(save_dir, 'user_passwords.csv')
    with open(save_path, 'w') as f:
        writer = csv.writer(f)
        for user_name, password in users.items():
            writer.writerow([user_name, password])

    admin_uuid = admin_conn.getSession().getUuid().getValue()
    host = admin_conn.host

    # creating groups
    run_command(f"omero group -k {admin_uuid} -s {host} add Lab1 --perms 'rwra--' --ignore-existing")
    run_command(f"omero group -k {admin_uuid} -s {host} add Lab2 --perms 'rwr---' --ignore-existing")
    run_command(f"omero group -k {admin_uuid} -s {host} add Lab3 --perms 'rwrw--' --ignore-existing")
    run_command(f"omero group -k {admin_uuid} -s {host} add Lab4 --perms 'rw----' --ignore-existing")
    logger.info('Groups created')

    # creating users
    for n, (u, w) in enumerate(users.items()):
        run_command(f"omero user -k {admin_uuid} -s {host} add {u} {FULL_NAMES[n]} Lab1 Lab2 Lab3 Lab4 -P {w} --ignore-existing")
        logger.info(f'User {u} created')

    return users


def run_command(command):
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'Error: {e.output}')
        logger.error(f'Command: {e.cmd}')
        raise RuntimeError(f'Command could not be run: {command}')

    return output.stdout.decode('utf-8')


def copy_annotations(source_object, dest_object):
    copy_tags(source_object, dest_object)
    copy_kvps(source_object, dest_object)
    copy_attachments(source_object, dest_object)


def copy_tags(source_object, dest_object):
    pass


def copy_kvps(dest_conn, source_object, dest_object):
    for ann in source_object.listAnnotations():
        if type(ann).__name__ == 'MapAnnotationWrapper':
            new_ann = toolbox.create_annotation_map(dest_conn, ann.getValue())
            toolbox.link_annotation(dest_object, new_ann)


def copy_attachments(source_object, dest_object):
    pass


def copy_rois(source_image, dest_image):
    pass


def copy_description(dest_conn, source_obj, dest_object):
    dest_object.setDescription(source_obj.getDescription())
    return dest_conn.getUpdateService().saveAndReturnObject(dest_object)


def copy_object_annotations(source_conn, dest_conn, source_obj_id, dest_obj_id, obj_type):
    source_obj = source_conn.getObject(obj_type, source_obj_id)
    dest_obj = dest_conn.getObject(obj_type, dest_obj_id)

    dest_obj = copy_description(dest_conn, source_obj, dest_obj)
    copy_kvps(dest_conn, source_obj, dest_obj)


def get_original_file_names(image):
    fileset = image.getFileset()
    return [f.getName() for f in fileset.listFiles()]


def copy_image(source_conn, dest_conn, source_image, dest_dataset):
    source_uuid = source_conn.getSession().getUuid().getValue()
    dest_uuid = dest_conn.getSession().getUuid().getValue()
    source_host = source_conn.host
    dest_host = dest_conn.host
    image_path = f'{TEMP_DIR}{get_original_file_names(source_image)[0].replace(" ", "")}'

    if not path.exists(f'{image_path}'):
        run_command(f"omero download -k {source_uuid} -s {source_host} Image:{source_image.getId()} {image_path}")
    output = run_command(f"omero import -k {dest_uuid} -s {dest_host} -d {dest_dataset.getId().getValue()} {image_path}")
    try:
        dest_images = [toolbox.get_image(dest_conn, i) for i in eval(output[6:])]
    except TypeError:
        dest_images = [toolbox.get_image(dest_conn, eval(output[6:]))]

    if len(dest_images) == 1:
        copy_image_annotations(source_conn, dest_conn. source_image, dest_images[0])


def copy_image_annotations(source_conn, dest_conn, source_image, dest_image):
    copy_kvps(dest_conn, source_image, dest_image)


def match_images(source_conn, dest_conn, source_dataset_id, dest_dataset_id):
    return [0], [0]


def copy_dataset(source_conn, dest_conn, source_dataset, dest_project):
    dest_dataset = toolbox.create_dataset(connection=dest_conn,
                                          dataset_name=source_dataset.getName(),
                                          dataset_description=source_dataset.getDescription(),
                                          parent_project=dest_project)
    copy_dataset_annotations(source_conn, dest_conn, source_dataset.getId(), dest_dataset.getId())

    images = source_dataset.listChildren()
    orig_file_names = []
    for image in images:
        if get_original_file_names(image)[0] not in orig_file_names:
            orig_file_names.append(get_original_file_names(image)[0])
            copy_image(source_conn, dest_conn, image, dest_dataset)


def copy_dataset_annotations(source_conn, dest_conn, source_dataset_id, dest_dataset_id):
    pass


def copy_project(source_conn, dest_conn, source_project):
    dest_project = toolbox.create_project(dest_conn, source_project.getName())
    copy_project_annotations(source_conn, dest_conn, source_project.getId(), dest_project.getId())

    datasets = source_project.listChildren()
    for dataset in datasets:
        copy_dataset(source_conn, dest_conn, dataset, dest_project)


def copy_project_annotations(source_conn, dest_conn, source_project_id, dest_project_id):
    pass


def run(source_conf, dest_conf, admin_conf, source_project_ids: list, nb_users: int, nb_trainers: int):
    try:
        admin_conn = toolbox.open_connection(**admin_conf)

        users = create_users(admin_conn, nb_users=nb_users, nb_trainers=nb_trainers)

        admin_conn.close()

        try:
            source_conn = toolbox.open_connection(**source_conf)

            for user_nb, (user_name, user_pw) in enumerate(users.items()):
                dest_conf['username'] = user_name
                dest_conf['password'] = user_pw
                dest_conf['group'] = f'Lab{user_nb + 1//(nb_users//2) + 1}'

                dest_conn = toolbox.open_connection(**dest_conf)

                for project_id in source_project_ids:
                    project = toolbox.get_project(source_conn, project_id)
                    copy_project(source_conn, dest_conn, project)

                dest_conn.close()

        finally:
            source_conn.close()
            dest_conn.close()

    finally:
        if admin_conn.isConnected():
            admin_conn.close()


if __name__ == '__main__':
    argh.dispatch(run)
