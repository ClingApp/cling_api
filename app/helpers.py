def response_builder(object, entity, excluded=[]):
    """
    Helps to build appropriate response, parsing given object and included/excluded needed fields
    :param object: current object, from which we want to build a response
    :param entity: global entity the given object belongs to.
    :param excluded: array of fields we do not want to see in response.
    :return: return a dict with needed fields
    """
    result = {}
    for columnName in entity.__table__.columns.keys():
        if columnName not in excluded:
            result[columnName] = getattr(object, columnName)
    return result