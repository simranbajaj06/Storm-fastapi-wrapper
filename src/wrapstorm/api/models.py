from pydantic import BaseModel
from typing import Optional

class StormRequest(BaseModel):
    topic: str
    do_research: Optional[bool] = True
    do_generate_outline: Optional[bool] = True
    do_generate_article: Optional[bool] = True
    do_polish_article: Optional[bool] = True
    stream: Optional[bool] = False

