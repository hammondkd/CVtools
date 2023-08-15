__all__ = ("DEPT_TEACHING_AVERAGE", "COLLAB_AGE",
    "set_AUTHOR", "set_INVESTIGATOR", "set_SCHOOL",
    "set_SCOPUS_API_KEY", "set_WOS_USERNAME", "set_WOS_PASSWORD",
    'PUBLISHED', 'ACCEPTED', 'INPRESS', 'SUBMITTED', 'UNSUBMITTED')

DEPT_TEACHING_AVERAGE = 4.16 # FIXME

AUTHOR = None
INVESTIGATOR = None
SCHOOL = 'University of Missouri'
UNIVTHE = 'The'
SCOPUS_API_KEY = None
WOS_USERNAME = None
WOS_PASSWORD = None
MAX_LENGTH = 20 # maximum length of a Scopus citation list by default
MAX_AUTHORS = 5 # maximum length of author list on a presentation for the CV
MAX_SCOPUS_QUERIES = 25
MAX_CV_PAGES = 25 # set by the Provost's call letter
PRINT_CITATION_COUNTS = True
PLOT_WOS_CITATIONS_PER_YEAR = False
SHOW_CITES_TO_MOST_CITED_PAPER = False

IDENTIFY_MINIONS = True # by default, we italicize students, undergrads, etc.

# Years ago that we track collaborators
COLLAB_AGE = 4

# Publication status
PUBLISHED = 0
ACCEPTED = INPRESS = 1
SUBMITTED = 2
UNSUBMITTED = 3

WAIT_TIME = 3
GOOGLE_TIME_BETWEEN = 3

def set_SCOPUS_API_KEY (key) :
    global SCOPUS_API_KEY
    SCOPUS_API_KEY = key

def set_WOS_USERNAME (username) :
    global WOS_USERNAME
    WOS_USERNAME = username

def set_WOS_PASSWORD (password) :
    global WOS_PASSWORD
    WOS_PASSWORD = password

def set_AUTHOR (newauthor) :
    global AUTHOR
    AUTHOR = newauthor

def set_SCHOOL (newschool, the = True) :
    global SCHOOL, UNIVTHE
    SCHOOL = newschool
    if the :
        UNIVTHE = 'The'
    else :
        UNIVTHE = ''

def set_INVESTIGATOR (newinvestigator) :
    global INVESTIGATOR
    INVESTIGATOR = newinvestigator
