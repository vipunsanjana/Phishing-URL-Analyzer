from pydantic import BaseModel
from typing import List, Optional

class PhishingAnalysisResponse(BaseModel):
    is_related_to_LK: bool
    is_political_content: bool
    phishing_score: int
    impersonated_brand: Optional[str]
    is_phishing: bool
    number_of_keyword: int
    keyword_list: List[str]