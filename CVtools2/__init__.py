'''Module for storing and generating career-long curricula vitarum.  

Intended for academics, though other disciplines should be handled without
intervention. To get started:

from CVtools import *
set_INVESTIGATOR([your name]) # used to embolden names in grants
set_AUTHOR([your full name]) # used to embolden names in
    # presentations and publications that don't have BibTeX keys
    # Can be a list or tuple if you use more than one name
set_SCHOOL([where you work now])
CV = CV_data()

You set your name with CV.professor = Professor() [see Professor class]

Now you use CV.append() to append degrees, publications, awards, etc. via
their respective classes.

At the end of your CV input file, append this:

if __name__ == '__main__' :
    write_CV([arguments])
    write_Dossier([arguments])
    write_NSF_Biosketch([arguments])

these will actually create the CV (short form), CV (long form), and
biosketch (two pages). This class should accompany the file MU-dossier.cls,
the LaTeX class that provides the formatting specification for the
aforementioned three files.

The aforementioned steps, with the exception of entering your name and such,
can be accomplished by running "python CVtools" or executing
CVtools.create_new_user
'''

from .constants import *
#from .utilities import *
from .utilities import remove_duplicates
from .recent import *
from .professor import Professor
from .degree import Degree
from .job import Job
from .award import Award
from .news import NewsCoverage
from .grant import Grant

from .course import courses_from_this_school, Course, UndergraduateCourse, \
    GraduateCourse, TeachingAssistantship

from .employee import UndergraduateStudent, MastersStudent, DoctoralStudent, \
    Postdoc, VisitingProfessor, ThesisCommittee, DissertationCommittee, \
    Collaborator, write_Collaborators_table

from .presentation import Presentation, Poster, InvitedTalk, Interview

from .publication import JournalArticle, BookChapter, ConferenceProceedings, \
    Book, Patent, Publication
    # FIXME try to remove Publication from the public interface?

from .service import InternationalService, NationalService, RegionalService, \
    UniversitySystemService, UniversityService, CollegeService, \
    DepartmentService, SocietyMembership, ReviewPanel, ManuscriptReview, \
    RegionalConferenceChair, NationalConferenceChair, \
    InternationalConferenceChair, \
    RegionalSessionChair, NationalSessionChair, InternationalSessionChair

from .data import CV_data

from .makeCV import write_CV
from .makeDossier import write_Dossier
from .makeBiosketch import write_NSF_Biosketch
from .makeListOfPapers import write_List_of_Papers

from .__main__ import create_new_user
