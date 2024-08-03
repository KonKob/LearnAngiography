# LearnAngiography
<img align="left" width="200" height="200" src="/angiography/media/favicon.png?raw=true">

This is a free web application to improve your understanding of x-ray coronary angiography images in different quiz modules. You can currently use the GUI via [Google Colab](https://colab.research.google.com/github/KonKob/LearnAngiography/blob/main/angiography.ipynb). 




Module | Description
------ | -----------
Right or left | Choose whether right or left coronary artery is depicted predominantely in the image. 
Choose artery name | Choose the name of the artery outlined in the image.
Locate artery | Locate the requested artery in the x-ray angiography image. 
Locate stenosis | Locate the stenosis in the x-ray angiography image.       


>[!IMPORTANT]  
>This is an initial version of the application and will be improved in the future. If you want to contribute, write your ideas as an issue!




## Coronary Angiography Data
This application is meant for learning purposes. It is based on the data and annotations of the publicly available ARCADE Dataset published in 2024 [1]. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10390295.svg)](https://doi.org/10.5281/zenodo.10390295)


The dataset targets the two purposes syntax and stenosis detection with 1500 images each. 1000 training images of each category are used in this application.
The data was acquired from 1500 patients with clinical suspicion of coronary heart disease from the Research Institute of Cardiology and Internal Diseases in Almaty (Kazakhstan).
0 to 2 images per each of the six different angulations were recorded per patient resulting in 0 to 12 images per patient in the final dataset. Two different angiographs were used for acquisitation: Philips Azurion 3 (Philips, Amsterdam, Netherlands) and Siemens Artis Zee (Siemens Medical Solutions, Erlangen, Germany).
The different angulations contain 4 views for the left coronary artery (Left Anterior Oblique (LAO) and Right Anterior Oblique (RAO) caudal views, Postero-Anterior (PA) and RAO cranial views) and 2 views for the right coronary artery (LAO and RAO cranial views). The authors of the ARCADE dataset [1], used the syntax score [2], to define stenosis as >= 50% degree of constriction  in coronary arteries of at least 1.5 _mm_ diameter.

> [!TIP]
> Check out the [paper](https://doi.org/10.1038/s41597-023-02871-z) to the ARCADE dataset!



> [1] Popov, M., Amanturdieva, A., Zhaksylyk, N., Alkanov, A., Saniyazbekov, A., Aimyshev, T., Ismailov, E., Bulegenov, A., Kuzhukeyev, A., Kulanbayeva, A., Kalzhanov, A., Temenov, N., Kolesnikov, A., Sakhov, O., & Fazli, S. (2024). Dataset for Automatic Region-based Coronary Artery Disease Diagnostics Using X-Ray Angiography Images. Scientific data, 11(1), 20.

> [2] Sianos, G., Morel, M. A., Kappetein, A. P., Morice, M. C., Colombo, A., Dawkins, K., van den Brand, M., Van Dyck, N., Russell, M. E., Mohr, F. W., & Serruys, P. W. (2005). The SYNTAX Score: an angiographic tool grading the complexity of coronary artery disease. EuroIntervention : journal of EuroPCR in collaboration with the Working Group on Interventional Cardiology of the European Society of Cardiology, 1(2), 219–227.


