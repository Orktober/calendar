'''
Represents a coach
'''
from settings import coach_coll
from models.user import User

class Coach(User):

    coll   = coach_coll
    fields = User.fields + ('availability',)

    def __init__(self, email, **kwargs):

        User.__init__(self, email, **kwargs)


