# Writing Clear Tasks

Read this file when a task is hard to understand, too large, or in the wrong
place.

## Contents

- What the labels mean
- A good task
- When to split a task
- Linking and carrying out tasks
- Phases and feedback
- Common problems
- Org rules

## What the labels mean

| Label | Meaning |
|---|---|
| Known | Checked against the current files, system, or other current source |
| Older information | Was true before, but has not been checked now |
| Assumption | Used for now, but still needs checking |
| Idea | A suggested future choice |
| Question | A choice that needs an owner |

Put an unanswered Question before every task that needs its answer.

## A good task

#+begin_src org
** TODO Add a safe sign-in check
:PROPERTIES:
:ID: PLAN-020
:SIZE: M
:DEPENDS: PLAN-010
:OWNER:
:END:

Result:

- Every request is tied to one verified user.

Steps:

- [ ] Check the request before loading private data.
- [ ] Reject unknown or disabled users.

Proof:

- [ ] Tests for a valid user and an invalid user.

Done when:

- [ ] A valid user can continue.
- [ ] An invalid user cannot read private data.
#+end_src

The four parts answer:

- Result: what changes?
- Steps: what should be done?
- Proof: what will we inspect?
- Done when: what clearly passes or fails?

"Tests pass" is not enough. Say what the tests prove.

## When to split a task

Split it when:

- different people can do the parts;
- one part can fail without the other;
- the parts need different proof;
- research and a risky change are mixed together;
- the title joins unrelated work with "and."

Keep it together when the parts form one short test-and-fix loop or only make
sense as one complete change.

Use simple sizes:

- S: one small, clear area;
- M: several related changes;
- L: several areas or failure cases;
- XL: too large to start without checking whether it should be split.

## Linking tasks

=DEPENDS= means the earlier task creates something this task truly needs.
It does not mean "we would rather do this first."

Good links:

- decide before building;
- create shared basics before using them;
- prove safety before a risky move;
- prove backup and restore before deleting old data;
- build one real example before adding many versions;
- practice undoing the change before putting it live.

Work done at the same time should meet at a shared phase check. Do not add
links merely to force teams into a preferred calendar order.

## Carrying out a task

Take the first task whose required earlier work is done. Check each step while
doing it and attach the named proof.

If the approach keeps failing, do not keep repeating it merely because it is in
the plan. Record the failure, check what changed, and revise or replace the
remaining tasks.

## Phases and feedback

A phase should leave the project in a clearly better or safer state.

Each phase needs:

1. A result.
2. An =Expected= line written before the work starts.
3. Tasks that create the result.
4. A =Phase N check= that tests the combined result against =Expected=.
5. Feedback about what happened and what changes next.
6. Later tasks linked to that check.

Use this shape:

#+begin_src org
Expected:

- {{WHAT_SHOULD_BE_TRUE_IF_THE_PLAN_IS_RIGHT}}

Feedback:

- What happened: {{ACTUAL_RESULT}}
- Difference from expected: {{GAP_OR_NONE}}
- Why: {{CAUSE_OR_NONE}}
- What we learned: {{LEARNED}}
- Changes to remaining tasks: {{PLAN_CHANGES}}
#+end_src

Write =Expected= while it is still a prediction; if it is written after the
result, it checks nothing. The gap between =Expected= and what happened sets
the depth of the replan: a surprise means reconsidering all unfinished work, a
match means confirming it still fits and saying why.

End every =Replan= with a premortem line: assume the next phase has already
failed and name the most likely cause. When that cause is worth removing now,
add or change the work that removes it.

Do not write a diary. Record feedback when it changes what is known, changes
the remaining work, or gives a useful lesson for another project.

Useful order for many plans:

1. Answer questions that stop later work.
2. Learn what is true now.
3. Build the shared basics.
4. Prove one real example from start to finish.
5. Cover the remaining cases.
6. Practice moving existing work and undoing the change.
7. Make the live change in small steps.
8. Run the final check and name who owns the result.

Change this order when the work requires it.

## Common problems

### Many boxes, no result

Add Result and Done when. Remove steps that do not help reach either.

### Phases named after teams

"Backend," "Frontend," and "Operations" often hide the real order. Name phases
after a result or reduced risk. Use tags to show who is involved.

### A hidden choice

If a task quietly chooses who can use something, where information lives,
safety rules, cost, or how old work moves to the new system, move that choice
into an earlier Question.

### A risky move too early

Place separation, backup, restore, and proof that the change can be undone
before a live move or deletion.

### A broad system before one real example

Build one full example first. Add more cases only after it works.

### Weak finish line

Replace "support X," "handle errors," or "tests pass" with a good case, bad
case, failure case, recovery case, and named proof.

### Feedback with no effect

If feedback changes what is known or shows that an approach is weak, update the
remaining tasks before continuing. Do not file the feedback and then follow the
old plan.

### An old plan

Keep stable IDs, cancel old tasks with a reason, update task links, and check
the full plan again.

## Org rules

Use:

#+begin_src org
#+STARTUP: overview
#+TODO: TODO(t) NEXT(n) BLOCKED(b@) REVIEW(r) | DONE(d!) CANCELLED(c@)
#+end_src

Use these properties:

#+begin_src org
:PROPERTIES:
:ID: PLAN-020
:SIZE: M
:DEPENDS: PLAN-010
:OWNER:
:END:
#+end_src

- Keep IDs stable and unique.
- Give phase headings IDs too.
- Separate several task links with spaces.
- Use tags for filtering, not for task order.
- Mark old work CANCELLED and say why.
- Keep the user's wording in the Final check where possible.
