import matplotlib.pyplot as plt
import numpy as np
import imageio.v3 as iio
from ..meta.segment_definitions import segment_definitions
import random
from ..meta.styles import plot_style

def show_annotations_over_image(image, segment_ids="all", show_name: bool=True, show_alias: bool=False, colors={}, point=None, size=(7, 4)):
    fig, ax = plt.subplots(figsize=size)
    ax.imshow(iio.imread(image["file_path"]), cmap="Greys")
    if point is not None:
        if "point" in colors:
            color = colors["point"]
        else:
            color = plot_style["foreground"]
        ax.scatter(point[0], point[1], s = (size[0]*size[1])*1.5, color=color)
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
        if segment_category in colors:
            color = colors[segment_category]
        else:
            color = plot_style["foreground"]
        ax.plot(x, y, color=color)
        if show_name:
          ax.text(np.mean(x), np.mean(y), segment_definitions.loc[segment_definitions["segment_id"]==segment_category, "segment_name"].values[0], color=plot_style["text-color"])
        if show_alias:
          ax.text(np.mean(x), np.mean(y), i, color=plot_style["text-color"], fontsize=(size[0]*size[1])/2)
          
    ax.set_facecolor(plot_style["face-color"])
    fig.set_facecolor(plot_style["face-color"])
    ax.xaxis.label.set_color(plot_style["axis-color"])
    ax.yaxis.label.set_color(plot_style["axis-color"])
    ax.tick_params(axis='x', colors=plot_style["axis-color"])
    ax.tick_params(axis='y', colors=plot_style["axis-color"])
    ax.spines['left'].set_color(plot_style["axis-color"])
    ax.spines['bottom'].set_color(plot_style["axis-color"])
    display(fig)
    plt.close()
    return segment_ids


def get_ids_names_explanations(self, id, name_parts=["segment_alphanumeric", "segment_name", "segment_description"]):
    name = ""
    for part in name_parts:
      name += (self.segment_definitions.loc[self.segment_definitions["segment_id"]==id, part].values[0] + " ")
    name = name[:-1]
    return name


def get_image(images_annotations):
    image_id = random.sample(list(images_annotations.keys()), k=1)[0]
    return images_annotations[image_id]