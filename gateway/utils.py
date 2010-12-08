'''
'''
import os
from mako.template import Template

baseTemplate = "%s/gateway/templates/messages" % os.getcwd()

def make_message(template="error.txt", lang="fr", **kwargs):
    """Builds a template based on name and langauge with kwargs passed
    to the template..  Returns a template object
    """
    templateName = "%s/%s/%s" % (baseTemplate, lang, template)
    template = Template(filename=templateName).render(**kwargs)
    return template


def raise_first_leter(word):
    word = word[0].upper() + word[1:]
    return word.replace("_"," ")

def get_fields(model): 
    """Takes a model and returns a useful dict"""
    fields = {} 
    mapper = model.__mapper__ 
    columns = mapper.columns
    for key in columns.keys():         
        field = columns.get(key).name
        niceName = raise_first_leter(field)
        fields.update({ niceName.replace('_',' ') : 
                        {"value" : str(model.__getattribute__(field)),
                         "name" : field,
                         "type" : "input"}})
    return fields


def model_from_request(request,model): 
    params = request.params
    keys = params.keys() 
    keys.remove("submit") 
    for key in keys:
        model.__setattr__(key,params.get(key))            
    return model


def make_table_header(klass): 
    fields = []
    keys = klass.__mapper__.columns.keys()
    for key in keys: 
        fields.append({ "id" :key, 
                        "sortable": True,
                        "name" : raise_first_leter(key), 
                        "field" : key})
    return fields


def make_table_data(models):    
    if models:
        first = models[0]
        data = [] 
        for model in models:
            field = {} 
            for key in first.__mapper__.columns.keys(): 
                field.update({ key : str(model.__getattribute__(key))}) 
            data.append(field)
        return data 
    else: 
        return [] 
