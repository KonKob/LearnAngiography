from datetime import datetime
import random


class Score():
  def __init__(self, score=0, user_stats=None, module_name="test", timestamp=datetime.now().strftime('%y_%m_%d %H:%M'), score_dict=None):
    self.score = score
    if user_stats is not None:
      self.user_name = user_stats.user_name
    else:
      self.user_name = "empty"
    self.module_name = module_name
    self.timestamp = timestamp
    self.score_dict = score_dict


def adjust_to_stats(segment_ids, user_stats=None, module_stats=None, k=1):
    stats = [stats for stats in [user_stats, module_stats] if stats is not None]
    if stats:
      segment_percentage_score = {}
      for segment_id in segment_ids:
        segment_mean = 0.9
        segment_means = []
        for stat in stats:
          if segment_id in stat:
            segment_means.append(sum(stat[segment_id])/len(stat[segment_id]))
        if segment_means:
          segment_mean = sum(segment_means)/len(segment_means)
        if segment_mean > 0.9:
          segment_mean = 0.9
        if segment_mean < 0.1:
          segment_mean = 0.1
        segment_percentage_score[segment_id] = segment_mean
      segment_adjustment = {key : (1-segment_percentage_score[key]/sum(segment_percentage_score.values())) for key in segment_percentage_score}
      chosen_segment = random.choices(list(segment_adjustment.keys()), weights=list(segment_adjustment.values()), k=k)
    else:
      chosen_segment = random.sample(segment_ids, k)
    return chosen_segment