from genericpath import exists
from pathlib import Path
import argparse
import json
import pathlib
from PIL import Image

parser = argparse.ArgumentParser(description="Convert COCO dataset to ImageFolder")

parser.add_argument("--coco_dataset_path", type=str)
parser.add_argument("--coco_json_filename", type=str)
parser.add_argument("--image_folder_output_path", type=str)

args = parser.parse_args()

path_to_coco = Path(args.coco_dataset_path)
coco_json_filename = args.coco_json_filename
dataset_ouptut_path = Path(args.image_folder_output_path)

with open(path_to_coco / coco_json_filename, "r") as coco_file:
    coco_json = json.load(coco_file)

category_id_to_name_dict = {}
for category in coco_json["categories"]:
    category_id_to_name_dict[category["id"]] = category["name"]

image_id_to_name_dict = {}
for image in coco_json["images"]:
    image_id_to_name_dict[image["id"]] = image["file_name"]

for annotation in coco_json["annotations"]:
    coco_bbox = annotation["bbox"]

    category_name = category_id_to_name_dict[annotation["category_id"]]
    image_filename = Path(image_id_to_name_dict[annotation["image_id"]])

    image_crop = Image.open(path_to_coco / "img" / image_filename).crop((coco_bbox[0], coco_bbox[1], coco_bbox[0] + coco_bbox[2], coco_bbox[1] + coco_bbox[3]))

    (dataset_ouptut_path / category_name).mkdir(parents= True, exist_ok = True)
    image_crop.save(dataset_ouptut_path / category_name / (category_name + "_" + str(annotation["id"]) + image_filename.suffix))
    