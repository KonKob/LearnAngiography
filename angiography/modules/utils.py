import matplotlib.pyplot as plt
import imageio.v3 as iio
from ..meta.segment_definitions import segment_definitions_dict
import random
from ..meta.styles import plot_style
import numpy as np

def show_annotations_over_image(image_data, image, segment_ids="all", show_name: bool=True, show_alias: bool=False, colors={}, point=None, size=(7, 4), return_data=False):
    fig, ax = plt.subplots(figsize=size)
    ax.imshow(image_data, cmap="Greys")
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
        ax.plot(x+[x[0]], y+[y[0]], color=color)
        if show_name:
          ax.text(sum(x)/len(x), sum(y)/len(y), get_ids_names_explanations(segment_definitions_dict, segment_category, name_parts=["segment_name"]), color=plot_style["text-color"])
        if show_alias:
          ax.text(sum(x)/len(x), sum(y)/len(y), i, color=plot_style["text-color"], fontsize=(size[0]*size[1])/2)
          
    ax.set_facecolor(plot_style["face-color"])
    fig.set_facecolor(plot_style["face-color"])
    ax.xaxis.label.set_color(plot_style["axis-color"])
    ax.yaxis.label.set_color(plot_style["axis-color"])
    ax.tick_params(axis='x', colors=plot_style["axis-color"])
    ax.tick_params(axis='y', colors=plot_style["axis-color"])
    ax.spines['left'].set_color(plot_style["axis-color"])
    ax.spines['bottom'].set_color(plot_style["axis-color"])
    if return_data:
        fig.canvas.draw()
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.close()
        return data
    else:
        display(fig) 
        plt.close()
        return None


def get_ids_names_explanations(segment_definitions_dict, id, name_parts=["segment_alphanumeric", "segment_name", "segment_description"]):
    name = ""
    for part in name_parts:      
      key = list(segment_definitions_dict["segment_id"].keys())[list(segment_definitions_dict["segment_id"].values()).index(id)]
      name += (segment_definitions_dict[part][key] + " ")
    name = name[:-1]
    return name


def get_image(images_annotations):
    image_id = random.sample(list(images_annotations.keys()), k=1)[0]
    return images_annotations[image_id]