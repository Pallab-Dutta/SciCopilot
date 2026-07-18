---
title: "How to Proofread a LaTeX Paper Without Breaking Your Equations"
slug: "proofread-latex-without-breaking-equations"
date: 2026-07-18
draft: false
summary: "The usual advice strips the math out before you proofread, so it never gets checked. Here is how to proofread LaTeX in Overleaf, equations left in."
tags: ["LaTeX", "Overleaf", "proofreading", "equations", "scientific-writing", "Benjamin", "SciCoagent"]
categories: ["Benjamin"]
tools: ["proofread", "benjamin"]
agent: "benjamin"
faq:
  - q: "Why do general grammar tools break LaTeX?"
    a: "They read your `.tex` as flat English. A backslash command like `\\cite{}` or a math delimiter like `$` looks like text to them, so they either rewrite it into something that no longer compiles, or they are told to ignore anything code-shaped, which means your equations, units and notation are skipped."
  - q: "Is it safe to paste my paper into an online proofreader?"
    a: "Check the tool's data policy first, especially under double-blind review. Prefer a tool with a clear confidentiality stance, and when in doubt proofread section by section rather than uploading a full identifiable manuscript."
  - q: "How do I keep my equations from being ignored?"
    a: "Use a proofreader that reads LaTeX and reads mathematics, rather than one that asks you to replace `$...$` with placeholders. If you must use a placeholder workflow, at minimum proofread the display equations yourself against the checklist in this post."
  - q: "Does this work with Overleaf?"
    a: "Yes. Download the `.tex` (or the whole project) from Overleaf, run it through a LaTeX-aware proofreader such as Benjamin, then apply the tracked changes or paste the corrected source back into Overleaf."
---

Search for how to proofread a LaTeX paper and you will keep meeting the same advice: take the math out first.

Replace every inline `$...$` with a placeholder like `[MATH1]`. Pull your `\begin{equation}` blocks out of the tool entirely. Proofread what is left, then paste the originals back in. It is careful, sensible advice for keeping your file compiling, and it has one enormous blind spot. At no point in that workflow does anyone read the equations. You have protected the math by promising never to look at it.

For most papers, the equations are the part most likely to be wrong, and the part a reviewer is most likely to catch. So let us do the harder, more useful thing: proofread the LaTeX with the math left in.

## Why generic tools break LaTeX in the first place

A `.tex` file is not prose. It is prose braided together with code and mathematics. A tool built for general English sees `\cite{Feynman1965}` or `\alpha_{ij}` and has no idea it is looking at structure, so it does one of two unhelpful things:

- It "fixes" your markup and you get back a file that will not compile.
- It is configured to skip anything code-shaped, so it silently ignores your equations, your units and your notation.

The placeholder workflow is really a manual version of the second option. It stops the tool from mangling your math by hiding the math from the tool. Compilation survives. The proofreading does not happen.

## A workflow that keeps the equations in

The goal is to proofread all three layers of the manuscript, the prose, the notation and units, and the equations, without ever asking the file to pretend the math is not there.

1. **Export the source, do not retype it.** From Overleaf, use Menu then Source, or download the project as a zip. Keep the real `.tex`, macros and all. The moment you paste rendered text into a box, you have thrown away the structure that makes the errors visible.
2. **Proofread with a LaTeX-native, science-aware tool.** Use a proofreader that parses `.tex` and reads mathematics, so commands and environments stay intact and the equations are actually examined. This is the step where the placeholder crowd quietly gives up, and it is the whole reason [Benjamin](/blog/latex-proofreader/) exists.
3. **Review the changes, do not auto-apply them.** Insist on tracked changes: a clean copy plus a list of edits you accept or reject one line at a time. You want to see the reasoning on an equation edit, not have your source rewritten under you.
4. **Round-trip back into Overleaf.** Paste the corrected source back, or apply the tracked changes, and recompile. Because the structure never left, this is a paste, not a reconstruction.

## What to check inside the math

If you are proofreading the equations by hand, or sanity-checking a tool that claims it did, this is the checklist that catches the errors that get papers returned:

- **Indices and ranges.** Does a sum over $i \neq j$ secretly double count pairs when you meant $i < j$? Do your limits match the text?
- **Units and dimensions.** Is every quantity dimensionally possible? A diffusion coefficient in $\mathrm{m/s}$ is a red flag, because it should be area over time, $\mathrm{m^2/s}$.
- **Roman versus italic.** An upright `d` is a differential operator, an italic $d$ is a variable. Same letter, different physics.
- **Operators wearing costumes.** An epsilon $\varepsilon$ standing in for an "element of" $\in$, a stray dot that turned a product into a time derivative.
- **Notation drift.** The symbol you defined on page 2 still means the same thing on page 12, and two quantities are not sharing one letter.

Here is the kind of correction that should come back, shown as a diff you can read rather than a silent rewrite:

```diff
- \kappa = 1.38 \times 10^{-23}\,\mathrm{J/K}   % "kappa" for Boltzmann?
+ k_B = 1.38 \times 10^{-23}\,\mathrm{J/K}       % conventional symbol, no collision later

- D = 2.3 \times 10^{-9}\,\mathrm{m/s}
+ D = 2.3 \times 10^{-9}\,\mathrm{m^2/s}         % diffusion coefficient is area/time
```

None of that is a spelling mistake. None of it would be flagged by a tool reading the prose. All of it changes what the paper says.

## The point of keeping the math in

The placeholder trick is not wrong, it is just aimed at the wrong goal. It optimizes for "the file still compiles" when the goal you actually care about is "the science is right." Those are not the same target, and the gap between them is precisely the set of errors that survive to peer review.

If your equations are worth writing, they are worth reading. Proofread the paper with the math left in, and give the hardest layer to a proofreader who was built to read it. For the full picture of what that means, see the [pillar guide on AI proofreading for LaTeX](/blog/posts/ai-proofreader-for-latex/), or hand your next draft straight to [Benjamin](https://benjamin.scicoagent.com) and let him read the science, not just the spelling.
