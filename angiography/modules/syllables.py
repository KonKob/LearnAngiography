import random
from ..stats.utils import adjust_to_stats
from ..modules.utils import show_annotations_over_image, show_points_over_image
from shapely.geometry import Polygon, Point
import solara
import imageio.v3 as iio

class Syllable():
  def __init__(self, images_annotations, segment_definitions, user_stats = None, module_stats = None, n_syllables = 3, print=True):
    self.answered = False
    self.print = print
    self.segment_definitions = segment_definitions
    self.user_stats = user_stats
    self.module_stats = module_stats
    self.image = self.get_image(images_annotations)
    solution_options = self.get_options_and_solution()
    self.solution, self.options = solution_options["solution"], solution_options["options"]
    self.solara_dict = self.create_solara_dict()

  def answer(self, answer):
    if not self.answered:
      self.assert_answer(answer)
      self.answered = True
      if self.check_answer(answer):
        self.score = 1
        if self.print:
          print(f"Congratulation, your answer {answer} is correct!")
      else:
        if self.print:
          print(f"{answer} is not the correct answer!")
        self.score = 0

  def start(self):
    self.view_func()
    if self.print:
      print(self.task_description)
      for option in self.options:
        print(option)


class ChooseArteryNameSyllable(Syllable):
  @property
  def k_possibilities(self):
    return 4
  
  def create_solara_dict(self):
    return {"widgets": [solara.ToggleButtonsSingle, solara.VBox],
            "widget_options": [{"options": self.options}, {"text": [solara.Text for i in range(len(self.options))], "values": [f"i) {option} " for i, option in enumerate(self.options)], "tooltips": [solara.Tooltip for i in range(len(self.options))], "tooltip_descriptions": [self.segment_definitions.loc[self.segment_definitions["segment_id"]==id, "segment_description"].values[0] for id in self.all_segment_ids]}],
            "answer_value": [solara.reactive(self.options[0]), None]}

  def get_image(self, images_annotations):
    image_id = random.sample(list(images_annotations.keys()), k=1)[0]
    return images_annotations[image_id]

  def get_options_and_solution(self):
    return {"solution": self.get_solution(), "options": self.get_options()}

  def get_solution(self):
    self.solution_id = adjust_to_stats(list(self.image["annotations"].keys()), user_stats = self.user_stats, module_stats = self.module_stats, k=1)[0]
    self.solution = self.get_ids_names_explanations(self.solution_id)
    return self.solution

  def get_options(self):
    segment_ids_without_correct = list(self.image["annotations"].keys())
    segment_ids_without_correct.remove(self.solution_id)
    if len(segment_ids_without_correct) >= self.k_possibilities - 1:
      self.all_segment_ids = random.sample(segment_ids_without_correct, k=self.k_possibilities - 1)
    else:
      self.all_segment_ids = segment_ids_without_correct
    self.all_segment_ids.append(self.solution_id)
    random.shuffle(self.all_segment_ids)
    ids_names_explanations = [self.get_ids_names_explanations(id) for id in self.all_segment_ids]
    self.task_description = "Enter the name of the selected artery!"
    return ids_names_explanations

  def get_ids_names_explanations(self, id):
    syntax_id = self.segment_definitions.loc[self.segment_definitions["segment_id"]==id, "segment_alphanumeric"].values[0]
    name = self.segment_definitions.loc[self.segment_definitions["segment_id"]==id, "segment_name"].values[0]
    explanation = self.segment_definitions.loc[self.segment_definitions["segment_id"]==id, "segment_description"].values[0]
    #return f"{id}\n{name}\n{explanation}"
    return f"{syntax_id} {name}"

  def view_func(self):
    show_annotations_over_image(self.image, segment_ids=self.solution_id, show_name = False)

  def check_answer(self, answer):
    return answer == self.solution

  def assert_answer(self, answer):
    assert answer in self.options, f"Your answer has to be one of {self.options}!"


class RightOrLeftSyllable(Syllable):

  @property
  def left_segments(self):
    return ["5", "6", "7", "11", "13"]

  @property
  def right_segments(self):
    return ["1", "2", "3"]
  
  def create_solara_dict(self):
    return {"widgets": [solara.ToggleButtonsSingle],
            "widget_options": [{"options": self.options}],
            "answer_value": [solara.reactive(self.options[0])]}

  def get_image(self, images_annotations):
    while True:
      image_id = random.sample(list(images_annotations.keys()), k=1)[0]
      image = images_annotations[image_id]
      all_segment_ids = list(image["annotations"].keys())
      if any([d in all_segment_ids for d in self.right_segments]) or any([d in all_segment_ids for d in self.left_segments]):
        break
    return image

  def view_func(self):
    show_annotations_over_image(self.image, segment_ids=[], show_name = False)

  def get_options_and_solution(self):
    return {"solution": self.get_solution(), "options": self.get_options()}

  def get_solution(self):
    all_segment_ids = list(self.image["annotations"].keys())
    if any([d in all_segment_ids for d in self.right_segments]):
      solution = "right"
    if any([d in all_segment_ids for d in self.left_segments]):
      solution = "left"
    return solution

  def get_options(self):
    self.task_description = "Choose the right view!"
    return ["right", "left"]

  def check_answer(self, answer):
    return answer == self.solution

  def assert_answer(self, answer):
    assert answer in self.options, f"Your answer has to be one of {self.options}!"


class FindStenosisSyllable(Syllable):
  @property
  def px_soft(self):
    return 10
  
  def create_solara_dict(self):
    return {"widgets": [solara.SliderFloat, solara.SliderFloat],
            "widget_options": [{"label": "x", "min": 0, "max": iio.imread(self.image["file_path"]).shape[0]}, {"label": "y", "min": 0, "max": iio.imread(self.image["file_path"]).shape[1]}],
            "answer_value": [self.point[0], self.point[1]]}

  def get_image(self, images_annotations):
    image_id = random.sample(list(images_annotations.keys()), k=1)[0]
    return images_annotations[image_id]

  def view_func(self):
    show_points_over_image(self.image, [self.point[0].value, self.point[1].value])

  def get_options_and_solution(self):
    return {"options": self.get_options(), "solution": self.get_solution()}

  def get_solution(self):
    segmentation = self.image["annotations"]["26"]["segmentation"][0]
    x = segmentation[::2]
    y = segmentation[1::2]
    coords = [[xi, yi] for xi, yi in zip(x, y)]
    self.solution_polygon = Polygon(coords)
    return "26"

  def get_options(self):
    self.task_description = "Find the stenosis in the image!"
    self.point = [solara.reactive(0), solara.reactive(0)]
    return []

  def check_answer(self, answer):
    return self.solution_polygon.distance(Point(answer[0], answer[1])) < self.px_soft

  def assert_answer(self, answer):
    assert len(answer) == 2, ""


class ChooseArteryBoxSyllable(Syllable):
  @property
  def px_soft(self):
    return 10
  
  def create_solara_dict(self):
    return {"widgets": [solara.Tooltip, solara.SliderFloat, solara.SliderFloat],
            "widget_options": [{"tooltip": self.segment_definitions.loc[self.segment_definitions["segment_id"]==self.solution_key, "segment_description"].values[0], "widget_within": solara.Text, "widget_within_label": "description", "widget_within_style": {"outline-style": "solid"}}, {"label": "x", "min": 0, "max": iio.imread(self.image["file_path"]).shape[0]}, {"label": "y", "min": 0, "max": iio.imread(self.image["file_path"]).shape[1]}],
            "answer_value": [None, self.point[0], self.point[1]]}

  def get_image(self, images_annotations):
    image_id = random.sample(list(images_annotations.keys()), k=1)[0]
    return images_annotations[image_id]

  def view_func(self):
    show_points_over_image(self.image, [self.point[0].value, self.point[1].value])

  def get_options_and_solution(self):
    return {"options": self.get_options(), "solution": self.get_solution()}

  def get_solution(self):
    self.solution_key = adjust_to_stats(list(self.options_dict.keys()), user_stats = self.user_stats, module_stats = self.module_stats, k=1)[0]
    artery_to_find = self.segment_definitions.loc[self.segment_definitions["segment_id"]==self.solution_key, "segment_name"].values[0]
    self.task_description = f"Find {artery_to_find} in the image!"
    segmentation = self.image["annotations"][self.solution_key]["segmentation"][0]
    x = segmentation[::2]
    y = segmentation[1::2]
    coords = [[xi, yi] for xi, yi in zip(x, y)]
    self.solution_polygon = Polygon(coords)
    return self.solution_key

  def get_options(self):
    self.options_dict = {segment_id : str(i) for i, segment_id in enumerate(self.image["annotations"])}
    self.point = [solara.reactive(0), solara.reactive(0)]
    return []

  def check_answer(self, answer):
    return self.solution_polygon.distance(Point(answer[0], answer[1])) < self.px_soft

  def assert_answer(self, answer):
    assert len(answer) == 2, ""