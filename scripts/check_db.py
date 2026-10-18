from models.application import Base, Application

print(Base.metadata.tables.keys())
print(Application.__table__.columns.keys())

for column in Application.__table__.columns:
    print(
        column.name,
        column.type,
        "nullable =", column.nullable,
        "primary_key =", column.primary_key,
        "default =", column.default,
        "server_default =", column.server_default,
    )

print(Application.__table__.constraints) # type: ignore