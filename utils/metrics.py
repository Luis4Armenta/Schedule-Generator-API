from typing import List
from statistics import mean, stdev

def get_positive_score(positive_scores: List[float]) -> float:
  if len(positive_scores) < 2:
    return positive_scores[0]
  
  m = mean(positive_scores)
  std = stdev(positive_scores)
  
  if std == 0:
    return m
  
  z_scores = [(x - m) / std for x in positive_scores]
  
  threshold = 3  
  filtered_scores = [score for score, z_score in zip(positive_scores, z_scores) if abs(z_score) < threshold]
  
  result = mean(filtered_scores)
  
  return result