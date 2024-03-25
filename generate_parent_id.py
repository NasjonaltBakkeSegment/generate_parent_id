from sentinelsat import SentinelAPI
import uuid
import yaml
import argparse
import re


def get_config():
    file_path = "config/config.yml"
    with open(file_path, "r") as yaml_file:
        cfg = yaml.safe_load(yaml_file)
        return cfg


def name_parent(metadata):
    if metadata['platform'].startswith('S1'):
        parent_name = f"{metadata['platform']}_{metadata['mode']}_{metadata['producttype']}"
    else:
        parent_name = f"{metadata['platform']}_{metadata['producttype']}"
    return parent_name


def get_product_metadata(product_name, cfg):
    username = cfg['colhub_archive_credentials']['username']
    password = cfg['colhub_archive_credentials']['password']
    web = 'https://colhub-archive.met.no/'
    api = SentinelAPI(username, password, web)
    all_metadata = api.query(filename=product_name+'*')
    #TODO: s3 not querying for products after november 2023
    platform = product_name.split('_')[0]
    uuid = list(all_metadata.keys())[0]
    metadata = {
        'uuid': uuid,
        'platform': platform,
        'producttype': all_metadata[uuid]['producttype']
    }
    if platform.startswith('S1'):
        metadata['mode'] = product_name.split('_')[1]

    return metadata


def generate_v5_uuid(text):
    # Create a version 5 uuid
    namespace = uuid.UUID('d84d177b-5755-4e16-9b8e-6a9f335c8376')
    uuid5 = str(uuid.uuid5(namespace, text))
    return uuid5


def parent_id_from_metadata(metadata):
    text = ' '.join(str(value) for key, value in metadata.items() if key != 'uuid')
    parentid = generate_v5_uuid(text)
    return parentid


def generate_parent_id(child_product_name):
    child_product_name = child_product_name.split('.')[0]
    cfg = get_config()
    metadata = get_product_metadata(child_product_name, cfg)
    parentid = parent_id_from_metadata(metadata)
    parent_name = name_parent(metadata)
    return parentid, metadata, parent_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script to create an ID for the parent of a sentinel product"
        )

    parser.add_argument(
        "--product_name",
        type=str,
        required=True,
        help="Filepath to the parent MMD file"
    )

    args = parser.parse_args()
    product_name = args.product_name
    parent_id, metadata, parent_name = generate_parent_id(product_name)
    print("Generated Parent ID:", parent_id, '\nName:', parent_name, '\nAssociated Metadata:', metadata)
