from .recent import Recent
from . import constants
from .utilities import markup_authors, list2string

class Grant (Recent) : # {{{1

    '''Class for grant proposals. Required arguments: title, PI, source, start,
       end'''

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        from .constants import SCHOOL
        # Required arguments
        try :
            self.title = args['title']
            self.PI = args['PI']
            self.source = args['source']
            self.start = args['start']
            self.end = args['end']
        except KeyError :
            #traceback.print_stack()
            missing_keys = []
            for key in ('title','PI','source','start','end') :
                if key not in args :
                    missing_keys.append(key)
            if len(missing_keys) == 1 :
                raise KeyError ('Missing required argument ' \
                    + repr(missing_keys[0]) + ' in ' + self.__class__.__name__)
            else :
                raise KeyError ('Missing required arguments ' \
                    + repr(missing_keys) + ' in ' + self.__class__.__name__)
            #raise SystemExit(1)
        try :
            self.amount = args['amount']
        except KeyError :
            try :
                self.CPU_hours = args['CPU_hours']
                self.amount = 0
            except KeyError :
                raise
        # Defaults
        self.awarded = False
        self.rejected = False
        self.completed = False
        self.coPI = None
        self.coI = None
        self.senior_personnel = None
        self.location = None
        self.teaching = False
        self.external_amount = None
        self.total_amount = None
        self.number = None
        self.shared_credit = None
        self.students_supported = None
        self.post_tenure = None
        self.post_appointment = None
        self.months_summer = 0
        self.months_academic = 0
        self.months_calendar = 0
        self.federal = True
        self.internal = False
        self.description = None
        self.CPU_hours = None
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise AttributeError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)
        if self.location is None :
            self.location = SCHOOL
        # Error checking
        if not isinstance(self.awarded, bool) :
            raise TypeError('Grant.awarded must be True or False')
        if not isinstance(self.rejected, bool) :
            raise TypeError('Grant.rejected must be True or False')
        if not isinstance(self.completed, bool) :
            raise TypeError('Grant.completed must be True or False')
        if not isinstance(self.teaching, bool) :
            raise TypeError('Grant.teaching must be True or False')
        if not isinstance(self.federal, bool) :
            raise TypeError('Grant.federal must be True or False')

##############################################################################

    def write (self, texfile, show_description = False) : # {{{2
        #print (r'\penalty -400%', file = texfile)
        print (r'\item', file = texfile)
        self.begin_recent(texfile)
        if self.number is None :
            print (r'Title: \emph{' + self.title + r'} \\*\indent',
                file = texfile)
        else :
            print (r'Title: \emph{' + self.title + r'}',
                '(' + str(self.number) + r') \\*\indent', file = texfile)
        for invest in ('PI','coPI','coI') :
            if not hasattr(self,invest) :
                continue
            printedform = invest.replace('coPI','Co-PI').replace('coI','Co-I')
            if getattr(self,invest) is not None :
                separator = r' \\\indent'
                if isinstance(getattr(self,invest), str) :
                    print (printedform, ': ',
                        markup_authors(getattr(self,invest),
                            CV_author=constants.INVESTIGATOR, printand=False),
                        separator, sep = '', file = texfile)
                elif isinstance(getattr(self,invest), (list,tuple)) :
                    if len(getattr(self,invest)) == 1 :
                        print (printedform, ': ',
                            markup_authors(getattr(self,invest),
                                CV_author=constants.INVESTIGATOR,
                                printand=False),
                            separator, sep = '', file = texfile)
                    else :
                        print (printedform, 's: ',
                            markup_authors(getattr(self,invest),
                                CV_author=constants.INVESTIGATOR,
                                printand=False),
                            separator, sep = '', file = texfile)
                else :
                    raise TypeError(invest + \
                        ' must be a string, tuple, or list')
        if self.senior_personnel is not None :
            separator = r' \\\indent'
            print (r'\mbox{Key Personnel:}',
                markup_authors(self.senior_personnel,
                    CV_author=constants.INVESTIGATOR,
                printand = False) + separator, file = texfile)

        print ('Source:', self.source, r' \\\indent', file = texfile)
        print (r'Amount: \$' + format(int(str(self.amount).replace(',','')),
            ',d'), end = '', file = texfile)
        if self.CPU_hours is not None :
            print ('${}+{}$' + format(int(str(self.CPU_hours).replace(',','')),
                ',d'), 'CPU-hours', end = '', file = texfile)
        if self.total_amount is not None :
            print (r'; Total Amount: \$',
                format(int(str(self.total_amount).replace(',','')), ',d'),
                sep = '', file = texfile)
        if self.external_amount is not None and self.external_amount > 0 :
            print (r'~(external: \$',
                format(int(str(self.external_amount).replace(',','')), ',d'), \
                ')', sep = '', file = texfile)
        print (r'\\\indent', file = texfile)
        if self.shared_credit is not None :
            print (r'Shared Credit:', str(self.shared_credit) +  r'\%',
                file = texfile)
        else :
            print (r'Shared Credit: 100\%', file = texfile)
        print (r'\\\indent', file = texfile)
        if self.end is None or self.start == self.end :
            print ('Project Dates:', self.start, file = texfile)
        else :
            print ('Project Dates:', self.start, 'through', self.end,
                file = texfile)
        # students supported
        if self.students_supported is not None :
            print (r'\\\indent Students Supported:',
                list2string(self.students_supported),
                file = texfile)
        # effort
        if isinstance(self.months_summer, (list,tuple)) :
            months_summer = sum(self.months_summer) / len(self.months_summer)
        else :
            months_summer = self.months_summer
        if isinstance(self.months_academic, (list,tuple)) :
            months_academic = sum(self.months_academic) / \
                len(self.months_academic)
        else :
            months_academic = self.months_academic
        if isinstance(self.months_calendar, (list,tuple)) :
            months_calendar = sum(self.months_calendar) / \
                len(self.months_calendar)
        else :
            months_calendar = self.months_calendar
        if months_summer + months_academic + months_calendar > 0.0 :
            print (r'\\\indent', file = texfile)
            print ('Effort:', file = texfile)
            if months_summer > 0.0 and months_academic > 0.0 :
                print ('  %0.2G' % months_summer, 'months/year (summer) + ',
                    file = texfile)
                print ('  %0.2G' % months_academic,
                    'months/year (academic year)', file = texfile)
            else :
                if months_summer > 0.0 :
                    if months_summer == 1 :
                        print ('  ', months_summer, 'month/year (summer)',
                            file = texfile)
                    else :
                        print ('  ', months_summer, 'months/year (summer)',
                            file = texfile)
                elif months_academic > 0.0 :
                    if months_academic == 1 :
                        print ('  ', months_academic,
                            'month/year (academic year)', file = texfile)
                        print ('  ', months_academic,
                            'months/year (academic year)', file = texfile)
                elif months_calendar > 0.0 :
                    if months_calendar == 1 :
                        print ('  ', months_academic,
                            'month (calendar year)', file = texfile)
                    else :
                        print ('  ', months_academic,
                            'months (calendar year)', file = texfile)
                else :
                    print ('   None', file = texfile)
        # Added description to satisfy committee's questions
        if show_description and self.description is not None :
            print (r'\par', file = texfile)
            print (r'Description: \emph{', self.description, '}',
                sep = '', file = texfile)

        self.end_recent(texfile)

##############################################################################

    def write_condensed (self, texfile) : # {{{2
        #print (r'\penalty -400%', file = texfile)
        print (r'\item', file = texfile)
        self.begin_recent(texfile)
        print (r'\emph{' + self.title + r'}', end='', file = texfile)
        if self.number is not None :
            print (' (' + str(self.number) + r')', end='', file = texfile)
        if constants.INVESTIGATOR == self.PI :
            print (r'; role: PI;', self.source + ', ', end='', file=texfile)
        elif isinstance(self.PI, (list,tuple)) \
                and constants.INVESTIGATOR in self.PI :
            print (r'; role: PI;', self.source + ', ', end='', file=texfile)
        elif constants.INVESTIGATOR == self.coPI :
            print (r'; role: Co-PI;', self.source + ', ', end='', file=texfile)
        elif isinstance(self.coPI,(list,tuple)) \
                and constants.INVESTIGATOR in self.coPI :
            print (r'; role: Co-PI;', self.source + ', ', end='', file=texfile)
        elif constants.INVESTIGATOR == self.coI :
            print (r'; role: Co-I;', self.source + ', ', end='', file=texfile)
        elif isinstance(self.coI, (list,tuple)) \
                and constants.INVESTIGATOR in self.coI :
            print (r'; role: Co-I;', self.source + ', ', end='', file=texfile)
        else :
            print (r'; role: senior personnel;', self.source + ', ', end='',
                file=texfile)
        #
        try :
            if self.CPU_hours is None :
                print (r'\$' + format(int(str(self.amount).replace(',','')),
                    ',d') + ';', file = texfile)
            else :
                print (r'\$',
                    format(int(str(self.amount).replace(',','')),',d'),
                    '${}+{}$',
                    format(int(str(self.CPU_hours).replace(',','')),',d'),
                    ' CPU-hours;', sep='', file = texfile)
        except ValueError :
            print (str(self.amount) + ';', file = texfile)
        #
        if self.shared_credit is not None :
            print (r'shared credit:', str(self.shared_credit) +  r'\%;',
                file = texfile)
        else :
            print (r'shared credit: 100\%;', file = texfile)
        #
        if self.end is None or self.start == self.end :
            print (self.start + '.', file = texfile)
        else :
            print (self.start, 'through', self.end + '.', file = texfile)
        self.end_recent(texfile)
