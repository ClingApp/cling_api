def get_info(object, type, not_used):
    information = {}
    for columnName in type.__table__.columns.keys():
        if columnName not in not_used:
            information[columnName] = getattr(object, columnName)
    return information