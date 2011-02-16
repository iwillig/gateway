from pyramid.paster import get_app
import sys
sys.stdout = sys.stderr

application = get_app(
  '/usr/local/gateway-env/gateway/production.ini', 'main')

