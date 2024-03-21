# generate_parent_id
Generate ID for the virtual parent of a sentinel product using the product name as the only arguement. Also returns the metadata terms used to categorise the product within that parent.

## Usage

To use this script, simply run it using Python 3, passing the product name you want to create a parentID for as an argument:

```bash
python3 generate_parent_id.py --product_name <product_name>
python3 generate_parent_id.py --product_name S2B_MSIL2A_20180504T133059_N0500_R024_T27XWB_20230812T061053