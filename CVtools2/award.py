import re
from .recent import Recent

class Award (Recent) : # {{{1

    'An award, such as induction into the National Academy of Sciences.'

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        try :
            self.description = args['description']
            self.agency = args['agency']
            self.year = args['year']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required variable in class Award',
                file = sys.stderr)
            raise SystemExit(1)
        # Defaults
        self.student = None
        self.date = None
        self.teaching = False
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise AttributeError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)
        # Error checking
        if not isinstance(self.teaching, bool) :
            raise TypeError('Award.teaching must be True or False')

##############################################################################

    def write (self, texfile) : # {{{2
        print (r'\item', file = texfile)
        self.begin_recent(texfile)
        if self.student is not None :
            print (r'   \emph{' + self.student + '},', file = texfile)
        print ('   ', self.description + ',', self.agency + ',',
            file = texfile)
        if self.date is None :
            print ('    ', str(self.year) + r'.\relax', file = texfile)
        else :
            if re.search('[0-9]',self.date[-1]) :
                print ('    ', str(self.date) + ',', str(self.year) \
                    + r'.\relax', file = texfile)
            else :
                print ('    ', str(self.date), str(self.year) + r'.\relax',
                    file = texfile)
        self.end_recent(texfile)
