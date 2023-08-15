from math import sqrt, ceil
from .publication import JournalArticle, ConferenceProceedings, Book, \
    BookChapter
from .presentation import Poster
from . import constants

class PubCount : # {{{1

    'Counts of publications, including citations, for all publications.'

    def __init__ (self) : # {{{2
        self.npubs = 0
        self.npubs_post_appointment = 0
        self.npubs_post_tenure = 0
        self.ncites_wos = 0
        self.ncites_scopus = 0
        self.ncites_MSacad = 0
        self.ncites_google = 0
        self.ncites = 0
        self.narticles = 0
        self.narticles_post_appointment = 0
        self.narticles_post_tenure = 0
        self.nchapters = 0
        self.nchapters_post_appointment = 0
        self.nchapters_post_tenure = 0
        self.nproceedings = 0
        self.nproceedings_post_appointment = 0
        self.nproceedings_post_tenure = 0
        self.nbooks = 0
        self.nbooks_post_appointment = 0
        self.nbooks_post_tenure = 0
        self.nother = 0
        self.nother_post_appointment = 0
        self.nother_post_tenure = 0
        self.nsubmitted = 0
        self.naccepted = 0
        self.ninprep = 0
        self.nprocinprep = 0
        self.nprocsubmitted = 0
        self.nprocaccepted = 0
        self.nproc_notreviewed = 0
        self.nproc_notreviewed_inprep = 0
        self.nproc_notreviewed_post_appointment = 0
        self.nproc_notreviewed_post_tenure = 0
        self.nchapinprep = 0
        self.nchapsubmitted = 0
        self.nchapaccepted = 0
        self.nteaching = 0
        self.nteaching_post_appointment = 0
        self.nteaching_post_tenure = 0
        self.oral = 0
        self.oral_pre_appt = 0
        self.oral_post_appt_pre_tenure = 0
        self.oral_post_tenure = 0
        self.poster = 0
        self.poster_pre_appt = 0
        self.poster_post_appt_pre_tenure = 0
        self.poster_post_tenure = 0
        self.awards = 0
        self.awards_post_tenure = 0
        self.awards_post_appointment = 0
        self.student_awards = 0
        self.student_awards_post_tenure = 0
        self.student_awards_post_appointment = 0
        self.initialized = False

##############################################################################

    def setup_counts (self, data) : # {{{2
        'Parse the database and count everything.'
        if self.initialized :
            return
        else :
            self.initialized = True
        for pub in data.publication :
            if pub.teaching :
                self.nteaching += 1
                if pub.post_tenure :
                    self.nteaching_post_tenure += 1
                if pub.post_appointment :
                    self.nteaching_post_appointment += 1
            if pub.peer_reviewed and pub.status == constants.PUBLISHED :
                self.npubs += 1
                if pub.post_appointment :
                    self.npubs_post_appointment += 1
                if pub.post_tenure :
                    self.npubs_post_tenure += 1
                self.ncites_wos += pub.ncites_wos
                self.ncites_scopus += pub.ncites_scopus
                self.ncites_google += pub.ncites_google
                self.ncites += pub.ncites
            if pub.peer_reviewed and isinstance(pub,JournalArticle) :
                if pub.status == constants.SUBMITTED :
                    self.nsubmitted += 1
                elif pub.status == constants.UNSUBMITTED :
                    self.ninprep += 1
                elif pub.status == constants.ACCEPTED :
                    self.naccepted += 1
                else :
                    self.narticles += 1
                    if pub.post_tenure :
                        self.narticles_post_tenure += 1
                    if pub.post_appointment :
                        self.narticles_post_appointment += 1
            elif pub.peer_reviewed and isinstance(pub,BookChapter) :
                if pub.status == constants.UNSUBMITTED :
                    self.nchapinprep += 1
                elif pub.status == constants.ACCEPTED :
                    self.nchapaccepted += 1
                if pub.status == constants.SUBMITTED :
                    self.nchapsubmitted += 1
                else :
                    self.nchapters += 1
                    if pub.post_appointment :
                        self.nchapters_post_appointment += 1
                    if pub.post_tenure :
                        self.nchapters_post_tenure += 1
            elif pub.peer_reviewed and isinstance(pub,ConferenceProceedings) :
                if pub.status == constants.UNSUBMITTED :
                    self.nprocinprep += 1
                elif pub.status == constants.ACCEPTED :
                    self.nprocaccepted += 1
                if pub.status == constants.SUBMITTED :
                    self.nprocsubmitted += 1
                else :
                    self.nproceedings += 1
                    if pub.post_appointment :
                        self.nproceedings_post_appointment += 1
                    if pub.post_tenure :
                        self.nproceedings_post_tenure += 1
            elif not pub.peer_reviewed \
                    and isinstance(pub,ConferenceProceedings) :
                if pub.status == constants.UNSUBMITTED :
                    self.nproc_notreviewed_inprep += 1
                else :
                    self.nproc_notreviewed += 1 # change from noref!
                    if pub.post_appointment :
                        self.nproc_notreviewed_post_appointment += 1
                    if pub.post_tenure :
                        self_notreviewed_post_tenure += 1
            elif isinstance(pub,Book) :
                self.nbooks += 1
                if pub.post_appointment :
                    self.nbooks_post_appointment += 1
                if pub.post_tenure :
                    self.nbooks_post_tenure += 1
            else :
                self.nother += 1
                if pub.post_appointment :
                    self.nother_post_appointment += 1
                if pub.post_tenure :
                    self.nother_post_tenure += 1

        for pres in data.presentation :
            if isinstance(pres,Poster) :
                self.poster += 1
            else :
                self.oral += 1
            if pres.post_tenure :
                if isinstance(pres,Poster) :
                    self.poster_post_tenure += 1
                else :
                    self.oral_post_tenure += 1
            elif pres.post_appointment :
                if isinstance(pres,Poster) :
                    self.poster_post_appt_pre_tenure += 1
                else :
                    self.oral_post_appt_pre_tenure += 1
            else :
                if isinstance(pres,Poster) :
                    self.poster_pre_appt += 1
                else :
                    self.oral_pre_appt += 1

        for award in data.award :
            if award.student is None :
                self.awards += 1
                if award.post_tenure :
                    self.awards_post_tenure += 1
                if award.post_appointment :
                    self.awards_post_appointment += 1
            else :
                self.student_awards += 1
                if award.post_tenure :
                    self.student_awards_post_tenure += 1
                if award.post_appointment :
                    self.student_awards_post_appointment += 1

##############################################################################

class OptimumOrdinate : # {{{1

    'Class to determine the optimum spacing of citations in the plots.'

    def __init__ (self, array, delta = None, max_ticks = 12) : # {{{2
        class IdealStrides : #{{{3
            def __init__ (self) :
                self.value = 1
                self.exponent = 0
            def __iter__ (self) :
                return self
            def __next__ (self) :
                if self.value == 1 :
                    self.value = 2
                elif self.value == 2 :
                    if self.exponent == 0 :
                        self.value = 5
                    else :
                        self.value = 2.5
                elif self.value == 2.5 :
                    self.value = 5
                elif self.value == 5 :
                    self.value = 1
                    self.exponent += 1
                else :
                    raise ValueError
                return int(self.value * 10**self.exponent)
            # 3}}}
        stride = IdealStrides()
        interval = 1
        if delta is not None :
            while interval < delta :
                interval = next(stride)
            interval = delta
        max_value = max(array)
        nticks = ceil(max_value/interval)
        max_ordinate = nticks * interval
        while nticks > max_ticks :
            interval = next(stride)
            nticks = ceil(max_value / interval)
            max_ordinate = nticks * interval
        self.max_value = max_value
        self.max_ordinate = max_ordinate
        self.nticks = nticks + 1
        self.ticks = [x * interval for x in range(nticks+1)]
        self.delta = interval

##############################################################################

class PubStats : # {{{1

    'Calculates and stores the Hirsch index and other publication metrics.'

    def __init__ (self, CV) : # {{{2
        # Calculate Hirsch index
        Hirsch_index = len(CV.publication)
        while sum( max(pub.ncites_scopus,pub.ncites_wos) \
                >= Hirsch_index for pub in CV.publication) < Hirsch_index :
            Hirsch_index -= 1
        self.h = Hirsch_index
        # h2 index
        h2 = 0
        while h2 < sum ( max(pub.ncites_scopus,pub.ncites_wos) \
                >= h2**2 for pub in CV.publication ) :
            h2 += 1
        h2 = sum ( max(pub.ncites_scopus,pub.ncites_wos) \
                >= h2**2 for pub in CV.publication )
        self.h2 = h2
        # g index
        garray = []
        for pub in CV.publication:
            garray.append (max(pub.ncites_scopus,pub.ncites_wos))
        garray.sort()
        garray.reverse()
        g = len(garray)
        while sum(garray[0:g]) < g**2 :
            g = g - 1
        g = min(g,len(garray))
        self.g = g

        # m-index
        firstyear = min([x.year if x.peer_reviewed else 10000 for x in \
            CV.publication])
        lastyear = max([x.year if x.peer_reviewed else 0 for x in \
            CV.publication])
        if ( lastyear == firstyear ) :
            m = 0
        else :
            m = float(Hirsch_index) / (lastyear - firstyear + 0)
        self.m = m

        # i10-index
        i10 = 0
        for pub in CV.publication:
            if pub.peer_reviewed and \
                    max(pub.ncites_scopus,pub.ncites_wos) >= 10 :
                i10 += 1
        self.i10 = i10

        # o-index
        most_cites = max([max(pub.ncites_scopus,pub.ncites_wos) for pub \
                in CV.publication])
        o = int(sqrt(Hirsch_index * most_cites))
        self.o = o
