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
    print("STATEMENT: ",stmt)
    applications = session.scalars(stmt).all()

    for app in applications:
        print(app.id, app.company, app.title, app.status)