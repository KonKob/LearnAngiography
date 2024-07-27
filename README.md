# LearnAngiography
This is a free [web application](https://billowing-snow-9570.ploomberapp.io) to improve your understanding of coronary angiography in different quiz modules. You can also use the GUI via [Google Colab](https://colab.research.google.com/github/KonKob/LearnAngiography/blob/main/angiography/angiography.ipynb). 


Module | Description
------ | -----------
RightOrLeft | Choose between right or left, depending on the artery view.
ChooseArteryName | Choose the name of the artery outlined in the image.
ChooseArteryBox | Choose the number of the box outlining the artery of interest in the image.
FindStenosis | Enter the coordinates of the stenosis in the image.


>[!IMPORTANT]  
>This is an initial version of the application and will be improved in the future. If you want to contribute, write your ideas as an issue!




## Coronary Angiography Data
This application is meant for learning purposes. It is based on the data and annotations of the publicly available ARCADE Dataset published in 2024 [1]. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10390295.svg)](https://doi.org/10.5281/zenodo.10390295)

Of the dataset divided into 1500 images for syntax and 1500 images for stenoses, the 1000 and 1000 training images are being used in this application. The data was acquired from 1500 patients with clinical suspicion of coronary heart disease from the Research Institute of Cardiology and Internal Diseases in Almaty (Kazakhstan). 0 to 2 images in six different angulations were recorded per patient and 0 to 12 images per patient were included into the final dataset. Two different angiographs were used for acquisitation: Philips Azurion 3 (Philips, Amsterdam, Netherlands) and Siemens Artis Zee (Siemens Medical Solutions, Erlangen, Germany). The different angulations contain 4 views for the left coronary artery (Left Anterior Oblique (LAO) and Right Anterior Oblique (RAO) caudal views, Postero-Anterior (PA) and RAO cranial views) and 2 views for the right coronary artery (LAO and RAO cranial views).

> [!TIP]
> Check out the [paper](https://doi.org/10.1038/s41597-023-02871-z) to the ARCADE dataset!



[1] Popov, M., Amanturdieva, A., Zhaksylyk, N. et al. Dataset for Automatic Region-based Coronary Artery Disease Diagnostics Using X-Ray Angiography Images. Sci Data 11, 20 (2024).



