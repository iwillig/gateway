"""

"""
import csv
import cStringIO
import datetime
from webob import Response
from pyramid.view import action
from gateway import models

session = models.DBSession()

def findModel(modelName):
    """ Inspects model module and returns dict """
    klass = getattr(models,modelName)
    if klass:
        query = session.query(klass).all()
        mapper = klass.__mapper__        
        return {"class" : klass, "query" : query, "mapper" : mapper}
    else:
        return None

def makeDict(model):
    collector = {}
    modelDict = model.__dict__
    for k,v in modelDict.iteritems():            
        if isinstance(v,object):
            collector.update({ k : str(v)})
        else:
            collector.update({ k : v})
    collector.pop('_sa_instance_state')
    return collector

class ExportLoadHandler(object):
    def __init__(self,request):
        self.request = request

    @action(renderer="sys/index.mako")
    def index(self):
        return {} 

    @action()
    def export(self):
        s = cStringIO.StringIO()
        csvWriter = csv.writer(s)
        modelName = str(self.request.params.get("model"))
        results = findModel(modelName)
        if results:
            csvWriter.writerow(makeDict(results["query"][0]).keys())            
            csvWriter.writerows([makeDict(x).values() for x in results["query"]])
            s.reset()
            resp = Response(s.getvalue())
            resp.content_type = 'application/x-csv'
            resp.headers.add('Content-Disposition',
                             'attachment;filename=export_data.csv')
            return resp        
        else:
            return Response("Unable to find table") 

    @action(renderer="sys/download.mako",permission="admin")
    def download(self):
        tables = models.Base.metadata.tables.keys()
        return {"tables" : tables} 
