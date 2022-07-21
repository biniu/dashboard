from invoke import task

from app.db import Base, engine
from app.routers.CodeWars import model as cw_model
from app.routers.User import model as user_model


@task
def init_db(ctx):
    print("Creating all resources.")

    Base.metadata.create_all(bind=engine)
    cw_model.Base.metadata.create_all(bind=engine)
    user_model.Base.metadata.create_all(bind=engine)


@task
def drop_all(ctx):
    if input(
            "Are you sure you want to drop all tables? (y/N)\n").lower() == "y":
        print("Dropping tables...")
        Base.metadata.drop_all()
