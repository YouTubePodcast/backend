from invoke import task  # NOQA


TEST_FOLDER = "tests"
PROJECT_FOLDER = "youtube_podcast"
PE_V = "env PIPENV_VERBOSITY=-1"


@task
def clean_cache(c):
    print("Cleaning module cache.")
    c.run("rm -rf .pytest_cache")


@task
def clean_test_cache(c):
    print("Cleaning test cache.")
    c.run("rm -rf {}/.pytest_cache".format(TEST_FOLDER))


@task(pre=[clean_cache, clean_test_cache])
def clean(c):
    pass


@task
def delete_cassettes(c):
    print("Deleting VCRpy cassettes...")
    for folder in ["api", "controllers", "helpers"]:
        c.run("rm -rf tests/{}/cassettes".format(folder))


@task
def test(c):
    c.run(f"{PE_V} pipenv run pytest -s {TEST_FOLDER}", pty=True)


@task
def test_spec(c):
    c.run(f"{PE_V} pipenv run pytest --spec -s -p no:sugar {TEST_FOLDER}", pty=True)


@task
def test_this(c):
    c.run(f"{PE_V} pipenv run pytest --spec -s -p no:sugar -m 'runthis' {TEST_FOLDER}", pty=True)


@task
def test_coverage(c):
    c.run(f"{PE_V} pipenv run pytest --cov='{PROJECT_FOLDER}' -s {TEST_FOLDER}", pty=True)


@task
def run(c):
    # VSCODE LAUNCH CONFIG for running and debugging
    # {
    #     "name": "Launch run.py",
    #     "type": "python",
    #     "request": "launch",
    #     "program": "run.py",
    #     "console": "integratedTerminal"
    # }
    c.run(f"{PE_V} pipenv run python run.py", pty=True)


@task
def debug(c):
    # VSCODE LAUNCH CONFIG for detached debugging
    # {
    # "name": "Python: Attach",
    # "type": "python",
    # "request": "attach",
    # "connect": {
    #     "host": "localhost",
    #     "port": 5678
    # }
    c.run(f"{PE_V} pipenv run python -m debugpy --listen 5678 --wait-for-client run.py", pty=True)


@task
def debug_test(c):
    # VSCODE LAUNCH CONFIG for detached debugging
    # {
    # "name": "Python: Attach",
    # "type": "python",
    # "request": "attach",
    # "connect": {
    #     "host": "localhost",
    #     "port": 5678
    # }
    c.run(f"{PE_V} pipenv run python -m debugpy --listen 5678 --wait-for-client .venv/bin/pytest {TEST_FOLDER}",
          pty=True)
