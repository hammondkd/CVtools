import re
import sys
import time
from .recent import Recent
from . import recent
from . import constants
from .utilities import markup_authors, toordinal

class Publication (Recent) : # {{{1

    '''Declares information about a journal article, book chapter, or similar
       publication.'''

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        try :
            self.year = args['year']
        except KeyError :
            raise KeyError ('Missing year in Publication')
        # Defaults
        self.key = None
        self.teaching = False 
        self.peer_reviewed = True
        self.status = constants.PUBLISHED
        self.doi = None
        self.author = None
        self.title = None
        self.booktitle = None
        self.month = None
        self.publisher = None
        self.journal = None
        self.volume = None
        self.number = None
        self.pages = None
        self.note = None
        self.address = None
        self.editor = None
        self.series = None
        self.school = None
        self.chapter = None
        self.thesis_type = None
        self.student = None
        self.undergraduate = None
        self.corauth = None
        self.most_significant = False
        self.significant = False
        self.journal_IF = None
        self.journal_immediacy = None

        self.primary = False
        self.post_appointment = None
        self.post_tenure = None
        self.wos_update_url = None
        self.role = None
        self.ncites_wos = 0
        self.ncites_scopus = 0
        self.ncites_google = 0
        self.cite_years_wos = []
        self.cite_years_scopus = []
        self.citing_dois_wos = []
        self.cite_years_google = []
        self.citing_dois_scopus = []
        self.citing_dois_google = []
        self.citable = True
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise AttributeError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)
        if self.post_appointment is None :
            self.post_appointment = recent.POST_APPOINTMENT
        if self.post_tenure is None :
            self.post_tenure = recent.POST_TENURE
        self.ncites = max(self.ncites_wos, self.ncites_scopus, 
            self.ncites_google)
        # Error checking
        if not isinstance(self.teaching, bool) :
            raise TypeError('Publication.teaching must be True or False')
        if not isinstance(self.peer_reviewed, bool) :
            raise TypeError('Publication.peer_reviewed must be True or False')
        if not isinstance(self.most_significant, bool) :
            raise TypeError('Publication.most_significant must be True or False')
        if not isinstance(self.significant, bool) :
            raise TypeError('Publication.significant must be True or False')
        if not isinstance(self.primary, bool) :
            raise TypeError('Publication.primary must be True or False')
        if not isinstance(self.post_appointment, bool) :
            raise TypeError('Publication.post_appointment must be True, False, or None')
        if not isinstance(self.post_tenure, bool) :
            raise TypeError('Publication.post_tenure must be True, False, or None')
        # Check for inconsistent citation entries
        length = len(self.cite_years_scopus)
        if length > 0 and self.ncites_scopus != length :
            print ("WARNING: ncites_scopus is inconsistent for entry ", self,
                ' (', self.ncites_scopus, ' vs. ', length, ')',
                sep='', file=sys.stderr)
        length = len(self.cite_years_wos)
        if length > 0 and self.ncites_wos != length :
            print ("WARNING: ncites_wos is inconsistent for entry ", self,
                ' (', self.ncites_wos, ' vs. ', length, ')',
                sep='', file=sys.stderr)

##############################################################################

    def __str__ (self) : # {{{2
        if self.key is not None :
            return self.key
        elif self.doi is not None :
            return self.doi
        elif self.title is not None :
            return self.title
        elif self.booktitle is not None :
            return self.booktitle
        raise ValueError

##############################################################################

    def write (self, texfile, end='.') : # {{{2

        '''Writes out an entry about a particular publication. Assumes it is
        part of a list, either itemized or enumerated.'''

        print (r'\item', end=' ', file = texfile)
        self.begin_recent(texfile)
        if self.key is not None :
            print (r'\bibentry{' + self.key + '}' + end + r'\relax',
                file = texfile)
        else :
            author_list = markup_authors (authors = self.author,
                CV_author = constants.AUTHOR, students = self.student,
                undergraduates = self.undergraduate, initials = True,
                corauth = self.corauth)
            print (author_list + ".", file = texfile)
            if self.title is not None :
                print ("``" + self.title + ".''", file = texfile)
            if self.journal is not None :
                print (r'\emph{' + self.journal + '}', file = texfile)
            if self.booktitle is not None :
                print (r'\emph{' + self.booktitle + '},', file = texfile)
            if self.series is not None :
                print (r'\emph{' + self.series + '},', file = texfile)
            if self.editor is not None :
                editor_list = markup_authors (authors = self.editor,
                    CV_author = constants.AUTHOR, students = self.student,
                    undergraduates = self.undergraduate,
                    initials = True)
                if isinstance(self.editor, (tuple,list)) \
                        and len(self.editor) > 1 :
                    print (editor_list + ', Eds.', file = texfile)
                elif isinstance(self.editor, (tuple,list)) \
                        and len(self.editor) == 1 :
                    print (editor_list[0] + ', Eds.', file = texfile)
                else :
                    print (editor_list + ', Eds.', file = texfile)
            if self.volume is not None :
                if self.number is not None :
                    print (r'\textbf{' + str(self.volume) + '}~(' + \
                        str(self.number) + '): ', file = texfile, end = '')
                else :
                    print (r'\textbf{' + str(self.volume) + '}: ',
                        file = texfile, end = '')
            if self.pages is not None :
                print (self.pages, file = texfile)
            else :
                print (' ', end = '', file = texfile)
            if self.publisher is not None :
                print ('   ', self.publisher + ',', file = texfile)
            if self.thesis_type is not None :
                print ('   ', self.thesis_type + ',', file = texfile)
            if self.school is not None :
                print ('   ', self.school + ',', file = texfile)
            if self.address is not None :
                print ('   ', self.address + ',', file = texfile)
            if self.year is not None :
                if self.booktitle is not None :
                    print (str(self.year) + '.', file = texfile)
                else :
                    if self.month is not None :
                        print ('(' + #str(self.month),
                        str(self.year) + r').', file = texfile)
                    else :
                        print ('(' + str(self.year) + r').',
                            file = texfile)
            else :
                if self.key is not None :
                    raise ValueError ('No year for entry ' + str(self.key))
                else :
                    raise ValueError ('No year for entry "' \
                        + str(self.title) + '"')
            if self.chapter is not None :
                print ('Chapter', str(self.chapter) + '.', file = texfile)
            if self.note is not None :
                print (self.note + r'\relax', file = texfile)
            if (self.pages == 'in press' or self.pages == '(in press)') \
                    and self.doi is not None :
                print ('DOI:', self.doi + '.', file = texfile)

        self.end_recent(texfile)

##############################################################################

    def write_citations (self, texfile) : # {{{2

        'Prints "[Cited X times in (a database)]" after an entry.'

        if self.ncites_scopus > 0 or self.ncites_wos > 0 :
            print (r'  \space', file = texfile, end='')
            self.begin_recent(texfile)
            if self.ncites_scopus > self.ncites_wos :
                print (r'[Cited', toordinal(self.ncites_scopus),
                    'in Scopus]', file = texfile)
            elif self.ncites_scopus == self.ncites_wos :
                print (r'[Cited', toordinal(self.ncites_scopus),
                    'in Scopus and Web of Science]', file = texfile)
            else :
                print (r'[Cited', toordinal(self.ncites_wos),
                    'in Web of Science]', file = texfile)
            self.end_recent(texfile)

##############################################################################

    def write_role (self, texfile) : # {{{2

        '''Prints the role the author had in a publication. Example:
        corresponding author; made the figures, wrote most text, editing.'''

        if self.role is None :
            return
        self.begin_recent(texfile)
        print (r'\begin{role}Role: ', self.role, r'\end{role}',
            sep = '', file = texfile)
        self.end_recent(texfile)

##############################################################################

    def write_journal_stats (self, texfile) : # {{{2

        '''Prints statistics about the journal that the author has entered.
        This is, at present, the journal's impact factor and its immediacy
        index during that year. These values are available from Journal
        Citation Reports (Thomson-Reuters).'''

        if any((self.journal_IF,self.journal_immediacy)) :
            self.begin_recent(texfile)
        if self.journal_IF is not None :
            print (r"\nopagebreak Periodical's impact factor (", self.year,
                '): ', "{:.3f}".format(self.journal_IF),
                sep = '', file = texfile)
        if self.journal_immediacy is not None :
            print (r"\\* Periodical's immediacy index (", self.year, '): ',
                "{:.3f}".format(self.journal_immediacy),
                sep = '', file = texfile)
        if any((self.journal_IF,self.journal_immediacy)) :
            self.end_recent(texfile)

##############################################################################

    def update_Google (self, browser=None) : # {{{2

        '''Updates Google Scholar citation counts. Whether it works varies
           with Google's paranoia and is an open question.'''

        import selenium.webdriver
        import urllib.parse
        if not self.citable : # skip non-citable publications
            return
        if self.status != constants.PUBLISHED : # and unpublished stuff
            return
        if self.title is not None :
            try :
                query_string = re.sub(r'\\[a-zA-Z]+{([^}]+)}', r'\1',
                    self.title)
                query_string = re.sub(r'\$', '', query_string)
            except TypeError :
                print ("WARNING: unable to update Google Scholar citations",
                    "for key", self.key, file = sys.stderr)
                return
        elif self.doi is not None :
            query_string = self.doi
        else :
            try :
                query_string = re.sub(r'\\[a-zA-Z]+{([^}]+)}', r'\1',
                    self.booktitle)
                query_string = re.sub(r'\$', '', query_string)
            except TypeError :
                print ("WARNING: unable to update Google Scholar citations",
                    "for key", self.key, file = sys.stderr)
                return
        # Pause for a while so Google doesn't think you're a robot
        time.sleep(constants.GOOGLE_TIME_BETWEEN)
        # Start the browser, if necessary
        close_browser = False
        if browser is None :
            options = selenium.webdriver.firefox.options.Options()
            options.set_headless()
            assert options.headless
            browser = selenium.webdriver.Firefox (options = options)
            close_browser = True
        ncites_google = 0
        try :
            browser.get('https://scholar.google.com/scholar?hl=en&q=' \
                + urllib.parse.quote(query_string, safe='') )
            anchors = browser.find_elements_by_tag_name('a')
            href = None
            for a in anchors :
                if 'Cited by' in a.text :
                    ncites_google = int(a.text.split()[-1])
                    href = a.get_attribute('href')
                    break
            else :
                headings = browser.find_elements_by_tag_name('h1')
                for h in headings :
                    if 'not a robot' in h.text or 'unusual traffic' in h.text :
                        if self.key is not None :
                            print ("Updating key", self.key, file=sys.stderr)
                        elif self.title is not None :
                            print ("Updating '" + self.title + "'",
                                file=sys.stderr)
                        print ("ERROR. Google thinks I'm a robot. Exiting.",
                            file = sys.stderr)
                        input('press enter to retry')
                print ("WARNING: couldn't find 'Cited by' for key", \
                    (self.key if self.key is not None else self.title),
                    file = sys.stderr)
                input('press enter to retry')

            if ncites_google != self.ncites_google :
                if self.key is not None :
                    print ('WARNING:  ncites_google is out of date for',
                        'entry', self.key, '(' + str(self.ncites_google),
                        '-->', str(ncites_google) + ')', file = sys.stderr)
                    # Update citation counts
                    old_cite_years_google = list(self.cite_years_google)
                    if len(self.cite_years_google) > 0 :
                        for year in \
                                reversed(range(min(self.cite_years_google), \
                                    max(self.cite_years_google)+1)) :
                            a = old_cite_years_google.count(year)
                            b = self.cite_years_google.count(year)
                            if a != b :
                                print (a, '*[', year, '] -> ', b,
                                    '*[', year, ']', sep = '')
                else :
                    print ('WARNING:  ncites_google is out of date for',
                        'entry', str(self), '(' + str(self.ncites_google),
                        '-->', str(ncites_google) + ')', file = sys.stderr)
                print ('Google Scholar URL is',
                    'https://scholar.google.com/scholar?q=', end='')
                if self.title is not None :
                    print (urllib.parse.quote(self.title))
                else :
                    print (urllib.parse.quote(self.doi))
            self.ncites_google = ncites_google
        finally :
            if close_browser :
                browser.close()
        self.ncites = max(self.ncites_wos, self.ncites_scopus,
            self.ncites_google)

##############################################################################

    def update_Google_years (self, browser, url) : # {{{2

        'Updates Google Scholar citation years'

        years = range(self.year, datetime.date.today().year + 1)
        cite_years = self.cite_years_google
        for year in years :
            time.sleep(WAIT_TIME)
            browser.get(url + '&as_ylo=' + str(year) + '&as_yhi=' + str(year))
            tags = browser.find_elements_by_class_name('gs_ab_mdw')
            for tag in tags :
                if 'result' in tag.text :
                    field = tag.text.split()
                    ninyear = int(field[0])
                    while ninyear > cite_years.count(year) :
                        cite_years.append(year)
                    #cite_years.sort(reverse=True)

##############################################################################

    def update_Scopus (self) : # {{{2

        'Update citations from Scopus. (obsolete)'

        if self.doi is None :
            return
        else :
            citedata = subprocess.Popen ('wget -q --header '
                + '"X-ELS-APIKey:' + SCOPUS_API_KEY + '" '
                + '"http://api.elsevier.com/content/search/scopus?query=DOI('
                + self.doi + ')&field=citedby-count" -O -',
                shell=True, stdout=subprocess.PIPE)
            output = str(citedata.communicate()[0])
            try :
                citestr = output.rpartition('"citedby-count":')[-1]
                citestr = citestr.lstrip('":').rstrip('}]\"\'')
                ncites_scopus = int(citestr)
                if self.ncites_scopus != ncites_scopus :
                    print ('WARNING:  ncites_scopus is out of date for',
                        'entry', str(self), '(' + str(self.ncites_scopus),
                        '-->', str(ncites_scopus) + ')', file = sys.stderr)
                self.ncites_scopus = ncites_scopus
                self.ncites = max(self.ncites_wos, self.ncites_scopus,
                    self.ncites_google)
            except ValueError :
                print ('WARNING:  unable to extract Scopus cite count for key',
                    self.key, file = sys.stderr)

##############################################################################

    def update_MSacad (self) : # {{{2
        'Update citations from Microsoft Academic. (They suck....)'
        if self.doi is None :
            self.ncites_MSacad = 0
        else :
            p1 = subprocess.Popen (r'wget -q -O - "http://academic.research.microsoft.com/Search?query=doi(' + self.doi + ')"',
                shell=True, stdout=subprocess.PIPE)
            p2 = subprocess.Popen ('fgrep -i Citations', shell=True,
                stdin=p1.stdout, stdout=subprocess.PIPE)
            output = str(p2.communicate()[0])
            output = re.sub(r'.*>Citations:\s*', '', output)
            output = re.sub(r'</a>.*', '', output)
            try :
                self.ncites_MSacad = int(output)
            except ValueError :
                self.ncites_MSacad = 0
            print ('article: ', self.key, '; MSacad_cites:',
                self.ncites_MSacad, file=sys.stderr)

##############################################################################

    def update_Scopus_years (self) : # {{{2

        'Update the citation counts from each year from Scopus. (obsolete)'

        if self.doi is None :
            return
        else :
            citedata = subprocess.Popen ('wget -q --header '
                + '"X-ELS-APIKey: ' + SCOPUS_API_KEY + '" '
                + '"http://api.elsevier.com/content/search/scopus?query=DOI('
                + self.doi + ')" -O -',
                shell=True, stdout=subprocess.PIPE)
            output = str(citedata.communicate()[0])
            if re.search ('scopus-citedby', output) :
                citestr = output.rpartition('"scopus-citedby", "@href": "')[-1]
                citestr = citestr.partition('}')[0]
                url = citestr.rstrip('"')
                # FIXME:  Hack until you are able to solve the problem
                if ( len(self.cite_years_scopus) != self.ncites_scopus ) :
                    print ('URL for updating Scopus years for', self.key,
                        'is', url)
                return
                # END HACK
                citedata = subprocess.Popen ('wget -q --header '
                    + '"X-ELS-APIKey:' + SCOPUS_API_KEY + '" "'
                    + url + '" -O -', shell=True, stdout=subprocess.PIPE)
                output = citedata.communicate()[0]
                flag = False
                years = []
                for line in output.split('\n') :
                    if re.match ('<span class="">', line) :
                        continue
                    if re.match('</span>', line) :
                        flag = False
                        continue
                    if flag :
                        years.append(int(line))
                    if re.match('<label class="hidden-label">Year the Document was Publish</label>', line) :
                        flag = True
                        continue
                print ('key: ', self.key, '; years =', years,
                    '; self.cite_years =', self.cite_years_scopus,
                    file=sys.stderr)
                print ('url:  "' + url + '"', file=sys.stderr)
                print ('output:', output)
                y = self.cite_years_scopus[:]
                extras = []
                while years > y :
                    extras.append(years.pop(0))
                if len(extras) > 0 :
                    print ('WARNING:  cite_years_scopus is out of date for',
                            'entry', str(self) + ';',
                            'these dates seem to be missing:', extras)
                    self.cite_years_scopus = extras + self.cite_years_scopus
            elif re.search ('Result set was empty', output) :
                print('WARNING:  No document found for key', self.key,
                    'with DOI', self.doi, file=sys.stderr)
            else :
                print('WARNING:  unable to extract Scopus cited document URL',
                    'from this:', file = sys.stderr)
                print(output, file=sys.stderr)

##############################################################################

class JournalArticle (Publication) : # {{{1
    'An article in a journal.'
    pass

##############################################################################

class BookChapter (Publication) : # {{{1
    'A book chapter, as in a collection.'
    pass

##############################################################################

class ConferenceProceedings (Publication) : # {{{1
    'An article in a conference proceedings.'
    pass

##############################################################################

class Book (Publication) : # {{{1
    'A book. Typically not peer-reviewed.'
    def __init__ (self, **args) :
        if 'peer_reviewed' in args :
            super().__init__(**args)
        else :
            super().__init__(peer_reviewed = False, **args)

##############################################################################

class Patent (Recent) : # {{{1

    'Information about a patent.'

    def __init__ (self, **args) : # {{{2
        super().__init__(**args)
        # Defaults
        self.key = None
        self.pending = False
        self.author = None
        self.title = None
        self.number = None
        self.year = None
        self.month = None
        self.student = None
        self.undergraduate = None
        for (arg,value) in args.items() :
            if hasattr(self,arg) :
                setattr(self,arg,value)
            else :
                raise AttributeError ('class ' + self.__class__.__name__ \
                    + ' does not define the key word ' + arg)
        # Error checking
        if not isinstance(self.pending, bool) :
            raise TypeError('Patent.pending must be True or False')

##############################################################################

    def write (self, texfile, end='.') : # {{{2
        self.begin_recent(texfile)
        if self.key is not None :
            print (r'\item \bibentry{' + self.key + '}' + end + '%',
                file = texfile)
        else :
            author_list = markup_authors (authors = self.author,
                CV_author = constants.AUTHOR, students = self.student,
                undergraduates = self.undergraduate, initials = True)
            print (r'\item', author_list + ".", file = texfile)
            if self.title is not None :
                print ("``" + self.title + ".''", file = texfile)
            if self.number is not None :
                print ("United States Patent",
                    add_commas_to_number(self.number), file = texfile)
            if self.year is not None :
                print ('(' + str(self.year) + ').', file = texfile)
        self.end_recent(texfile)
