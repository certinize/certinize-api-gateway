# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

# Types of Contributions

## Report Bugs

Report bugs at https://github.com/certinize/certinize-api-gateway/issues.

If you are reporting a bug, please include:

* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

## Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

## Write Documentation

certinize-api-gateway could always use more documentation, whether as part of the official certinize-api-gateway docs, in docstrings, or even on the web in blog posts, articles, and such.

## Submit Feedback

The best way to send feedback is to file an issue at https://github.com/huenique/certinize-api-gateway/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome.

## Get Started

Ready to contribute? Here's how to set up `certinize-api-gateway` for local development.

1. Fork the `certinize-api-gateway` repo on GitHub.
2. Clone your fork locally

    ```
    $ git clone https://github.com/[Your GitHub Username]/certinize-api-gateway.git
    ```

3. Install your local copy into a virtualenv. Assuming you have python [poetry](https://github.com/python-poetry/poetry) installed, this is how you set up your fork for local development

    ```
    $ cd certinize-api-gateway/
    $ poetry shell
    $ poetry install
    ```

4. Create a branch for local development

    ```
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8, pylint, and pyright.

    ```
    $ flake8 app
    $ pylint app
    $ pyright app
    ```

## Commit Message Guidelines
certinize-api-gateway uses precise rules over how git commit messages can be formatted. This leads to more readable messages that are easy to follow when looking through the project history. But also, git commit messages are used to generate the change log. For instructions, head over to this site: https://www.conventionalcommits.org/en/v1.0.0/.

```
$ git add .
$ git commit -m "<type>(<scope>): <subject>"
```

## Pull Request Guidelines

Please open an issue before submitting, unless it's just a typo or some other small error.

Before you submit a pull request, check that it meets these guidelines:

1. If the pull request adds functionality, the docs should be updated. Implement your functionality with a docstring if needed.
2. The pull request should work for Python 3.10 and above.

Before making changes to the code, install the development requirements using

```
$ poetry install
```

Before committing, stage your files and run style and linter checks

```
$ black app/  # apply codestyle
$ isort --profile black app/  # sort imports
$ flake8 app/
$ pylint app/
$ pyright app/  # optional static type checking
```
