from .recent import Recent
import datetime

class SocietyMembership (Recent) : # {{{1

    'Membership in a professional society.'

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        # Mandatory arguments
        try :
            self.name = args['name']
            self.dates = args['dates']
            if isinstance(self.dates, (list,tuple)) :
                for i in range(len(self.dates)) :
                    self.dates[i] = str(self.dates[i])
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required key word for SocietyMembership',
                file = sys.stderr)
            raise SystemExit(1)
        # Defaults
        self.abbr = None
        self.active = True
        self.rank = None
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise AttributeError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)
        # Error checking
        if not isinstance(self.active, bool) :
            raise TypeError('SocietyMembership.active must be True or False')

##############################################################################

    def write (self, texfile) : # {{{2
        print (texfile, r'\item')
        self.begin_recent(texfile)
        print ('  ', self.society, '(' + self.abbr + ')',
            self.dates)
        if self.rank is not None :
            print ('[' + self.rank + ']', file = texfile)
        self.end_recent(texfile)

##############################################################################
##############################################################################

class ReviewPanel (Recent) : # {{{1

    'Service on a grant proposal review committee.'

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        # Mandatory arguments
        try :
            self.agency = args['agency']
            self.year = args['year']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required key word for class ReviewPanel',
                file = sys.stderr)
            raise SystemExit(1)
        # Defaults
        self.division = None
        self.div_abbr = None
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise AttributeError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)

##############################################################################

    def write (self, texfile) : # {{{2
        print (r'\item', file = texfile)
        self.begin_recent(texfile)
        print ('  ', self.agency + ',', file = texfile)
        if self.division is not None :
            if self.div_abbr is None :
                print ('     ', self.division + ',', file = texfile)
            else :
                print ('     ', self.division, '(' + self.div_abbr + '),',
                    file = texfile)
        print (str(self.year) + '.', file = texfile)
        self.end_recent(texfile)

##############################################################################
##############################################################################

class SessionChair (Recent) : # {{{1

    'Service as chair or co-chair of a session at a conference.'

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        try :
            self.role = args['role']
            self.event = args['event']
            self.location = args['location']
            self.date = args['date']
            self.year = args['year']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required key word for SessionChair',
                file = sys.stderr)
            raise SystemExit(1)
        # Defaults
        self.note = None
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise AttributeError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)

##############################################################################

    def write (self, texfile) : # {{{2
        print (r'\item', file = texfile)
        self.begin_recent(texfile)
        print ('   ', self.role + ',', self.event + ';', file = texfile)
        print (r'  ', self.location + ',', self.date + ',',
            str(self.year) + '.', file = texfile)
        if self.note is not None :
            print (r'  \emph{' + self.note + '}', file = texfile)
        self.end_recent(texfile)

##############################################################################
##############################################################################

class Local : # {{{1
    'Container class for local service activities.'
    pass

class Regional : # {{{1
    'Container class for regional service activities.'
    pass

class National : # {{{1
    'Container class for national service activities.'
    pass

class International : # {{{1
    'Container class for international service activities.'
    pass

class ConferenceChair (SessionChair) : # {{{1
    'Chair/host of a conference'
    pass

class RegionalConferenceChair (ConferenceChair,Regional) :
    'Conference chair at a regional conference'
    pass

class NationalConferenceChair (ConferenceChair,National) :
    'Conference chair at a national conference'
    pass

class InternationalConferenceChair (ConferenceChair,National) :
    'Conference chair at an international conference'
    pass

class RegionalSessionChair (SessionChair,Regional) : # {{{1
    'Session chair at a regional conference'
    pass

class NationalSessionChair (SessionChair,National) : # {{{1
    'Session chair at a national conference'
    pass

class InternationalSessionChair (SessionChair,International) : # {{{1
    'Session chair at an international conference'
    pass

##############################################################################

class ManuscriptReview (Recent) : # {{{1

    'Service in the review of a manuscript.'

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        # Mandatory arguments
        try :
            self.journal = args['journal']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required key word for ManuscriptReview',
                file = sys.stderr)
            raise SystemExit(1)
        # Defaults
        self.note = None
        self.date = None
        self.year = None
        self.number = None
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise AttributeError ('class ' + self.__class__.__name__ \
                     + ' does not define the key word ' + arg)
        self.count = 0
        if self.date is None :
            # If no date is provided, assume it's February 2 (just 'cause)
            self.earliest = datetime.date(self.year,2,2)
            self.latest = datetime.date(self.year,2,2)
        else :
            month = int(self.date.split('/')[0])
            day = int(self.date.split('/')[1])
            self.earliest = datetime.date(self.year,month,day)
            self.latest = datetime.date(self.year,month,day)

##############################################################################

    def __lt__ (self, other) : # {{{2
        return self.journal < other.journal

    def __le__ (self, other) : # {{{2
        return self.journal <= other.journal

    def __eq__ (self, other) : # {{{2
        return self.journal == other.journal

    def __ne__ (self, other) : # {{{2
        return self.journal != other.journal

    def __gt__ (self, other) : # {{{2
        return self.journal > other.journal

    def __ge__ (self, other) : # {{{2
        return self.journal >= other.journal

    def __hash__ (self) : # {{{2
        return hash(self.journal)

    def __str__ (self) : # {{{2
        return str(self.journal)

##############################################################################

    def write (self, texfile, print_count = True) : # {{{2
        '''Formats manuscript review activities for output on the CV and
           dossier'''
        print (r'\item', file = texfile)
        self.begin_recent(texfile)
        print (r'   \emph{' + self.journal + '}', file = texfile)
        if print_count :
            if self.note is not None :
                print (r'    (' + self.note + ')', file = texfile)
            if self.count == 1 :
                print (r'     (', self.count, ' manuscript in ',
                    self.earliest.year, ')', sep='', file = texfile)
            elif self.earliest.year == self.latest.year :
                print (r'     (', self.count, ' manuscripts in ',
                    self.earliest.year, ')', sep='', file = texfile)
            else :
                print (r'     (', self.count, ' manuscripts between ',
                    self.earliest.year, ' and ', self.latest.year, ')', sep='',
                    file = texfile)
        self.end_recent(texfile)

##############################################################################

class Service (Recent) : # {{{1

    'Service activities not fitting into other categories.'

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        try :
            self.role = args['role']
            self.description = args['description']
            self.start = args['start']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required argument in Service',
                file = sys.stderr)
            raise SystemExit(1)
        # Defaults
        self.end = None
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise AttributeError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)

##############################################################################

    def merge (self, other) : # {{{2
        if not isinstance(other, Service) :
            raise TypeError
        if isinstance(self.start,list) \
                and isinstance(other.start,(list,tuple)) :
            self.start.extend(other.start)
        elif isinstance(self.start,list) and isinstance(other.start,str) :
            self.start.extend(other.start)
        elif isinstance(self.start,tuple) and isinstance(other.start,tuple) :
            self.start = self.start + other.start
        elif isinstance(self.start,tuple) and isinstance(other.start,str) :
            self.start = self.start + (other.start,)
        else :
            self.start = [self.start,self.other]

##############################################################################

    def write (self, texfile) : # {{{2
        print (r'\item', file = texfile)
        self.begin_recent(texfile)
        print (self.role + ',', self.description + ',',
            end = ' ', file = texfile)
        # If start is a list or tuple, we combine them appropriately
        if isinstance(self.start, (tuple,list)) :
            for i in range(len(self.end)) :
                if self.end[i] is None :
                    print (self.start[i], 'to present',
                        end = '', file = texfile)
                elif self.start[i] == self.end[i] :
                    print (self.start[i], end='', file = texfile)
                else :
                    print (self.start[i], 'to', self.end[i],
                        end='', file = texfile)
                if i < len(self.end) :
                    print ('; ', end='', file=texfile)
            # Catch the last one if end is shorter than start
            # (assumes one would not be serving twice simultaneously)
            if len(self.start) > len(self.end) :
                print (self.start[-1], 'to present',
                    end = '', file = texfile)
        else :
            # Otherwise, start is a string, and we output as normal
            if self.end is None :
                print (self.start, 'to present', end = '', file = texfile)
            elif self.end == self.start :
                print (self.start, end='', file = texfile)
            else :
                print (self.start, 'to', self.end, end='', file = texfile)
        print (r'\relax',file=texfile)
        self.end_recent(texfile)

##############################################################################

class LocalService (Service,Local) : # {{{1
    'Container class for service to the University System, College, etc.'
    pass

class NonLocalService (Service) : # {{{1
    'Container for service outside the University System.'
    pass

class DepartmentService (LocalService) : # {{{1
    'Service to your Department'
    pass

class CollegeService (LocalService) : # {{{1
    'Service to your College'
    pass

class UniversityService (LocalService) : # {{{1
    'Service to your University'
    pass

class UniversitySystemService (LocalService) : # {{{1
    'Service to the University System.'
    pass

class NationalService (NonLocalService,National) : # {{{1
    'Service to a national-level organization'
    pass

class RegionalService (NonLocalService,Regional) : # {{{1
    '''Service to a regional organization or a national-level organization
       for a regional function'''
    pass

class InternationalService (NonLocalService,International) : # {{{1
    'Service at an international event or to an international organization.'
    pass
