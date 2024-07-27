class UserStatistics(ABC):
  def __init__(self, user_name):
    self.user_name = user_name
    self.highscores_per_module = self._initialize_highscores_per_module()
    self.module_ranking = self._initialize_module_ranking()
    self.number_of_trials_per_module = self._initialize_number_of_trials_per_module()
    self.number_of_trials_total = self._initialize_number_of_trials_total()
    self.meta_score_dict = self._initialize_meta_score_dict()


  @property
  def len_highscore(self):
    return 10

  def _initialize_module_ranking(self):
    return {}

  def _initialize_number_of_trials_total(self):
    return 0

  def _initialize_highscores_per_module(self):
    return {}

  def _initialize_number_of_trials_per_module(self):
    return {}

  def _initialize_meta_score_dict(self):
    return {}


  def make_new_score_entry(self, score):
    assert score.user_name == self.user_name
    self._update_number_of_trials(score)
    self._add_to_score_ranking(score)
    self._extract_score_dict(score)

  def get_highscore(self, module_name):
    return [f"{key} : {self.highscores_per_module[module_name][key].score} - {self.highscores_per_module[module_name][key].user_name} - {self.highscores_per_module[module_name][key].timestamp}" for key in self.highscores_per_module[module_name]]

  def _add_to_score_ranking(self, score):
    if score.module_name in self.module_ranking:
      self.module_ranking[score.module_name][score.timestamp] = score.score
    else:
      self.module_ranking[score.module_name] = {score.timestamp:score.score}
    self._check_new_highscore(score)

  def _update_number_of_trials(self, score):
    if score.module_name not in self.number_of_trials_per_module:
      self.number_of_trials_per_module[score.module_name] = 0
    self.number_of_trials_per_module[score.module_name] += 1
    self.number_of_trials_total = sum(self.number_of_trials_per_module.values())

  def _check_new_highscore(self, score):
    if score.module_name not in self.highscores_per_module:
      self.highscores_per_module[score.module_name] = {key:Score(module_name=score.module_name) for key in range(self.len_highscore)}
    for i in range(self.len_highscore):
      if score.score > self.highscores_per_module[score.module_name][i].score:
        for v in range(self.len_highscore-1, i, -1):
          self.highscores_per_module[score.module_name][v] = self.highscores_per_module[score.module_name][v-1]
        self.highscores_per_module[score.module_name][i] = score
        if i == 0:
          print("New personal best!", self.get_highscore(module_name = score.module_name))
        break

  def _extract_score_dict(self, score):
    if score.score_dict is not None:
      if score.module_name not in self.meta_score_dict:
        self.meta_score_dict[score.module_name] = {}
      for key in score.score_dict:
        if key not in self.meta_score_dict[score.module_name]:
          self.meta_score_dict[score.module_name][key] = []
        self.meta_score_dict[score.module_name][key] += score.score_dict[key]