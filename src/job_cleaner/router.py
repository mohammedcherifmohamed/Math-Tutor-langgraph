from langgraph.graph import END
from .state import JobCleanerState

SCORE_THRESHOLD = 8
MAX_ATTEMPTS = 3

def should_retry(state:JobCleanerState) -> str:
    if state['score'] >= SCORE_THRESHOLD : 
        return END
    if state['attemtpts'] >= MAX_ATTEMPTS : 
        return END
    return "rewrite"

