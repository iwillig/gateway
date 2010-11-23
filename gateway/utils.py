



def get_fields(klass): 
    fields = {} 
    mapper = klass.__mapper__ 
    columns = mapper.columns
    for key in columns.keys():         
        field = columns.get(key).name
        fields.update({ field : {"value" : str(klass.__getattribute__(field)),
                                 "type" : "input"}})
    return fields
