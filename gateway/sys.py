"""

"""
import csv
import cStringIO
import datetime
from webob import Response
from pyramid.view import action
from gateway import models
from gateway.utils import nice_print

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
            csvWriter.writerow(nice_print(results["query"][0]).keys())            
            csvWriter.writerows([nice_print(x).values() for x in results["query"]])
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
