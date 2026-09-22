# Comparing a Chatbot, Rule-Based Workflow, and AI Agent — College Fee Scenario

## Scenario

A college has three courses with fee data that no public LLM has seen:
CS101 = Rs. 12,000, AI202 = Rs. 18,000, and DS303 = Rs. 15,000. Three
systems were built to answer the same set of questions about these
fees: a plain chatbot, a rule-based workflow, and an AI agent.

## 1. Explanation of Each Approach

### Plain Chatbot

The chatbot sends the user's question straight to a large language
model, with no access to the college's private fee data and no tools.
When I ran it, the model did not wait ot hallucinate specific wrong numbers —
instead, for every question that depended on the fee data, it asked me
to provide the missing information (for example, asking which
institution AI202 belonged to, or asking for the original tuition
amounts before it could calculate a scholarship). This is actually one
of the two acceptable behaviors for a chatbot lacking data: either it
guesses confidently and wrongly, or it admits it doesn't have the
information and asks for it. My model chose the second, safer
behavior. It did answer the fourth question — a generic welcome
message — well, since that required no private data. This shows the
core limitation of a plain chatbot: it provides responses using an LLM
alone, with nothing to ground it in real data, so it either fabricates
an answer or has to stop and ask.

### Rule-Based Workflow

The rule-based workflow uses no LLM at all. It is a fixed Python
program that finds a course code in the question with a pattern match,
looks up the fee in a hardcoded dictionary, and applies a small set of
if/else rules. When I ran it, it correctly and instantly answered the
direct fee lookup (Rs. 18,000 for AI202) and the total-fee-with-
scholarship question (Rs. 27,000). It failed on the comparison question
("Is DS303 more expensive than CS101, and by how much?") and on the
welcome-message question, both falling back to the same generic
"Sorry, I can only answer questions about course fees" message, because
no rule existed to handle either case. This demonstrates the defining
trait of a rule-based workflow: it follows predefined steps and
conditions with zero reasoning ability, making it fully reliable inside
its coded scope but unable to do anything outside it — even a question
like the welcome message, which needs no data at all, still gets
rejected because it doesn't match any rule.

### AI Agent

The AI agent combines a large language model with two tools
(get_course_fee and calculator) inside a reasoning loop. For every
question, it reasons about what it needs, decides whether to call a
tool, observes the tool's result, and repeats until it can answer. In
my run, the agent called get_course_fee once for the direct lookup,
called it twice and then used calculator for the scholarship question
(returning exactly Rs. 27,000), and called it twice again plus
calculator for the comparison question (correctly finding DS303 costs
Rs. 3,000 more than CS101) — a question the rule-based workflow could
not handle at all. For the welcome-message question, it correctly used
no tool and answered directly. I also ran the extra challenge question
("I can pay Rs. 30,000, which two courses can I take together?"), which
neither the chatbot nor the workflow could really solve. The agent
checked all three possible course pairs using the calculator tool and
correctly identified that both CS101+AI202 (exactly Rs. 30,000) and
CS101+DS303 (Rs. 27,000) fit the budget, while AI202+DS303 (Rs. 33,000)
did not. This demonstrates the full LLM + Tools + Loop structure of an
agent: reasoning about the task, selecting and using the right tools,
observing their results, and continuing to act until the task is
genuinely finished, rather than stopping at the first fixed rule or
guessing an answer.

## 2. Comparison Table

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| Flexibility | Low — cannot answer data questions without more input from the user | Very low — only the exact question patterns it was coded for work | High — handled a direct lookup, a calculation, a comparison, and an unplanned multi-step question |
| Decision-making | None — asks for missing data or answers directly, with no verification | Fixed, deterministic if/else logic | Dynamic — the LLM decides which tool(s) to call, in what order, and when it has a final answer |
| Tool usage | None | None — no LLM, no tools, just direct code | Uses tools (fee lookup, calculator) selected at runtime, called multiple times per question when needed |
| Private-data access | No access — must ask the user for the data itself | Full access, but only through hardcoded rules | Full access via tools, usable across many different question types |
| Multi-step task handling | Cannot do genuine multi-step reasoning | Only the one multi-step pattern that was coded (total with scholarship) | Handled multi-step questions naturally, including the unplanned challenge question requiring three lookups and multiple calculator calls |
| Automation | Fully automatic, but often stalls waiting for the user to supply data | Fully automatic and reliable, but narrow | Fully automatic and correct across every question I tested, including the challenge |
| Reliability | Safe but unhelpful on data questions — it does not hallucinate, but also cannot answer | Very high within scope, zero outside it | High in my run — correct on all four standard questions and the challenge question |

## 3. Suitability Analysis

Based on what I actually observed, the AI agent is the most suitable
approach for this scenario. The rule-based workflow was completely
reliable for the two question types it was built for, but it rejected
both the comparison question and the welcome-message question with the
exact same generic error, even though the welcome message needed no
data at all — this shows how rigid a fixed rule set really is in
practice. The plain chatbot behaved more safely than I expected,
choosing to ask for missing data rather than invent numbers, but this
means it still could not actually answer any of the fee questions on
its own; it simply shifted the burden back onto me. The AI agent was
the only system that correctly handled every question I tested,
including the challenge question that none of the other two systems
were designed for. It found both valid course combinations within the
Rs. 30,000 budget by actually reasoning through the possible pairs
using its tools, rather than relying on a single hardcoded rule. Its
only real weakness, going by the criteria in the table, is that its
steps and exact wording could vary on a repeat run, which is a
reasonable tradeoff for the reliability and flexibility it delivered.

## 4. Conclusion

In general, a plain chatbot is most appropriate for tasks that don't
depend on private or precise data, where a generic or safely-cautious
answer is acceptable — such as open-ended writing or requests where
asking a clarifying question is a fine outcome. A rule-based workflow
is best suited to a narrow, well-defined, high-stakes task where every
valid input and the required logic are known in advance and perfect
consistency matters more than flexibility, such as a fixed fee
calculation used by a finance office. An AI agent is the right choice
when a task needs real private data, may involve multiple steps that
cannot all be anticipated ahead of time, and has to handle question
types the original programmer never planned for — exactly what
happened with the challenge question in this lab. The right choice
ultimately depends on how predictable the task is in advance: narrow,
fixed tasks suit rule-based workflows; open-ended tasks without real
data needs suit a plain chatbot; and tasks that combine real data
requirements with unpredictable phrasing or multi-step reasoning are
best handled by an AI agent.