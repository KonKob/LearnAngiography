import wget
from zipfile import ZipFile
from pathlib import Path
import json
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
    destination_dir_path = str(Path.cwd().parent)
    arcade_path = Path(destination_dir_path).joinpath("arcade/")

    if not arcade_path.exists():
        destination_dir_path = download_sample_data(destination_dir_path=destination_dir_path)
    
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
    
    module_dict = {"ChooseArteryName": {"images": images_annotations, "syllable": ChooseArteryNameSyllable},
                "RightOrLeft": {"images": images_annotations, "syllable": RightOrLeftSyllable},
                "FindStenosis": {"images": stenosis_images_annotations, "syllable": FindStenosisSyllable},
                "ChooseArteryBox": {"images": images_annotations, "syllable": ChooseArteryBoxSyllable}
                }
            
    return module_dict
