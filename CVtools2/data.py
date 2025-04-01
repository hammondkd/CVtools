__all__ = ['CV_data']

import re
import requests
import os
import sys
from math import ceil
from . import constants
from .pub_stats import PubCount, PubStats
from .professor import Professor
from .degree import Degree
from .job import Job
from .course import Course
from .employee import Employee, Collaborator
from .grant import Grant
from .presentation import Presentation
from .publication import Publication, Patent
from .news import NewsCoverage
from .service import SocietyMembership, ReviewPanel, SessionChair, \
    ManuscriptReview, Service
from .award import Award
from .pub_stats import OptimumOrdinate

class CV_data : # {{{1

    '''Main class containing all information for the CV, Dossier,
       and Biosketch.'''

    def __init__ (self) : # {{{2
        self.professor = None
        self.degree = []
        self.jobhistory = []
        self.course = []
        self.employee = []
        self.service = []
        self.technology = []
        self.teaching_development = []
        self.student_engagement = []
        self.award = []
        self.grant = []
        self.publication = []
        self.presentation = []
        self.patent = []
        self.news = []
        self.society = []
        self.panel = []
        self.session = []  # i.e., chaired a session at a meeting
        self.journal_review = []
        self.service = []
        self.synergistic = []
        self.research_interests = []
        self.collaborator = []
        self.texfile = None
        self.texfile_name = None
        self.count = PubCount()

##############################################################################

    def append (self, x) : # {{{2

        'Determines to which array the next class should be appended.'

        if isinstance(x, Professor) :
            self.professor.append (x)
        elif isinstance(x, Degree) :
            self.degree.append (x)
        elif isinstance(x, Job) :
            self.jobhistory.append (x)
        elif isinstance(x, Course) :
            self.course.append (x)
        elif isinstance(x, Employee) :
            self.employee.append (x)
        elif isinstance(x, Collaborator) :
            self.collaborator.append (x)
        elif isinstance(x, Grant) :
            self.grant.append (x)
        elif isinstance(x, Presentation) :
            self.presentation.append (x)
        elif isinstance(x, Publication) :
            self.publication.append (x)
        elif isinstance(x, Patent) :
            self.patent.append (x)
        elif isinstance(x, NewsCoverage) :
            self.news.append (x)
        elif isinstance(x, SocietyMembership) :
            self.society.append (x)
        elif isinstance(x, ReviewPanel) :
            self.panel.append (x)
        elif isinstance(x, SessionChair) :
            self.session.append (x)
        elif isinstance(x, ManuscriptReview) :
            self.journal_review.append (x)
        elif isinstance(x, Service) :
            # FIXME: This should remove/merge services that are duplicates
            self.service.append (x)
        elif isinstance(x, Award) :
            self.award.append (x)
        else :
            raise TypeError

##############################################################################

    def insert (self, i, x) : # {{{2

        'Inserts a record elsewhere in the appropriate array.'

        if isinstance(x, Professor) :
            self.professor.insert (i,x)
        elif isinstance(x, Degree) :
            self.degree.insert (i,x)
        elif isinstance(x, Job) :
            self.jobhistory.insert (i,x)
        elif isinstance(x, Course) :
            self.course.insert (i,x)
        elif isinstance(x, Employee) :
            self.employee.insert (i,x)
        elif isinstance(x, Collaborator) :
            self.collaborator.insert (i,x)
        elif isinstance(x, Grant) :
            self.grant.insert (i,x)
        elif isinstance(x, Presentation) :
            self.presentation.insert (i,x)
        elif isinstance(x, Publication) :
            self.publication.insert (i,x)
        elif isinstance(x, Patent) :
            self.patent.insert (i,x)
        elif isinstance(x, NewsCoverage) :
            self.news.insert (i,x)
        elif isinstance(x, SocietyMembership) :
            self.society.insert (i,x)
        elif isinstance(x, ReviewPanel) :
            self.panel.insert (i,x)
        elif isinstance(x, SessionChair) :
            self.session.insert (i,x)
        elif isinstance(x, ManuscriptReview) :
            self.journal_review.insert (i,x)
        elif isinstance(x, Service) :
            self.service.insert (i,x)
        elif isinstance(x, Award) :
            self.award.insert (i,x)

##############################################################################

    def update_Scopus (self) : # {{{2

        '''Updates the times a paper has been cited, according to Scopus.
           Doing this requires a Scopus API key.'''

        print ("Updating Scopus citation information")
        # compile list of all DOIs to look for
        doi_list = []
        for pub in self.publication :
            if pub.doi is not None :
                doi_list.append(pub.doi)
        # split DOI list into groups of constants.MAX_SCOPUS_QUERIES
        num_queries = len(doi_list) // constants.MAX_SCOPUS_QUERIES + 1
        doi_query = []
        for i in range(num_queries) :
            doi_query.append([])
        for i in range(len(doi_list)) :
            doi_query[i//constants.MAX_SCOPUS_QUERIES].append(doi_list[i])
        # check for empty list (occurs if len(doi_list)/constants.MAX_SCOPUS_QUERIES==0)
        if doi_query[-1] == [] :
            doi_query.pop(-1)
        # send query
        for i in range(len(doi_query)) :
            citedata = requests.get('http://api.elsevier.com/content/search/'
                  + 'scopus?query=DOI(' + ')+OR+DOI('.join(doi_query[i]) + ')',
                headers = {'Accept':'application/json',
                    'X-ELS-APIKey': constants.SCOPUS_API_KEY})
            output = citedata.json()
            if 'search-results' not in output :
                print ('KeyError: search invalid for DOI', doi_query,
                    file = sys.stderr)
                print ('       output is:', output, file = sys.stderr)
                raise SystemExit(1)
            for pub in output['search-results']['entry'] :
                if 'prism:doi' not in pub :
                    continue
                for pub2 in self.publication :
                    if pub2.doi == pub['prism:doi'] :
                        # we check for a bad connection here
                        try :
                            ncites_scopus = int(pub['citedby-count'])
                        except KeyError :
                            print ('KeyError: "citedby-count" not found in',
                                'list of keys in publication', pub2.doi + ';',
                                'is Scopus available?', file = sys.stderr)
                            raise SystemExit(1)
                        # 1/23/2020: added a check for the cite_years counts
                        # not adding up to ncites_scopus
                        if pub2.ncites_scopus != ncites_scopus \
                              or len(pub2.cite_years_scopus) != ncites_scopus :
                            if pub2.key is not None :
                                print ('WARNING: ncites_scopus is inconsistent',
                                    'for entry', pub2.key,
                                    '(' + str(pub2.ncites_scopus), '-->',
                                    pub['citedby-count'] + ')',
                                    file = sys.stderr)
                            else :
                                print ('WARNING: ncites_scopus is inconsistent',
                                    #'for entry', re.sub(r'\s+',' ',
                                    #    pub2.title).rstrip('\n'),
                                    'for entry', pub2.doi,
                                    '(' + str(pub2.ncites_scopus), '-->',
                                    pub['citedby-count'] + ')',
                                    file = sys.stderr)
                            pub2.ncites_scopus = ncites_scopus
                            # Find updated year list
                            #print ('URL for updating Scopus years is',
                            #    pub['link'][3]['@href'], file = sys.stderr)
                            eid = str(pub['eid'])
                            years = []
                            prevyears = []
                            totalResults = 0
                            offset = 0
                            while True :
                                if offset > totalResults :
                                    break
                                citedata = requests.get('https://api.' \
                                    + 'elsevier.com/content/search/scopus?' \
                                    + 'query=refeid(' + eid + ')&start=' \
                                    + str(offset),
                                    headers = {'Accept':'application/json',
                                      'X-ELS-APIKey': constants.SCOPUS_API_KEY})
                                out = citedata.json()
                                totalResults = int(out['search-results']\
                                    ['opensearch:totalResults'])
                                try :
                                    for paper in out['search-results']['entry'] :
                                        years.append(int( \
                                            paper['prism:coverDate']\
                                            .split('-')[0]))
                                except KeyError :
                                    pass
                                if years == prevyears : # FIXME does this actually work to replace the previous entry?
                                    break
                                offset += constants.MAX_SCOPUS_QUERIES
                                prevyears = list(years)
                            try :
                                for year in reversed(range(min(years),max(years)+1)) :
                                    a = pub2.cite_years_scopus.count(year)
                                    b = years.count(year)
                                    # If the number in the oldest year we
                                    # looked up earlier is less than the count
                                    # we already know, assume it's incomplete
                                    # and skip that year's output
                                    if a > b and year == min(years) :
                                        continue
                                    if a != b :
                                        print (a, '*[', year, '] -> ',
                                            b, '*[', year, ']', sep='')
                            except TypeError :
                                pass
                            pub2.cite_years_scopus = years
                        break
        print ("Done updating Scopus citation information")

##############################################################################

    # TODO This needs to be updated to use the Web of Science Starter API,
    # as Links AMR has been sunset since November 1, 2023 and is not available.
    def update_WoS (self) : # {{{2

        '''Updates the times a paper has been cited, according to Web of
           Science. Doing this requires a user name and password from
           Thomson-Reuters.'''

        if constants.WOS_USERNAME is None :
            print ("WARNING: no Web of Science username provided;",
                "skipping WoS update.", file=sys.stderr)
            return
        print ("Updating Web of Science citation information")
        doi = {}
        for pub in self.publication :
            if pub.status != constants.PUBLISHED or pub.doi is None :
                continue
            if pub.key is None :
                # set "key" equal to first unique Last + year [+ abc/etc]
                if isinstance(pub.author, (tuple,list)) :
                    auth = pub.author[0].split(' ')[-1]
                elif isinstance(pub.author, str) :
                    auth = pub.author.split(' ')[-1]
                else :
                    raise TypeError
                key_root = auth + str(pub.year)
                if key_root not in doi :
                    key = key_root
                else :
                    i = ord('a')
                    key = key_root + chr(i)
                    while key in doi :
                        i += 1
                        key = key_root + chr(i)
                    key = key_root + chr(i)
                pub.alt_key = key
            else :
                pub.alt_key = pub.key
            doi[pub.alt_key] = pub.doi
        # Assemble list of DOIs and corresponding indices
        # list must be at most 50 elements long, so break up the list if it's
        # longer than that
        n = 0
        doi_list = {}
        cite_count = {}
        update_url = {}
        for DOI in doi :
            n += 1
            doi_list[DOI] = doi[DOI]
            if n >= 50 or n == len(doi) - 1 : # every 50 items & after last one
                # Submit XML request
                request = open ('http_request_wos.xml','w')
                print ('''<?xml version="1.0" encoding="UTF-8" ?>
<request xmlns="http://www.isinet.com/xrpc42"
src="app.id=PartnerApp,env.id=PartnerAppEnv,partner.email=EmailAddress">
  <fn name="LinksAMR.retrieve">
    <list>
      <map>
        <val name="username">''' + constants.WOS_USERNAME + '''</val>
        <val name="password">''' + constants.WOS_PASSWORD + '''</val>
      </map>
      <map>
        <list name="WOS">
          <val>timesCited</val>
          <val>citingArticlesURL</val>
        </list>
      </map>
      <map>''', file = request)

                for d in doi_list :
                    if doi[d] is None :
                        continue
                    print ('      <map name="' + d + '">', file = request)
                    print ('        <val name="doi">' + doi[d] + '</val>',
                        file = request)
                    print ('      </map>', file = request)
                print ('''      </map>
    </list>
  </fn>
</request>
''', file = request)

                request.close()
                # Get citation counts back
                request = open ('http_request_wos.xml', 'r')
                citedata = requests.post('https://ws.isiknowledge.com/cps/xrpc',
                    headers = {'Content-Type': 'text/xml'},
                    data = request)
                xml = citedata.text
                field = str(xml).split('\n')
                print (str(xml))
                indices = {}
                url = {}
                for i in range(len(field)) :
                    if re.search('map name="WOS"', field[i]) :
                        continue
                    if re.search('map name=', field[i]) :
                        key = field[i].split('\"')[1].split('\"')[0]
                    if re.search('val name="timesCited"', field[i]) :
                        indices[key] = i
                    if re.search('val name="citingArticlesURL"', field[i]) :
                        url[key] = i
                # Append citations to end of cite_count dictionary
                for key in indices :
                    i = indices[key]
                    cite_count[key] = int(field[i].split('>')[1].split('<')[0])
                    j = url[key]
                    update_url[key] = field[j].split('[')[2].split(']')[0]
                doi_list = {}
                n = 0
                os.remove('http_request_wos.xml')

        # Update citation counts and provide update URLs
        for paper in self.publication :
            if not hasattr(paper,'alt_key') :
                continue
            if paper.alt_key in cite_count :
                if paper.ncites_wos != cite_count[paper.alt_key] :
                    print ('WARNING:  ncites_wos is out of date for',
                        'entry', str(paper), '(' + str(paper.ncites_wos),
                        '-->', str(cite_count[paper.alt_key]) + ')',
                        file = sys.stderr)
                    paper.wos_update_url = update_url[paper.alt_key]
                    paper.ncites_wos = cite_count[paper.alt_key]

                    # Update the cite_years_wos attribute
                    # New implementation based on selenium
                    # Updated 7/30/2021 for new WoS interface
                    if paper.wos_update_url is None :
                        continue
                    import selenium.webdriver
                    options = selenium.webdriver.firefox.options.Options()
                    options.set_headless()
                    assert options.headless
                    browser = selenium.webdriver.Firefox(options=options)
                    cite_years = {}
                    try :
                        browser.get(paper.wos_update_url)
                        # wait until the page loads
                        selenium.webdriver.support.ui.WebDriverWait(browser,
                            timeout=5).until( lambda x:
                                len(browser.find_elements_by_class_name(
                                    'filter-option-count')) > 0 )
                        names = browser.find_elements_by_class_name(
                            'filter-option-name')
                        counts = browser.find_elements_by_class_name(
                            'filter-option-count')
                        years = browser.find_elements_by_xpath(
                            '//span[contains(@title, "Publication Years")]')
                        for i in range(len(names)) :
                            if names[i] in years :
                                y = int(names[i].text)
                                cite_years[y] = int(counts[i].text)
                    finally :
                        browser.close()
                    needs_update = False
                    years = []
                    for year in cite_years :
                        if sum([x == year for x in paper.cite_years_wos]) \
                                != cite_years[year] :
                            needs_update = True
                        years.extend(cite_years[year] * [year])
                    years.sort(reverse=True)
                    if needs_update :
                        try :
                            for year in \
                                    reversed(range(min(years),max(years)+1)) :
                                a = paper.cite_years_wos.count(year)
                                b = years.count(year)
                                # If number in the oldest year is less than the
                                # count we already know, assume it's simply
                                # incomplete and skip it
                                if a > b and year == min(years) :
                                    continue
                                if a != b :
                                    print (a, '*[', year, '] -> ',
                                        b, '*[', year, ']', sep='')
                        except TypeError :
                            pass
                    else :
                        print ("UMMM...shouldn't I have updated something on",
                            paper.key + '?', file=sys.stderr)
                        print ('URL is',
                            paper.wos_update_url.replace('http:','https:'),
                            file=sys.stderr)

                    paper.cite_years_wos = years

        print ("Done updating Web of Science citation information")

##############################################################################

    def purge_duplicate_collaborators (self) : # {{{2

        'Removes collaborators that have been added multiple times.'

        collab = sorted(self.collaborator, key = lambda x: x.last)
        i = 0
        while i < len(collab) - 1 :
            if collab[i].last == collab[i+1].last and \
                    collab[i].first[0] == collab[i+1].first[0] and \
                    collab[i].year >= collab[i+1].year :
                if re.search(collab[i].institution,'FIXME') :
                    collab[i].institution = collab[i+1].institution
                collab.pop(i+1)
            elif collab[i].last == collab[i+1].last and \
                    collab[i].first[0] == collab[i+1].first[0] :
                if re.search(collab[i+1].institution,'FIXME') :
                    collab[i+1].institution = collab[i].institution
                collab.pop(i)
            else :
                i += 1

        # Now remove anyone who is listed as the author's employee (former or
        # current)
        empl_last = \
            [e.last for e in self.employee \
                if not isinstance(e,(GraduateCommittee,VisitingProfessor))]
        empl_first = \
            [e.first[0] for e in self.employee \
                if not isinstance(e,(GraduateCommittee,VisitingProfessor))]
        i = 0
        while i < len(collab) :
            if collab[i].last in empl_last and \
                    empl_first[empl_last.index(collab[i].last)] == \
                        collab[i].first[0] :
                collab.pop(i)
            else :
                i += 1

        # Now remove anyone who is a graduate/postdoctoral advisor
        i = 0
        while i < len(collab) :
            popped = False
            for degree in self.degree :
                if degree.advisor is None :
                    continue
                if isinstance(degree.advisor, str) :
                    advisors = [degree.advisor]
                elif isinstance(degree.advisor, (tuple,list)) :
                    advisors = degree.advisor
                else :
                    raise TypeError
                for advisor in advisors :
                    # FIXME
                    # We assume that you don't have a collaborator with the
                    # same last name and first initial as one of your advisors!
                    if collab[i].last in advisor and \
                            advisor[0] == collab[i].first[0] :
                        collab.pop(i)
                        popped = True
                        break
                if popped :
                    break
            # Now check for the CV author him/herself!
            if collab[i].last in INVESTIGATOR \
                    and collab[i].first in INVESTIGATOR :
                collab.pop(i)
                popped = True
                continue
            if not popped :
                i += 1

        self.collaborator = collab

##############################################################################

    def update_collaborators (self, bibliography=None) : # {{{2

        '''Scans grants, publications, and presentations and adds anyone
           within COLLAB_AGE years of the present to the list of collaborators
           on the biosketch.'''

        for grant in self.grant :
            if grant.awarded :
                year = int(grant.end.split('/')[-1])
                if year < datetime.datetime.now().year - COLLAB_AGE :
                    continue
                for investigator in \
                      (grant.PI,grant.coPI,grant.coI,grant.senior_personnel) :
                    if isinstance(investigator, (list,tuple)) :
                        for person in investigator :
                            if person == INVESTIGATOR :
                                continue
                            else :
                                fields = person.split('(')
                                affil = fields[1].rstrip(')')
                                fields = fields[0].rstrip().split()
                                last = fields[-1]
                                first = ' '.join(fields[0:-1])
                                self.append( Collaborator(first = first,
                                    last = last, institution = affil,
                                    year = year) )
                    elif investigator is None :
                        continue
                    elif investigator != INVESTIGATOR :
                        fields = investigator.split('(')
                        affil = fields[1].rstrip(')')
                        fields = fields[0].rstrip().split()
                        last = fields[-1]
                        first = ' '.join(fields[0:-1])
                        self.append( Collaborator( first=first,last=last,
                            institution=affil, year=year) )
        #'''
        # Now update based on presentations
        for talk in self.presentation :
            if isinstance(talk.year, str) :
                print ("WARNING: year is a string for presentation",
                    talk.title, file = sys.stderr)
            if int(talk.year) < datetime.datetime.now().year - COLLAB_AGE :
                continue
            if not isinstance(talk.author, str) :
                for author in talk.author :
                    author = author.replace('~',' ')
                    self.append( Collaborator(
                        first = author.split(' ')[0],
                        last = author.split(' ')[-1],
                        institution = r'UNKNOWN/\allowbreak FIXME',
                        year = talk.year
                    ))
            else :
                author = talk.author.replace('~',' ')
                self.append( Collaborator(
                    first = author.split(' ')[0],
                    last = author.split(' ')[-1],
                    institution = r'UNKNOWN/\allowbreak FIXME',
                    year = talk.year
                ))
        #'''

        # Now based on publications (which is harder...)
        USE_BIBLIB = False
        try :
            # do this: git clone https://github.com/aclements/biblib.git biblib
            sys.path.append('biblib')
            import biblib.bib
            USE_BIBLIB = True
        except ModuleNotFoundError :
            print ("WARNING: Unable to import biblib; collaborators will not",
                "be fully updated.", file = sys.stderr)
            USE_BIBLIB = False
        # First, we parse the BibTeX file and get access to all of its keys...
        if USE_BIBLIB :
            if bibliography is not None :
                files = bibliography.split(',')
                parser = biblib.bib.Parser()
                for f in files :
                    f = re.sub(r'[^-\.\+a-zA-Z0-9_]+','',f)
                    f = f.rstrip().rstrip('.bib') + '.bib'
                    proc = subprocess.run(['kpsewhich',f],
                        stdout=subprocess.PIPE)
                    path = proc.stdout.decode().strip('\n')
                    openfile = open(path,'r')
                    parser.parse(openfile)
                    openfile.close()
                bibtex_entries = parser.get_entries()
                bibtex_entries = biblib.bib.resolve_crossrefs (bibtex_entries)

        # Now we parse each entry and add it to the list of collaborators
        for pub in self.publication :
            if pub.key is None :
                # This is easier, because we have everything we need!
                if isinstance(pub.year, str) :
                    print ("WARNING: year is a string for publication",
                        pub.title, file = sys.stderr)
                if int(pub.year) >= datetime.datetime.now().year - COLLAB_AGE :
                    continue
                if isinstance(pub.author, (list,tuple)) :
                    for author in pub.author :
                        author = author.replace('~',' ')
                        self.append( Collaborator(
                            first = author.split(' ')[0],
                            last = author.split(' ')[-1],
                            institution = r'UNKNOWN/\allowbreak FIXME',
                            year = pub.year
                        ))
            elif bibliography is not None and USE_BIBLIB :
                # For key-based entries, we use the .bib file
                key = pub.key.lower()
                author = bibtex_entries[key].authors()
                year = int(bibtex_entries[key].get('year'))
                for a in author :
                    self.append( Collaborator(
                        first = a.first,
                        last = a.last,
                        institution = r'UNKNOWN/\allowbreak FIXME',
                        year = year
                    ))
        self.purge_duplicate_collaborators()

##############################################################################

    def print_statistics_summary (self, texfile,
            show_pubs_since_appt = False) :
        '''Prints a summary of peer-reviewed publications, including
           citations, h/m/i10/etc. indices, and total publications.'''
        if len(self.publication) == 0 :
            return
        if not self.count.initialized :
            self.count.setup_counts (self)

        stats = PubStats(self)
        print (r'   \noindent', file = texfile)
        print ('   Peer-reviewed publications:',
            r'{} ({} teaching, {} research) \\'.format(
            self.count.npubs, self.count.nteaching,
            self.count.npubs - self.count.nteaching), file = texfile)
        # added 7/14/2019: list "publications as PI since appointment"
        if show_pubs_since_appt :
            pubs_as_primary = sum(x.primary and x.peer_reviewed \
                and x.status in (constants.PUBLISHED, constants.ACCEPTED) \
                    for x in self.publication)
            pubs_as_primary_post_appt = sum(x.post_appointment and x.primary \
                and x.status in (constants.PUBLISHED, constants.ACCEPTED) \
                and x.peer_reviewed for x in self.publication)
            print ('   Peer-reviewed publications as primary or group author:',
                pubs_as_primary, '(' + str(pubs_as_primary_post_appt),
                r'since appointment) \\', file = texfile)
        # end added lines
        print (r'   Citations to peer-reviewed publications: \\',
            file = texfile)
        print (r'     \mbox{}\hspace{1.25em}', self.count.ncites_wos,
            r'(from Web of Science) \\', file = texfile)
        print (r'     \mbox{}\hspace{1.25em}', self.count.ncites_scopus,
            r'(from Scopus) \\', file = texfile)
        print (r'     \mbox{}\hspace{1.25em}', self.count.ncites_google,
            r'(from Google Scholar) \\', file = texfile)
        print (r'     $h$-index:', stats.h, r'\quad', file = texfile)
        print (r'     $m$-index: {0:.2f}'.format(stats.m), r'\quad',
            file = texfile)
        print (r'     $i10$-index:', stats.i10, r'\quad', file = texfile)
        #print (r'     $h(2)$-index:', stats.h2, r'\quad', file = texfile)
        print (r'     $g$-index:', stats.g, r'\quad', file = texfile) 
        print (r'     $o$-index:', stats.o, r'\par', file = texfile) 

##############################################################################

    def print_condensed_statistics_summary (self, texfile) : # {{{2

        '''A shortened statistics summary, intended for the CV rather than
           the dossier.'''

        self.count.setup_counts(self)
        stats = PubStats(self)

        print (r'''Peer-reviewed publications: {} ({} teaching, {} research)
            \\'''.format(self.count.npubs, self.count.nteaching,
            self.count.npubs - self.count.nteaching), file = texfile)
        if self.count.ncites_scopus >= self.count.ncites_wos :
            print (r'Citations to peer-reviewed publications',
                '(according to Scopus):', self.count.ncites_scopus,
                file = texfile)
        else :
            print (r'Citations to peer-reviewed publications',
                '(according to Web of Science):', self.count.ncites_scopus,
                file = texfile)
        print (r'\\ Hirsch index:', stats.h, file = texfile)

##############################################################################

    def plot_publications_vs_time (data, texfile) : # {{{2

        '''Plots peer-reviewed publications over time.'''

        if len(data.publication) == 0 :
            return
        #top = 2.25  # height of boxes, in inches
        #top = 2.30  # height of boxes, in inches
        top = 2.4
        right = 2.65 # width of boxes, in inches
    #    top = 1.80 # height in inches
    #    right = 2.25 # width in inches
        # Make plot of publications vs. time
        print (r'\begin{center}', file = texfile)
        print (r'\small', file = texfile)
        firstyear = min([x.year if x.peer_reviewed else 10000 for x in \
            data.publication])
        lastyear = max([x.year if x.status <= constants.SUBMITTED \
            and x.peer_reviewed else firstyear for x in data.publication])
        # no more than 16 labels on the horizontal axis
        #xstride = max(int(lastyear - firstyear + 1) // 12,1)
        xstride = max(int(lastyear - firstyear + 1) // 8,1)
        if xstride == 1 :
            spacing = 3
        else :
            spacing = 2
        #elif xstride == 3 :
        #    spacing = 1
        #spacing = 3 # pts
        print (r'  \begin{tikzpicture}', file = texfile)
        print (r'    \node at (', right/2, 'in,', top + 0.2,
            r'in) {\bfseries Peer-Reviewed Publications Per Year};',
            file = texfile)
        # bars are just the right width so that they are separated by 1 pt
        width = (72.0 * right - (lastyear - firstyear + 2) * spacing) \
            / (lastyear - firstyear + 1)
        # bars are just the right height so the tallest one nearly touches the top
        pubsinyear = []
        pendinginyear = []
        maxpubs = 0
        for year in range(firstyear,lastyear+1) :
            pubsinyear.append(sum([(x.year == year and x.peer_reviewed
                and x.status == constants.PUBLISHED) \
                for x in data.publication]))
            pendinginyear.append(sum([(x.year == year and x.peer_reviewed
                    and (x.status == constants.ACCEPTED \
                    or x.status == constants.SUBMITTED) \
                ) for x in data.publication]))
            if pubsinyear[-1] + pendinginyear[-1] > maxpubs :
                maxpubs = pubsinyear[-1] + pendinginyear[-1]
        ordinate = OptimumOrdinate([ pubsinyear[i] + pendinginyear[i] for i \
            in range(len(pubsinyear)) ])
        height = (top * 72.0 - spacing) / ordinate.max_ordinate
        # Draw vertical axis
        stride = ordinate.delta
        for y in range (0, ordinate.max_ordinate+1, ordinate.delta) :
            print (r'    \draw (-4pt,', y * height, 'pt)', file = texfile)
            print (r'       -- (0,', y * height, 'pt);', file = texfile)
            print (r'    \node [anchor=east] at (-0.25em,', y * height,
                'pt) {', y, '};', file = texfile)
        for year in range(firstyear,lastyear+1) :
            x = (year - firstyear) * width + (year - firstyear + 1) * spacing
            y = pubsinyear[year - firstyear] * height
            #print (r'    \draw[fill=gray] (', x, 'pt, 0)', file = texfile)
            print (r'    \fill[gray] (', x, 'pt, 0)', file = texfile)
            print (r'      -- (', x, 'pt,', y, 'pt)', file = texfile)
            print (r'      -- (', x + width, 'pt,', y, 'pt)', file = texfile)
            print (r'      -- (', x + width, 'pt,0);', file = texfile)
            # horizontal axis labels
            if (year - firstyear) % xstride == 0 :
                print (r'    \node[rotate=290] at (', x + width/1.7 + 2,
                    'pt,-3ex) {', year, '};', file = texfile)
            # Pending publications
            print (r'    \path[pattern color=gray,pattern=north east lines] (',
                x, 'pt,', y, 'pt)', file = texfile)
            print (r'      -- (', x, 'pt,',
                y + pendinginyear[year-firstyear] * height, 'pt)',
                file = texfile)
            print (r'      -- (', x + width, 'pt,',
                y + pendinginyear[year-firstyear] * height, 'pt)',
                file = texfile)
            print (r'      -- (', x + width, 'pt,', y, 'pt);', file = texfile)
        # Draw frame around plot
        print (r'    \draw (0,0) -- (', right, 'in,0)', file = texfile)
        print (r'                -- (', right, 'in,', top, 'in)',
            file = texfile)
        print (r'                -- (0,', top, 'in) -- cycle;', file = texfile)
        # End drawings!
        print (r'  \end{tikzpicture}', file = texfile)

##############################################################################

    def plot_citations_vs_time (data, texfile, show_wos = None,
            show_google = None) :
        '''Plots your citations from Scopus (and Google and/or Web of Science,
           if necessary).'''
        if len(data.publication) == 0 :
            return
        if show_wos is None :
            show_wos = constants.PLOT_WOS_CITATIONS_PER_YEAR
        # Make plot of citations vs. time
        #top = 2.25  # height of boxes, in inches
        #top = 2.30  # height of boxes, in inches
        top = 2.40  # height of boxes, in inches
        right = 2.65 # width of boxes, in inches
        cite_years_scopus = []
        for pub in data.publication :
            cite_years_scopus.extend(pub.cite_years_scopus)
        if len(cite_years_scopus) > 0 :
            cite_years_scopus.sort()
            firstyear = min([x.year if x.peer_reviewed else 10000 for x in \
                data.publication])
            firstyear = min(firstyear, cite_years_scopus[0])
            lastyear = max([x.year if x.status <= constants.SUBMITTED and \
                x.peer_reviewed else firstyear for x in data.publication])
            lastyear = max(lastyear, cite_years_scopus[-1])
            #xstride = max(int(lastyear - firstyear + 1) // 12,1)
            xstride = max(int(lastyear - firstyear + 1) // 8,1)
            if xstride == 1 :
                spacing = 3
            else :
                spacing = 2
            print (r'  \begin{tikzpicture}', file = texfile)
            print (r'    \node at (', right/2, 'in,', top + 0.2,
                r'in) {\bfseries Scopus', end='', file = texfile)
            #if show_google :
            if show_google \
                    and sum([x.ncites_google for x in data.publication]) :
                print (r', \textcolor{Green}{Google}, ', file = texfile,
                    end='')
            #if show_google and show_wos :
            if show_google and show_wos \
                    and sum([x.ncites_wos for x in data.publication]) :
                print (r' and \textcolor{Blue}{WoS}', file = texfile,
                    end='')
            #elif show_wos :
            elif show_wos \
                    and sum([x.ncites_wos for x in data.publication]) :
                print (r' and \textcolor{Blue}{Web of Science}',
                    file = texfile, end='')
            print (r'   Citations Per Year};', file = texfile)
            # bars are just the right width so that they are separated by 1 pt
            width = (72.0 * right - (lastyear - firstyear + 2) * spacing) \
                / (lastyear - firstyear + 1)
            # bars are just the right height so the tallest one nearly touches the top
            citesinyear = []
            for year in range(firstyear,lastyear+1) :
                citesinyear.append(sum([x == year for x in cite_years_scopus]))
            # WOS ADDED LINES
            if show_wos :
                cite_years_wos = []
                for pub in data.publication :
                    cite_years_wos.extend(pub.cite_years_wos)
                cite_years_wos.sort()
                wos_citesinyear = []
                for year in range(firstyear,lastyear+1) :
                    wos_citesinyear.append(sum([x == year for x in \
                        cite_years_wos]))
            # WOS END ADDED LINES
            # GOOGLE ADDED LINES
            if show_google :
                cite_years_google = []
                for pub in data.publication :
                    cite_years_google.extend(pub.cite_years_google)
                cite_years_google.sort()
                google_citesinyear = []
                for year in range(firstyear,lastyear+1) :
                    google_citesinyear.append(sum([x == year for x in \
                        cite_years_google]))
            # GOOGLE END ADDED LINES
            # ADDED LINES to highlight cites from most-cited paper
            # FIXME
            if constants.SHOW_CITES_TO_MOST_CITED_PAPER :
                cite_years_max = []
                ordered_papers = sorted(list(data.publication), reverse=True,
                    key=lambda x: x.ncites_scopus)
                #MOST_CITED_COLORS = ('DarkRed','Chocolate','DarkOrange','Orange',
                #    'Goldenrod','Gold','YellowGreen','Green','DarkGreen',
                #    'Blue','DarkBlue','Indigo','DarkViolet','Purple','black')
                #print (r'  \definecolorseries{mostcited}{rgb}{last}{DarkBlue}{Gold}', file = texfile)
                #print (r'  \definecolorseries{mostcited}{rgb}{last}{DarkRed}{DarkGreen}', file = texfile)
                #print (r'  \definecolorseries{mostcited}{rgb}{step}[rgb]{.95,.85,.55}{.17,.47,.37}', file = texfile)
                #print (r'  \definecolorseries{mostcited}{rgb}{grad}[rgb]{.95,.85,.55}{3,11,17}', file = texfile)
                print (r'  \definecolorseries{mostcited}{rgb}{last}[rgb]{0.05,0.15,0.55}[rgb]{.95,.85,.55}', file = texfile)
                for rpub in ordered_papers :
                    cite_years_max.append(list(rpub.cite_years_scopus))
                    cite_years_max[-1].sort()
                print (r'  \resetcolorseries[' + str(len(ordered_papers)) + \
                    ']{mostcited}', file = texfile)

                max_citesinyear = []
                for i in range(len(cite_years_max)) :
                    max_citesinyear.append([])
                    for year in range(firstyear,lastyear+1) :
                        max_citesinyear[-1].append(
                            sum([x == year for x in cite_years_max[i]])
                        )
            # END ADDED LINES to highlight cites from most-cited paper
            maxcitesceil = int(ceil(max(citesinyear)/10.0)*10)
            # ADDED LINES
            if show_wos :
                maxcitesceil = max(maxcitesceil,
                    int(ceil(max(wos_citesinyear)/10.0)*10))
            if show_google :
                maxcitesceil = max(maxcitesceil,
                    int(ceil(max(google_citesinyear)/10.0)*10))
            # END ADDED LINES
            # new lines
            most_citesinyear = list(citesinyear)
            if show_wos :
                for i in range(len(citesinyear)) :
                    if wos_citesinyear[i] > most_citesinyear[i] :
                        most_citesinyear[i] = wos_citesinyear[i]
            if show_google :
                for i in range(len(citesinyear)) :
                    if google_citesinyear[i] > most_citesinyear[i] :
                        most_citesinyear[i] = google_citesinyear[i]
            ordinate = OptimumOrdinate(most_citesinyear)
            maxcitesceil = ordinate.max_ordinate
            stride = ordinate.delta

            # end new
            height = (top * 72.0 - spacing) / maxcitesceil
            # Draw vertical axis tick marks and labels
            #stride = int(round(max(maxcitesceil / 10, 1)))
            for y in range (0, maxcitesceil+1, stride) :
                print (r'    \draw (-4pt,', y * height, 'pt)', file = texfile)
                print (r'       -- (0,', y * height, 'pt);', file = texfile)
                print (r'    \node[anchor=east] at (-0.25em,',
                    y * height, 'pt) {', y, '};', file = texfile)
            # Draw plot
            for year in range(firstyear,lastyear+1) :
                x = (year - firstyear) * width \
                    + (year - firstyear + 1) * spacing
                y = citesinyear[year - firstyear] * height
                print (r'    \fill[gray] (', x, 'pt, 0)', file = texfile)
                print (r'      -- (', x, 'pt,', y, 'pt)', file = texfile)
                print (r'      -- (', x + width, 'pt,', y, 'pt)',
                    file = texfile)
                print (r'      -- (', x + width, 'pt,0);', file = texfile)
                ## WOS LINES
                if show_wos :
                    y = wos_citesinyear[year - firstyear] * height
                    print (r'    \draw[Blue] (', x, 'pt, 0)',
                        file = texfile)
                    print (r'      -- (', x, 'pt,', y, 'pt)', file = texfile)
                    print (r'      -- (', x + width, 'pt,', y, 'pt)',
                        file = texfile)
                    print (r'      -- (', x + width, 'pt,0);', file = texfile)
                ## END WOS LINES
                ## GOOGLE LINES
                if show_google :
                    y = google_citesinyear[year - firstyear] * height
                    print (r'    \draw[Green] (', x, 'pt, 0)',
                        file = texfile)
                    print (r'      -- (', x, 'pt,', y, 'pt)', file = texfile)
                    print (r'      -- (', x + width, 'pt,', y, 'pt)',
                        file = texfile)
                    print (r'      -- (', x + width, 'pt,0);', file = texfile)
                ## END GOOGLE LINES
                ## LINES for most-cited paper
                if constants.SHOW_CITES_TO_MOST_CITED_PAPER :
                    y1 = 0
                    for i in range(len(max_citesinyear)) :
                        y2 = y1 + max_citesinyear[i][year - firstyear] * height
                        #print (r'    \fill[',
                        #    MOST_CITED_COLORS[i % len(MOST_CITED_COLORS)],
                        #    '] (', x, 'pt,', y1, 'pt)', file = texfile)
                        print (r'    \fill[mostcited!![',
                            len(max_citesinyear)//6 * (i % 6) + int(i/6),
                            '] (', x, 'pt,', y1, 'pt)', file = texfile)
                        print (r'      -- (', x, 'pt,', y2, 'pt)',
                            file = texfile)
                        print (r'      -- (', x + width, 'pt,', y2, 'pt)',
                            file = texfile)
                        print (r'      -- (', x + width, 'pt,', y1, 'pt);',
                            file = texfile)
                        y1 = y2
                # horizontal axis labels
                if (year - firstyear) % xstride == 0 :
                    print (r'    \node[rotate=290] at (', x + width/1.7 + 2,
                        'pt,-3ex) {', year, '};', file = texfile)
            # Draw frame around plot
            print (r'    \draw (0,0) -- (', right, 'in,0)', file = texfile)
            print (r'                -- (', right, 'in,', top, 'in)',
                file = texfile)
            print (r'                -- (0,', top, 'in) -- cycle;',
                file = texfile)
            print (r'  \end{tikzpicture}\par', file = texfile)

            # Print the actual numbers (for debugging)
            if constants.PRINT_CITATION_COUNTS and show_wos and show_google :
                print ("Citation counts:")
                print ('year S W G')
                for year in range(firstyear,lastyear+1) :
                    print (year, citesinyear[year-firstyear],
                        wos_citesinyear[year-firstyear],
                        google_citesinyear[year-firstyear])
        print (r'\end{center}', file = texfile)

##############################################################################

    def plot_reviews_over_time (self, texfile, startyear = None) : # {{{2

        'Like its publication-related cousin, but with peer reviews.'

        firstyear = min([x.year for x in self.journal_review])
        lastyear = max([x.year for x in self.journal_review])
        if startyear is None :
            startyear = firstyear
        rev_per_year = []
        for year in range(firstyear, lastyear+1) :
            rev_per_year.append(sum((x.year == year for x in self.journal_review)))
        # draw the plot
        top = 2.4 # in
        right = 2.65 # in
        #spacing = 3 # pt
        xstride = max(int(lastyear - startyear + 1) // 8,1)
        if xstride == 1 :
            spacing = 3
        else :
            spacing = 2
        print (r'\begin{small}', file = texfile)
        print (r'  \begin{tikzpicture}', file = texfile)
        print (r'    \node at (', right/2, 'in,', top + 0.2,
            r'in) {\bfseries Peer Reviews Per Year};', file = texfile)
        # bars are separated by 1 pt
        width = (72.0 * right - (lastyear - startyear + 2) * spacing) \
            / (lastyear - startyear + 1)
        # bars are just tall enough so the tallest one is 1pt from the top
        maxrevs = max(rev_per_year)
        height = (top * 72.0 - spacing) / maxrevs
        # Draw vertical axis
        stride = max(maxrevs // 10, 1)
        for y in range (0, maxrevs + 1, stride) :
            print (r'    \draw (-4pt,', y * height, 'pt)', file = texfile)
            print (r'      -- (0,', y * height, 'pt);', file = texfile)
            print (r'    \node [anchor=east] at (-0.25em,', y * height,
                'pt) {', y, '};', file = texfile)
        # No more than 16 labels on the horizontal axis
        #xstride = max(int(lastyear - startyear + 1) // 12, 1)
        xstride = max(int(lastyear - startyear + 1) // 8, 1)
        for year in range(startyear, lastyear+1) :
            x = (year - startyear) * width + (year - startyear + 1) * spacing
            y = rev_per_year[year - firstyear] * height
            print (r'    \fill[gray] (', x, 'pt, 0)', file = texfile)
            print (r'      -- (', x, 'pt,', y, 'pt)', file = texfile)
            print (r'      -- (', x + width, 'pt,', y, 'pt)', file = texfile)
            print (r'      -- (', x + width, 'pt,0);', file = texfile)
            # horizontal axis labels
            if (year - startyear) % xstride == 0 :
                print (r'    \node[rotate=290] at (', x + width/1.7 + 2,
                    'pt,-3ex) {', year, '};', file = texfile)
        # Draw frame around plot
        print (r'    \draw (0,0) -- (', right, 'in,0)', file = texfile)
        print (r'                -- (', right, 'in,', top, 'in)',
            file = texfile)
        print (r'                -- (0,', top, 'in) -- cycle;', file = texfile)
        # End drawings!
        print (r'  \end{tikzpicture}', file = texfile)
        print (r'\end{small}', file = texfile)
