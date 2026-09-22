"""System 2: a rule-based workflow. Fixed if/else rules, no LLM at all."""
import re
from config import BOOK_FINES, QUESTIONS

def workflow(question):
    codes = re.findall(r"[A-Z]\d{3}", question.upper())
    fines = [BOOK_FINES[code] for code in codes if code in BOOK_FINES]

    if not fines:
        return "Sorry, I can only answer questions about book fines."

    text = question.lower()

    if "total" in text:
        total = sum(fines)
        days = re.search(r"(\d+)\s*days?", text)
        if days:
            total = total * int(days.group(1))
        return f"Total fine: Rs. {total:,.0f}"

    if len(fines) == 1:
        return f"Fine for {codes[0]}: Rs. {fines[0]:,}"

    return "Sorry, I do not have a rule for this type of question."

if __name__ == "__main__":
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW (no LLM) ===\n")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)