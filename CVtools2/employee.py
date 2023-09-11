import datetime
import sys
import traceback
from .utilities import list2string, datestring2monthyear, markup_authors
from .degree import DOCTORATES, MASTERS
from . import constants
from . import recent
from .recent import Recent

class Employee (Recent) : # {{{1

    '''Provides information about employees, including undergraduate, graduate,
       and post-doctoral scholars, as well as student committees on which the
       CV author has served.'''

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        # Required arguments
        try :
            self.last = args['last']
            self.first = args['first']
        except KeyError :
            raise KeyError ('Missing required key word for class ' \
                + self.__class__.__name__)
        # Defaults
        self.middle = None
        self.start_date = None
        self.end_date = None
        self.project = None
        self.funding = None
        self.graduation = None
        self.advisor = None
        self.coadvisor = None
        self.current = True
        self.key = None
        self.title = None
        self.year = None
        self.committee = None
        self.defense = None
        self.school = None
        self.salutation = ''
        self.present_address = None
        self.post_tenure = None
        self.post_appointment = None
        self.email = None
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise KeyError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)
        if self.advisor is None :
            self.advisor = (constants.AUTHOR \
                if isinstance(constants.AUTHOR,str) else constants.AUTHOR[0])
        if self.school is None :
            self.school = constants.SCHOOL
        if self.post_tenure is None :
            self.post_tenure = recent.POST_TENURE
        if self.post_appointment is None :
            self.post_appointment = recent.POST_APPOINTMENT
        # Error checking
        if not isinstance(self.current, bool) :
            raise TypeError('Employee.current must be True or False')

##############################################################################
    
    def __str__ (self) : # {{{2
        return self.last + ', ' + self.first \
            + ('' if self.middle is None else ' ' + self.middle)
        # Warning: the above lines are used in the Collaborators document!

##############################################################################

    def funding_sources (self) : # {{{2
        if isinstance(self.funding, (list,tuple)) :
            return ', '.join(self.funding)
        elif self.funding is None :
            return ''
        else :
            return self.funding

##############################################################################

    def coadvised (self) : # {{{2
        if self.advisor == constants.AUTHOR :
            return False
        elif isinstance (self.advisor, str) :
            return self.advisor not in constants.AUTHOR
        else : # both are lists => more than 1 advisor
            return True

##############################################################################

    def description (self) : # {{{2
        'Returns a string such as "Ph.D. student" for use in the CV.'
        return NotImplemented

##############################################################################

    def write_thesis_or_dissertation (self, texfile, show_committee = False) :
        raise NotImplementedError

##############################################################################

    def write (self, texfile, print_funding=False, print_address=False) :
        raise NotImplementedError

##############################################################################

class Student (Employee) : # {{{1

    '''This is only there to add "major" to the list of required attributes and
       add define attributes specific to students'''

    def __init__ (self, **args) : # {{{2
        self.major = None
        self.minor = None
        self.degree = None
        super().__init__(**args)
        try:
            self.major = list2string(args['major'])
        except KeyError :
            traceback.print_stack()
            print ('KeyError: missing required key word for class Student',
                file = sys.stderr)
            raise SystemExit(1)

##############################################################################

class UndergraduateStudent (Student) : # {{{1

    'An undergraduate student employee'

    def __init__ (self, **args) : # {{{2
        if 'degree' not in args :
            args['degree'] = 'B.S.'
        super().__init__(**args)
        try :
            self.start_date = args['start_date']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: missing required key word "start_date"',
                'for class UndergraduateStudent', file = sys.stderr)
            raise SystemExit(1)
        if self.degree[0] != 'B' :
            print ('WARNING: Undergraduate student is getting a',
                self.degree + "? (does not start with 'B'?)",
                file = sys.stderr)

##############################################################################

    def description (self) : # {{{2
        if self.current :
            return 'undergraduate student, ' + self.major.lower() + ', ' \
                + datestring2monthyear(self.start_date) + ' to ' + \
                ('present' if self.end_date is None \
                           else datestring2monthyear(self.end_date))
        elif self.graduation is None :
            return self.degree + ', ' + self.major.lower() + ', ' \
                + self.school + ' (anticipated)'
        else :
            return self.degree + ', ' + self.major.lower() + ', ' \
                + self.school + ', ' \
                + datestring2monthyear(self.graduation)

##############################################################################

    def write (self, texfile, print_funding=False, print_address=False) : # {{{2
        print (r'\item', file = texfile, end='')
        self.begin_recent (texfile)
        if self.middle is None :
            full_name = self.first + ' ' + self.last
        else :
            full_name = self.first + ' ' + self.middle + ' ' + self.last
        if self.current or self.end_date is None :
            print (r'  ', full_name + ',', self.major.lower() + ',',
                file = texfile)
            try :
                start = datetime.datetime.strptime(self.start_date,
                    '%m/%d/%Y')
            except ValueError :
                start = datetime.datetime.strptime(self.start_date,
                    '%m/%Y')
            #print (start.strftime('%B %-d, %Y'),
            print (start.strftime('%B %Y'),
                'to present.', file = texfile)
        elif self.graduation is None :
            print ("WARNING: graduation is empty for", full_name,
                file = sys.stderr)
            if self.school != constants.SCHOOL :
                print (r'  ', full_name + ',', self.degree + ',',
                    self.major + ',', self.school + ', (anticipated);',
                    file = texfile)
            else :
                print (r'  ', full_name + ',', self.degree + ',',
                    self.major + ', (anticipated);', file = texfile)
            try :
                start = datetime.datetime.strptime(self.start_date,
                    '%m/%d/%Y')
            except ValueError :
                start = datetime.datetime.strptime(self.start_date,
                    '%m/%Y')
            try :
                end = datetime.datetime.strptime(self.end_date,
                    '%m/%d/%Y')
            except ValueError :
                end = datetime.datetime.strptime(self.end_date,
                    '%m/%Y')
            #print (self.start_date, 'to', self.end_date + '.',
            #    file = texfile)
            print (start.strftime('%B %Y'), 'to', end.strftime('%B %Y') \
                + '.', file = texfile)
        else :
            try :
                graddate = datetime.datetime.strptime(self.graduation,
                    #'%m/%d/%Y').strftime('%B %-d, %Y')
                    '%m/%d/%Y').strftime('%B %Y')
                # anticipated?
                if datetime.datetime.strptime(self.graduation,'%m/%d/%Y')\
                        > datetime.datetime.now() :
                    graddate += ' (anticipated)'
            except ValueError :
                try :
                    graddate = datetime.datetime.strptime(self.graduation,
                        '%m/%Y').strftime('%B %Y')
                    # anticipated?
                    if datetime.datetime.strptime(self.graduation, \
                            '%m/%Y') > datetime.datetime.now() :
                        graddate += ' (anticipated)'
                except ValueError :
                    graddate = self.graduation
            # print the student's info
            if self.school != constants.SCHOOL :
                print (r'  ', full_name + ',', self.degree + ',',
                    self.major + ',', self.school + ',', graddate + ';',
                    file = texfile)
            else :
                print (r'  ', full_name + ',', self.degree + ',',
                    self.major + ',', graddate + ';', file = texfile)
            try :
                start = datetime.datetime.strptime(self.start_date,
                    #'%m/%d/%Y').strftime('%B %-d, %Y')
                    '%m/%d/%Y').strftime('%B %Y')
            except ValueError :
                start = datetime.datetime.strptime(self.start_date,
                    '%m/%Y').strftime('%B %Y')
            try :
                end = datetime.datetime.strptime(self.end_date,
                    #'%m/%d/%Y').strftime('%B %-d, %Y')
                    '%m/%d/%Y').strftime('%B %Y')
            except ValueError :
                end = datetime.datetime.strptime(self.end_date,
                    '%m/%Y').strftime('%B %Y')
            print (start, 'to', end + '.', file = texfile)
        # This should evaluate to True if advisor is not None and
        # the author is not the sole advisor
        if self.coadvised() :
            if isinstance(self.advisor, str) :
                co_advisors = [self.advisor]
            else :
                co_advisors = list(self.advisor)
            primary = (co_advisors[0] == constants.AUTHOR \
                        or co_advisors[0] in constants.AUTHOR)
            try :
                if isinstance(constants.AUTHOR,str) :
                    co_advisors.remove(constants.AUTHOR)
                else :
                    for auth in constants.AUTHOR :
                        co_advisors.remove(auth)
            except ValueError :
                pass
            if len(co_advisors) == 1 :
                if primary :
                    print (r'  Co-advisor:', co_advisors[0] + '.',
                        file = texfile)
                else :
                    print (r'  Primary advisor:', co_advisors[0] + '.',
                        file = texfile)
            else :
                if primary :
                    print (r'  Co-advisors:', ','.join(co_advisors) + '.',
                        file = texfile)
                else :
                    print (r'  Primary advisor:', co_advisors[0] + ';',
                        file = texfile)
                    print (r'  Co-advisors:', ','.join(co_advisors[1:]) + '.',
                        file = texfile)
        # Funding provided to the student
        if print_funding and len(self.funding_sources()) > 0 :
            print ('    Funding:', self.funding_sources() + '.', file=texfile)
        # Student's current location
        if print_address and self.present_address is not None :
            print (r'    Current affiliation:', self.present_address + '.',
                file = texfile)
        self.end_recent(texfile)

##############################################################################

class GraduateStudent (Student) : # {{{1

    '''A graduate student. No student should be declared explicitly as this
       type of object; instead, use MastersStudent or DoctoralStudent'''

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        try :
            self.start_date = args['start_date']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required key word "start_date"',
                'for class GraduateStudent', file = sys.stderr)
            raise SystemExit(1)

##############################################################################
    # write_thesis_or_dissertation {{{2
    def write_thesis_or_dissertation (self, texfile, show_committee = False,
            end='.') :
        'Outputs the title, year, etc. of a students thesis/dissertation.'
        if self.current :
            return
        print (r'\item ', end='', file = texfile)
        self.begin_recent (texfile)
        # Use the BibTeX key, if present
        if self.key is not None :
            print (r'\bibentry{' + self.key + '}' + end + '%',
                file = texfile)
        else : # if not, use title/year information
            if self.middle is not None :
                author_name = self.first + ' ' + self.middle + ' ' + self.last
            else :
                author_name = self.first + ' ' + self.last
            print (markup_authors(author_name, initials = True), '.',
                sep = '', file = texfile)
            if self.title is not None :
                print (r'    \emph{' + self.title + "}.", file = texfile)
            else :
                print ('WARNING: missing thesis/dissertation title for student',
                    self.last, file = sys.stderr)
            if self.year is None :
                print ('WARNING: missing year for thesis/dissertation for',
                    self.last, file = sys.stderr)
            #print ('   ', self.degree, self.thesis_type + ',',
            print ('   ', self.thesis_type.title() + ',',
                self.school, '(' + str(self.year) + ').', file = texfile)
        # Print the committee members, if desired
        if show_committee :
            if self.committee is not None :
                print (r'\space Committee: ', markup_authors(self.committee,
                    initials=True) + '.', file = texfile)
            else :
                print ('WARNING: missing thesis/dissertation committee for',
                    self.last, file = sys.stderr)
        self.end_recent (texfile)

##############################################################################

    def write (self, texfile, print_funding=False, print_address=False) : #{{{2
        print (r'\item ', file = texfile, end='')
        self.begin_recent(texfile)
        if self.middle is None :
            full_name = self.first + ' ' + self.last
        else :
            full_name = self.first + ' ' + self.middle + ' ' + self.last
        if self.current or self.graduation is None :
            student = ' student'
        else :
            student = ''
        try :
            start = datetime.datetime.strptime(self.start_date,
                '%m/%d/%Y').strftime('%B %Y')
        except TypeError :
            print ("ERROR in start_date for entry", full_name,
                file = sys.stderr)
            raise
        except ValueError :
            start = datetime.datetime.strptime(self.start_date,
                '%m/%Y').strftime('%B %Y')
        if self.end_date is None :
            end = 'present'
        else :
            try :
                end = datetime.datetime.strptime(self.end_date,
                    '%m/%d/%Y').strftime('%B %Y')
            except ValueError :
                end = datetime.datetime.strptime(self.end_date,
                    '%m/%Y').strftime('%B %Y')
            except TypeError :
                print ("ERROR in end_date for entry", full_name,
                    file = sys.stderr)
                raise
        print(r'  ', full_name + ',', self.degree + student + ',',
            self.major.lower() + ',', start, 'to', end + '.',
            file = texfile)
        if self.defense is not None :
            try :
                defdate = datetime.datetime.strptime(self.defense,
                    '%m/%d/%Y').strftime('%B %-d, %Y')
            except ValueError :
                try :
                    defdate = datetime.datetime.strptime(self.defense,
                        '%m/%Y').strftime('%B %Y')
                except ValueError :
                    defdate = self.defense
            print (r'  Defense:', defdate + '.', file = texfile)
        if self.coadvised() :
            if isinstance(self.advisor, str) :
                co_advisors = [self.advisor]
            else :
                co_advisors = list(self.advisor)
            primary = (co_advisors[0] == constants.AUTHOR \
                        or co_advisors[0] in constants.AUTHOR)
            try :
                if isinstance(constants.AUTHOR,str) :
                    co_advisors.remove(constants.AUTHOR)
                else :
                    for auth in constants.AUTHOR :
                        co_advisors.remove(auth)
            except ValueError :
                pass
            if len(co_advisors) == 1 :
                if primary :
                    print (r'  Co-advisor:', co_advisors[0] + '.%',
                        file = texfile)
                else :
                    print (r'  Primary advisor:', co_advisors[0] + '.%',
                        file = texfile)
            else :
                if primary :
                    print (r'  Co-advisors:', ','.join(co_advisors) + '.%',
                        file = texfile)
                else :
                    print (r'  Primary advisor:', co_advisors[0] + ';',
                        file = texfile)
                    print (r'  Co-advisors:', ','.join(co_advisors[1:]) + '.%',
                        file = texfile)
        if print_funding and len(self.funding_sources()) > 0 :
            print ('    Funding:', self.funding_sources() + '.', file=texfile)

        # Student's current location
        if print_address and self.present_address is not None :
            print (r'    Current affiliation:', self.present_address + '.',
                file = texfile)

        self.end_recent (texfile)

##############################################################################

class MastersStudent (GraduateStudent) : # {{{1

    'A Master''s student you advise.'

    def __init__ (self, **args) :
        if 'degree' not in args :
            args['degree'] = 'M.S.'
        super().__init__(**args)
        self.thesis_type = 'thesis'
        if self.degree[0] != 'M' :
            print ("WARNING: Master's student is getting a",
                self.degree + "? (does not start with 'M'?)",
                file = sys.stderr)

##############################################################################

    def description (self) : # {{{2
        if self.current :
            return "Master's student, " + self.major.lower() + ', ' \
                + datestring2monthyear(self.start_date) + ' to ' + \
                ('present' if self.end_date is None \
                           else datestring2monthyear(self.end_date))
        else :
            return self.degree + ', ' + self.major.lower() + ', ' \
                + self.school + ', ' + datestring2monthyear(self.graduation)

##############################################################################

class DoctoralStudent (GraduateStudent) : # {{{1

    'A Ph.D. (or other doctoral degree) student you advise.'

    def __init__ (self, **args) : # {{{2
        if 'degree' not in args :
            args['degree'] = 'Ph.D.'
        super().__init__(**args)
        self.thesis_type = 'dissertation'
        if self.degree not in DOCTORATES :
            print ("WARNING: Doctoral student's degree, ",
                self.degree, ", is not a recognized doctorate.",
                sep = '', file = sys.stderr)
        if 'salutation' not in args and not self.current :
            self.salutation = r'Dr.~\relax'

##############################################################################

    def description (self) : # {{{2
        if self.current :
            return "doctoral student, " + self.major.lower() + ', ' \
                + datestring2monthyear(self.start_date) + ' to ' + \
                ('present' if self.end_date is None \
                           else datestring2monthyear(self.end_date))
        else :
            return self.degree + ', ' + self.major.lower() + ', ' \
                + self.school + ', ' + datestring2monthyear(self.graduation)

##############################################################################

class Postdoc (Employee) : # {{{1

    'A Post-doctoral scholar advised by you.'

    def __init__ (self, **args) : # {{{2
        try :
            self.start_date = args['start_date']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required key word "start_date"',
                'for Postdoc', file = sys.stderr)
            raise SystemExit(1)
        super().__init__(**args)

##############################################################################

    def description (self) : # {{{2
        return "post-doctoral research associate, " \
            + self.major.lower() + ', ' + self.start_date + ' to ' + \
                ('present' if self.end_date is None else self.end_date)

##############################################################################

    def write (self, texfile, print_funding=False, print_address=False) : # {{{2
        print (r'\item ', file = texfile, end='')
        self.begin_recent(texfile)
        if self.middle is None :
            full_name = self.first + ' ' + self.last
        else :
            full_name = self.first + ' ' + self.middle + ' ' + self.last
        print (r'   Dr.~' + full_name + ',', self.degree + ',',
            self.major + ';', self.start_date, 'to',
                ('present' if self.end_date is None else self.end_date),
            #',', self.project, '&', self.funding_sources(), r'\\',
            file = texfile)
        if print_funding and len(self.funding_sources()) > 0 :
            print ('   Funding:', self.funding_sources() + '.', file=texfile)
        if print_address and self.present_address is not None :
            print (r'    Current affiliation:', self.present_address,
                file = texfile)
        self.end_recent (texfile)

##############################################################################

class VisitingProfessor (Employee) : # {{{1

    'A visiting scholar working with your group.'

    def __init__ (self, **args) : # {{{2
        try :
            self.start_date = args['start_date']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required key word "start_date"',
                'for VisitingProfessor', file = sys.stderr)
            raise SystemExit(1)
        super().__init__(**args)

##############################################################################

class GraduateCommittee (Student) : # {{{1

    "A student's dissertation or thesis committee. Use those classes instead."

    def write (self, texfile, print_funding=False, print_address=False) :
        print (r'\item ', file = texfile, end='')
        self.begin_recent(texfile)
        if self.middle is None :
            full_name = self.first + ' ' + self.last
        else :
            full_name = self.first + ' ' + self.middle + ' ' + self.last
        if any(x is None for x in [self.major,self.degree,self.advisor]) :
            print ('Required field missing for', full_name,
                file = sys.stderr)
            raise SystemExit(2)
        if self.current :
            student = ' student,'
        else :
            student = ','
        if self.graduation is not None :
            try :
                graddate = datetime.datetime.strptime(self.graduation,
                    '%m/%d/%Y').strftime('%Y')
            except ValueError :
                try :
                    graddate = datetime.datetime.strptime(self.graduation,
                        '%m/%Y').strftime('%Y')
                except ValueError :
                    graddate = self.graduation
        # Name, degree, etc.
        print ('     ', full_name + ',', self.degree + student,
                self.major + '%', file = texfile)
        # graduation date
        if self.graduation is not None :
            print ('     ,', graddate + '%', file = texfile)
        # advisor(s)
        if isinstance(self.advisor, (list,tuple)) :
            if len(self.advisor) > 1 :
                print ('. Chairs:', list2string(self.advisor) + '.',
                    file = texfile)
            else :
                print ('. Chair:', self.advisor[0] + '.', file = texfile)
        else :
            print ('. Chair:', self.advisor + '.', file = texfile)
        # Defense date
        if self.defense is not None :
            try :
                graddate = datetime.datetime.strptime(self.defense,
                    '%m/%d/%Y').strftime('%B %-d, %Y')
            except ValueError :
                try :
                    graddate = datetime.datetime.strptime(self.defense,
                        '%m/%Y').strftime('%B %Y')
                except ValueError :
                    graddate = self.defense
            #print (r'    \linebreak[3]Defense date:', graddate + '.',
            print (r'    \linebreak[3]Defense:', graddate + r'.\relax',
                file = texfile)
        self.end_recent(texfile)

##############################################################################

class ThesisCommittee (GraduateCommittee) : # {{{1

    "An M.S. student's committee"

    def __init__ (self, **args) :
        if 'degree' not in args :
            args['degree'] = 'M.S.'
        super().__init__(**args)

##############################################################################

class DissertationCommittee (GraduateCommittee) : # {{{1

    "A Ph.D. student's committee"

    def __init__ (self, **args) :
        if 'degree' not in args :
            args['degree'] = 'Ph.D.'
        super().__init__(**args)

##############################################################################

class Collaborator : # {{{1

    'Declares a collaborator for the purposes of the biosketch.'

    def __init__ (self, first, last, institution, middle = None, year = None) :
        self.first = first
        self.last = last
        self.institution = institution
        self.middle = middle
        self.year = year

    def __str__ (self) :
        "Returns a string of the collaborator's full name"
        return(self.first + ' ' + self.last + ' (' + self.institution + ')')

##############################################################################

def write_Collaborators_table (data, bibliography = None, max_age = 2) : # {{{1
    data.update_collaborators(bibliography)
    # remove those longer ago than max_age years
    collab = filter(lambda x: x.year >= datetime.datetime.now().year - max_age,
        data.collaborator)
    collab = list(collab)
    collab = sorted(collab, key=lambda c: c.last)
    # Table 1
    print ("TABLE 1")
    # FIXME: Professor class should know last name vs. rest of name?
    name = data.professor.name.split()
    last = name[-1]
    rest = ' '.join(name[:-1])
    print ('\t', last, ", ", rest, '\t',data.professor.school, sep='')
    print ()

    print ("TABLE 2") # have to do these manually...
    print ("R:\tHammond-Weinberger, Dena R.\tMurray State University")
    print ("R:\tHammond, Pamela I.\tMayo Clinic")
    print ()

    print ("TABLE 3")
    lines = []
    # advisors
    for degree in data.degree :
        if degree.degree in DOCTORATES or degree.degree == 'Postdoc' \
                or (degree.degree in MASTERS and degree.advisor is not None) :
            if isinstance(degree.advisor, str) :
                advisor = [degree.advisor]
                address = [degree.advisor_address]
            else :
                advisor = degree.advisor
                address = degree.advisor_address
            for i in range(len(advisor)) :
                name = advisor[i].split()
                if address[i] is None :
                    affiliation = degree.school + ', ' + address[i]
                else :
                    affiliation = address[i]
                lines.append('G:\t' + name[-1] + ', ' + " ".join(name[:-1]) \
                    + '\t' + affiliation)
    lines = remove_duplicates(lines)
    for line in lines :
        print (line)

    # students
    lines = []
    for student in data.employee :
        if not isinstance(student, GraduateStudent) :
            continue
        if not student.current and student.graduation is not None :
            lines.append('T:\t' + str(student) + '\t' \
                + (student.present_address \
                    if student.present_address is not None \
                    else 'University of Missouri') )
    lines = remove_duplicates(lines)
    for line in lines :
        print (line)
    print ()

    print ('TABLE 4')
    lines = []
    for person in collab :
        lines.append('C:\t' + person.last + ', ' + person.first \
            + ('' if person.middle is None else person.middle) \
            + '\t' + person.institution + '\t\t' + str(person.year) )
    lines = remove_duplicates(lines)
    for line in lines :
        print (line)
    print ()
