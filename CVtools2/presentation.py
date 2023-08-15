from .recent import Recent
from .utilities import markup_authors
import re

class Presentation (Recent) : # {{{1

    'Declares information about a conference proceedings talk or poster.'

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        # Mandatory arguments
        try :
            self.author = args['author']
            self.title = args['title']
            self.location = args['location']
            self.date = args['date']
            self.year = args['year']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required key word for Presentation',
                file = sys.stderr)
            raise SystemExit(1)
        # Defaults
        self.presenter = None
        self.event = None
        self.student = None
        self.undergraduate = None
        self.teaching = False
        self.note = None
        self.role = None
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise KeyError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)
        if self.presenter is None :
            if isinstance(self.author, (list,tuple)) :
                self.presenter = self.author[0]
            else :
                self.presenter = self.author
        # Error checking
        if not isinstance(self.teaching, bool) :
            raise TypeError('Presentation.teaching must be True or False')

##############################################################################

    # def write (self, ...) : {{{2
    def write (self, texfile, show_presenter = True, short = False,
            show_students = True, poster_note = '(poster)') :
        from .constants import AUTHOR, MAX_AUTHORS
        'Formats presentations for output on the CV and dossier'
        print (r'\item', file = texfile)
        self.begin_recent(texfile)
        shortened = False
        if short and isinstance(self.author, (list,tuple)) and \
                len(self.author) > MAX_AUTHORS + 1 :
            authors = self.author[0:MAX_AUTHORS]
            shortened = True
        else :
            authors = self.author
        if show_students :
            students = self.student
            undergraduates = self.undergraduate
        else :
            students = None
            undergraduates = None
        author_list = markup_authors (authors = authors, CV_author = AUTHOR,
            students = students, undergraduates = undergraduates,
            presenter = (self.presenter if show_presenter else None),
            printand = not shortened, initials = True)
        if shortened :
            author_list += r', \emph{et al}' # . gets put on later
        if re.match('[0-9]', self.date[-1]) :
            date_string = self.date + ', ' + str(self.year)
        else :
            date_string = self.date + ' ' + str(self.year)
        if self.event is None :
            print (author_list + '. ``' + self.title + ".''",
                self.location + ',', date_string + '.',
                file = texfile)
        else :
            print (author_list, ". ``",  self.title, ".'' ", 
                self.event, ', ', self.location, ', ', date_string, r'.\relax',
                sep='', file = texfile)
        if self.note is not None :
            if show_presenter :
                note = markup_authors (authors = self.note, CV_author = AUTHOR,
                    presenter = self.presenter, students = students,
                    undergraduates = undergraduates)
            else :
                note = markup_authors (authors = self.note, CV_author = AUTHOR,
                    students = students, undergraduates = undergraduates)
            note = r'\space\emph{' + note + '}'
            if note[-2] == '.' :
                print (note, file = texfile)
            else :
                print (note + r'.\relax', file = texfile)
        if isinstance(self,Poster) :
            print (r'     \space', poster_note, r'\relax',
                sep='', file = texfile)
        if isinstance(self, InvitedTalk) and self.invited_by is not None :
            print (r'\space\emph{Invited by', self.invited_by + '}.%',
                file = texfile)
        self.end_recent(texfile)

##############################################################################

class Poster (Presentation) : # {{{1
    'A poster presentation.'
    pass

##############################################################################

class InvitedTalk (Presentation) : # {{{1
    'An invited presentation at a university, conference, etc.'
    def __init__ (self, **args) : # {{{2
        self.invited_by = None
        super().__init__(**args)

##############################################################################

class Interview (InvitedTalk) : # {{{1
    'An interview presentation at a university, national laboratory, etc.'
    pass
    #def __init__ (self, **args) : # {{{2
    #    super().__init__(**args)
