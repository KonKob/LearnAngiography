import wget
from zipfile import ZipFile
from pathlib import Path
import json
import requests
from ..modules.syllables import RightOrLeftSyllable, ChooseArteryNameSyllable, ChooseArteryBoxSyllable, FindStenosisSyllable

def download_sample_data(destination_dir_path: str, dataset_url = 'https://zenodo.org/api/records/10390295/files-archive') -> None:
    wget.download(url = dataset_url, out=destination_dir_path)
    zip_folders = ['10390295.zip', 'arcade.zip']
    for folder in zip_folders:
        path = Path(destination_dir_path).joinpath(folder)
        with ZipFile(path, 'r') as zObject:
            zObject.extractall(path=destination_dir_path)
            path.unlink()
    return destination_dir_path


def load_data():
    cwd = Path.cwd()
    destination_dir_path = str(cwd.parent)
    arcade_path = Path(destination_dir_path).joinpath("arcade/")

    if not arcade_path.exists():
        #destination_dir_path = download_sample_data(destination_dir_path=destination_dir_path)
        files_urls_path = "https://raw.githubusercontent.com/KonKob/LearnAngiography/main/angiography/media/files_urls_final.json"
        r = requests.get(files_urls_path)
        files_urls = r.json()
        files_urls_path = "https://raw.githubusercontent.com/KonKob/LearnAngiography/main/angiography/media/syntax.json"
        r = requests.get(files_urls_path)
        annotations = r.json()
        files_urls_path = "https://raw.githubusercontent.com/KonKob/LearnAngiography/main/angiography/media/stenosis.json"
        r = requests.get(files_urls_path)
        stenosis_annotations = r.json()
        
        images_annotations = {str(image["id"]):{"file_path": files_urls["syntax"][image["file_name"]], "annotations": {str(annotation["category_id"]):annotation for annotation in annotations["annotations"] if image["id"]==annotation["image_id"]}} for image in annotations["images"]}
        stenosis_images_annotations = {str(image["id"]):{"file_path": files_urls["stenosis"][image["file_name"]], "annotations": {str(annotation["category_id"]):annotation for annotation in stenosis_annotations["annotations"] if image["id"]==annotation["image_id"]}} for image in stenosis_annotations["images"]}

    else:
        syntax_path = arcade_path.joinpath("syntax/train/")
        syntax_images_path = syntax_path.joinpath("images/")
        stenosis_path = arcade_path.joinpath("stenosis/train/")
        stenosis_images_path = stenosis_path.joinpath("images/")
        with open(syntax_path.joinpath("annotations/train.json"), "rb") as file:
            annotations = json.load(file)
        with open(stenosis_path.joinpath("annotations/train.json"), "rb") as file:
            stenosis_annotations = json.load(file)
        images_annotations = {str(image["id"]):{"file_path": syntax_images_path.joinpath(image["file_name"]), "annotations": {str(annotation["category_id"]):annotation for annotation in annotations["annotations"] if image["id"]==annotation["image_id"]}} for image in annotations["images"]}
        stenosis_images_annotations = {str(image["id"]):{"file_path": stenosis_images_path.joinpath(image["file_name"]), "annotations": {str(annotation["category_id"]):annotation for annotation in stenosis_annotations["annotations"] if image["id"]==annotation["image_id"]}} for image in stenosis_annotations["images"]}

    module_dict = {
        "Right or left": {"images": images_annotations, "syllable": RightOrLeftSyllable},
        "Choose artery name": {"images": images_annotations, "syllable": ChooseArteryNameSyllable},
        "Locate artery": {"images": images_annotations, "syllable": ChooseArteryBoxSyllable},
        "Locate stenosis": {"images": stenosis_images_annotations, "syllable": FindStenosisSyllable},
                }
            
    return module_dict
