
USERS = {'admin':'3ebrufu3',
          'viewer':'viewer'}

GROUPS = {'admin':['group:admins']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
