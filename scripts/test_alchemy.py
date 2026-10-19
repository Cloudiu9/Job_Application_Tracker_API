# from sqlalchemy import text
# from db_alchemy import engine
from sqlalchemy import select
from db_alchemy import SessionFactory
from models.application import Application


# with engine.connect() as con:
#     result = con.execute(text("SELECT * from applications"))
#     print(result.all())


with SessionFactory() as session:
    stmt = select(Application)
    applications = session.scalars(stmt).all()

    # all applications
    for app in applications:
        print("Before: ", app.id, app.company, app.title, app.status)

    app = session.get(Application, 24)
    assert app is not None
    app.company = "Updated company"
    session.commit()

    # modified application
    print("After: ", app.id, app.company, app.title, app.status)