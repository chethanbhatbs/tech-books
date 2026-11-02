"""Chapters 0 to 9 (modules 0 to 3). Every terminal block is produced by engine.run_steps."""
from engine import (CUR, concept, table, demo, rule, lab, exercises, takeaways, source, figure,
                    sbox, sarrow, stext, scircle, sline, GIT_VER)

PAGE = "<!--page-->"
CHAPTERS = []   # (num, slug, title, goal, html)

SRC_PROGIT_WHAT = ("Pro Git 1.3: What is Git?", "https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F")
SRC_PROGIT_HIST = ("Pro Git 1.2: A short history of Git", "https://git-scm.com/book/en/v2/Getting-Started-A-Short-History-of-Git")
SRC_FIRST = ("Git's first commit, on GitHub", "https://github.com/git/git/commit/e83c5163316f89bfbde7d9ab23ca2e25604af290")
SRC_ABOUT = ("GitHub: about", "https://github.com/about")
SRC_DL = ("git-scm.com: downloads", "https://git-scm.com/downloads")
SRC_SWITCH = ("git switch", "https://git-scm.com/docs/git-switch")
SRC_IGNORE = ("gitignore", "https://git-scm.com/docs/gitignore")
SRC_RESET = ("git reset", "https://git-scm.com/docs/git-reset")
SRC_MERGE = ("git merge", "https://git-scm.com/docs/git-merge")


def hide(*cmds):
    return [("h", c) for c in cmds]


CONFLICT = hide("git init -q", "echo 'Open 9am' > hours.txt", "git add .", 'git commit -q -m "Add hours"', "git switch -q -c early",
                "echo 'Open 7am' > hours.txt", 'git commit -q -am "Open early"', "git switch -q main", "echo 'Open 8am' > hours.txt",
                'git commit -q -am "Open at 8"')
MENU = hide("git init -q", "echo Welcome > home.txt", "git add .", 'git commit -q -m "Add home page"', "git switch -q -c menu",
            "echo 'Dosa 60' > menu.txt", "git add .", 'git commit -q -m "Add menu"')


def chapter(num, slug, title, goal, parts):
    CUR["ch"] = num
    CHAPTERS.append((num, slug, title, goal, parts))


def build_chapters():
    """Chapters are built lazily so the rule counter sees the right chapter."""
    out = []
    for num, slug, title, goal, parts in CHAPTERS:
        CUR["ch"] = num
        out.append((num, slug, title, goal, "".join(p() if callable(p) else p for p in parts)))
    return out


# ---------------------------------------------------------------- diagrams
def d_versions():
    s = []
    names = ["report.docx", "report_final.docx", "report_final_v2.docx", "report_FINAL_real.docx"]
    for i, n in enumerate(names):
        s.append(sbox(20, 20 + i * 62, 300, 46, [n], fill="hr", size=17, mono=True))
    s.append(stext(170, 290, "Without Git: which one is right?", size=18, anchor="middle"))
    xs = [420, 560, 700, 840]
    for i, x in enumerate(xs):
        s.append(scircle(x, 120, 34, f"c{i + 1}", fill="hg"))
        if i:
            s.append(sarrow(xs[i - 1] + 36, 120, x - 38, 120))
    for i, (x, t) in enumerate(zip(xs, ["first draft", "add intro", "fix totals", "add chart"])):
        s.append(stext(x, 182, t, size=16, anchor="middle"))
    s.append(sbox(780, 30, 120, 40, ["report.docx"], fill="hn", size=15, mono=True))
    s.append(sarrow(840, 72, 840, 84))
    s.append(stext(640, 290, "With Git: one file, every version kept, each with a note", size=18, anchor="middle"))
    return figure(920, 310, "".join(s), "Left: copies with confusing names. Right: Git keeps one file and remembers every saved version.")


def d_git_github():
    s = [sbox(30, 60, 300, 150, ["Your laptop", "folder + .git", "(Git runs here)"], fill="hy", num=1),
         sbox(590, 60, 300, 150, ["GitHub", "a copy of the repo", "online"], fill="hp", num=2),
         sarrow(335, 110, 585, 110, "git push", curve=16),
         sarrow(585, 170, 335, 170, "git pull / git clone", ly=205, curve=-16)]
    return figure(920, 250, "".join(s), "Git is the program. GitHub is a website that keeps a copy you can share.",
                  legend=["<b>Your laptop:</b> the real work happens here. Git saves snapshots into a hidden <code>.git</code> folder.",
                          "<b>GitHub:</b> holds a copy online. You send snapshots up with <code>push</code> and bring them down with <code>pull</code> (Module 4)."])


def d_three_areas():
    s = [sbox(20, 60, 230, 120, ["Working folder", "the files you edit"], fill="hy", num=1),
         sbox(370, 60, 230, 120, ["Staging area", "the 'ready' tray"], fill="hb", num=2),
         sbox(720, 60, 230, 120, ["Repository", "saved snapshots (.git)"], fill="hg", num=3),
         sarrow(254, 105, 366, 105, "git add", ly=88),
         sarrow(604, 105, 716, 105, "git commit", ly=88),
         sarrow(716, 165, 254, 165, "git restore (copy back)", ly=228, curve=-40, dash=True)]
    return figure(970, 250, "".join(s), "The three places a change moves through.",
                  legend=["<b>Working folder:</b> your normal files. You edit them in any editor.",
                          "<b>Staging area:</b> a list of changes you have picked for the next snapshot. Git calls it the <i>index</i>.",
                          "<b>Repository:</b> every snapshot you have committed, stored in the hidden <code>.git</code> folder."])


def d_states():
    s = [sbox(20, 70, 160, 70, ["untracked"], fill="hn", num=1),
         sbox(280, 70, 160, 70, ["staged"], fill="hb", num=2),
         sbox(540, 70, 160, 70, ["committed"], fill="hg", num=3),
         sbox(800, 70, 160, 70, ["modified"], fill="hy", num=4),
         sarrow(184, 105, 276, 105, "git add", ly=90),
         sarrow(444, 105, 536, 105, "git commit", ly=90),
         sarrow(704, 105, 796, 105, "you edit", ly=90),
         sarrow(880, 142, 360, 142, "git add again", ly=200, curve=-60)]
    return figure(980, 220, "".join(s), "The life of one file. After the first commit it goes round 2 → 3 → 4 → 2.",
                  legend=["<b>Untracked:</b> a new file Git has never saved.", "<b>Staged:</b> picked for the next snapshot.",
                          "<b>Committed:</b> saved, and the same as the last snapshot.", "<b>Modified:</b> changed since the last snapshot, not picked yet."])


def d_chain(branches=None, title="Commits point back to the one before. A branch is a label on one commit."):
    s = []
    xs = [80, 260, 440]
    for i, x in enumerate(xs):
        s.append(scircle(x, 150, 36, f"c{i + 1}", fill="hg"))
        if i:
            s.append(sarrow(x - 38, 150, xs[i - 1] + 38, 150))
    s.append(sbox(385, 30, 110, 44, ["main"], fill="hb", size=17, mono=True, num=1))
    s.append(sarrow(440, 76, 440, 110))
    s.append(sbox(555, 30, 110, 44, ["HEAD"], fill="hy", size=17, mono=True, num=2))
    s.append(sarrow(553, 52, 498, 52))
    return figure(700, 220, "".join(s), title,
                  legend=["<b>main:</b> a branch. It is only a label that points at the newest commit on that line of work.",
                          "<b>HEAD:</b> points at the branch you are on now. Your next commit goes there."])


def d_branch_split():
    s = [scircle(80, 160, 34, "c1", fill="hg"), scircle(240, 160, 34, "c2", fill="hg"),
         scircle(400, 90, 34, "c3", fill="hp"), scircle(400, 230, 34, "c4", fill="hy"),
         sarrow(204, 160, 116, 160), sarrow(366, 100, 272, 145), sarrow(366, 220, 272, 175),
         sbox(470, 66, 120, 44, ["menu"], fill="hp", size=17, mono=True, num=1),
         sbox(470, 208, 120, 44, ["main"], fill="hb", size=17, mono=True, num=2),
         sarrow(468, 88, 436, 90), sarrow(468, 230, 436, 230)]
    return figure(640, 300, "".join(s), "Two branches that both moved on from c2.",
                  legend=["<b>menu</b> got commit c3.", "<b>main</b> got commit c4. Neither branch has the other's work yet."])


def d_ff():
    s = [scircle(80, 120, 32, "c1", fill="hg"), scircle(230, 120, 32, "c2", fill="hg"), scircle(380, 120, 32, "c3", fill="hp"),
         sarrow(196, 120, 114, 120), sarrow(346, 120, 264, 120),
         sbox(170, 20, 120, 42, ["main"], fill="hb", size=16, mono=True, num=1),
         sbox(320, 20, 120, 42, ["menu"], fill="hp", size=16, mono=True, num=2),
         sarrow(230, 64, 230, 86), sarrow(380, 64, 380, 86),
         sarrow(292, 40, 318, 40, "moves", ly=200, dash=True),
         stext(380, 200, "after merge: main slides to c3", size=17, anchor="middle")]
    return figure(560, 220, "".join(s), "Fast-forward: main had nothing new, so Git just slides the main label forward.",
                  legend=["<b>main</b> is behind, with no commits of its own.", "<b>menu</b> is ahead. Merging moves main to the same commit."])


def d_merge3():
    s = [scircle(80, 160, 32, "c1", fill="hg"), scircle(220, 90, 32, "a", fill="hp"), scircle(220, 230, 32, "m", fill="hy"),
         scircle(380, 160, 36, "M", fill="hb"),
         sarrow(190, 100, 110, 148), sarrow(190, 220, 110, 172),
         sarrow(346, 145, 252, 100), sarrow(346, 175, 252, 220),
         stext(470, 165, "merge commit: two parents", size=17)]
    return figure(720, 290, "".join(s), "Both branches moved, so Git makes a new merge commit M that joins them.")


# ---------------------------------------------------------------- Chapter 0
chapter("0", "what", "What is version control?",
        "The problem Git solves, what Git and GitHub are, and where Git came from.", [
    concept("The problem", '''
<p>You write a report. You want to keep the old version before a big change, so you copy it. A week later your folder looks like the left side of the picture below, and nobody knows which file is the real one.</p>'''),
    d_versions(),
    concept("What version control does", '''
<p><b>Version control saves a snapshot of your whole folder each time you ask, with a short note, so you can see or go back to any earlier one.</b></p>
<p>Think of save points in a game. You play, you save, you play on. If things go wrong, you load an old save. Each save point in Git is called a <b>commit</b>.</p>'''),
    table(["It lets you", "In plain words"], [
        ["Go back", "Bring back the file exactly as it was last Tuesday."],
        ["See what changed", "Line by line: what was added, what was removed."],
        ["Know who and why", "Every snapshot has a name, a time and a note."],
        ["Try ideas safely", "Work on a copy of the line of work (a <i>branch</i>), and throw it away if it fails."],
        ["Work together", "Many people change the same project without overwriting each other."],
    ]),
    PAGE,
    concept("Git and GitHub are not the same thing", '''
<p><b>Git</b> is a program on your laptop that takes and keeps the snapshots. <b>GitHub</b> is a website that keeps a copy of your snapshots online so you can back them up and share them.</p>'''),
    table(["", "Git", "GitHub"], [
        ["What it is", "A program you install", "A website (github.com)"],
        ["Where it runs", "Your laptop", "On the internet"],
        ["Works offline?", "Yes", "No"],
        ["Needs the other?", "No. Git works alone.", "Yes. It stores Git repositories."],
        ["Analogy", "A camera", "An online photo album"],
    ]),
    d_git_github(),
    concept("Where Git came from", '''
<p>From 2002 the Linux project used a paid tool called BitKeeper for free. In 2005 that free deal ended, so the Linux developers, and in particular Linus Torvalds (who created Linux), built their own tool. That tool is Git.</p>
<p>They wanted it to be fast, simple in design, good at many parallel branches, fully distributed (every copy has the full history), and able to handle a project as big as Linux.</p>
<p>Git's very first commit was made by Linus Torvalds on 7 April 2005, with the note <code>Initial revision of "git", the information manager from hell</code>.</p>''' + source(SRC_PROGIT_HIST, SRC_FIRST)),
    PAGE,
    concept("Words you will meet", ""),
    table(["Word", "What it means"], [
        ["<b>repository</b> (repo)", "A folder that Git is watching, plus its full history."],
        ["<b>commit</b>", "One saved snapshot, with a note, a name and a time."],
        ["<b>staging area</b>", "The tray where you put changes before you commit them."],
        ["<b>branch</b>", "A separate line of work, so you can try something without touching the main version."],
        ["<b>merge</b>", "Bring the work from one branch into another."],
        ["<b>remote</b>", "A copy of the repo somewhere else, usually on GitHub."],
        ["<b>push / pull</b>", "Send your commits to the remote / bring its commits to you."],
        ["<b>clone</b>", "Download a whole repo, with its history, to your laptop."],
    ]),
    source(SRC_PROGIT_WHAT),
    takeaways(["Version control keeps every saved version of a folder, each with a note.",
               "A <b>commit</b> is one saved snapshot.",
               "<b>Git</b> is the program on your laptop. <b>GitHub</b> is a website that stores a copy.",
               "Git was built in 2005 for the Linux project."]),
    exercises([
        ("think", "Your friend says “I use GitHub, so I don't need Git.” What is wrong with that?",
         "GitHub only stores Git repositories. The snapshots are made by Git on your laptop; GitHub keeps a copy of them."),
        ("think", "You have <code>essay_v3_final.docx</code> and <code>essay_v4.docx</code>. Name two things Git would tell you that these file names cannot.",
         "Any two of: exactly which lines changed between the versions, when each version was saved, who saved it, and the note saying why."),
        ("think", "Can you use Git with no internet connection?",
         "Yes. Git runs on your laptop and keeps the history there. You only need the internet to push to or pull from GitHub."),
    ]),
])

# ---------------------------------------------------------------- Chapter 1
chapter("1", "setup", "Install and set up Git",
        "Check that Git is installed, tell it who you are, and choose the name of your first branch.", [
    concept("Open a terminal", '''
<p>Git is used by typing commands. On a Mac press <b>Cmd + Space</b>, type <b>Terminal</b> and press Enter. On Windows, install Git from git-scm.com and open <b>Git Bash</b>.</p>
<p>In this book a line that starts with <code>$</code> is a command you type. Do not type the <code>$</code>. The lines under it are what Git prints back.</p>'''),
    lambda: rule("Check Git is installed with <code>git --version</code>",
        "<p>This prints the version of Git on your laptop. If you see a version, Git is ready.</p>",
        ok=["git --version"],
        bad=[("!", "git --versoin", "unknown option: --versoin")],
        why="Git only knows its own spellings. A typo in an option makes Git print <code>unknown option</code> and a list of the options it does accept. If instead your terminal says <i>command not found</i>, Git is not installed: get it from git-scm.com/downloads." + source(SRC_DL)),
    lambda: rule("Tell Git your name",
        "<p>Every commit records who made it. <code>git config --global user.name</code> sets the name. <code>--global</code> means “for every repo on this laptop”.</p>",
        ok=['git config --global user.name "Asha Rao"', "git config --global user.name"],
        bad=[("!", "git config --global user.name", None)],
        ok_kw={"config": False}, bad_kw={"config": False},
        why="With a value, the command saves it. Without a value, it reads it back. On a fresh laptop nothing is saved yet, so reading prints nothing and Git ends with an error code (1). It looks like nothing happened; that silence <i>is</i> the answer “not set”."),
    lambda: rule("Put a name with a space inside quotes",
        "<p>The terminal splits what you type at spaces. Quotes keep <code>Asha Rao</code> together as one value.</p>",
        ok=['git config --global user.name "Asha Rao"', "git config --global user.name"],
        trap=(['git config --global user.name Asha Rao', "git config --global user.name"],
              "No error, but Git saved only <code>Asha</code>. The word <code>Rao</code> went to Git as a separate extra argument, not as part of the name."),
        ok_kw={"config": False}, trap_kw={"config": False}),
    PAGE,
    lambda: rule("Tell Git your email",
        "<p>The email is also stored in every commit. Use the same email as your GitHub account, so GitHub can link your commits to you.</p>",
        ok=["git config --global user.email asha@example.com", "git config --global user.email"],
        ok_kw={"config": False}),
    lambda: rule("Name the first branch <code>main</code>",
        "<p>A new repo starts with one branch. Today Git calls it <code>master</code> unless you choose a name, and prints a long hint every time. GitHub and most teams use <code>main</code>.</p>",
        trap=(["git init", "git status"],
              "Not an error, a <b>hint</b>: the repo works, but you are on <code>master</code>, and Git warns that the default will change to <code>main</code> in Git 3.0."),
        ok=["git config --global init.defaultBranch main", "git init", "git status"],
        ok_kw={"config": False}, trap_kw={"config": False},
        why="Setting <code>init.defaultBranch</code> once makes every new repo start on <code>main</code>, and the hint goes away."),
    lambda: rule("See everything you set with <code>--list</code>",
        "<p>Your global settings live in one plain text file in your home folder: <code>~/.gitconfig</code>.</p>",
        ok=['git config --global user.name "Asha Rao"', "git config --global user.email asha@example.com",
            "git config --global --list", "cat ~/.gitconfig"],
        ok_kw={"config": False},
        why="<code>--list</code> shows each setting as <code>section.key=value</code>. The file shows the same settings grouped under <code>[user]</code>. You can edit that file by hand, but the command is safer."),
    PAGE,
    takeaways(["<code>git --version</code> checks Git is installed.",
               "<code>git config --global user.name \"Your Name\"</code>: quotes when there is a space.",
               "<code>git config --global user.email you@example.com</code>: same email as GitHub.",
               "<code>git config --global init.defaultBranch main</code> once, and every new repo starts on <code>main</code>.",
               "All of it lives in <code>~/.gitconfig</code>; see it with <code>git config --global --list</code>."]),
    lambda: lab("Set up Git on your laptop", '''
<p>Type each command in your own terminal and tick it off. Use your own name and email, not Asha's. If you set these up before, running them again just replaces the old values.</p>''', [
        "git --version",
        'git config --global user.name "Asha Rao"',
        "git config --global user.email asha@example.com",
        "git config --global init.defaultBranch main",
        "git config --global user.name",
    ], config=False),
    lambda: exercises([
        ("predict", "A fresh laptop. What does the last command print?",
         ['git config --global user.name Asha', "git config --global user.name"], {"config": False}),
        ("predict", "No quotes this time. What name does Git keep?",
         ['git config --global user.name Ravi Kumar', "git config --global user.name"], {"config": False}),
        ("think", "Why does Git need your email at all?",
         "Every commit stores the author's name and email. GitHub uses the email to link a commit to your account."),
        ("think", "What does <code>--global</code> mean?",
         "The setting applies to every repo on this laptop for your user. It is saved in <code>~/.gitconfig</code>."),
    ]),
])

# ---------------------------------------------------------------- Chapter 2
chapter("2", "first", "Your first repository",
        "Turn a folder into a repo, and save your first snapshot: init, status, add, commit, log.", [
    concept("A repository is a watched folder", '''
<p><b>A repository is a normal folder that Git watches, plus a hidden <code>.git</code> folder where Git keeps every snapshot.</b> Your files stay where they are. Git only adds the <code>.git</code> folder.</p>'''),
    d_three_areas(),
    lambda: rule("Git commands only work inside a repo",
        "<p>Most Git commands look for a <code>.git</code> folder in the current folder or one above it. <code>git init</code> creates it.</p>",
        bad=[("!", "git status", "fatal: not a git repository")],
        ok=["git init", "git status"],
        why="Before <code>git init</code> there is no <code>.git</code> folder, so Git has nothing to read and stops with <code>fatal</code>. After it, <code>git status</code> works and says there are no commits yet."),
    lambda: rule("<code>git init</code> adds a hidden <code>.git</code> folder",
        "<p>Run <code>git init</code> once per project, inside the project folder. <code>ls -a</code> lists hidden files too.</p>",
        ok=["git init", "ls -a"],
        trap=(["git init -q", "echo hi > notes.txt", "git add notes.txt", 'git commit -q -m "Add notes"', "rm -rf .git", ("!", "git log", "fatal: not a git repository")],
              "Deleting <code>.git</code> gives no warning, and every snapshot is gone. Your current files stay, but the history does not. Never delete <code>.git</code>."),
        why="<code>.</code> and <code>..</code> mean “this folder” and “the folder above”. The only thing <code>git init</code> added is <code>.git</code>."),
    lambda: rule("A new file is <i>untracked</i> until you add it",
        "<p><code>echo \"text\" &gt; file</code> creates a file with that text in it. Git sees the new file but does not save it yet.</p>",
        ok=["git init -q", 'echo "Buy milk" > notes.txt', "git status"],
        why="Git never saves a file you did not ask it to. <i>Untracked</i> means “Git sees it, but has never saved it”. That stops junk files from slipping into your history."),
    PAGE,
    lambda: rule("<code>git add</code> puts a file in the staging area",
        "<p>Staging means “I want this in my next snapshot”.</p>",
        ok=["git init -q", 'echo "Buy milk" > notes.txt', "git add notes.txt", "git status"],
        bad=["git init -q", ("!", "git add note.txt", "did not match any files")],
        why="Git now lists the file under <i>Changes to be committed</i>. In the second box the name is misspelt (<code>note.txt</code>); Git cannot find that file, so it stops with <code>pathspec ... did not match any files</code> and stages nothing."),
    lambda: rule("<code>git commit -m</code> saves the snapshot",
        "<p><code>-m</code> is the message: a short note saying what you changed. Each commit gets an ID.</p>",
        ok=["git init -q", 'echo "Buy milk" > notes.txt', "git add notes.txt", 'git commit -m "Add shopping notes"'],
        bad=["git init -q", 'echo "Buy milk" > notes.txt', ("!", 'git commit -m "Add shopping notes"', "nothing added to commit")],
        why="<code>root-commit</code> means it is the first one. <code>1 file changed, 1 insertion(+)</code> says one line was added. In the second box nothing was staged, so the commit is refused: the staging area is empty."),
    lambda: rule("<code>git log</code> shows the history",
        "<p>Newest first. <code>--oneline</code> shows one line per commit with a short ID.</p>",
        ok=["git init -q", 'echo "Buy milk" > notes.txt', "git add notes.txt", 'git commit -q -m "Add shopping notes"',
            'echo "Buy eggs" >> notes.txt', "git add notes.txt", 'git commit -q -m "Add eggs"', "git log", "git log --oneline"],
        bad=["git init -q", ("!", "git log", "does not have any commits yet")],
        why="Each commit shows its full ID, the author, the date and the message. <code>&gt;&gt;</code> adds a line to the end of a file (one <code>&gt;</code> would replace it). A repo with no commits has no history to show, so <code>git log</code> stops with an error."),
    PAGE,
    takeaways(["A repo = your folder + a hidden <code>.git</code> folder holding every snapshot.",
               "<code>git init</code> once per project. Never delete <code>.git</code>.",
               "New files are <i>untracked</i> until <code>git add</code>.",
               "<code>git commit -m \"note\"</code> saves only what is staged.",
               "<code>git status</code> tells you where every file is. Run it all the time."]),
    lambda: lab("Make your first repo", '''
<p>You will make a folder called <code>git-labs/first</code> in your home folder and save two snapshots in it. <code>mkdir -p</code> makes the folder; <code>cd</code> moves into it.</p>''', [
        "mkdir -p ~/git-labs/first",
        "cd ~/git-labs/first",
        "git init",
        "git status",
        'echo "Buy milk" > notes.txt',
        "git status",
        "git add notes.txt",
        "git status",
        'git commit -m "Add shopping notes"',
        'echo "Buy eggs" >> notes.txt',
        "git add notes.txt",
        'git commit -m "Add eggs"',
        "git log --oneline",
    ]),
    lambda: exercises([
        ("predict", "A new folder with one file in it. What does <code>git status</code> print?",
         ["git init -q", 'echo "hello" > hi.txt', "git status"]),
        ("predict", "Now you stage the file. What changes?",
         ["git init -q", 'echo "hello" > hi.txt', "git add hi.txt", "git status"]),
        ("predict", "You forget <code>git add</code>. What happens?",
         ["git init -q", 'echo "hello" > hi.txt', ("!", 'git commit -m "Add hi"', "nothing added")]),
        ("think", "Why does Git not save new files automatically?",
         "So you choose what goes into each snapshot. Folders often hold files you never want saved: passwords, build output, big downloads."),
        ("do", "Delete <code>~/git-labs/first/.git</code>? Only in your head: what would you lose, and what would stay?",
         "You would lose every commit (the history). The files currently in the folder would stay as they are."),
    ]),
])

# ---------------------------------------------------------------- Chapter 3
chapter("3", "loop", "The everyday loop",
        "Edit, check, stage, commit, over and over. Several files at once, and what a commit ID is.", [
    concept("The loop you will repeat all day", '''
<p>1. Edit files. 2. <code>git status</code> to see what changed. 3. <code>git add</code> the changes you want. 4. <code>git commit -m</code>. Back to 1.</p>'''),
    d_states(),
    lambda: rule("A changed file must be added again",
        "<p>After you edit a file that is already saved, Git marks it <i>modified</i>. There is no <code>git update</code>: you use <code>git add</code> again.</p>",
        given="a repo with <code>notes.txt</code> committed.",
        ok=["git init -q", 'echo "Buy milk" > notes.txt', "git add notes.txt", 'git commit -q -m "Add notes"',
            'echo "Buy eggs" >> notes.txt', "git status", "git add notes.txt", 'git commit -m "Add eggs"'],
        why="<code>git add</code> means “put this file's current content in the tray”, not “start tracking”. That is why it is the same command for new and changed files. It lets you pick which changes go into each snapshot."),
    lambda: rule("Stage several files at once",
        "<p>List them, or use <code>.</code> which means “everything in this folder”.</p>",
        ok=["git init -q", "echo a > a.txt", "echo b > b.txt", "echo c > c.txt", "git add a.txt b.txt", "git status --short", "git add .", "git status --short"],
        trap=(["git init -q", "echo menu > menu.txt", "echo 'my password' > secret.txt", "git add .", "git status --short"],
              "<code>git add .</code> took <code>secret.txt</code> too. No error. Always run <code>git status</code> before committing. Chapter 6 shows how to make Git ignore such files."),
        why="<code>A</code> means added to the staging area. <code>??</code> means untracked. <code>--short</code> prints one line per file instead of the long form."),
    lambda: rule("A commit saves only what is staged",
        "<p>If you stage one of two changed files, the commit takes that one. The other stays modified for later.</p>",
        given="a repo with <code>a.txt</code> and <code>b.txt</code> committed.",
        ok=["git init -q", "echo a > a.txt", "echo b > b.txt", "git add .", 'git commit -q -m "Start"',
            "echo a2 >> a.txt", "echo b2 >> b.txt", "git add a.txt", 'git commit -m "Update a"', "git status --short"],
        why="That is how you make small, clear commits: one change, one commit, even when you edited many files. <code> M</code> (space then M) means modified and not staged."),
    PAGE,
    lambda: rule("<code>git commit -a</code> skips <code>git add</code> for tracked files",
        "<p><code>-a</code> stages every file Git already knows that you changed, then commits. <code>-am</code> is <code>-a</code> and <code>-m</code> together.</p>",
        given="a repo with <code>a.txt</code> committed.",
        ok=["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Start"', "echo more >> a.txt", 'git commit -am "Update a"'],
        trap=(["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Start"', "echo more >> a.txt", "echo new > new.txt",
               'git commit -q -am "Update"', "git status --short"],
              "<code>new.txt</code> was left behind. <code>-a</code> only covers files Git already tracks; a brand new file still needs <code>git add</code>."),
        why="Handy for quick commits, but you lose the chance to pick. Use it when every change belongs in the same commit."),
    lambda: rule("Every commit has an ID",
        "<p>The ID is 40 characters of 0-9 and a-f, worked out from the snapshot's content. You only need to type the start of it, at least 4 characters.</p>",
        ok=["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Start"', "echo b > b.txt", "git add .", 'git commit -q -m "Add b"',
            "git log --oneline", "git log -1 --format=%H", "git show --oneline --stat 667e"],
        bad=["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Start"', ("!", "git show 66", "ambiguous argument '66'")],
        why="<code>git log -1 --format=%H</code> prints the full ID of the newest commit. Git accepts any unique start of it, but needs at least 4 characters: <code>66</code> is too short, so Git treats it as a file name and stops. The ID is a checksum (SHA-1), so if any byte of the snapshot changed, the ID would change." + source(SRC_PROGIT_WHAT)),
    lambda: rule("Read <code>git status --short</code>",
        "<p>Two columns: the left one is the staging area, the right one is your working folder.</p>",
        given="a repo where <code>a.txt</code> and <code>b.txt</code> are committed.",
        ok=["git init -q", "echo a > a.txt", "echo b > b.txt", "git add .", 'git commit -q -m "Start"',
            "echo a2 >> a.txt", "echo b2 >> b.txt", "git add b.txt", "echo c > c.txt", "git status --short"],
        why='<code> M a.txt</code>: changed, not staged. <code>M  b.txt</code>: changed and staged. <code>?? c.txt</code>: untracked. A file can even be <code>MM</code>: staged, then changed again.'),
    PAGE,
    concept("Write messages your future self can use", ""),
    table(["Weak", "Better", "Why"], [
        ["<code>test</code>", "<code>Add login test for wrong password</code>", "Says what changed."],
        ["<code>fix</code>", "<code>Fix total when cart is empty</code>", "Says which bug."],
        ["<code>changes</code>", "<code>Rename notes.txt to todo.txt</code>", "One clear action."],
    ]),
    concept("", "<p>A common style: start with a verb, keep it under about 50 characters, and describe what the commit does (“Add”, “Fix”, “Remove”).</p>"),
    takeaways(["Edited a saved file? <code>git add</code> it again.",
               "<code>git add .</code> stages everything here. Check <code>git status</code> first.",
               "A commit takes only what is staged.",
               "<code>git commit -am</code> works for tracked files only.",
               "Commit IDs: type at least the first 4 characters."]),
    lambda: lab("Practise the loop", '''
<p>A new folder for this chapter. You will commit two files separately, even though you changed both.</p>''', [
        "mkdir -p ~/git-labs/loop",
        "cd ~/git-labs/loop",
        "git init -q",
        'echo "Dosa" > menu.txt',
        'echo "9am to 9pm" > hours.txt',
        "git add .",
        'git commit -m "Add menu and hours"',
        'echo "Idli" >> menu.txt',
        'echo "Closed on Monday" >> hours.txt',
        "git status --short",
        "git add menu.txt",
        'git commit -m "Add idli to menu"',
        "git status --short",
        'git commit -am "Add closing day"',
        "git log --oneline",
    ]),
    lambda: exercises([
        ("predict", "You edit a committed file. What does the short status show?",
         ["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Start"', "echo more >> a.txt", "git status --short"]),
        ("predict", "One tracked file changed, one new file. What is left after <code>commit -am</code>?",
         ["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Start"', "echo more >> a.txt", "echo n > n.txt", 'git commit -q -am "Update"', "git status --short"]),
        ("predict", "Staged, then edited again. What does the short status show?",
         ["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Start"', "echo 2 >> a.txt", "git add a.txt", "echo 3 >> a.txt", "git status --short"]),
        ("think", "You fixed a bug and also changed some colours. How do you make them two commits?",
         "Stage only the bug-fix files (<code>git add file1 file2</code>), commit with a bug message, then <code>git add</code> the colour files and commit again."),
        ("think", "Is <code>git commit -m \"test\"</code> a good message? What would be better?",
         "No: it does not say what changed. Something like <code>Add test for empty cart total</code>."),
    ]),
])

# ---------------------------------------------------------------- Chapter 4
chapter("4", "diff", "Seeing what changed",
        "diff, diff --staged, show, log -p and --stat, and the names HEAD and HEAD~1.", [
    concept("Read a diff", '''
<p><b>A diff lists the lines that are different between two versions.</b> Lines starting with <code>+</code> were added, lines with <code>-</code> were removed, and lines with a space did not change (they are there for context).</p>'''),
    lambda: rule("<code>git diff</code> shows changes you have not staged",
        "", given="<code>notes.txt</code> is committed with one line.",
        ok=["git init -q", 'echo "Buy milk" > notes.txt', "git add .", 'git commit -q -m "Add notes"', 'echo "Buy eggs" >> notes.txt', "git diff"],
        why="Compare the working folder with the staging area. <code>--- a/</code> is the old version, <code>+++ b/</code> the new one. <code>@@ -1 +1,2 @@</code> means: old file line 1; new file lines 1 to 2."),
    table(["Line", "Meaning"], [
        ["<code>diff --git a/notes.txt b/notes.txt</code>", "which file"],
        ["<code>index 89b24ec..7bba8c8</code>", "short IDs of the old and new content"],
        ["<code>--- a/...</code> / <code>+++ b/...</code>", "old version / new version"],
        ["<code>@@ -1 +1,2 @@</code>", "where: old line 1, new lines 1 to 2"],
        ["<code>+Buy eggs</code>", "a line that was added"],
    ]),
    lambda: rule("After <code>git add</code>, use <code>git diff --staged</code>",
        "", given="the same change, now staged.",
        trap=(["git init -q", 'echo "Buy milk" > notes.txt', "git add .", 'git commit -q -m "Add notes"', 'echo "Buy eggs" >> notes.txt', "git add notes.txt", "git diff"],
              "Empty. The change did not vanish: plain <code>git diff</code> compares only the working folder with the staging area, and they now match."),
        ok=["git init -q", 'echo "Buy milk" > notes.txt', "git add .", 'git commit -q -m "Add notes"', 'echo "Buy eggs" >> notes.txt', "git add notes.txt", "git diff --staged"],
        why="<code>--staged</code> compares the staging area with the last commit: exactly what your next commit will contain. Check it before every commit."),
    PAGE,
    lambda: rule("<code>git show</code> shows one commit",
        "<p>With no ID it shows the newest commit: the message, then its diff.</p>",
        ok=["git init -q", 'echo "Buy milk" > notes.txt', "git add .", 'git commit -q -m "Add notes"', 'echo "Buy eggs" >> notes.txt', 'git commit -q -am "Add eggs"', "git show"],
        why="This is how you answer “what did that commit actually change?”"),
    lambda: rule("<code>git log --stat</code> and <code>git log -p</code>",
        "<p><code>--stat</code> lists which files each commit changed. <code>-p</code> adds the full diff. <code>-2</code> limits it to the last 2 commits.</p>",
        ok=["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Add a"', "echo b > b.txt", "echo a2 >> a.txt", "git add .", 'git commit -q -m "Add b, extend a"', "git log --stat -2"],
        why="<code>|</code> is followed by the number of changed lines and a little bar of <code>+</code> and <code>-</code>."),
    lambda: rule("<code>HEAD</code> is where you are; <code>HEAD~1</code> is one before",
        "<p><b><code>HEAD</code> is Git's name for the commit you are on now.</b> <code>HEAD~1</code> is its parent, <code>HEAD~2</code> the one before that.</p>",
        ok=["git init -q", "echo 1 > n.txt", "git add .", 'git commit -q -m "One"', "echo 2 >> n.txt", 'git commit -q -am "Two"', "echo 3 >> n.txt", 'git commit -q -am "Three"',
            "git log --oneline", "git show --oneline -s HEAD~1", "git diff HEAD~2 HEAD"],
        bad=["git init -q", "echo 1 > n.txt", "git add .", 'git commit -q -m "One"', ("!", "git show HEAD~5", "unknown revision")],
        why="<code>-s</code> hides the diff. <code>git diff A B</code> compares any two commits. There are not 5 commits before the first one, so <code>HEAD~5</code> does not exist."),
    PAGE,
    d_chain(),
    takeaways(["<code>git diff</code>: changes not staged yet.",
               "<code>git diff --staged</code>: what the next commit will contain.",
               "<code>git show</code>: one commit and its changes.",
               "<code>git log --stat</code> / <code>-p</code>: files changed / full changes.",
               "<code>HEAD</code> = now, <code>HEAD~1</code> = one commit back."]),
    lambda: lab("Look before you commit", '''
<p>Make a change, look at it in both places, then commit.</p>''', [
        "mkdir -p ~/git-labs/diff",
        "cd ~/git-labs/diff",
        "git init -q",
        'echo "Buy milk" > notes.txt',
        "git add .",
        'git commit -q -m "Add notes"',
        'echo "Buy eggs" >> notes.txt',
        "git diff",
        "git add notes.txt",
        "git diff",
        "git diff --staged",
        'git commit -q -m "Add eggs"',
        "git log --oneline --stat",
    ]),
    lambda: exercises([
        ("predict", "One line added and staged. What does plain <code>git diff</code> print?",
         ["git init -q", "echo a > f.txt", "git add .", 'git commit -q -m "A"', "echo b >> f.txt", "git add f.txt", "git diff"]),
        ("predict", "Three commits. What does this print?",
         ["git init -q", "echo 1 > n.txt", "git add .", 'git commit -q -m "One"', "echo 2 >> n.txt", 'git commit -q -am "Two"', "echo 3 >> n.txt", 'git commit -q -am "Three"', "git log --oneline -1 HEAD~2"]),
        ("think", "You want to see exactly what will go into your next commit. Which command?", "<code>git diff --staged</code>."),
        ("think", "A diff line starts with <code>-</code>. What happened to that line?", "It was removed (it is in the old version, not in the new one)."),
    ]),
])

# ---------------------------------------------------------------- Chapter 5
chapter("5", "undo", "Undoing things",
        "Throw away an edit, unstage, fix the last commit, undo a commit safely, and move back in history.", [
    concept("Pick the undo for where the change is", ""),
    table(["The change is…", "Undo it with", "Your edits"], [
        ["edited, not staged", "<code>git restore file</code>", "<b>gone</b>"],
        ["staged", "<code>git restore --staged file</code>", "kept, just unstaged"],
        ["in the last commit (message or a missed file)", "<code>git commit --amend</code>", "kept"],
        ["in a commit you want to cancel, keeping history", "<code>git revert ID</code>", "undone by a new commit"],
        ["in recent commits you want to take back", "<code>git reset --soft / --mixed / --hard</code>", "see Rule 5"],
    ]),
    lambda: rule("<code>git restore file</code> throws away an unstaged edit",
        "<p>It copies the file back from the last saved version.</p>",
        given="<code>notes.txt</code> committed with one line.",
        ok=["git init -q", 'echo "Buy milk" > notes.txt', "git add .", 'git commit -q -m "Add notes"', 'echo "oops" >> notes.txt', "cat notes.txt", "git restore notes.txt", "cat notes.txt"],
        bad=["git init -q", 'echo "Buy milk" > notes.txt', "git add .", 'git commit -q -m "Add notes"', ("!", "git restore note.txt", "did not match any file(s) known to git")],
        why="<code>cat</code> prints a file. The edit was never committed, so Git has no copy of it: <code>restore</code> deletes it for good, with no question asked. The second box misspells the name."),
    lambda: rule("<code>git restore --staged file</code> takes a file out of the tray",
        "<p>The file goes back to <i>modified</i>. Your edit stays.</p>",
        given="a committed file with a staged change.",
        ok=["git init -q", 'echo "Buy milk" > notes.txt', "git add .", 'git commit -q -m "Add notes"', 'echo "Buy eggs" >> notes.txt', "git add notes.txt",
            "git status --short", "git restore --staged notes.txt", "git status --short"],
        bad=["git init -q", 'echo "Buy milk" > notes.txt', "git add notes.txt", ("!", "git restore --staged notes.txt", "could not resolve HEAD")],
        why="<code>--staged</code> copies the file's entry in the tray back from the last commit (<code>HEAD</code>). In a repo with no commits yet there is no <code>HEAD</code> to copy from, so it fails with <code>could not resolve HEAD</code>. Use <code>git rm --cached notes.txt</code> there instead."),
    PAGE,
    lambda: rule("<code>git commit --amend</code> fixes the last commit",
        "<p>It replaces the last commit with a new one. Use it for a typo in the message or a file you forgot to add.</p>",
        given="one commit with a typo in its message.",
        ok=["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Ad file a"', "git log --oneline", 'git commit --amend -m "Add file a"', "git log --oneline",
            "echo b > b.txt", "git add b.txt", "git commit -q --amend --no-edit", "git log --oneline --stat"],
        why="Look at the ID: it changed, because the commit is a new one. <code>--no-edit</code> keeps the message. Only amend commits you have not pushed yet: others may already have the old ID (Module 4)."),
    lambda: rule("<code>git revert</code> undoes a commit with a new commit",
        "<p>Nothing is deleted. Git adds a commit that does the opposite of the one you name.</p>",
        given="two commits; the second added <code>b.txt</code>.",
        ok=["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Add a"', "echo b > b.txt", "git add .", 'git commit -q -m "Add b"',
            "git revert HEAD --no-edit", "git log --oneline", "ls"],
        why="History now says what happened and that it was undone. This is the safe undo for commits other people already have. <code>--no-edit</code> accepts Git's message <code>Revert \"Add b\"</code>."),
    PAGE,
    lambda: rule("<code>git reset</code> moves your branch back",
        "<p><code>git reset HEAD~1</code> takes back the last commit. The option decides what happens to the changes that were in it.</p>",
        given="two commits; the second added <code>b.txt</code>.",
        ok=["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Add a"', "echo b > b.txt", "git add .", 'git commit -q -m "Add b"',
            "git reset --soft HEAD~1", "git status --short", "git log --oneline"],
        trap=(["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "Add a"', "echo b > b.txt", "git add .", 'git commit -q -m "Add b"',
               "git reset --hard HEAD~1", "ls", "git status --short"],
              "<code>--hard</code> took back the commit <b>and</b> deleted <code>b.txt</code> from your folder, with no warning. (Chapter on <code>reflog</code> in Module 7 shows the rescue.)"),
        why="This is how you “uncommit”. Use it only on commits you have not pushed." + source(SRC_RESET)),
    table(["<code>git reset … HEAD~1</code>", "The commit", "Staging area", "Your files"], [
        ["<code>--soft</code>", "taken back", "changes stay staged", "kept"],
        ["<code>--mixed</code> (the default)", "taken back", "changes unstaged", "kept"],
        ["<code>--hard</code>", "taken back", "cleared", "<b>changes deleted</b>"],
    ]),
    lambda: rule("Delete and rename with <code>git rm</code> and <code>git mv</code>",
        "<p>They change the file <i>and</i> stage the change in one step.</p>",
        given="<code>notes.txt</code> and <code>old.txt</code> committed.",
        ok=["git init -q", "echo n > notes.txt", "echo o > old.txt", "git add .", 'git commit -q -m "Start"',
            "git mv notes.txt todo.txt", "git rm old.txt", "git status --short", 'git commit -m "Rename notes, remove old"'],
        why="<code>R</code> means renamed, <code>D</code> deleted. If you delete or rename with Finder instead, it also works: <code>git add .</code> then stages it."),
    PAGE,
    takeaways(["Unstaged edit: <code>git restore file</code> (the edit is gone for good).",
               "Staged by mistake: <code>git restore --staged file</code>.",
               "Last commit wrong: <code>git commit --amend</code>, before you push.",
               "Shared commit wrong: <code>git revert ID</code>.",
               "Take back a commit: <code>git reset --soft HEAD~1</code>. Be careful with <code>--hard</code>."]),
    lambda: lab("Undo four ways", '''
<p>One folder, four mistakes, four undos.</p>''', [
        "mkdir -p ~/git-labs/undo",
        "cd ~/git-labs/undo",
        "git init -q",
        'echo "Buy milk" > notes.txt',
        "git add .",
        'git commit -q -m "Ad notes"',
        'git commit --amend -m "Add notes"',
        'echo "oops" >> notes.txt',
        "git restore notes.txt",
        "cat notes.txt",
        'echo "Buy eggs" >> notes.txt',
        "git add notes.txt",
        "git restore --staged notes.txt",
        "git status --short",
        'git commit -q -am "Add eggs"',
        "git revert HEAD --no-edit",
        "git log --oneline",
    ]),
    lambda: exercises([
        ("predict", "What is left in <code>a.txt</code>?",
         ["git init -q", "echo one > a.txt", "git add .", 'git commit -q -m "One"', "echo two >> a.txt", "git restore a.txt", "cat a.txt"]),
        ("predict", "After a soft reset, what does the short status show?",
         ["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "A"', "echo b > b.txt", "git add .", 'git commit -q -m "B"', "git reset --soft HEAD~1", "git status --short"]),
        ("predict", "And after a plain (mixed) reset?",
         ["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "A"', "echo b > b.txt", "git add .", 'git commit -q -m "B"', "git reset HEAD~1", "git status --short"]),
        ("think", "You committed README.md by mistake and have not pushed. How do you take the commit back but keep the file?",
         "<code>git reset --soft HEAD~1</code> (or <code>git reset HEAD~1</code>). The commit is gone; the file stays."),
        ("think", "A teammate already pulled your bad commit. Reset or revert?",
         "Revert. It adds a new commit, so nobody's history is rewritten."),
    ]),
])

# ---------------------------------------------------------------- Chapter 6
chapter("6", "ignore", "Ignoring files",
        "Keep passwords, logs and build files out of Git with .gitignore.", [
    concept("What .gitignore does", '''
<p><b><code>.gitignore</code> is a text file listing files that Git should act as if it cannot see.</b> Ignored files never show in <code>git status</code> and <code>git add .</code> skips them.</p>'''),
    lambda: rule("List a file in <code>.gitignore</code> and Git stops showing it",
        "", given="a new repo with <code>app.py</code> and a <code>.env</code> file holding a password.",
        ok=["git init -q", "echo 'print(1)' > app.py", "echo 'PASSWORD=1234' > .env", "git status --short", "echo '.env' > .gitignore", "git status --short"],
        why="Before: <code>.env</code> is untracked and would be caught by <code>git add .</code>. After: it disappears from the list. <code>.gitignore</code> itself shows up: commit it, so the rule is saved for everyone."),
    lambda: rule("Patterns: <code>*</code>, folders and <code>!</code>",
        "<p>Each line is one pattern.</p>",
        ok=["git init -q", "mkdir build", "echo x > build/out.bin", "echo e > error.log", "echo k > keep.log", "echo t > todo.txt",
            "printf '*.log\\n!keep.log\\nbuild/\\n' > .gitignore", "cat .gitignore", "git status --short"],
        why="<code>*.log</code>: any file ending in .log. <code>!keep.log</code>: except this one. <code>build/</code>: the whole folder. <code>printf</code> writes several lines at once (<code>\\n</code> is a new line)." + source(SRC_IGNORE)),
    table(["Pattern", "Ignores"], [
        ["<code>.env</code>", "a file named .env, in any folder"],
        ["<code>*.log</code>", "every file ending in .log"],
        ["<code>build/</code>", "the folder build and everything in it"],
        ["<code>!keep.log</code>", "un-ignores keep.log"],
        ["<code># note</code>", "a comment"],
    ]),
    PAGE,
    lambda: rule("Git refuses to <code>add</code> an ignored file",
        "", given="<code>.env</code> is listed in .gitignore.",
        bad=["git init -q", "echo 'PASSWORD=1234' > .env", "echo '.env' > .gitignore", ("!", "git add .env", "ignored by one of your .gitignore files")],
        ok=["git init -q", "echo 'PASSWORD=1234' > .env", "echo '.env' > .gitignore", "git check-ignore -v .env"],
        why="Git stops you adding it by name. <code>-f</code> would force it in; don't, for secrets. <code>git check-ignore -v</code> tells you which line of which file ignores it: here line 1 of .gitignore."),
    lambda: rule("<code>.gitignore</code> does not affect files already committed",
        "<p>To stop tracking a committed file but keep it on disk: <code>git rm --cached</code>.</p>",
        given="<code>app.log</code> was committed before .gitignore existed.",
        trap=(["git init -q", "echo start > app.log", "git add .", 'git commit -q -m "Add log"', "echo '*.log' > .gitignore", "echo more >> app.log", "git status --short"],
              "<code>app.log</code> still shows as modified. Git keeps tracking any file it already has; .gitignore only stops <i>untracked</i> files."),
        ok=["git init -q", "echo start > app.log", "git add .", 'git commit -q -m "Add log"', "echo '*.log' > .gitignore",
            "git rm --cached app.log", "git add .gitignore", 'git commit -q -m "Stop tracking logs"', "echo more >> app.log", "git status --short", "ls"],
        why="<code>--cached</code> means “remove from Git only, not from my folder”. After that commit the file is untracked and ignored: status is empty, and <code>ls</code> shows it is still there."),
    PAGE,
    takeaways(["Put patterns in <code>.gitignore</code> and commit that file.",
               "<code>*.log</code> any .log file, <code>build/</code> a folder, <code>!name</code> an exception.",
               "Ignore secrets (<code>.env</code>) before your first <code>git add .</code>.",
               "Already committed? <code>git rm --cached file</code>, then commit.",
               "<code>git check-ignore -v file</code> says why a file is ignored."]),
    lambda: lab("Hide a secret", "<p>Make a secret file and make sure Git never takes it.</p>", [
        "mkdir -p ~/git-labs/ignore",
        "cd ~/git-labs/ignore",
        "git init -q",
        "echo 'print(1)' > app.py",
        "echo 'PASSWORD=1234' > .env",
        "git status --short",
        "echo '.env' > .gitignore",
        "git status --short",
        "git add .",
        'git commit -q -m "Add app and gitignore"',
        "git log --oneline --stat",
    ]),
    lambda: exercises([
        ("predict", "What does the short status show?",
         ["git init -q", "echo a > a.txt", "echo l > debug.log", "echo '*.log' > .gitignore", "git status --short"]),
        ("predict", "The log was committed first. Now?",
         ["git init -q", "echo l > debug.log", "git add .", 'git commit -q -m "Add log"', "echo '*.log' > .gitignore", "echo m >> debug.log", "git status --short"]),
        ("think", "Should <code>.gitignore</code> itself be committed?", "Yes. Then everyone who clones the repo gets the same rules."),
        ("think", "You pushed <code>.env</code> with a real password last week. Is <code>git rm --cached</code> enough?",
         "No. It stops tracking from now on, but the password is still in the old commits. Change the password."),
    ]),
])

# ---------------------------------------------------------------- Chapter 7
chapter("7", "branches", "Branches",
        "Work on something new without touching main: create, list and switch branches.", [
    concept("What a branch is", '''
<p><b>A branch is a separate line of work: commits you make on it do not change other branches.</b> Inside Git it is tiny: just a label pointing at a commit. When you commit, the label of the branch you are on moves forward to the new commit.</p>'''),
    d_chain(title="A branch is a label on a commit. HEAD shows which branch you are on."),
    lambda: rule("<code>git branch</code> lists branches",
        "<p>The <code>*</code> marks the branch you are on.</p>", given="a repo with one commit.",
        ok=["git init -q", "echo Welcome > home.txt", "git add .", 'git commit -q -m "Add home page"', "git branch"]),
    lambda: rule("<code>git branch name</code> creates a branch but does not move you",
        "", given="a repo with one commit.",
        trap=(["git init -q", "echo Welcome > home.txt", "git add .", 'git commit -q -m "Add home page"', "git branch menu", "git branch"],
              "The branch exists, but the <code>*</code> is still on <code>main</code>. A commit now would go on main, not on menu."),
        why="<code>git branch menu</code> only puts a new label on the current commit."),
    lambda: rule("<code>git switch</code> moves you to a branch",
        "", given="a repo with branches <code>main</code> and <code>menu</code>.",
        ok=["git init -q", "echo Welcome > home.txt", "git add .", 'git commit -q -m "Add home page"', "git branch menu", "git switch menu", "git branch"],
        bad=["git init -q", "echo Welcome > home.txt", "git add .", 'git commit -q -m "Add home page"', ("!", "git switch menus", "invalid reference: menus")],
        why="Switching moves <code>HEAD</code> to that branch. A branch name that does not exist is an <i>invalid reference</i>." + source(SRC_SWITCH)),
    PAGE,
    lambda: rule("<code>git switch -c</code> creates and switches in one go",
        "<p><code>-c</code> means create. This is what you will use most.</p>", given="a repo with one commit on main.",
        ok=["git init -q", "echo Welcome > home.txt", "git add .", 'git commit -q -m "Add home page"', "git switch -c menu"],
        bad=["git init -q", "echo Welcome > home.txt", "git add .", 'git commit -q -m "Add home page"', "git branch menu", ("!", "git switch -c menu", "already exists")],
        why="If the name is taken, Git refuses and changes nothing. Use plain <code>git switch menu</code> to go to an existing branch."),
    lambda: rule("Commits land only on the branch you are on",
        "<p>Your folder shows the files of the branch you are on. Switch, and the files change.</p>",
        given="one commit on main.",
        ok=["git init -q", "echo Welcome > home.txt", "git add .", 'git commit -q -m "Add home page"', "git switch -c menu",
            "echo 'Dosa 60' > menu.txt", "git add .", 'git commit -q -m "Add menu"', "ls", "git switch main", "ls", "git log --oneline --graph --all"],
        why="On main, <code>menu.txt</code> is not in the folder: it only exists on the menu branch. It is safe in Git; switch back and it returns. <code>--graph --all</code> draws every branch."),
    lambda: rule("Git will not switch if it would lose your changes",
        "", given="<code>hours.txt</code> is different on main and on early, and you edited it without committing.",
        bad=["git init -q", "echo 'Open 9am' > hours.txt", "git add .", 'git commit -q -m "Add hours"', "git switch -q -c early", "echo 'Open 7am' > hours.txt",
             'git commit -q -am "Open early"', "git switch -q main", "echo 'Open 8am' > hours.txt", ("!", "git switch early", "would be overwritten")],
        why="Switching would replace your unsaved edit with early's version of the file, so Git stops. Commit the change first (or stash it, Module 6)."),
    PAGE,
    d_branch_split(),
    takeaways(["A branch is a label on a commit; your commits move it forward.",
               "<code>git branch</code> lists, <code>*</code> = where you are.",
               "<code>git switch -c name</code> creates and moves you.",
               "<code>git switch name</code> moves to an existing branch.",
               "Commit before switching, or Git may refuse."]),
    lambda: lab("Build a menu on its own branch", "<p>main stays untouched while you work on the menu.</p>", [
        "mkdir -p ~/git-labs/branches",
        "cd ~/git-labs/branches",
        "git init -q",
        "echo Welcome > home.txt",
        "git add .",
        'git commit -q -m "Add home page"',
        "git switch -c menu",
        "echo 'Dosa 60' > menu.txt",
        "git add .",
        'git commit -q -m "Add menu"',
        "ls",
        "git switch main",
        "ls",
        "git log --oneline --graph --all",
    ]),
    lambda: exercises([
        ("predict", "Which branch has the <code>*</code>?",
         ["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "A"', "git branch idea", "git branch"]),
        ("predict", "You commit on <code>idea</code>, then go back to main. What does <code>ls</code> show?",
         ["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "A"', "git switch -q -c idea", "echo b > b.txt", "git add .", 'git commit -q -m "B"', "git switch -q main", "ls"]),
        ("think", "Is a file lost when you switch away from the branch that has it?",
         "No. It is in that branch's commits. Switch back and it is in your folder again."),
        ("think", "Why create a branch for a new feature instead of working on main?",
         "main stays working while you experiment. If the idea fails, delete the branch; if it works, merge it (next chapter)."),
    ]),
])

# ---------------------------------------------------------------- Chapter 8
chapter("8", "merge", "Merging",
        "Bring a branch's work into main: fast-forward, merge commits, and deleting branches.", [
    concept("Merge means “bring that branch's work into this one”", '''
<p><b><code>git merge name</code> brings the commits from branch <code>name</code> into the branch you are on.</b> So first <code>git switch</code> to the branch that should <i>receive</i> the work (usually main), then merge.</p>'''),
    d_ff(),
    lambda: rule("If main did not move, the merge is a fast-forward",
        "", given="<code>menu</code> has one new commit; main has none.",
        ok=[*MENU, "git switch main", "git merge menu", "git log --oneline"],
        why="<code>Fast-forward</code>: main had nothing new, so Git just moved the main label forward to menu's commit. No new commit is made."),
    lambda: rule("If both moved, Git makes a merge commit",
        "", given="main and menu each have one new commit.",
        ok=[*MENU, "git switch -q main", "echo '9am to 9pm' > hours.txt", "git add .", 'git commit -q -m "Add hours"',
            "git merge menu", "git log --oneline --graph"],
        why="<code>ort</code> is the name of Git's merge method. The new commit <code>Merge branch 'menu'</code> has two parents, which is what the graph shows. Git wrote the message for you (in a real terminal it may open an editor to let you change it; save and close to accept)." + source(SRC_MERGE)),
    PAGE,
    d_merge3(),
    lambda: rule("Merge into the right branch",
        "", given="menu has a new commit; you are still on menu.",
        trap=([*MENU, "git merge main", "git switch -q main", "ls"],
              "You meant “put menu into main”, but you ran it on menu, so you asked to bring main into menu. Nothing to bring: <code>Already up to date.</code> main still has no menu.txt."),
        why="Read <code>git merge X</code> as “bring X <b>here</b>”. Check <code>git branch</code> first."),
    lambda: rule("Delete a merged branch with <code>git branch -d</code>",
        "<p>After merging, the branch label is no longer needed. The commits stay in main.</p>", given="menu was merged into main.",
        ok=[*MENU, "git switch -q main", "git merge -q menu", "git branch -d menu", "git branch"],
        bad=["git init -q", "echo Welcome > home.txt", "git add .", 'git commit -q -m "Add home page"', "git switch -q -c idea", "echo x > x.txt",
             "git add .", 'git commit -q -m "Try idea"', "git switch -q main", ("!", "git branch -d idea", "not fully merged")],
        why="<code>-d</code> refuses to delete a branch whose commits are not merged anywhere, because you would lose them. If you really want to throw the work away, Git's hint tells you: <code>-D</code>."),
    lambda: rule("You can only merge something that exists",
        "", given="a repo with only main.",
        bad=["git init -q", "echo Welcome > home.txt", "git add .", 'git commit -q -m "Add home page"', ("!", "git merge menu", "not something we can merge")],
        why="A typo in a branch name, or a branch that was never created, gives <code>not something we can merge</code>. <code>git branch</code> lists the real names."),
    PAGE,
    takeaways(["Switch to the branch that receives, then <code>git merge other</code>.",
               "Fast-forward: main had nothing new, so its label just moves.",
               "Both moved: Git adds a merge commit with two parents.",
               "<code>git branch -d name</code> after merging; <code>-D</code> throws unmerged work away.",
               "<code>git log --oneline --graph --all</code> shows the shape."]),
    lambda: lab("Merge a feature into main", "<p>Two branches, one merge commit.</p>", [
        "mkdir -p ~/git-labs/merge",
        "cd ~/git-labs/merge",
        "git init -q",
        "echo Welcome > home.txt",
        "git add .",
        'git commit -q -m "Add home page"',
        "git switch -c menu",
        "echo 'Dosa 60' > menu.txt",
        "git add .",
        'git commit -q -m "Add menu"',
        "git switch main",
        "echo '9am to 9pm' > hours.txt",
        "git add .",
        'git commit -q -m "Add hours"',
        "git merge menu --no-edit",
        "git log --oneline --graph",
        "git branch -d menu",
    ]),
    lambda: exercises([
        ("predict", "main has no new commits. What kind of merge is this?",
         ["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "A"', "git switch -q -c f", "echo b > b.txt", "git add .", 'git commit -q -m "B"', "git switch -q main", "git merge f"]),
        ("predict", "Merging main into a branch that already has everything:",
         ["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "A"', "git switch -q -c f", "echo b > b.txt", "git add .", 'git commit -q -m "B"', "git merge main"]),
        ("think", "You want feature <code>login</code> in main. Which branch do you stand on, and which command?",
         "Stand on main: <code>git switch main</code>, then <code>git merge login</code>."),
        ("think", "Why does <code>git branch -d</code> refuse some branches?",
         "Their commits are not merged anywhere, so deleting the label would lose that work. <code>-D</code> forces it."),
    ]),
])

# ---------------------------------------------------------------- Chapter 9
chapter("9", "conflicts", "Merge conflicts",
        "When two branches change the same line, Git asks you to choose. How to read, fix and abort a conflict.", [
    concept("Why conflicts happen", '''
<p><b>A conflict happens when two branches changed the same lines of the same file, so Git cannot know which version you want.</b> Changes in different files, or in different parts of a file, merge on their own.</p>'''),
    lambda: rule("Changes to different lines merge on their own",
        "", given="a file with three lines; main changes line 1, the other branch changes line 3.",
        ok=["git init -q", "printf 'Dosa 60\\nIdli 40\\nVada 30\\n' > menu.txt", "git add .", 'git commit -q -m "Menu"',
            "git switch -q -c prices", "sed -i.bak 's/Vada 30/Vada 35/' menu.txt && rm menu.txt.bak", 'git commit -q -am "Vada price"',
            "git switch -q main", "sed -i.bak 's/Dosa 60/Masala dosa 70/' menu.txt && rm menu.txt.bak", 'git commit -q -am "Masala dosa"',
            "git merge prices --no-edit", "cat menu.txt"],
        why="<code>sed 's/old/new/'</code> replaces text in a file. Both changes are in the result. <code>Auto-merging</code> just means Git combined the file line by line."),
    lambda: rule("Same line changed on both sides: <code>CONFLICT</code>",
        "", given="main says <code>Open 8am</code>, branch early says <code>Open 7am</code>, both changed from <code>Open 9am</code>.",
        bad=[*CONFLICT,
             ("!", "git merge early", "CONFLICT (content)"), "git status"],
        why="The merge stops halfway. Git has put both versions in the file and is waiting for you. <code>both modified</code> marks the file to fix. Nothing is lost."),
    PAGE,
    lambda: rule("Read the conflict markers",
        "", given="the same conflict.",
        ok=[*CONFLICT,
            ("?", "git merge -q early"), "cat hours.txt"],
        why="Everything between <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> and <code>=======</code> is your branch (the one you are on, main). Between <code>=======</code> and <code>&gt;&gt;&gt;&gt;&gt;&gt;&gt; early</code> is the branch you are merging in."),
    table(["Marker", "Means"], [
        ["<code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code>", "start of your version (current branch)"],
        ["<code>=======</code>", "divider"],
        ["<code>&gt;&gt;&gt;&gt;&gt;&gt;&gt; early</code>", "end of their version (the branch being merged)"],
    ]),
    lambda: rule("Fix it: edit, <code>git add</code>, <code>git commit</code>",
        "<p>Edit the file to the text you want, delete all three marker lines, stage it, commit.</p>", given="the same conflict.",
        ok=[*CONFLICT,
            ("?", "git merge -q early"), "echo 'Open 7am' > hours.txt", "git add hours.txt", "git commit --no-edit", "git log --oneline --graph"],
        bad=[*CONFLICT,
             ("?", "git merge -q early"), ("!", 'git commit -m "Done"', "Committing is not possible because you have unmerged files")],
        why="<code>git add</code> is how you tell Git “this file is fixed”. Until then Git will not commit. Here we chose 7am by writing the file again; in real life you edit it in your editor."),
    PAGE,
    lambda: rule("Check for leftover markers before you commit",
        "", given="the same conflict.",
        trap=([*CONFLICT,
               ("?", "git merge -q early"), "git add hours.txt", "git commit -q --no-edit", "cat hours.txt"],
              "Git accepted it. <code>git add</code> marks the file fixed whether or not you fixed it, so the markers are now committed in your file."),
        ok=[*CONFLICT,
            ("?", "git merge -q early"), "git add hours.txt", ("!", "git diff --cached --check", "leftover conflict marker")],
        why="<code>git diff --cached --check</code> looks through what you staged for marker lines and lists each one. If it prints anything, fix the file before committing."),
    lambda: rule("Changed your mind? <code>git merge --abort</code>",
        "", given="the same conflict, before you fixed anything.",
        ok=[*CONFLICT,
            ("?", "git merge -q early"), "git merge --abort", "git status", "cat hours.txt"],
        why="Everything goes back to how it was before <code>git merge</code>. Safe to try again later."),
    PAGE,
    takeaways(["A conflict = both branches changed the same lines.",
               "Between <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> and <code>=======</code> is yours; after it is theirs.",
               "Fix the text, delete the markers, <code>git add</code>, <code>git commit</code>.",
               "<code>git diff --cached --check</code> catches leftover markers.",
               "<code>git merge --abort</code> undoes the whole merge."]),
    lambda: lab("Make and fix a conflict", "<p>You will cause a conflict on purpose. Edit the file in any editor at step 13, or use the echo line given.</p>", [
        "mkdir -p ~/git-labs/conflict",
        "cd ~/git-labs/conflict",
        "git init -q",
        "echo 'Open 9am' > hours.txt",
        "git add .",
        'git commit -q -m "Add hours"',
        "git switch -c early",
        "echo 'Open 7am' > hours.txt",
        'git commit -q -am "Open early"',
        "git switch main",
        "echo 'Open 8am' > hours.txt",
        'git commit -q -am "Open at 8"',
        ("!", "git merge early", "CONFLICT"),
        "cat hours.txt",
        "echo 'Open 7am' > hours.txt",
        "git add hours.txt",
        "git commit --no-edit",
        "git log --oneline --graph",
    ]),
    lambda: exercises([
        ("predict", "Both branches added different files. Conflict?",
         ["git init -q", "echo a > a.txt", "git add .", 'git commit -q -m "A"', "git switch -q -c f", "echo b > b.txt", "git add .", 'git commit -q -m "B"',
          "git switch -q main", "echo c > c.txt", "git add .", 'git commit -q -m "C"', "git merge f --no-edit"]),
        ("predict", "You are mid-conflict and try to commit. What happens?",
         ["git init -q", "echo 1 > x.txt", "git add .", 'git commit -q -m "1"', "git switch -q -c f", "echo 2 > x.txt", 'git commit -q -am "2"', "git switch -q main",
          "echo 3 > x.txt", 'git commit -q -am "3"', ("?", "git merge -q f"), ("!", 'git commit -m "x"', "unmerged")]),
        ("think", "In a conflict, which part is the branch you are on?", "The part between <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> and <code>=======</code>."),
        ("think", "Does <code>git add</code> check that you removed the markers?", "No. It accepts the file as it is. Run <code>git diff --cached --check</code> first."),
    ]),
])
