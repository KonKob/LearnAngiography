from ..stats.utils import Score

class Module():
  def __init__(self, images_annotations, syllable, name, segment_definitions_dict, user_stats = None, module_stats = None, n_syllables = 3, use_syntax_scores = True, print=True):
    self.module_name = name
    self.user_stats = user_stats
    self.n_syllables = n_syllables
    self.module_stats = module_stats
    self.syllables = [syllable(images_annotations, segment_definitions_dict, self.get_user_stats_dict(user_stats), self.get_module_stats_dict(module_stats), print=print, use_syntax_scores=use_syntax_scores) for i in range(self.n_syllables)]
    self.executed_syllables = 0
    self.print=print

  def get_module_stats_dict(self, module_stats):
    if module_stats == None:
      module_stats_dict = {}
    else:
      module_stats_dict = module_stats.meta_score_dict
    return module_stats_dict

  def get_user_stats_dict(self, user_stats):
    if user_stats == None:
      user_stats_dict = {}
    else:
      if self.module_name not in user_stats.meta_score_dict:
        user_stats_dict = {}
      else:
        user_stats_dict = user_stats.meta_score_dict[self.module_name]
    return user_stats_dict

  def result(self):
    score_dict = {}
    self.total_score = 0
    for syllable in self.syllables:
      if syllable.solution not in score_dict:
        score_dict[syllable.solution] = []
      score_dict[syllable.solution].append(syllable.score)
      self.total_score += syllable.score
    self.relative_score = round(self.total_score/self.n_syllables, 3)
    self.score = Score(score=self.relative_score, user_stats=self.user_stats, module_name=self.module_name, score_dict=score_dict)
    if self.print:
      print(f"total score: {self.total_score}")
      print(f"relative score: {self.relative_score}")
    if self.user_stats is not None:
      self.user_stats.make_new_score_entry(self.score)
    if self.module_stats is not None:
      self.module_stats.make_new_score_entry(self.score)

  def execute(self):
    if self.executed_syllables < self.n_syllables:
      if not self.syllables[self.executed_syllables].answered:
        self.syllables[self.executed_syllables].start()
      else:
        print("Please answer before continuing the module!")
    else:
      print("Module finished!")
      self.result()

  def answer(self, entered_answer):
    if not self.syllables[self.executed_syllables].answered:
      self.syllables[self.executed_syllables].answer(entered_answer)
      self.executed_syllables += 1
    else:
      print("You finished this item already. Please continue to the next item!")
