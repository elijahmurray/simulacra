from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Memory:
  description: str
  importance_score: int
  created_at: datetime = datetime.utcnow()
  last_accessed: datetime = datetime.utcnow()

  def update_last_accessed(self):
    self.last_accessed = datetime.utcnow()

  def update_importance_score(self, score):
    self.importance_score = score

  def __str__(self):
    return self.description

