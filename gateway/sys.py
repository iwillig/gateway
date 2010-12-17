"""

"""
import csv
import cStringIO
import datetime
from webob import Response
from pyramid.view import action
from gateway import models



class ExportLoadHandler(object):
    def __init__(self,request):
        self.request = request
        self.session = models.DBSession()
        self.allowed = ["Meter","Circuit","PrimaryLog","Message"] 

    @action()
    def export(self):
        s = cStringIO.StringIO()
        csvWriter = csv.writer(s)
        model = str(self.request.matchdict.get("data"))
        if model in self.allowed:            
            klass = getattr(models,model)
            results = self.session.query(klass).all()
            mapper = klass.__mapper__
            csvWriter.writerow(mapper.columns.keys())            
            csvWriter.writerows(map(
                lambda model:
                map(lambda k: getattr(model,k),
                    mapper.columns.keys()),results))
            s.reset()
            resp = Response(s.getvalue())
            resp.content_type = 'application/x-csv'
            resp.headers.add('Content-Disposition',
                             'attachment;filename=export_data.csv')
            return resp

        else:
            return Response("Model not found, please try again")
        
    @action(permission="admin")
    def download(self):
        return {} 
