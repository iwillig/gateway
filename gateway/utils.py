



def get_fields(klass): 
    """
    Takes a model and returns a useful dict
    """
    fields = {} 
    mapper = klass.__mapper__ 
    columns = mapper.columns
    for key in columns.keys():         
        field = columns.get(key).name
        niceName = field[0].upper() + field[1:]
        fields.update({ niceName.replace('_',' ') : 
                        {"value" : str(klass.__getattribute__(field)),
                         "type" : "input"}})
    return fields

