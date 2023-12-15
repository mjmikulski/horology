# Dear Contributor!

I am happy that you think about contributing to this project. This is a good idea, keep reading!

## How can I contribute?
1. Propose new features.
2. Report or fix bugs.
3. Develop the code.
4. Create documentation.
5. Promote horology :heartpulse:

## How to report a bug or propose a new amazing feature?
Create an issue. 

## How to commit some code?
1. [Fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) horology.
2. Create a branch.
3. Create virtual env with conda using latest version of supported python, e.g.:
    ```bash
    conda create -n horology python=3.12
    conda activate horology
    ```
4. Install poetry using pip:
    ```bash
    pip install poetry
    ```
5. Use poetry to install all dev dependencies:
    ```bash
    poetry install
    ```
6. Write some useful and beautiful code that follows [PEP8](https://www.python.org/dev/peps/pep-0008/).
7. Write unit tests.
8. Run mypy and pytest and fix eventual errors:
    ```bash
    mypy .
    pytest
    ```
9. Commit and push your changes (in your fork).
10. [Create a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) 
from your fork to horology.
11. Wait for my feedback.
12. If I accept your changes, I will merge them into the master branch and release with the next release.

## How to write some documentation?
Follow numpy style, but no space before a colon ;)

## Commit messages
Follow the rules when writing a commit message:
- use the imperative mood in the first line of commit message,
- capitalize the first line,
- do not end the first line with a period,
- limit the first line to 72 characters,
- separate the first line from the body with one blank line.

_adopted from [here](https://chris.beams.io/posts/git-commit#seven-rules)._


## I am open
Feel free to connect. My email starts with `maciej.mikulski.jr` and ends with `gmail.com`.
