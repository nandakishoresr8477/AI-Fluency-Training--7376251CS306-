# Comparing a Chatbot, Rule-Based Workflow, and AI Agent — Library Fine Scenario

## Scenario

A college library tracks daily overdue fines for three book codes: B101
(Rs. 5 per day), B202 (Rs. 10 per day), and B303 (Rs. 7 per day). This
fine data is private to the library and has never been seen by any
public LLM. Three systems were built and tested on the same set of
questions: a plain chatbot, a rule-based workflow, and an AI agent.

## 1. Explanation of Each Approach

### Plain Chatbot

The chatbot sends the question directly to a large language model, with
no access to the library's real data and no tools. When I ran it, the
results were more revealing than a simple wrong-or-right answer. For
the first question, the model did not admit it lacked the data —
instead, it referenced real-sounding external policies (comparing B202
to a "New York Public Library" book category) and confidently stated a
fine of "$0.25 per day," which is entirely fabricated and unrelated to
the actual library in this scenario. For the second question, it
correctly stated that it could not give a specific numeric answer since
the rates weren't provided, but then illustrated the calculation using
invented example rates ($0.50 and $1.00) that have nothing to do with
the real B101/B202 fines. For the third question, it correctly
recognized it had no access to real records and asked me to supply the
data. The fourth question, needing no private data, was answered well.
This shows two different chatbot failure modes side by side: outright
hallucination dressed up with plausible-sounding external references,
and, in other cases, an honest admission that data is missing. Both
are consequences of the same root cause: a plain chatbot provides
responses using an LLM alone, with no way to check any of it against
real data.

### Rule-Based Workflow

The rule-based workflow involves no LLM at all. It is a fixed Python
program that matches a book code pattern in the question, looks up the
fine in a hardcoded dictionary, and applies simple if/else rules. When
I ran it, it correctly and instantly answered the direct fine lookup
(Rs. 10 for B202) and the total-fine-over-three-days question (Rs. 45).
It failed on the comparison question ("Is B303's fine higher than
B101's, and by how much?") and the reminder-message question, both
falling back to a generic message, because neither situation matched
any coded rule. This demonstrates the defining trait of a rule-based
workflow: it follows predefined steps and conditions with zero
reasoning, so it is completely reliable for the exact cases it was
built for, and completely unable to do anything else — even a harmless
question like the reminder message gets rejected simply because it
wasn't anticipated.

### AI Agent

The AI agent combines a large language model with two tools
(get_book_fine and calculator) inside a reasoning loop, reasoning about
what it needs, calling a tool, observing the result, and repeating
until it can answer. In my run, it called get_book_fine once for the
direct lookup, correctly returning 10. For the total-fine question, it
called get_book_fine twice and then calculator once, arriving at
exactly Rs. 45, and it showed its full working (5 x 3 = 15, 10 x 3 =
30, total 45) in the final answer. For the comparison question, it
again called get_book_fine twice and used calculator to compute the
difference, correctly concluding that B303's fine (Rs. 7) is Rs. 2
higher than B101's (Rs. 5) — a question the rule-based workflow could
not answer at all. For the reminder-message question, it correctly
used no tool and generated an appropriate two-line message directly.
This demonstrates the full LLM + Tools + Loop structure: the agent
reasoned about each task, selected and used the right tool at the
right time, observed the tool's output, and continued until it reached
a genuine, grounded answer rather than a guess or a fixed script.

### The Challenge Question

I also tested an unplanned question the systems were not designed for:
"I can pay Rs. 30,000. Which two courses can I take together within
this budget?" Note that this question actually refers to the course-fee
scenario's data (courses and rupee amounts in the tens of thousands),
not the library scenario's book codes and small per-day fines — a
mismatch between the question and the system's real data. The
rule-based workflow correctly refused, stating it can only answer
questions about book fines, since no course code pattern was present.
The agent behaved appropriately given this mismatch: rather than
guessing or forcing an answer using the wrong data, it recognized that
its available tools only cover book fines (B101, B202, B303) and not
course fees, and asked me to supply the course names and fees before it
could help. This is a meaningful result in itself — it shows the agent
correctly reasoning about the limits of its own tools rather than
fabricating a plausible-looking course fee answer, which is a safer
failure mode than the chatbot's earlier fabricated library policy.

## 2. Comparison Table

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| Flexibility | Low — cannot ground answers in real data; sometimes fabricates plausible-sounding but false details, sometimes asks for data instead | Very low — only the exact question patterns it was coded for produce an answer | High — correctly handled a lookup, a multi-step calculation, a comparison, and correctly recognized when a question was outside its tools' scope |
| Decision-making | None — generates an answer or asks a question with no way to verify either against real data | Fixed, deterministic if/else logic | Dynamic — the LLM decides which tool(s) to call, in what order, and when it has enough to answer, or that it cannot |
| Tool usage | None | None — no LLM, no tools, direct code logic only | Uses tools (fine lookup, calculator) selected at runtime, called multiple times per question when needed |
| Private-data access | No access — invents plausible details or asks the user to supply data | Full access, but only through hardcoded rules | Full access via tools, usable across question types, and aware of what data it does not have access to |
| Multi-step task handling | Cannot do genuine multi-step reasoning; showed a worked example using invented numbers instead | Only the one multi-step pattern that was coded (total across days) | Handled multi-step questions naturally, including correctly reasoning about a question involving data outside its tool scope |
| Automation | Fully automatic, but sometimes produces confident, fabricated answers | Fully automatic and reliable, but narrow | Fully automatic and correct on every in-scope question tested, and appropriately cautious on an out-of-scope one |
| Reliability | Low — mixed real-sounding fabrication with honest uncertainty in the same run | Very high within scope, zero outside it | High — correct results with visible, verifiable reasoning steps on every question tested |

## 3. Suitability Analysis

Based on what I actually observed, the AI agent is clearly the most
suitable approach for this scenario. The rule-based workflow was fully
reliable for the two question types it was built for, but it rejected
both the comparison question and the harmless reminder-message question
with the same generic error, showing how little room a fixed rule set
leaves for anything unplanned. The plain chatbot was the most
concerning of the three: rather than consistently admitting it lacked
data, it sometimes fabricated specific, plausible-sounding numbers
(such as citing an unrelated public library's fine policy) that could
easily be mistaken for a real answer, which is a genuinely risky
failure mode. The AI agent, by contrast, correctly answered every
question that its tools were built to support, showed its reasoning
steps so the answers could be verified, and — critically — recognized
the limits of its own data when the challenge question referred to
information it did not have access to, asking for that data rather
than guessing at it. This combination of grounded accuracy and
appropriate self-limitation makes it the clear best fit for a scenario
involving real private data that students might actually rely on.

## 4. Conclusion

In general, a plain chatbot is most appropriate for tasks that do not
depend on private or precise data, where a generic answer is acceptable
and there is no real data to get wrong or fabricate. A rule-based
workflow is best suited to a narrow, well-defined, high-stakes task
where every valid input and the required logic are known in advance,
and perfect consistency matters more than flexibility. An AI agent is
the right choice when a task needs access to specific private data, may
involve multiple steps that cannot all be anticipated in advance, and
must be able to recognize the boundaries of its own knowledge and tools
rather than fabricate an answer when data is missing — exactly the
behavior seen when the agent correctly identified that the challenge
question fell outside its available tools. The right choice ultimately
depends on how predictable the task is and how costly a wrong or
fabricated answer would be: narrow, fixed tasks suit rule-based
workflows; low-stakes, data-free tasks suit a plain chatbot; and tasks
combining real data needs with unpredictable phrasing are best handled
by an agent that can reason about, and admit the limits of, what it
actually knows.the program was succesfully completed.