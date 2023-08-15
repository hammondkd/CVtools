__all__ = ['Degree']

from .utilities import list2string

# Doctoral degrees we recognize
DOCTORATES = ['Ph.D.','PhD','D.Phil.','D.Eng.','M.D.','MD','D.Mu.','DDS',
    'D.D.S.','Ed.D.','D.Ed.','J.D.','JD','D.F.A.','D.M.','D.M.E.','D.M.A.',
    'A.Mus.D.','D.Mus.A.','D.N.Sc.','O.T.D.','D.P.E.','Dr.P.H.','D.Sc.',
    'Sc.D.','Th.D.','D.S.W.']

MASTERS = ['M.S.','M.A.','MPhil','M.Phil.','MSc','MBA','M.B.A.','LLM','LL.M.',
    'MChem','MEng','M.E.','MMath','MPharm','MPhys','MPsych','Msci']

class Degree : # {{{1
    'Gives information about a degree earned.'
    def __init__ (self, degree, major, school, address, year,
            longschool = None,
            thesis_title = None,
            dissertation_title = None,
            advisor = None, advisor_address = None,
            order = 1,
            postdoc = False) :
        self.degree = degree
        self.major = list2string(major)
        self.school = school
        self.longschool = longschool
        self.address = address
        self.year = year
        self.thesis_title = thesis_title
        self.dissertation_title = dissertation_title
        self.advisor = advisor
        self.advisor_address = advisor_address
        self.order = order
        self.postdoc = postdoc
        if isinstance(self.advisor, (list,tuple)) and \
                ( self.advisor_address is not None and \
                  len(advisor_address) != len(advisor) ) :
            raise ValueError ('"advisor_address" must be either None or the'
                + ' same length as "advisor"')

##############################################################################

    def write (self, texfile, longform = False) :
        print (self.degree + ',', self.major + ',',
            self.school + ',', self.address, '(' + str(self.year) + ')',
            file = texfile)
        if longform :
            if self.dissertation_title is not None :
                print (r"\\ Dissertation: \emph{" + self.dissertation_title
                    + '}', file = texfile)
            elif self.thesis_title is not None :
                print (r"\\ Thesis: \emph{" + self.thesis_title + '}\\',
                    file = texfile)
            if self.advisor is not None :
                advisors = list2string(self.advisor)
                if advisors.find(' and') == -1 :
                    print (r'\\ Advisor:', advisors, file = texfile)
                else :
                    print (r'\\ Advisors:', advisors, file = texfile)
        print (r'  \par', file = texfile)
