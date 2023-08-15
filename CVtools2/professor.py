from .degree import DOCTORATES, MASTERS

class Professor : # {{{1

    '''Declares the CV author's name, rank, department, and so forth.'''

    def __init__ (self, name, highest_degree, rank, department,
            school, office, city, state, zipcode, phone, email,
            website = None) :
        self.name = name
        self.highest_degree = highest_degree
        if highest_degree not in DOCTORATES :
            print ('WARNING: highest_degree is not a recognized doctorate',
                'for Professor', name, file = sys.stderr)
        self.rank = rank
        self.department = department
        self.school = school
        self.office = office
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.phone = phone
        self.email = email
        self.website = website

##############################################################################

    def write (self, texfile, large = False) :
        "Prints the professor's same, department, etc."
        if large :
            large = r'\large'
        else :
            large = r''
        iline = r'\hbox{}\hfill'
        eline = r'\hfill\hbox{}\\'
        eline = r'\\'
        iline = r''
        print (r'\vspace{3ex}', file = texfile)
        print (iline, '{' + large + r'\textbf{' + self.name + ',',
            self.highest_degree + r'}}', eline + r'[0.25\baselineskip]',
            file = texfile)
        print (iline, self.rank, eline, file = texfile)
        print (iline, self.department, eline, file = texfile)
        print (iline, self.school, eline, file = texfile)
        print (iline, self.city + ',', self.state + r' \,'
            + str(self.zipcode), eline, file = texfile)
        print (iline + r'\texttt{', self.email + '}', eline, file = texfile)
        if ( self.website is not None ) :
            print (iline, r'\url{', self.website, '}', file = texfile)

##############################################################################

    def write_address (self, texfile) :
        'Prints the professor''s address'
        print (r'\textbf{' + self.name + ', '
            + self.highest_degree + r'} \\[0.25\baselineskip]',
            file = texfile)
        print (self.department, r'\\', self.school, r'\\', file = texfile)
        print (self.city + ',', self.state, r'\,' + str(self.zipcode),
            r'\\', file = texfile)
        print (self.phone, r'\\', file = texfile)
        # August 10, 2019: removed the texttt command because OSPA keeps
        # freaking out about there being a different font
        #print (r'\texttt{' + self.email + '}', file = texfile)
        print (self.email, file = texfile)
