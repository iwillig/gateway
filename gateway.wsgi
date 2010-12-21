from pyramid.paster import get_app
import sys
sys.stdout = sys.stderr

application = get_app(
  '/home/ivan/gateway/production.ini', 'main')

