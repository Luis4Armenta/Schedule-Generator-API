from typing import List
from scrapy import Item, Field

class TeacherItem(Item):
  name: str = Field()
  url: str = Field()
  subjects: List[str] = Field()
  comments: List = Field()
  polarity: float = Field()