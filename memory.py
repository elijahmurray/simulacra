from dataclasses import dataclass
import datetime
from typing import List

@dataclass
class Memory:
  description: str
  type: str
  importance_score: int
  created_at: datetime.datetime
  last_accessed: datetime.datetime

  def update_last_accessed(self, access_time: datetime.datetime):
    self.last_accessed = access_time

  def update_importance_score(self, score):
    self.importance_score = score

  def __str__(self):
    return self.description
