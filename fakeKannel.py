from urlparse import parse_qs
from Queue import Queue
import time
import urllib
import urllib2
from threading import Thread
from pyramid.config import Configurator
from pyramid.response import Response
from paste.httpserver import serve

messages = Queue()

gatewayConfig = {
    'phone': 18182124554,
    'url': 'http://localhost:6543',
    'interface': 8 }


class SendDelete(Thread):
    """
    """

    def __init__(self):
        Thread.__init__(self)

    def respond_to_job(self, message):
        msgDict = parse_qs(message.text)
        print(msgDict)
        jobString = """(job=delete&status=1&tu=2256&ts=20110107192318&wh=9.7&cr=475.95&jobid=%s&ct=CIRCUIT)""" % msgDict['jobid'][0]
        print(jobString)
        data = urllib.urlencode({"message": jobString,
                                 "number": gatewayConfig.get('phone')})
        request = urllib2.Request(
            data=data,
            url="%s/interface/send/%s" % (gatewayConfig.get('url'),
                                          gatewayConfig.get('interface')))
        response = urllib2.urlopen(request)
        print(response.read())

    def run(self):
        print('Runing thread')
        while True:
            msg = messages.get()
            if msg:
                if msg.text.startswith('job'):
                    print('sending delete to meter')
                    print(self.respond_to_job(msg))


class Message(object):
    """Builds a message object from a Kannel request"""
    def __init__(self, request):
        self.number = request.params['to']
        self.text = request.params['text']

    def __str__(self):
        return 'Message number:%s text:%s ' % (self.number, self.text)


def sendMessage(request):
    print('------------------------------')
    msg = Message(request)
    print(msg)
    messages.put(msg)
    return Response()


def viewQueue(request):
    return Response("%s" % messages.qsize())


if __name__ == '__main__':
    config = Configurator()
    config.add_route('add-message',
                     '/cgi-bin/sendsms',
                     view=sendMessage)
    config.add_route('/view-messages',
                     'view-messages',
                     view=viewQueue)
    app = config.make_wsgi_app()
    delete = SendDelete()
    delete.start()
    serve(app, host='0.0.0.0', port=13001)
