from .config import model
from .state import JobCleanerState, ExtractedJob, Review


def extract(state: JobCleanerState) -> dict:
    structured = model.with_structured_output(ExtractedJob)
    r: ExtractedJob = structured.invoke(
        f"Extract role and a normalized skill list from:\n\n{state['raw']}"
    )
    return {"role": r.role, "skills": r.skills}


def flag(state: JobCleanerState) -> dict:
    flags: list[str] = []
    lowered = state["raw"].lower()
    for bad, label in {
        "rockstar":   "cliché: 'rockstar'",
        "ninja":      "cliché: 'ninja'",
        "fast-paced": "warning sign: 'fast-paced environment'",
    }.items():
        if bad in lowered:
            flags.append(label)

    result = model.invoke(
        f"List hidden red flags. One per line, or NONE.\n\n{state['raw']}"
    )
    for line in result.content.splitlines():
        line = line.strip("-• ").strip()
        if line and line.upper() != "NONE":
            flags.append(line)
    return {"red_flags": flags}


def rewrite(state: JobCleanerState) -> dict:
    flags = "\n".join(f"- {f}" for f in state["red_flags"]) or "(none)"
    if state["attempts"] == 0 or not state["feedback"]:
        prompt = (
            f"Rewrite this posting cleanly. Fix these issues:\n{flags}\n\n"
            f"Role: {state['role']}\nSkills: {', '.join(state['skills'])}\n\n"
            f"ORIGINAL:\n{state['raw']}\n\nReturn only the cleaned posting."
        )
    else:
        prompt = (
            f"Revise the following draft to fix this feedback:\n"
            f"{state['feedback']}\n\nDRAFT:\n{state['polished']}\n\n"
            f"Return only the improved posting."
        )
    return {
        "polished": model.invoke(prompt).content.strip(),
        "attempts": state["attempts"] + 1,
    }


def review(state: JobCleanerState) -> dict:
    structured = model.with_structured_output(Review)
    r: Review = structured.invoke(
        f"Rate this cleaned posting 1–10 for clarity, professionalism, "
        f"and freedom from red flags. If <8, list concrete fixes.\n\n"
        f"{state['polished']}"
    )
    return {"score": r.score, "feedback": r.feedback if r.score < 8 else ""}