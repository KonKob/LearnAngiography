import wget
from zipfile import ZipFile
from pathlib import Path

def download_sample_data(destination_dir_path: str = "/content/", dataset_url = 'https://zenodo.org/api/records/10390295/files-archive') -> None:
    wget.download(url = dataset_url, out=destination_dir_path)
    zip_folders = ['10390295.zip', 'arcade.zip']
    for folder in zip_folders:
        path = Path(destination_dir_path).joinpath(folder)
        with ZipFile(path, 'r') as zObject:
            zObject.extractall(path=destination_dir_path)
            path.unlink()