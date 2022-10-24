from app.models.user import Base as UserBase


def setup_db(engine):
    UserBase.metadata.create_all(bind=engine)


def drop_db(engine):
    UserBase.metadata.drop_all(bind=engine)
