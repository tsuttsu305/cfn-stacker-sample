from invoke import Context
from invoke import task
from typing import Any


@task
def dev(c):  # type: (Context) -> Any
    c.run('stacker build --region ap-northeast-1 conf/dev.env stacker.yaml')
