# self-replanning mode

<div align="center">
    <img src="./assets/img.png" width="300" />
</div>

Replan a plan that has been planned, then plan to replan it when everything goes exactly as unplanned.

OR A skill for creating, carrying out, and replanning clear plans.

It works in a loop:

1. Understand the problem.
2. Make a plan.
3. Carry out the plan and check each step.
4. Replan all unfinished work from phase evidence, validate it, and continue.

The generated plan records current facts, open questions, task order, proof,
phase feedback, whole-future replans, and a final check against the original
request. By default, it lives in the repository root and is added to
`.git/info/exclude`.

## Tests

```bash
python3 tests/run.py            # run
python3 tests/run.py --update   # regenerate the .stdout files
```

## Install / Update

```bash
# Install skill
npx skills add bekerk/self-replanning-mode

# Update skill
npx skills update self-replanning-mode
```

## References

- Pólya, G. (1988). How to solve it: A new aspect of mathematical method.
