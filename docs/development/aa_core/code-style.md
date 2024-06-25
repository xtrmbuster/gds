# Code Style

## Pre-Commit

Alliance Auth is a team effort with developers of various skill levels and background. To avoid significant drift or formatting changes between developers, we use [pre-commit](https://pre-commit.com/) to apply a very minimal set of formatting checks to code contributed to the project.

Pre-commit is also very popular with our Community Apps and may be significantly more opinionated or looser depending on the project.

To get started, `pip install pre-commit`, then `pre-commit install` to add the git hooks.

Before any code is "git push"-ed, pre-commit will check it for uniformity and correct it if possible

```shell
check python ast.....................................(no files to check)Skipped
check yaml...........................................(no files to check)Skipped
check json...........................................(no files to check)Skipped
check toml...........................................(no files to check)Skipped
check xml............................................(no files to check)Skipped
check for merge conflicts............................(no files to check)Skipped
check for added large files..........................(no files to check)Skipped
detect private key...................................(no files to check)Skipped
check for case conflicts.............................(no files to check)Skipped
debug statements (python)............................(no files to check)Skipped
fix python encoding pragma...........................(no files to check)Skipped
fix utf-8 byte order marker..........................(no files to check)Skipped
mixed line ending....................................(no files to check)Skipped
trim trailing whitespace.............................(no files to check)Skipped
check that executables have shebangs.................(no files to check)Skipped
fix end of files.....................................(no files to check)Skipped
Check .editorconfig rules............................(no files to check)Skipped
django-upgrade.......................................(no files to check)Skipped
pyupgrade............................................(no files to check)Skipped
```

## Editorconfig

[Editorconfig](https://editorconfig.org/) is supported my most IDE's to streamline the most common editor disparities. While checked by our pre-commit file, using this in your IDE (Either automatically or via a plugin) will minimize the corrections that may need to be made.

## Doc Strings

We prefer either [PEP-287](https://peps.python.org/pep-0287/)/[reStructuredText](https://docutils.sourceforge.io/rst.html) or [Google](https://google.github.io/styleguide/pyguide.html#381-docstrings) Docstrings.

These can be used to automatically generate our Sphinx documentation in either format.

## Best Practice

It is advisable to avoid wide formatting changes on code that is not being modified by an MR. Further to this, automated code formatting should be kept to a minimal when modifying sections of existing files.

If you are contributing whole modules or rewriting large sections of code, you may use any legible code formatting valid under Python.
