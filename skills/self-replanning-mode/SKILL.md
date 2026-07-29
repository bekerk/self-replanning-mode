---
name: self-replanning-mode
description: "Create and execute adaptive plans for large or uncertain work. Use when the user asks for a step-by-step plan, roadmap, implementation or migration plan, task list, or .org file, or wants to carry out or revise one. Verify each phase, reconstruct all unfinished work from current evidence, validate the revised plan, and continue when authorized."
---

# Work Through a Self-Replanning Org Plan

Make one Org file that shows:

- what needs to change;
- why the work is in this order;
- what is still unknown;
- how to prove each task is done;
- what was learned while doing the work;
- how that evidence changed the whole unfinished plan.

This records useful reasons and proof, not private chain-of-thought.

Work in a loop:

1. Understand the problem.
2. Make a plan.
3. Carry out the plan.
4. Replan all unfinished work from the evidence and continue.

The plan is a working record, not a fixed prediction. After every phase check,
reconsider every unfinished question, phase, task, dependency, and proof. Keep
the past intact, reconstruct the future from current evidence, validate it,
and continue when the user asked for execution.

## Choose what to do

- If the user asks for a plan, write all four parts into the Org file, validate
  it, and hand it over. Do not carry out the planned work.
- If the user asks to carry out a plan, take the first ready task, check each
  step, record proof, complete the phase check, replan all unfinished work,
  validate it, and continue from the first ready task.
- If the user asks to revise a plan, check what changed, keep IDs for tasks that
  still mean the same thing, reconstruct all unfinished work, and validate it.

## Output

Start from =assets/execution-plan.org=. Change it to fit the work; do not keep
sections that add no value.

Unless the user specifies otherwise, write =<goal-name>-execution-plan.org= in
the repository root and add it to =.git/info/exclude=.

Do not write an ADR, PRD, issue set, or Markdown plan unless the user asks for
one.

The Org file must include:

- the goal, rules, current facts, and open questions;
- the order of work, phases, first ten tasks, and a before-and-after map;
- =Result=, =Steps=, =Proof=, and =Done when= for every task;
- a check at the end of each phase with =Expected=, =Feedback=, and =Replan=;
- a final check covering every user request.

## 1. Understand the problem

Read every source named by the user. Check the current files, system, or other
current source before trusting an old plan or summary.

Ask:

- What is the user asking for?
- Can the problem be restated in plain language?
- What is known, unknown, required, or forbidden?
- Is there enough current information?
- Do any facts or requests disagree?

Label important statements:

- =Known=: checked now.
- =Older information=: true before, but not checked now.
- =Assumption=: useful, but not yet checked.
- =Idea=: a suggested future choice.
- =Question=: someone must decide before related work can start.

Done when every user request is listed, every important statement has the
right label, and ideas are not presented as facts.

## 2. Make the plan

For every user request, record:

- what is true now;
- what should be true;
- which task closes the gap;
- what proof will show it is closed.

Put this information in the current-state section, the before-and-after map,
and the final check. Do not write a diary of the reasoning process.

Before inventing a new approach, check whether a related example, an earlier
solution, a smaller version of the problem, or working backward makes the plan
clearer.

Put the work in a safe order:

- unanswered questions before work that depends on them;
- shared basics before work that uses them;
- safety checks before risky changes;
- one real example from start to finish before using it more widely;
- backup and restore checks before deletion;
- practice putting the change live and undoing it before the real change.

Use task IDs to show these links. The order must not contain a loop.

Split a task when different people can do the parts, one part can fail alone,
or each part needs different proof. Keep a short test-and-fix loop together.

Write =Expected= in every phase check while the plan is still a prediction:
what should be true after the phase if the plan is right. The phase review
compares the result against this line, so it must be written before the work,
not after.

Use the Org states and task fields from the template. Read
=references/clear-tasks.md= when tasks feel vague, too large, or badly ordered.

Done when every request appears in a task and the final check, every task has a
unique ID and all four fields, every phase check states its =Expected= outcome,
the links contain no loop, and no risky step comes before its safety proof.

## 3. Carry out the plan

When the user asks to do the work:

- take the first task whose required earlier work is done;
- follow its steps with care;
- check each step and attach the named proof;
- keep unrelated user work unchanged;
- mark the task DONE only when its =Done when= conditions pass.

If a step fails, fix it and check again. If the chosen approach keeps failing
or new facts show it is wrong, stop following it blindly. Record what happened,
change or replace the remaining plan, and continue from the first ready task.

Passing tasks is not permission to skip replanning. At the end of every phase,
follow the full review and replan in the next section even when the approach
appears to be working.

Done when each completed task has current proof and the Org file still matches
the real situation.

## 4. Replan the unfinished work

End each phase with a =Phase N check=. It must test the combined result, not
merely ask whether its tasks were marked DONE.

Before writing =Feedback= or =Replan=, synchronize the plan's present tense:

- update =What is true now= with the phase evidence;
- update, resolve, or remove affected =Open questions=;
- remove statements that still describe completed proof as missing;
- check that task and phase states agree with the current facts.

Each phase check must include =Feedback:= comparing the result with the
=Expected= line written before the phase:

- What happened?
- How does it differ from what was expected?
- Why is there a difference?
- What did we learn?
- Which facts, questions, or remaining tasks must change?

Then write =Replan:= that accounts for the whole unfinished plan:

- keep the original goal, user requests, and rules unless the user changes
  them;
- preserve completed work, its proof, and cancellation reasons as history;
- let the gap set the depth: when the result differs from =Expected=,
  reconsider every unfinished question, phase, task, dependency, order, and
  required proof, including work not directly affected by the last phase;
  when the result matches =Expected=, confirm that the unfinished plan still
  fits the evidence and record why it stands;
- record what was kept, changed, added, or cancelled and name the next ready
  task;
- answer the premortem: assume the next phase has already failed and name the
  most likely cause; when that cause is worth removing now, add or change the
  work that removes it;
- keep an ID when the task still means the same thing; use a new ID when its
  meaning changes materially;
- rebuild the unfinished order and dependencies, then validate the Org file.

Do not force a change merely to make the replan look active. When the result
matches =Expected=, still record that the unfinished work was reconsidered and
why it fits the current evidence.

When the user asked for execution, continue automatically from the first ready
task after validation. Pause when the new plan requires a user decision, wider
scope, greater risk or cost, a destructive action, or authority not already
given. Cancel or replace obsolete work; do not preserve an outdated plan for
appearance's sake.

State consistency is part of the proof. Do not mark a phase check or final
check DONE when:

- its current-facts section contradicts completed evidence;
- a resolved question still appears open;
- an active or BLOCKED task is required by that check's =Done when= conditions.

When unresolved work is outside the completed scope, record it explicitly as
a non-blocking follow-up with its owner and reason; do not present it as a
blocker to work already declared complete.

End the whole plan with a =Final check=. Repeat every original request, name
the proof that shows it was met, and record what should be reused or changed
next time. Missing, old, partial, or indirect proof means the request is not
done.

Done when current facts and open questions match the evidence, every unfinished
item is accounted for in =Replan=, task states do not contradict completed
checks, the revised plan passes validation, and later work depends on a passed
phase check.

## Check the file

Resolve paths from the folder containing this =SKILL.md=. Run:

#+begin_src bash
python3 scripts/validate_org_plan.py --strict PATH_TO_PLAN.org
#+end_src

If Emacs is available, run:

#+begin_src bash
python3 scripts/validate_org_plan.py --strict --emacs-lint PATH_TO_PLAN.org
#+end_src

Fix every error and warning. Done when IDs and task links are valid, every
phase has a check with =Expected=, =Feedback=, and =Replan=, every task has all
four fields, the final check exists, and Org lint passes when available.

## Hand over the plan

Link the Org file. State the number of phases and tasks, the main order, open
questions, checks run, and the first tasks to start.

If the user asked only for a plan, do not say the planned work is complete.
Only the plan is complete.

## Improving this skill

After using the skill, notice whether:

- the user corrected the order or structure;
- work exposed a missing earlier task;
- a task was too vague to start;
- a phase check passed without proving enough;
- feedback did not change a plan that was clearly wrong;
- the validator missed a clear problem.

Finish the user's work first. Only turn a lesson into a general rule when it is
likely to help on other projects. Test it against a real plan when possible.
Propose the exact change and wait for approval before editing this skill.

#+begin_example
Skill update proposal:
  File: <file to change>
  Trigger: <what went wrong>
  Tested: yes (<proof>) | no (<reason>)
  Removes content: no | yes
  Change: <exact change>
#+end_example
