class ModuleStatistics(ABC):

  def __init__(self, module_name):
    self.module_name = module_name
    self.highscores = self._initialize_highscores()
    self.score_ranking = self._initialize_score_ranking()
    self.number_of_trials_per_user = self._initialize_number_of_trials()
    self.number_of_trials_total = self._initialize_number_of_trials_total()
    self.meta_score_dict = self._initialize_meta_score_dict()


  @property
  def len_highscore(self):
    return 10

  def _initialize_score_ranking(self):
    return {}

  def _initialize_number_of_trials_total(self):
    return 0

  def _initialize_highscores(self):
    return {key:Score(module_name=self.module_name) for key in range(self.len_highscore)}

  def _initialize_number_of_trials(self):
    return {}

  def _initialize_meta_score_dict(self):
    return {}


  def make_new_score_entry(self, score):
    assert score.module_name == self.module_name, "Can't add score from a different module!"
    self._update_number_of_trials(score)
    self._add_to_score_ranking(score)
    self._extract_score_dict(score)

  def get_highscore(self):
    return [f"{key} : {self.highscores[key].score} - {self.highscores[key].user_name} - {self.highscores[key].timestamp}" for key in self.highscores]


  def _update_number_of_trials(self, score):
    if score.user_name not in self.number_of_trials_per_user:
      self.number_of_trials_per_user[score.user_name] = 0
    self.number_of_trials_per_user[score.user_name] += 1
    self.number_of_trials_total = sum(self.number_of_trials_per_user.values())

  def _add_to_score_ranking(self, score):
    if score.user_name in self.score_ranking:
      self.score_ranking[score.user_name][score.timestamp] = score.score
    else:
      self.score_ranking[score.user_name] = {score.timestamp:score.score}
    self._check_new_highscore(score)

  def _check_new_highscore(self, score):
    for i in range(self.len_highscore):
      if score.score > self.highscores[i].score:
        for v in range(self.len_highscore-1, i, -1):
          self.highscores[v] = self.highscores[v-1]
        self.highscores[i] = score
        if i == 0:
          print("New highscore!", self.get_highscore())
        break

  def _extract_score_dict(self, score):
    if score.score_dict is not None:
      for key in score.score_dict:
        if key not in self.meta_score_dict:
          self.meta_score_dict[key] = []
        self.meta_score_dict[key] += score.score_dict[key]