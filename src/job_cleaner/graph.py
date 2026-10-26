from langgraph.graph import StateGraph,START , END 

from .state import JobCleanerState
from .nodes import extract , flag , rewrite ,  review
from .router import should_retry

def build_graph() :
    g = StateGraph(JobCleanerState)

    g.add_node("extract",extract)
    g.add_node("flag",flag)
    g.add_node("rewrite",rewrite)
    g.add_node("review",review)

    g.add_edge(START,"extract")
    g.add_edge("extract","flag")
    g.add_edge("flag","rewrite")
    g.add_edge("rewrite","review")
    g.add_conditional_edges("review",should_retry)

    return g.compile()

app = build_graph()


