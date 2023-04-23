from dataclasses import dataclass
from datetime import datetime

@dataclass
class Memory:
  description: str
  created_at: datetime = datetime.utcnow()
  last_accessed: datetime = datetime.utcnow()
  importance_score: int = 1

  def update_last_accessed(self):
    self.last_accessed = datetime.utcnow()

  def update_importance_score(self, score):
    self.importance_score = score

  def __str__(self):
    return self.description

