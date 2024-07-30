import matplotlib.pyplot as plt
import numpy as np
import imageio.v3 as iio

def show_annotations_over_image(image, segment_ids="all", show_name: bool=True, show_alias: bool=False):
    fig, ax = plt.subplots()
    ax.imshow(iio.imread(image["file_path"]), cmap="Greys")
    for i, annotation in enumerate(image["annotations"].values()):
        segment_category = str(annotation["category_id"])
        if segment_ids != "all":
            if type(segment_ids) == list:
                if segment_category not in segment_ids:
                    continue
            elif type(segment_ids) == str:
                if segment_ids != segment_category:
                    continue
            else:
                raise TypeError("segment_ids has to be a string or a list of strings or 'all'")
        segmentation = annotation["segmentation"][0]
        x = segmentation[::2]
        y = segmentation[1::2]
        ax.plot(x, y, color='blue')
        if show_name:
          ax.text(np.mean(x), np.mean(y), segment_definitions.loc[segment_definitions["segment_id"]==segment_category, "segment_name"].values[0])
        if show_alias:
          ax.text(np.mean(x), np.mean(y), i, color="blue", fontsize=20)
    display(fig)
    plt.close()
    return segment_ids


def show_points_over_image(image, point):
    fig, ax = plt.subplots()
    ax.imshow(iio.imread(image["file_path"]), cmap="Greys")
    ax.scatter(point[0], point[1], s = 20)
    display(fig)
    plt.close()
    return None