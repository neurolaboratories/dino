from pathlib import Path
import argparse
import json
from PIL import Image
from tqdm import tqdm
parser = argparse.ArgumentParser(description="Convert COCO dataset to ImageFolder")

parser.add_argument("--coco_dataset_path", type=str)
parser.add_argument("--dataset_type", type=str, choices=["train", "test"])
parser.add_argument("--image_folder_output_path", type=str)

args = parser.parse_args()

path_to_coco = Path(args.coco_dataset_path)

coco_json_filenames = ["coco_train.json", "coco_val.json"]
output_folder = ["train", "val"]

if args.dataset_type == "test":
    coco_json_filenames = ["coco_test.json"]
    output_folder = ["test"]

dataset_ouptut_path = Path(args.image_folder_output_path)

def check_and_correct_bbox_annotations(img, bbox):
    # check if the coordinates xmax, ymax are outside of the image and correct them
    if (bbox[0] + bbox[2]) > img.size[0]:
        bbox[2] = img.size[0] - bbox[0]
    if (bbox[1] + bbox[3]) > img.size[1]:
        bbox[3] = img.size[1] - bbox[1]
    # check if the coordinates xmin, ymin are outside of the image and correct them
    if bbox[0] > img.size[0]:
        bbox[0] = img.size[0]
    if bbox[1] > img.size[1]:
        bbox[1] = img.size[1]
    return bbox


for coco_json_filename, output_folder in zip(coco_json_filenames, output_folder):

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

        
        image_crop = Image.open(path_to_coco / "img" / image_filename).crop(
            (coco_bbox[0], coco_bbox[1], coco_bbox[0] + coco_bbox[2], coco_bbox[1] + coco_bbox[3])
        )

        (dataset_ouptut_path / output_folder / category_name).mkdir(parents=True, exist_ok=True)
        image_crop.save(dataset_ouptut_path / output_folder / category_name / (category_name + "_" + str(annotation["id"]) + image_filename.suffix))
