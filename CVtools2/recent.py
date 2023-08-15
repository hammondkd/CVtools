__all__ = ('set_RECENT','set_SHOW_RECENT',
    "set_POST_APPOINTMENT", "set_POST_TENURE")

RECENT = False  # used to set whether things are marked recent by default
SHOW_RECENT = True # whether recent things are highlighted
POST_APPOINTMENT = False # used to easily set whether things are pre/post-appt
POST_TENURE = False # ...and pre/post-tenure

def set_RECENT (value = True) :
    global RECENT
    RECENT = value

def set_SHOW_RECENT (value = True) :
    global SHOW_RECENT
    SHOW_RECENT = value

def set_POST_APPOINTMENT (value = True) :
    global POST_APPOINTMENT
    POST_APPOINTMENT = value

def set_POST_TENURE (value = True) :
    global POST_TENURE
    POST_TENURE = value

class Recent : # {{{1

    '''Container class for objects that can be flagged as added since the last
    promotion, last P&T evaluation, etc.'''

    def __init__ (self, **args) :
        #if SHOW_RECENT :
        if 'recent' in args :
            self.recent = args['recent']
        else :
            self.recent = RECENT
        if self.recent is None :
            self.recent = RECENT
        # We set pre/post appointment and pre/post tenure, too (why not?)
        if 'post_appointment' in args :
            self.post_appointment = args['post_appointment']
        else :
            self.post_appointment = POST_APPOINTMENT
        if 'post_tenure' in args :
            self.post_tenure = args['post_tenure']
        else :
            self.post_tenure = POST_TENURE
    def begin_recent (self, texfile) :
        'Opens the color change for recent entries.'
        if SHOW_RECENT and self.recent :
            print (r'\begingroup\color{recent}%', file = texfile)
    def end_recent (self,texfile) :
        'Closes the color change for recent entries.'
        if SHOW_RECENT and self.recent :
            print (r'\endgroup', file = texfile)
