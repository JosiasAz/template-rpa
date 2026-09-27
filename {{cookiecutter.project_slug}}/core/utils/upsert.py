def upsert(session, model, data, unique_by):
    target = model.__table__ if hasattr(model, "__table__") else model
    dialect = session.bind.dialect.name
    payload = data if isinstance(data, list) else [data]
    unique_by = list(unique_by)
    update_cols = [key for key in payload[0] if key not in unique_by]

    if dialect == "postgresql":
        from sqlalchemy.dialects.postgresql import insert

        stmt = insert(target).values(payload)
        stmt = stmt.on_conflict_do_update(
            index_elements=unique_by,
            set_={col: getattr(stmt.excluded, col) for col in update_cols},
        )
        session.execute(stmt)
        return

    if dialect in ("mysql", "mariadb"):
        from sqlalchemy.dialects.mysql import insert

        stmt = insert(target).values(payload)
        stmt = stmt.on_duplicate_key_update(
            **{col: getattr(stmt.inserted, col) for col in update_cols}
        )
        session.execute(stmt)
        return

    if dialect == "sqlite":
        from sqlalchemy.dialects.sqlite import insert

        stmt = insert(target).values(payload)
        stmt = stmt.on_conflict_do_update(
            index_elements=unique_by,
            set_={col: getattr(stmt.excluded, col) for col in update_cols},
        )
        session.execute(stmt)
        return

    if hasattr(model, "__table__"):
        for row in payload:
            session.merge(model(**row))
        return

    from sqlalchemy import insert

    session.execute(insert(target).values(payload))
