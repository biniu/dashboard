from invoke import task

from app.db import Base


@task
def init_db(ctx):
    print("Creating all resources.")

    Base.metadata.create_all()


@task
def drop_all(ctx):
    if input(
            "Are you sure you want to drop all tables? (y/N)\n").lower() == "y":
        print("Dropping tables...")
        Base.metadata.drop_all()
