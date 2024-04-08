from sentinelsat import SentinelAPI
import uuid
import argparse


def name_parent(metadata):
    if metadata['platform'].startswith('S1'):
        parent_name = f"{metadata['platform']}_{metadata['mode']}_{metadata['producttype']}"
    elif metadata['platform'].startswith('S2'):
        parent_name = f"{metadata['platform']}_{metadata['producttype']}"
    elif metadata['platform'].startswith('S3'):
        parent_name = f"{metadata['platform']}_{metadata['instrument']}"
    elif metadata['platform'].startswith('S5'):
        parent_name = f"{metadata['platform']}_{metadata['producttype']}"

    return parent_name


def get_product_metadata(product_name):

    # TODO: Get metadata from file name so we don't have to query.
    platform = product_name.split('_')[0]
    metadata = {
        'platform': platform
    }

    if platform.startswith('S1'):
        metadata['mode'] = product_name.split('_')[1]
        metadata['producttype'] = product_name.split('_')[2]
    elif platform.startswith('S2'):
        metadata['producttype'] = product_name.split('_')[1]
    elif platform.startswith('S3'):
        short_name = product_name.split('_')[1]
        if short_name == 'OL':
            metadata['instrument'] = 'OLCI'
        elif short_name == 'SL':
            metadata['instrument'] = 'SLSTR'
        elif short_name == 'SY':
            metadata['instrument'] = 'Synergy'
        elif short_name == 'SR':
            metadata['instrument'] = 'SRAL'
    elif platform.startswith('S5'):
        metadata['producttype'] = product_name[9:19]
    else:
        raise ValueError(f'Product {product_name} not found')


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
    metadata = get_product_metadata(child_product_name)
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
