# Git From Zero - a hands-on Git and GitHub book

A beginner-first Git book in one HTML file. Every rule shows a command that **works**, one that **breaks** with Git's **exact message**, and **why**. Each chapter ends with a **hands-on lab** you type in your own terminal: paste your output and the page checks it against the book (commit IDs, dates, names and paths ignored).

Every output on the page was produced by really running Git when the book was built. The build stops if a command that should work fails, or a command that should break prints a different error than the text says.

*Part 1 (modules 0 to 3, chapters 0 to 9) is done. Part 2 (GitHub, teamwork, rewriting history, advanced) comes next.*

## Read it

```bash
cd git-course
python3 -m http.server 8790
# open http://127.0.0.1:8790/git-course.html
```

Or double-click `git-course/git-course.html`.

## Part 1

| Module | Chapters |
|---|---|
| 0 · Foundations | 0 What is version control? · 1 Install and set up Git |
| 1 · First repo | 2 Your first repository · 3 The everyday loop |
| 2 · See and undo | 4 Seeing what changed · 5 Undoing things · 6 Ignoring files |
| 3 · Branches | 7 Branches · 8 Merging · 9 Merge conflicts |

Plus a chapter quiz for every chapter, a mixed test per module, a cheat sheet and a revision sheet.

## Build

```bash
cd git-course
python3 build.py
```

- `engine.py` runs every command in a throwaway home folder with a fixed author and clock, so commit IDs are the same on every build.
- `chapters.py` is the content, `bank.py` the quizzes, cheat sheet and revision sheet, `styles.py` the CSS and JS.

Light by default, with a dark mode switch. Git logo by Jason Long, CC BY 3.0.
