from .recent import Recent

def courses_from_this_school (inlist, school = None, reverse = False) : # {{{1
    
    'Returns a list of courses which were taught at this particular school.'

    from .constants import SCHOOL
    if school is None :
        school = SCHOOL
    outlist = []
    for item in inlist :
        if item.school == school :
            outlist.append(item)
    if reverse :
        outlist.reverse()
    return outlist

class Course (Recent) : # {{{1

    '''Gives information about courses taught.
    
    Required arguments: school, title, number, semester, year
    Optional arguments: credits, developed, students, responses, dropped,
        content_score, delivery_score, environment_score, assessment_score,
        effectiveness_score, composite_score, composite_AB_score,
        mean_GPA, mean_content_score, mean_delivery_score,
        mean_environment_score, mean_assessment_score,
        mean_effectiveness_score, mean_composite_score,
        mean_composite_AB_score, guest, note, recent'''

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        try :
            self.school = args['school']
            self.title = args['title']
            self.number = args['number']
            self.semester = args['semester']
            self.year = args['year']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: The Course class requires the following',
                'non-optional arguments:', file = sys.stderr)
            print ('   school, title, number, semester, year',
                file = sys.stderr)
            raise SystemExit(1)
        # Set default values (can be overridden by values of args)
        self.credits = 3
        self.developed = False
        self.students = None
        self.responses = None
        self.dropped = 0
        self.content_score = None
        self.delivery_score = None
        self.environment_score = None
        self.assessment_score = None
        self.effectiveness_score = None
        self.composite_score = None
        self.composite_AB_score = None
        self.mean_GPA = None,
        # These values are the means for the entire Department
        self.mean_content_score = None
        self.mean_delivery_score = None
        self.mean_environment_score = None
        self.mean_assessment_score = None
        self.mean_effectiveness_score = None
        self.mean_composite_score = None
        self.mean_composite_AB_score = None
        self.guest = False
        self.note = None
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise AttributeError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)
        # Escape any underscores
        self.number = self.number.replace(' ','~').replace('_',r'\_')
        # Error checking
        if not isinstance(self.credits, int) :
            raise TypeError ('Course.credits must be an integer')
        if not isinstance(self.dropped, int) and self.dropped is not None :
            raise TypeError ('Course.dropped must be an integer')
        if not isinstance(self.developed, bool) :
            raise TypeError ('Course.developed must be True or False')
        if not isinstance(self.guest, bool) :
            raise TypeError ('Course.guest must be True or False')

##############################################################################

    def __str__ (self) : # {{{2
        if self.students is None :
            return self.number + ' ' + self.title
        elif self.students == 1 :
            return self.number + ' ' + self.title + r' (' \
                + str(self.students) + '~student)'
        else :
            return self.number + ' ' + self.title + r' (' \
                + str(self.students) + '~students)'

##############################################################################

    def write (self, texfile) : # {{{2
        print (r'\item', file=texfile)
        self.begin_recent(texfile)
        print ('   ', self.title, '(' + self.number + ')', file = texfile)
        if self.note is not None :
            print ('(' + self.note + ')', file = texfile)
        self.end_recent(texfile)

##############################################################################

class UndergraduateCourse (Course) : # {{{1
    def __init__ (self, **args) :
        super().__init__(**args)

class GraduateCourse (Course) : # {{{1
    def __init__ (self, **args) :
        super().__init__(**args)

class TeachingAssistantship (Course) : # {{{1
    def __init__ (self, **args) :
        super().__init__(**args)
