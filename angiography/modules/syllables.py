import random
from ..stats.utils import adjust_to_stats
from ..modules.utils import show_annotations_over_image, get_ids_names_explanations, get_image
from shapely.geometry import Polygon, Point
import solara
import imageio.v3 as iio

class Syllable():
  def __init__(self, images_annotations, segment_definitions_dict, user_stats = None, module_stats = None, n_syllables = 3, print=True, use_syntax_scores=True):
    self.answered = False
    self.print = print
    self.segment_definitions_dict = segment_definitions_dict
    self.user_stats = user_stats
    self.module_stats = module_stats
    self.image = self.get_image(images_annotations)
    self.image_data = iio.imread(self.image["file_path"])
    solution_options = self.get_options_and_solution(use_syntax_scores)
    self.solution, self.options = solution_options["solution"], solution_options["options"]
    self.solara_dict = self.create_solara_dict()

  def answer(self, answer):
    self.answer = answer
    if not self.answered: 
      self.assert_answer(self.answer)
      self.answered = True
      if self.check_answer(self.answer):
        self.score = 1
      else:
        self.score = 0

  def result(self, return_data=False):
    data = self.create_solution(return_data=return_data)
    if self.print:
      if self.score:
        print(f"Congratulation, your answer {self.result_answer} is correct!")
      else:
        print(f"{self.result_answer} is not the correct answer!")
    if return_data:
      return data

  def start(self, return_data=False):
    np_data = self.view_func(return_data=return_data)
    if self.print:
      print(self.task_description)
      for option in self.options:
        print(option)
    if return_data:
      return np_data

class ChooseArteryNameSyllable(Syllable):
  @property
  def k_possibilities(self):
    return 4
  
  def create_solara_dict(self):
    return {"widgets": [solara.ToggleButtonsSingle, solara.VBox],
            "widget_options": [{"options": self.options}, {"text": [solara.Text for i in range(len(self.options))], "values": [f"i) {option} " for i, option in enumerate(self.options)], "tooltips": [solara.Tooltip for i in range(len(self.options))], "tooltip_descriptions": [self.get_ids_names_explanations(id, ["segment_description"]) for id in self.all_segment_ids]}],
            "answer_value": [solara.reactive(self.options[0]), None]}
  
  def create_solution(self, return_data = False):
    answer_index = self.options.index(self.answer)
    answer_id = self.all_segment_ids[answer_index]
    self.result_answer = self.answer
    self.result_solution = self.solution
    if self.score:
      segment_ids = [self.solution_id]
      colors = {self.solution_id: "green"}
    else:
      segment_ids = [self.solution_id, answer_id]
      colors = {self.solution_id:"yellow", answer_id: "red"}
    return show_annotations_over_image(self.image_data, self.image, segment_ids=segment_ids, show_name = True, colors=colors, size=(3, 1), return_data=return_data)

  def get_image(self, images_annotations):
      return get_image(images_annotations)

  def get_options_and_solution(self, use_syntax_scores):
    if not use_syntax_scores: 
      name_parts = ["segment_alphanumeric", "segment_name"]
    else:
      name_parts = ["segment_alphanumeric"]
    return {"solution": self.get_solution(name_parts), "options": self.get_options(name_parts)}

  def get_solution(self, name_parts):
    self.solution_id = adjust_to_stats(list(self.image["annotations"].keys()), user_stats = self.user_stats, module_stats = self.module_stats, k=1)[0]
    self.solution = self.get_ids_names_explanations(self.solution_id, name_parts)
    return self.solution

  def get_options(self, name_parts):
    segment_ids_without_correct = list(self.image["annotations"].keys())
    segment_ids_without_correct.remove(self.solution_id)
    if len(segment_ids_without_correct) >= self.k_possibilities - 1:
      self.all_segment_ids = random.sample(segment_ids_without_correct, k=self.k_possibilities - 1)
    else:
      self.all_segment_ids = segment_ids_without_correct
    self.all_segment_ids.append(self.solution_id)
    random.shuffle(self.all_segment_ids)
    ids_names_explanations = [self.get_ids_names_explanations(id, name_parts) for id in self.all_segment_ids]
    self.task_description = "Enter the name of the selected artery!"
    return ids_names_explanations

  def get_ids_names_explanations(self, id, name_parts=["segment_alphanumeric", "segment_name", "segment_description"]):
    return get_ids_names_explanations(self.segment_definitions_dict, id, name_parts)

  def view_func(self, return_data=False):
    return show_annotations_over_image(self.image_data, self.image, segment_ids=self.solution_id, show_name = False, return_data=return_data)

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
  
  def create_solution(self, return_data=False):
    self.result_answer = self.answer
    self.result_solution = self.solution
    if self.solution=="right":
      segment_ids = self.right_segments
    else:
      segment_ids = self.left_segments
    if self.score:
      colors = {id:"green" for id in segment_ids}
    else:
      colors = {id:"red" for id in segment_ids}
    return show_annotations_over_image(self.image_data, self.image, segment_ids=segment_ids, show_name = True, colors=colors, size=(4, 2), return_data=return_data)

  def get_image(self, images_annotations):
    while True:
      image_id = random.sample(list(images_annotations.keys()), k=1)[0]
      image = images_annotations[image_id]
      all_segment_ids = list(image["annotations"].keys())
      if any([d in all_segment_ids for d in self.right_segments]) or any([d in all_segment_ids for d in self.left_segments]):
        break
    return image

  def view_func(self, return_data=False):
    return show_annotations_over_image(self.image_data, self.image, segment_ids=[], show_name = False, return_data=return_data)

  def get_options_and_solution(self, use_syntax_scores):
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
            "widget_options": [{"label": "x", "min": 0, "max": iio.imread(self.image["file_path"]).shape[0]-1}, {"label": "y", "min": 0, "max": iio.imread(self.image["file_path"]).shape[1]-1}],
            "answer_value": [self.point[0], self.point[1]]}

  def create_solution(self, return_data=False):
    self.result_answer = self.answer
    self.result_solution = f"Your answer is {round(self.distance, 1)}px far from the solution!\nA distance of <{self.px_soft}px is considered as correct."
    if self.score:
      colors = {"point": "green", self.solution: "yellow"}
    else:
      colors = {"point": "red", self.solution: "yellow"}
    return show_annotations_over_image(self.image_data, self.image, segment_ids=self.solution, point=[self.point[0].value, self.point[1].value], colors=colors, show_name=False, size=(3, 1), return_data=return_data)

  def get_image(self, images_annotations):
    return get_image(images_annotations)

  def view_func(self, return_data=False):
    return show_annotations_over_image(self.image_data, self.image, segment_ids = [], point=[self.point[0].value, self.point[1].value], colors={"point": "magenta"}, return_data=return_data)

  def get_options_and_solution(self, use_syntax_scores):
    return {"options": self.get_options(), "solution": self.get_solution()}

  def get_solution(self):
    segmentation = self.image["annotations"]["26"]["segmentation"][0]
    x = segmentation[::2]
    y = segmentation[1::2]
    coords = [[xi, yi] for xi, yi in zip(x, y)]
    self.solution_polygon = Polygon(coords)
    return "26"

  def get_options(self):
    self.task_description = "Locate the stenosis in the image!"
    self.point = [solara.reactive(0), solara.reactive(0)]
    return []

  def check_answer(self, answer):
    self.distance = self.solution_polygon.distance(Point(answer[0], answer[1]))
    return self.distance < self.px_soft

  def assert_answer(self, answer):
    assert len(answer) == 2, ""


class ChooseArteryBoxSyllable(Syllable):
  @property
  def px_soft(self):
    return 10
  
  def create_solara_dict(self):
    return {"widgets": [solara.Tooltip, solara.SliderFloat, solara.SliderFloat],
            "widget_options": [{"tooltip": self.get_ids_names_explanations(self.solution_key, ["segment_description"]), "widget_within": solara.Text, "widget_within_label": "Description"}, {"label": "x", "min": 0, "max": iio.imread(self.image["file_path"]).shape[0]-1}, {"label": "y", "min": 0, "max": iio.imread(self.image["file_path"]).shape[1]-1}],
            "answer_value": [None, self.point[0], self.point[1]]}
  
  def create_solution(self, return_data = False):
    self.result_answer = self.answer
    self.result_solution = f"Your answer is {round(self.distance, 1)}px far from the solution!\nA distance of <{self.px_soft}px is considered as correct."
    if self.score:
      colors = {"point": "green", self.solution: "yellow"}
    else:
      colors = {"point": "red", self.solution: "yellow"}
    return show_annotations_over_image(self.image_data, self.image, segment_ids=self.solution, point=[self.point[0].value, self.point[1].value], colors=colors, show_name=False, size=(3, 1), return_data=return_data)

  def get_image(self, images_annotations):
    return get_image(images_annotations)

  def view_func(self, return_data = False):
    return show_annotations_over_image(self.image_data, self.image, segment_ids = [], point=[self.point[0].value, self.point[1].value], colors={"point": "magenta"}, return_data=return_data)

  def get_options_and_solution(self, use_syntax_scores):
    if not use_syntax_scores: 
      name_parts = ["segment_alphanumeric", "segment_name"]
    else:
      name_parts = ["segment_alphanumeric"]
    return {"options": self.get_options(), "solution": self.get_solution(name_parts)}

  def get_solution(self, name_parts):
    self.solution_key = adjust_to_stats(list(self.options_dict.keys()), user_stats = self.user_stats, module_stats = self.module_stats, k=1)[0]
    artery_to_find = self.get_ids_names_explanations(self.solution_key, name_parts)
    self.task_description = f"Locate {artery_to_find} in the image!"
    segmentation = self.image["annotations"][self.solution_key]["segmentation"][0]
    x = segmentation[::2]
    y = segmentation[1::2]
    coords = [[xi, yi] for xi, yi in zip(x, y)]
    self.solution_polygon = Polygon(coords)
    return self.solution_key
  
  def get_ids_names_explanations(self, id, name_parts=["segment_alphanumeric", "segment_name", "segment_description"]):
    return get_ids_names_explanations(self.segment_definitions_dict, id, name_parts)

  def get_options(self):
    self.options_dict = {segment_id : str(i) for i, segment_id in enumerate(self.image["annotations"])}
    self.point = [solara.reactive(0), solara.reactive(0)]
    return []

  def check_answer(self, answer):
    self.distance = self.solution_polygon.distance(Point(answer[0], answer[1]))
    return self.distance < self.px_soft

  def assert_answer(self, answer):
    assert len(answer) == 2, ""