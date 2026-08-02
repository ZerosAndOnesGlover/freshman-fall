# CS 101 Week 0 Reading Guide & Resources

**Week 0: Orientation: What is Computer Science?**

---

## Required Reading This Week

### Primary Text: Guttag (MIT Python Book)

**Chapter 1: "Getting Started"** (Pages 1–14)

Focus on:
- Section 1.1: Computers and their programs
- Section 1.2: Knuth's definition of an algorithm
- Section 1.3: Python as a programming language

Questions to answer as you read:
1. What does Guttag say is the distinguishing characteristic of a "fixed-program computer" vs. a "stored-program computer"?
2. How does Guttag define a "computational process"?
3. What is the difference between a "syntax error" and a "semantic error"?

---

### Supplemental: Turing's Original Paper (Optional but Remarkable)

**Alan Turing, "On Computable Numbers, with an Application to the Entscheidungs problem" (1936)**

Available at: https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf

Read **pages 1–7** only. You do not need to follow every mathematical detail. What to notice:
- How Turing defines a "computing machine" (now called a Turing Machine)
- The informal but precise description of the tape, head, and "m-configurations" (states)
- The audacity of defining all computation with such a simple model

This paper is 89 years old and still defines the foundations of our field. Reading even the first few pages connects you to that history.

---

### Supplemental: History (Optional, Highly Recommended)

**Walter Isaacson, "The Innovators": Chapters 1–2**

Chapter 1 covers Ada Lovelace and Charles Babbage. Chapter 2 covers the invention of modern computing during WWII.

If you want the full picture of *how we got here*, this book is the best accessible history of computing.

---

## Recommended Online Resources

### For Python Basics
- **Official Python Tutorial:** https://docs.python.org/3/tutorial/index.html
  - Start with Sections 1–3 (the interpreter, first steps, informal introduction)
- **Python Tutor (visualization tool):** https://pythontutor.com
  - Paste any Python code and see it execute step by step, with memory visualization
  - **Use this constantly.** It is one of the best learning tools available.

### For Understanding Binary and Types
- **"Binary and Data Representation" — Khan Academy**
  - https://www.khanacademy.org/computing/computer-science/computers-and-internet-intro
- **"Floating Point" — What Every Programmer Should Know**
  - https://floating-point-gui.de/
  - Read: "What Every Computer Scientist Should Know About Floating-Point Arithmetic" (the short version)

### For Git
- **Git Official Documentation:** https://git-scm.com/doc
- **Learn Git Branching (interactive):** https://learngitbranching.js.org/
  - Play through the first 4 levels — it takes 30 minutes and will make Git intuitive

### For Computing History
- **Computerphile (YouTube channel):** https://www.youtube.com/@Computerphile
  - Recommended videos this week:
    - "Turing Machines Explained"
    - "The Church-Turing Thesis"
    - "What is a Turing Machine?"
- **MIT OpenCourseWare — 6.001 "Structure and Interpretation of Computer Programs"**
  - Lecture 1: "Overview and Introduction to Lisp" — Abelson and Sussman at their finest

---

## Turing Machine Simulator

Experience the theory directly:

**Online Turing Machine Simulator:** http://morphett.info/turing/turing.html

Try the following example — a Turing Machine that decides if a string has balanced 0s and 1s:
1. Open the simulator
2. Load the "Palindrome checker" example
3. Run it with a few different input strings
4. Try to read the state table and understand what each rule does

This is what all computation reduces to — simple symbol manipulation by a mechanical rule table.

---

## Environment Setup Resources

If you encounter problems during Lab 0:

### Python Installation
- **Windows:** https://docs.python.org/3/using/windows.html
- **macOS:** https://docs.python.org/3/using/mac.html
- **Linux:** https://docs.python.org/3/using/unix.html

Common issues:
- **"Python not found" on Windows:** You need to add Python to PATH. Reinstall and check the box.
- **"Permission denied" on macOS/Linux:** Never use `sudo pip install` for course packages. Use `python3 -m pip install --user package_name`
- **Multiple Python versions:** Always use `python3` (not `python`) to ensure you're using Python 3

### VS Code Python Setup
1. Install VS Code: https://code.visualstudio.com/
2. Install the Python extension by Microsoft (search "Python" in Extensions)
3. Select your Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter" → choose Python 3.x

### Git Setup
- **First-time Git setup:** https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup
- **GitHub Student Pack (free):** https://education.github.com/pack — get private repos, GitHub Copilot, and more for free with a student email

---

## Week 0 Learning Objectives Checklist

By end of Week 0, you should be able to:

**Conceptual:**
- [ ] Define an algorithm with its three key properties
- [ ] Explain what a Turing Machine is and why it matters
- [ ] State the Church-Turing Thesis
- [ ] Name the key difference between CS, Software Engineering, and Computer Engineering
- [ ] Explain the Von Neumann architecture
- [ ] Know why the Halting Problem matters (even if not yet fully proved)

**Practical:**
- [ ] Open a terminal and navigate the file system
- [ ] Run Python programs from the command line
- [ ] Use the Python REPL for experimentation
- [ ] Create variables, use operators, and perform type conversions in Python
- [ ] Write and run a complete Python program that takes input and produces output
- [ ] Initialize a Git repository, stage files, and make commits
- [ ] Explain the difference between `git add` and `git commit`

---

## Office Hours This Week

Office hours are especially important in Week 0. Installation problems are common. Do not struggle alone for more than 30 minutes: come to office hours.

**Professor:** [See course page for schedule]
**Teaching Assistants:** [See course page for schedule]
**Peer Tutoring Center:** [See course page for location]

---

## What to Expect in Week 1

Week 1 begins the actual course content: data types, variables, and expressions. The material builds on what you learned in Week 0. Make sure you:
1. Have your environment fully working
2. Have completed Lab 0
3. Have read Guttag Chapter 1
4. Have played with the REPL

Week 1's first quiz (Wednesday morning) will cover Week 0 material, so review the self-assessment quiz and make sure you understand all the answers.

---

*CS 101 · Week 0 · Reading Guide · © CSE Department*
