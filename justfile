#!/usr/bin/env just --justfile
# We use this justfile to organize frequently-run commands and recipes
# in one place.
# To use this justfile, you must install "just" from
# [[https://github.com/casey/just]]. After that, run the "just"
# command from a terminal or command prompt to see a list of available recipes.
# Use bash to execute backticked lines.

set shell := ["bash", "-uc"]

# (Default) list all the just recipes.
list:
    @just --list

# Check version of python.
check-py:
    # Check poetry installation and pyproject.toml is healthy.
    poetry check
    # Print environment being used by poetry.
    poetry env info
    # Make sure you are using Python >= 3.10

# Install all pip requirements for "normal_form" project.
install dependencies="": check-py
    python3 -m pip install --upgrade pip
    python3 -m pip install poetry
    poetry install {{dependencies}}
    # poetry run nbstripout --install
    # Consider running "just test" for testing the project.

# Update dependendencies (for package devs only).
update:
    poetry update
    poetry run safety check

# Lint and check the codebase for style.
lint:
    poetry run autoflake --in-place --recursive --expand-star-imports --remove-all-unused-imports normal_form/* tests/*
    poetry run isort normal_form/ tests/
    # stop the build if there are Python syntax errors or undefined names
    poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
    poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    poetry run pylint -vvv normal_form/ tests/
    poetry run pycodestyle normal_form/ tests/
    poetry run pydocstyle normal_form/ tests/

# Typecheck the code using mypy.
typecheck files="./stubs/ normal_form/ tests/":
    poetry run mypy {{ files }}
    # poetry run nbqa mypy benchmarking/
    # Consider running "just lint" for linting the code.

# Run all the tests.
test flags="--cov-report term-missing --cov=normal_form --workers auto":
    # Helpful command for debugging: just test "-x --ff -v -s --pdb"
    poetry run pytest {{ flags }}
    # To test Jupyter notebooks, uncomment the following:
    # poetry run pytest --nbmake --nbmake-timeout=30 benchmarking/*.ipynb
    # Consider running "just typecheck" for statically checking types.

# Run the "if __name__ == "__main__" block of all the scripts.
mains:
    poetry run python -m normal_form.cnf
    poetry run python -m normal_form.sat

# Remove cache files.
clean:
    rm -rf **/__pycache__
    rm -rf normal_form/__pycache__
    rm -rf normal_form/test/__pycache__

# Create etags for Emacs navigation.
tags:
    etags normal_form/*.py

ORG_FILES := "benchmarking.org"
TEX_FILES := "benchmarking.tex"
PY_FILES := ""

# Convert org file to tex file using emacs script `lisp_code.el`
org2tex:
    cd benchmarking && emacs -l lisp_code.el --batch {{ ORG_FILES }} -f org-latex-export-to-latex --kill

# Convert tex file to pdf file using latexmk.
tex2pdf:
    cd benchmarking && latexmk -pdflatex=lualatex -pdf -shell-escape {{ TEX_FILES }}

# Convert org file to python and compare with direct-python copy.
org2py:
    emacs --batch {{ ORG_FILES }} -f org-babel-tangle --kill
    git diff {{ ORG_FILES }} {{ PY_FILES }}

docs:
    # README.org -> README.md conversion should be done in org by (auto-org-md-mode).
    just _write_md
    -poetry run mkdocs serve

_write_md:
    #!/usr/bin/env bash
    for file in `ls normal_form/*.py`; do
      base=$(basename -- $file .py)
      if [ "$base" = "__init__" ]; then
        continue
      fi
      echo "## $base.py" > docs/$base".md"
      echo "::: normal_form.$base" >> docs/$base".md"
    done
