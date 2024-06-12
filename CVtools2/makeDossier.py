import datetime
import re
import os
import sys
from .award import ResearchAward, ServiceAward, TeachingAward
from .course import UndergraduateCourse, GraduateCourse, \
    TeachingAssistantship, courses_from_this_school
from .employee import VisitingProfessor, Postdoc, DoctoralStudent, \
    MastersStudent, GraduateStudent, UndergraduateStudent, GraduateCommittee
from .presentation import InvitedTalk, Poster
from .publication import JournalArticle, Book, BookChapter, \
    ConferenceProceedings
from .service import LocalService, NonLocalService, DepartmentService, \
    CollegeService, UniversityService, UniversitySystemService, Regional, \
    National, International
from .tex2pdf import write_preamble, set_typeface, generate_pdf
from .utilities import remove_duplicates, tocardinal
from . import constants

def write_Dossier (data, filename, bibliography = None, typeface = None,
        numbers = True, show_interviews = True, CV_only = False,
        separate_posters = False, show_rejected = True, show_news = True,
        hide_pre_tenure = False, hide_pre_appointment = False) :

    '''Generates a CV intended for a promotion and tenure dossier. This is the
       "long" form. It contains EVERYTHING, differentiates former from
       previous students, shows interviews (as invited talks), publications,
       and presentations.'''

    constants.IDENTIFY_MINIONS = True

    if not isinstance(numbers, bool) :
        raise TypeError('numbers must be True or False')
    if not isinstance(show_interviews, bool) :
        raise TypeError('show_interviews must be True or False')
    if not isinstance(CV_only, bool) :
        raise TypeError('CV_only must be True or False')
    if not isinstance(separate_posters, bool) :
        raise TypeError('separate_posters must be True or False')
    if not isinstance(show_rejected, bool) :
        raise TypeError('show_rejected must be True or False')
    if not isinstance(show_news, bool) :
        raise TypeError('show_news must be True or False')

##############################################################################
    # Student advising {{{2
    def employees_advised (data, texfile, heading = r'\subsection') :
        'Prints a list of all students, postdocs, etc. advised'
        for current in (True,False) :
            if current :
                prefix = 'Current '
            else :
                prefix = 'Past '
            for level in (VisitingProfessor, Postdoc, DoctoralStudent, \
                    MastersStudent, UndergraduateStudent, GraduateCommittee) :
                if any(isinstance(data.employee[i], level) and \
                        data.employee[i].current == current \
                        for i in range(len(data.employee))) :
                    if level is VisitingProfessor :
                        print (heading, '{', prefix, 'Visiting Scholars}',
                            sep='', file = texfile)
                    elif level is Postdoc :
                        print (heading, '{', prefix, 'Post-Doctoral Scholars}',
                            sep='', file = texfile)
                    elif level is DoctoralStudent :
                        print (heading, '{', prefix, 'Doctoral Students}',
                            sep='', file = texfile)
                    elif level is MastersStudent :
                        print (heading, '{', prefix, "Master's Students}",
                            sep='', file = texfile)
                    elif level is UndergraduateStudent :
                        print (heading, '{', prefix, 'Undergraduate Students}',
                            sep='', file = texfile)
                    elif level is GraduateCommittee :
                        print (heading, '{', prefix,
                            'Thesis/Dissertation Committee Memberships}',
                            sep='', file = texfile)
                    print (r'\begin{CVrevnumerate}', file = texfile)
                    for person in reversed(data.employee) :
                        if isinstance(person, level) \
                                and person.current == current :
                            person.write (texfile)
                    print (r'\end{CVrevnumerate}', file = texfile)

##############################################################################

    # Teaching awards {{{2
    def teaching_awards (data, texfile, level = 2) :
        '''Prints a list of teaching awards. Level indicates section (1) or
           subsection(2) headings.'''
        any_awards = False
        for award in data.award :
            if award.teaching :
                any_awards = True
        if any_awards :
            if level == 1 :
                print (r'\section{Teaching Awards and Honors}', file = texfile)
            elif level == 2 :
                print (r'\subsection{Teaching Awards and Honors}',
                    file = texfile)
            elif level == 3 :
                print (r'\subsubsection{Teaching Awards and Honors}',
                    file = texfile)
            else :
                raise ValueError
            print (r'\begin{CVitemize}', file = texfile)
            for award in reversed(data.award) :
                if isinstance(award, TeachingAward) :
                    award.write (texfile)
            print (r'\end{CVitemize}', file = texfile)

##############################################################################

    # Teaching grants and contracts {{{2
    def print_teaching_grants (data, texfile, level = 2, separate = True,
            long =True) :

        '''Prints a list of grants that have to do with teaching.
        Level indicates section (1) or subsection(2) headings.'''

        teaching_grants = False
        funded_teaching_grants = False
        funded_federal_teaching_grants = False
        funded_nonfederal_teaching_grants = False
        pending_teaching_grants = False
        pending_federal_teaching_grants = False
        pending_nonfederal_teaching_grants = False
        rejected_teaching_grants = False
        for grant in data.grant : # {{{3
            if grant.teaching :
                if grant.awarded :
                    teaching_grants = True
                    funded_teaching_grants = True
                    if grant.federal :
                        funded_federal_teaching_grants = True
                    else :
                        funded_nonfederal_teaching_grants = True
                elif grant.rejected :
                    if show_rejected :
                        teaching_grants = True
                    rejected_teaching_grants = True
                else :
                    teaching_grants = True
                    if grant.federal :
                        pending_federal_teaching_grants = True
                    else :
                        pending_nonfederal_teaching_grants = True
        # 3}}}
        if level == 1 :
            section = r'\section'
            subsection = r'\subsection'
        elif level == 2 :
            section = r'\subsection'
            subsection = r'\subsubsection'
        elif level == 3 :
            section = r'\subsubsection'
            subsection = r'\paragraph'
        else :
            raise ValueError
        if teaching_grants : # {{{3
            print (section + '{Teaching-Related Grants and Contracts}',
                file = texfile)
            if separate : # {{{4
                if funded_federal_teaching_grants :
                    print (subsection + \
                        '{Funded Federal Teaching Grants and Contracts}',
                        file = texfile)
                    print (r'\begin{grantlist}', file = texfile)
                    for grant in reversed(data.grant) :
                        if grant.teaching and grant.federal and grant.awarded :
                            if long :
                                grant.write (texfile)
                            else :
                                grant.write_condensed (texfile)
                    print (r'\end{grantlist}', file = texfile)
                if funded_nonfederal_teaching_grants :
                    print (subsection + \
                        '{Funded Non-Federal Teaching Grants and Contracts}',
                        file = texfile)
                    print (r'\begin{grantlist}', file = texfile)
                    for grant in reversed(data.grant) :
                        if grant.teaching and not grant.federal \
                                and grant.awarded :
                            if long :
                                grant.write (texfile)
                            else :
                                grant.write_condensed (texfile)
                    print (r'\end{grantlist}', file = texfile)
                if pending_federal_teaching_grants :
                    print (subsection + '''{Pending Federal Teaching-Related
                        Proposals and Letters of Intent}''',
                        file = texfile)
                    print (r'\begin{grantlist}', file = texfile)
                    for grant in reversed(data.grant) :
                        if grant.teaching and grant.federal \
                                and not grant.awarded and not grant.rejected :
                            if long :
                                grant.write (texfile)
                            else :
                                grant.write_condensed (texfile)
                    print (r'\end{grantlist}', file = texfile)
                if pending_nonfederal_teaching_grants :
                    print (subsection, '{Pending Non-Federal',
                        ' Teaching-Related Proposals and Letters of Intent}',
                        sep='', file = texfile)
                    print (r'\begin{grantlist}', file = texfile)
                    for grant in reversed(data.grant) :
                        if grant.teaching and not grant.federal \
                                and not grant.awarded and not grant.rejected :
                            if long :
                                grant.write (texfile)
                            else :
                                grant.write_condensed (texfile)
                    print (r'\end{grantlist}', file = texfile)
            else : # do NOT separate teaching grants {{{4
                if funded_teaching_grants :
                    print (subsection + \
                        '{Funded Teaching Grants and Contracts}',
                        file = texfile)
                    print (r'\begin{grantlist}', file = texfile)
                    for grant in reversed(data.grant) :
                        if grant.teaching and grant.awarded :
                            if long :
                                grant.write (texfile)
                            else :
                                grant.write_condensed (texfile)
                    print (r'\end{grantlist}', file = texfile)
                if pending_teaching_grants :
                    print (subsection + \
                        '{Pending Teaching Grants and Contracts}',
                        file = texfile)
                    print (r'\begin{grantlist}', file = texfile)
                    for grant in reversed(data.grant) :
                        if grant.teaching and not grant.awarded \
                                and not grant.rejected :
                            if long :
                                grant.write (texfile)
                            else :
                                grant.write_condensed (texfile)
                    print (r'\end{grantlist}', file = texfile)
            # endif separate
            if show_rejected and rejected_teaching_grants : # {{{4
                print (subsection + '''{Rejected Teaching-Related Proposals and
                    Letters of Intent}''',
                    file = texfile)
                print (r'\begin{grantlist}', file = texfile)
                for grant in reversed(data.grant) :
                    if grant.teaching and grant.rejected :
                        if long :
                            grant.write (texfile)
                        else :
                            grant.write_condensed (texfile)
                print (r'\end{grantlist}', file = texfile)

##############################################################################

    # Teaching responsibilities {{{3
    def teaching_responsibilities (data, texfile, level = 2) :

        '''Prints a list of the author's teaching responsibilities at this
        particular school.'''

        if not any( x.school == constants.SCHOOL for x in data.course ) :
            return
        if level == 1 :
            section = r'\section'
            subsection = r'\subsection'
        elif level == 2 :
            section = r'\subsection'
            subsection = r'\subsubsection'
        print (section + r'{Teaching Responsibilities at',
            constants.UNIVTHE.lower(), constants.SCHOOL + '}', file = texfile)
        crs = sorted(courses_from_this_school(data.course),
            key=lambda c: c.semester)
        course = sorted(crs, reverse=True, key=lambda c: c.year)
        semesters = [x.semester + ' ' + str(x.year) for x in course]
        semesters = remove_duplicates (semesters)
        # Find which course levels (Undergrad, grad) that get printed
        print_undergrad_course_heading = False
        print_grad_course_heading = False
        print_guest_heading = False
        for c in course :
            if isinstance(c,UndergraduateCourse) and not c.guest :
                print_undergrad_course_heading = True
            elif isinstance(c,GraduateCourse) and not c.guest :
                print_grad_course_heading = True
            if c.guest :
                print_guest_heading = True
            # Stop looking if they're both going to be printed anyway
            if print_grad_course_heading and print_undergrad_course_heading \
                    and print_guest_heading :
                break
        # Undergraduate courses # {{{4
        if print_undergrad_course_heading :
            print (r'\noindent', file = texfile)
            print (r'Undergraduate Courses\nopagebreak', file = texfile)
            for semester in semesters :
                if sum(semester == (c.semester + ' ' + str(c.year)) \
                            and isinstance(c,UndergraduateCourse) \
                        for c in course) == 0 :
                    continue
                print (r'\begin{courselist}{' + semester + '}', file = texfile)
                for c in course :
                    if c.semester + ' ' + str(c.year) == semester and \
                            isinstance(c,UndergraduateCourse) and not c.guest :
                        c.begin_recent(texfile)
                        print (r'\item', str(c), file = texfile)
                        c.end_recent(texfile)
                print (r'\end{courselist}', file = texfile)
        # Graduate courses # {{{4
        if print_grad_course_heading :
            print (r'\noindent', file = texfile)
            print (r'Graduate Courses\nopagebreak', file = texfile)
            for semester in semesters :
                if sum(semester == (c.semester + ' ' + str(c.year)) and \
                        isinstance(c,GraduateCourse) for c in course) == 0 :
                    continue
                print (r'\begin{courselist}{' + semester + '}', file = texfile)
                for c in course :
                    if c.semester + ' ' + str(c.year) == semester and \
                            isinstance(c,GraduateCourse) and not c.guest :
                        c.begin_recent(texfile)
                        print (r'\item', str(c), file = texfile)
                        c.end_recent(texfile)
                print (r'\end{courselist}', file = texfile)
        # Guest-lectured courses # {{{4
        if print_grad_course_heading :
            print (r'\noindent', file = texfile)
            print (r'Guest Lectures', file = texfile)
            for semester in semesters :
                if sum(semester == (c.semester + ' ' + str(c.year)) and \
                        c.guest for c in course) == 0 :
                    continue
                print (r'\begin{courselist}{' + semester + '}', file = texfile)
                for c in course :
                    if c.semester + ' ' + str(c.year) == semester and \
                            c.guest :
                        c.begin_recent(texfile)
                        print (r'\item', str(c), file = texfile)
                        c.end_recent(texfile)
                print (r'\end{courselist}', file = texfile)

##############################################################################

    # Teaching Publications {{{2
    def teaching_publications (data, texfile, level = 2, subdivide = False) :

        '''Prints a list of publications that have to do with teaching.
        Level indicates section (1) or subsection(2) headings.'''

        if level == 1 :
            section = r'\section'
            subsection = r'\subsection'
        elif level == 2 :
            section = r'\subsection'
            subsection = r'\subsubsection'
        elif level == 3 :
            section = r'\subsubsection'
            subsection = r'\paragraph'
        else :
            raise ValueError
        teaching_pubs = False
        for pub in data.publication :
            if pub.teaching :
                teaching_pubs = True
                break
        if teaching_pubs :
            print (section + '{Publications Concerning Teaching}',
                file = texfile)
            if subdivide :
                npre_appt = 0
                npost_tenure = 0
                npost_appt_pre_tenure = 0
                for pub in data.publication :
                    if pub.peer_reviewed \
                            and pub.status == constants.PUBLISHED \
                            and pub.teaching :
                        if pub.post_appointment :
                            if pub.post_tenure :
                                npost_tenure += 1
                            else :
                                npost_appt_pre_tenure += 1
                        else :
                            npre_appt += 1
                if npost_tenure > 0 :
                    print (subsection + '{Peer-Reviewed Teaching Publications',
                        '(Post-Tenure)}', file = texfile)
                    print (r'\begin{CVrevnumerate}', file = texfile)
                    for pub in reversed(data.publication) :
                        if pub.teaching and pub.peer_reviewed \
                        and pub.status == constants.PUBLISHED \
                        and pub.post_appointment and pub.post_tenure :
                            pub.write (texfile)
                    print (r'\end{CVrevnumerate}', file = texfile)
                if npost_appt_pre_tenure > 0 :
                    print (subsection + '{Peer-Reviewed Teaching Publications',
                        '(Post-Appointment)}', file = texfile)
                    print (r'\begin{CVrevnumerate}', file = texfile)
                    for pub in reversed(data.publication) :
                        if pub.teaching and pub.peer_reviewed \
                        and pub.status == constants.PUBLISHED \
                        and pub.post_appointment and not pub.post_tenure :
                            pub.write (texfile)
                    print (r'\end{CVrevnumerate}', file = texfile)
                if npre_appt > 0 :
                    print (subsection + '{Peer-Reviewed Teaching Publications',
                        '(Pre-Appointment)}', file = texfile)
                    print (r'\begin{CVrevnumerate}', file = texfile)
                    for pub in reversed(data.publication) :
                        if pub.teaching and pub.peer_reviewed \
                        and pub.status == constants.PUBLISHED \
                        and not pub.post_appointment :
                            pub.write (texfile)
                    print (r'\end{CVrevnumerate}', file = texfile)
            else :
                print (r'\begin{CVrevnumerate}', file = texfile)
                for pub in reversed(data.publication) :
                    if pub.teaching and pub.status == constants.PUBLISHED :
                        pub.write (texfile)
                print (r'\end{CVrevnumerate}', file = texfile)

##############################################################################

    # Student Theses and Dissertations {{{2
    def student_theses (data, texfile, level = 2, subdivide = False,
            show_committee = False) :
        if level == 1 :
            section = r'\section'
            subsection = r'\subsection'
        elif level == 2 :
            section = r'\subsection'
            subsection = r'\subsubsection'
        elif level == 3 :
            section = r'\subsubsection'
            subsection = r'\paragraph'
        else :
            raise ValueError
        ntheses = 0
        ndissertations = 0
        for student in data.employee :
            if isinstance(student,MastersStudent) and not student.current \
                  and (student.title is not None or student.key is not None) :
                ntheses += 1
            if isinstance(student,DoctoralStudent) and not student.current \
                  and (student.title is not None or student.key is not None) :
                ndissertations += 1
        graduates = [x for x in data.employee if x.defense is not None]
        graduates.sort(reverse = True, key = lambda x: \
                datetime.datetime.strptime(x.defense, '%m/%d/%Y'))
        if not subdivide :
            if ntheses > 0 and ndissertations == 0 :
                print (section + '{Student Theses}',
                    file = texfile)
            elif ndissertations > 0 and ntheses == 0 :
                print (section + '{Student Dissertations}',
                    file = texfile)
            elif ntheses + ndissertations > 0 :
                print (section + '{Student Theses and Dissertations}',
                    file = texfile)
            if ntheses + ndissertations > 0 :
                print (r'\begin{CVrevnumerate}', file = texfile)
                for student in graduates :
                    if isinstance(student,GraduateStudent) :
                        student.write_thesis_or_dissertation (texfile,
                            show_committee = show_committee)
                print (r'\end{CVrevnumerate}', file = texfile)
        else :
            if ntheses > 0 :
                print (section + '{Student Theses}',
                    file = texfile)
                print (r'\begin{CVrevnumerate}', file = texfile)
                for student in graduates :
                    if isinstance(student,MastersStudent) :
                        student.write_thesis_or_dissertation (texfile,
                            show_committee = show_committee)
                print (r'\end{CVrevnumerate}', file = texfile)
            if ndissertations > 0 :
                print (section + '{Student Dissertations}',
                    file = texfile)
                print (r'\begin{CVrevnumerate}', file = texfile)
                for student in graduates :
                    if isinstance(student,DoctoralStudent) :
                        student.write_thesis_or_dissertation (texfile,
                            show_committee = show_committee)
                print (r'\end{CVrevnumerate}', file = texfile)

##############################################################################

    # Teaching-related presentations {{{2
    def teaching_presentations (data, texfile, level = 2) :
        '''Prints a list of presentations that have to do with teaching.
        Level indicates section (1) or subsection(2) headings.'''
        if level == 1 :
            section = r'\section'
            subsection = r'\subsection'
        elif level == 2 :
            section = r'\subsection'
            subsection = r'\subsubsection'
        elif level == 3 :
            section = r'\subsubsection'
            subsection = r'\paragraph'
        else :
            raise ValueError
        teaching_presentations = False
        for presentation in data.presentation :
            if presentation.teaching :
                teaching_presentations = True
                break
        if teaching_presentations :
            print (section + '{Presentations Concerning Teaching',
                r'\textrm{(presenter is underlined)}}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.presentation) :
                if pub.teaching :
                    pub.write (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)

##############################################################################

    # Course Evaluations {{{2
    def course_evaluations (data, texfile, level=2, max_columns=4) :

        "Prints a table of the CV author's course evaluations."

        course = courses_from_this_school(data.course, reverse = True)
        done = False
        while not done :
            done = True # we iterate over the whole list until it stops changing
            for c in course :
                if c.guest :
                    course.remove(c)
                    done = False
                    break
                if c.responses is None :
                    done = False
                    course.remove(c)
                    break
        if len(course) == 0 : return # skip if no classes taught
        # FIXME
        print (r'% uncomment the line below to break the page before the table',
            file = texfile)
        print (r'%\needspace{11\baselineskip}', file = texfile) # requires needspace package
        if level == 1 :
            section = r'\section'
            subsection = r'\subsection'
        elif level == 2 :
            section = r'\subsection'
            subsection = r'\subsubsection'
        else :
            raise ValueError
        print (section + '{Course Evaluations}', file = texfile)
        print (r'\begin{footnotesize}', file = texfile)
        #print (r'\begin{tabular}{l |', end = '', file = texfile)
        print (r'\begin{longtable}{l |', end = '', file = texfile)
        ncolumns = min(max_columns, len(courses_from_this_school(data.course))+1)
        print (' l' * ncolumns, end = '', file = texfile)
        print (r'}', file = texfile)
        print (r'  \multicolumn{' + str(ncolumns+1) \
            + r'}{l}{\emph{Continued on next page\dots}}\endfoot',
            file = texfile)
        print (r'\kill\endlastfoot', file = texfile)
        print (r'\hline', file = texfile)

        # BEGIN find mean over ALL classes
        k = len(course)
        # FIXME
        overall = Course (school = None, title = None,
            number = r'\textbf{OVERALL}', semester = [''], year = '',
            credits = 0, students = 0, responses = 0, content_score = 0.0,
            delivery_score = 0.0, environment_score = 0.0,
            assessment_score = 0.0, effectiveness_score = 0.0,
            composite_score = 0.0, composite_AB_score = 0.0, mean_GPA = 0.0)
        nresponse = sum(0 if x.responses is None else x.responses \
            for x in course)
        nstudents = sum(0 if x.responses is None else x.students \
            for x in course)
        for c in course :
            if c.responses is None :
                continue
            overall.credits += (0 if c.students is None \
                                  else c.students * c.credits)
            overall.students += (0 if c.students is None else c.students)
            overall.responses += (0 if c.responses is None else c.responses)
            overall.content_score += (0.0 if c.content_score is None \
                else c.content_score * c.responses / nresponse)
            overall.delivery_score += (0.0 if c.delivery_score is None \
                else c.delivery_score * c.responses / nresponse)
            overall.environment_score += (0.0 if c.environment_score is None \
                else c.environment_score * c.responses / nresponse)
            overall.assessment_score += (0.0 if c.assessment_score is None \
                else c.assessment_score * c.responses / nresponse)
            overall.effectiveness_score += (0.0 if c.effectiveness_score \
                is None else c.effectiveness_score * c.responses / nresponse)
            overall.composite_score += (0.0 if c.composite_score is None \
                else c.composite_score * c.responses / nresponse)
            overall.composite_AB_score += (0.0 if c.composite_score is None \
                else c.composite_AB_score * c.responses / nresponse)
            if c.mean_GPA is not None :
                overall.mean_GPA += \
                    c.mean_GPA * (c.students - c.dropped) / nstudents
        # END
        #course.append(overall)

        # Make the table
        TABLE_HEIGHT = 13
        offset = 0
        max_j = min(len(course), max_columns)
        table = [ [ None for j in range(max_j + 1) ] \
            for i in range(TABLE_HEIGHT) ]
        table[0][0] = 'Course'
        table[1][0] = 'Semester'
        table[2][0] = 'Credits'
        table[3][0] = 'Students'
        table[4][0] = 'Responses'
        table[5][0] = 'Content/Structure'
        table[6][0] = 'Delivery'
        table[7][0] = 'Learning Environment'
        table[8][0] = 'Assessment'
        table[9][0] = 'Effectiveness'
        table[10][0] = 'Composite'
        table[11][0] = 'Composite (expecting A/B)'
        table[12][0] = 'Mean GPA'
        offset = 0
        while True :
            # first, clear previous contents
            for j in range(1,max_j + 1) :
                for i in range(TABLE_HEIGHT) :
                    table[i][j] = ''
            for j in range(1,max_j + 1) :
                k = j - 1 + offset
                if k >= len(course) :
                    break
                table[0][j] = course[k].number # course number
                table[1][j] = course[k].semester[0] + str(course[k].year)
                table[2][j] = course[k].credits
                table[3][j] = course[k].students
                table[4][j] = course[k].responses
                table[5][j] = course[k].content_score
                table[6][j] = course[k].delivery_score
                table[7][j] = course[k].environment_score
                table[8][j] = course[k].assessment_score
                table[9][j] = course[k].effectiveness_score
                table[10][j] = course[k].composite_score
                table[11][j] = course[k].composite_AB_score
                table[12][j] = course[k].mean_GPA
            # put Overall in the extreme right column if it's the last row
            if len(course) - offset < max_columns :
                table[0][-1] = overall.number
                #table[1][-1] = ''
                table[1][-1] = str(len(course)) + ' courses'
                table[2][-1] = overall.credits
                table[3][-1] = overall.students
                table[4][-1] = overall.responses
                table[5][-1] = overall.content_score
                table[6][-1] = overall.delivery_score
                table[7][-1] = overall.environment_score
                table[8][-1] = overall.assessment_score
                table[9][-1] = overall.effectiveness_score
                table[10][-1] = overall.composite_score
                table[11][-1] = overall.composite_AB_score
                table[12][-1] = overall.mean_GPA

            for i in range(TABLE_HEIGHT) :
                for j in range(max_j+1) :
                    if table[i][j] is None :
                        table[i][j] = ''
                    else :
                        if i >= 5 and j > 0 :
                            try :
                                table[i][j] = "%0.2f" % table[i][j]
                            except TypeError :
                                table[i][j] = str(table[i][j])
                        else :
                            table[i][j] = str(table[i][j])
            for i in range(TABLE_HEIGHT-1) :
                print (' & '.join(table[i]), r'\\*', file = texfile)
            print (' & '.join(table[-1]), r'\\', file = texfile)
            print (r'  \hline', file = texfile)
            offset += max_columns
            if offset >= len(course) :
                break
        # If the last column WASN'T printed, print it in its own row
        if len(course) % max_columns == 0 :
            for i in range(TABLE_HEIGHT) :
                for j in range(1,max_j+1) :
                    table[i][j] = ''
            table[0][1] = overall.number # course number
            table[1][1] = str(len(course)) + ' courses'
            table[2][1] = overall.credits
            table[3][1] = overall.students
            table[4][1] = overall.responses
            table[5][1] = overall.content_score
            table[6][1] = overall.delivery_score
            table[7][1] = overall.environment_score
            table[8][1] = overall.assessment_score
            table[9][1] = overall.effectiveness_score
            table[10][1] = overall.composite_score
            table[11][1] = overall.composite_AB_score
            table[12][1] = overall.mean_GPA
            for i in range(TABLE_HEIGHT) :
                for j in range(max_j+1) :
                    if table[i][j] is None :
                        table[i][j] = ''
                    else :
                        if i >= 5 and j > 0 :
                            try :
                                table[i][j] = "%0.2f" % table[i][j]
                            except TypeError :
                                table[i][j] = str(table[i][j])
                        else :
                            table[i][j] = str(table[i][j])
            for i in range(TABLE_HEIGHT-1) :
                print (' & '.join(table[i]), r'\\*', file = texfile)
            print (' & '.join(table[-1]), r'\\', file = texfile)
        #print (r'\end{tabular}', file = texfile)
        print (r'\end{longtable}', file = texfile)
        print (r'\end{footnotesize}', file = texfile)

##############################################################################

    # MU Course Evaluation Table (Teaching section) # {{{2
    def course_evaluation_table (data, texfile, level = 2) :

        """Prints a table of the CV author's course evaluations. This version
           is intended to match the format required by the University of
           Missouri in the Provost's call letter."""

        if level == 1 :
            section = r'\section'
            subsection = r'\subsection'
        elif level == 2 :
            section = r'\subsection'
            subsection = r'\subsubsection'
        else :
            raise ValueError
        print (r'\cleardoublepage', file = texfile)
        print (section + '{Course Evaluation Table}', file = texfile)
        print (r'\colorlet{cellbg}{lightgray!70}', file = texfile)
        #print (r'\colorlet{cellbg}{lightgray}', file = texfile)
        #print (r'\colorlet{cellbg}{white}', file = texfile)
        print (r'\begin{small}\noindent', file = texfile)
        print (r'\setlength{\extrarowheight}{1pt}%', file = texfile)
        print (r'\renewcommand{\tabularxcolumn}[1]{b{#1}}%', file = texfile)
        print (r'  \setlength{\tabcolsep}{0.1em}%', file = texfile)
        print (r'\begin{tabularx}{\linewidth}{c C >{\centering}b{0.5in} C C C C} \hline',
            file = texfile)
        print (r'  \bfseries\cellcolor{cellbg}{Semester}', file = texfile)
        print (r'& \bfseries\cellcolor{cellbg}{Course Number}', file = texfile)
        #print (r'& \bfseries\cellcolor{cellbg}{Credits}', file = texfile)
        print (r'& \bfseries\cellcolor{cellbg}{Credit Hours}', file = texfile)
        print (r'& \bfseries\cellcolor{cellbg}{Number of Students/ Number Evaluating}',
            file = texfile)
        print (r'& \bfseries\cellcolor{cellbg}{Mean Course GPA}',
            file = texfile)
        print (r'& \bfseries\cellcolor{cellbg}{Mean Composite Evaluation}',
            file = texfile)
        print (r'& \bfseries\cellcolor{cellbg}{Department Average for Course',
            'Level}', file = texfile)
        print (r'  \\ \hline', file = texfile)
        course = courses_from_this_school(data.course, reverse = True)
        for row in course :
            if row.responses is None :
                continue
            if row.mean_GPA is None :
                mean_GPA = ''
            else :
                mean_GPA = round(row.mean_GPA,3)
            if row.mean_composite_score is None :
                mean_composite = '(unavailable)'
            else :
                mean_composite = ('%0.02f' % row.mean_composite_score) + '/5.0'
            print (' ', row.semester[0] + str(row.year), '&', row.number, '&',
                row.credits, '&', str(row.students) + '/' + str(row.responses),
                '&', ('%0.03f' %  mean_GPA), '&',
                ('%0.02f' % row.composite_score), '&',
                mean_composite, r'\\',
                file = texfile)
        print (r'  \hline', file = texfile)
        print (r'\end{tabularx}', file = texfile)
        print (r'\end{small}', file = texfile)

##############################################################################

    # Student engagement {{{2
    def student_engagement (data, texfile, level = 2) :
        'Prints the list of student engagement activities.'
        if level == 1 :
            section = r'\section'
            subsection = r'\subsection'
        elif level == 2 :
            section = r'\subsection'
            subsection = r'\subsubsection'
        else :
            raise ValueError
        if len(data.student_engagement) > 0 :
            print (section + '{Campus-Wide Teaching and Student Engagement',
                'Activities}', file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for item in reversed(data.student_engagement) :
                print (r'\item', item, file = texfile)
            print (r'\end{CVitemize}', file = texfile)

##############################################################################

    # Funding per year graphic {{{2
    def generate_funding_graphic (texfile, right=2.75, top=2.20, spacing=3) :
        "Creates a graphic of the CV author's funding each year."
        try :
            print (r'  \begin{tikzpicture}\small', file = texfile)
        except IOError:
            traceback.print_stack()
            print ("IOError: texfile must be an open, writable file in",
                "generate_funding_graphic", file = sys.stderr)
            raise SystemExit(1)
        print (r'    \node at (', right/2, 'in,', top + 0.30,
            r'in) {\bfseries Total Funding Per Calendar Year};', file = texfile)
        print (r'    \node at (', right/2, 'in,', top + 0.12,
            r'in) {\small (assumes uniform budget over contract duration)};',
                file = texfile)
        lastyear = 1000
        firstyear = datetime.date.today().year
        for grant in data.grant :
            if grant.awarded :
                try :
                    startdate = datetime.datetime.strptime(grant.start,'%m/%d/%Y')
                except ValueError :
                    try :
                        startdate = datetime.datetime.strptime(grant.start,'%m/%Y')
                    except ValueError :
                        startdate = datetime.datetime.strptime(grant.start,'%Y')
                try :
                    enddate = datetime.datetime.strptime(grant.end,'%m/%d/%Y')
                except ValueError :
                    try :
                        enddate = datetime.datetime.strptime(grant.end,'%m/%Y')
                    except ValueError :
                        enddate = datetime.datetime.strptime(grant.end,'%Y')
                startyear = startdate.year
                endyear = enddate.year
                if startyear < firstyear :
                    firstyear = startyear
                if endyear > lastyear :
                    lastyear = endyear
        width = (72.0 * right - (lastyear - firstyear + 2) * spacing) \
                    / (lastyear - firstyear + 1)
        external_fundinginyear = [0]*(lastyear - firstyear + 1)
        internal_fundinginyear = [0]*(lastyear - firstyear + 1)
        for grant in data.grant :
            if grant.awarded :
                try :
                    startdate = datetime.datetime.strptime( \
                        grant.start,'%m/%d/%Y')
                except ValueError :
                    try :
                        startdate = datetime.datetime.strptime(grant.start,'%m/%Y')
                    except ValueError :
                        startdate = datetime.datetime.strptime(grant.start,'%Y')
                try :
                    enddate = datetime.datetime.strptime(grant.end,'%m/%d/%Y')
                except ValueError :
                    try :
                        enddate = datetime.datetime.strptime(grant.end,'%m/%Y')
                    except ValueError :
                        enddate = datetime.datetime.strptime(grant.end,'%Y')
                startyear = startdate.year
                startmonth = startdate.month
                endyear = enddate.year
                endmonth = enddate.month
                duration = (enddate - startdate).days/365.25*12 # months in contract
                if duration < 1 :
                    duration = 1.0
                for year in range(startyear,endyear+1) :
                    if grant.shared_credit is None :
                        shared_credit = 1.0
                    elif grant.shared_credit > 1.0 :
                        shared_credit = grant.shared_credit / 100.0
                    else :
                        shared_credit = grant.shared_credit
                    if year == startyear :
                        months = 12.0 - startmonth + 1
                    elif year == endyear :
                        months = float(endmonth)
                    else :
                        months = 12.0
                    if months < 1 :
                        months = 1.0
                    if grant.external_amount is None :
                        external_fundinginyear[ year - firstyear ] += \
                            float(grant.amount) * shared_credit * \
                                (months / duration)
                    else :
                        external_fundinginyear[ year - firstyear ] += \
                            float(grant.external_amount) * shared_credit * \
                                (months / duration)
                        internal_fundinginyear[ year - firstyear ] += \
                            (float(grant.amount) - \
                             float(grant.external_amount)) \
                               * shared_credit * (months / duration)
        total_fundinginyear = []
#        print ("EXTERNAL FUNDING:", external_fundinginyear)
#        print ("INTERNAL FUNDING:", internal_fundinginyear)
        for i in range(len(external_fundinginyear)) :
            total_fundinginyear.append(
                internal_fundinginyear[i] + external_fundinginyear[i])
        graph_max = 10000*int(max(total_fundinginyear)/10000.0 + 0.5)
        height = (top * 72.0 - spacing) / graph_max
        #stride = int(max(max(total_fundinginyear) / 10.0, 1))
        #stride = int(max(max(total_fundinginyear) / 6.0, 1))
        stride = max(int(graph_max / 6.0 + 0.5), 1)
        # tick marks
        #for y in range (0, int(max(total_fundinginyear)), stride) :
        #for y in range (0, graph_max + stride - 1, stride) :
        for y in range (0, graph_max + stride - 2, stride) :
            print (r'    \draw (-4pt,', y * height, 'pt)', file = texfile)
            print (r'       -- (0,', y * height, 'pt);', file = texfile)
            print (r'    \node[anchor=east] at (-0.25em,', y * height,
                'pt) {', int(y / 1000), 'K};', file = texfile)

        # Draw plot and abscissa
        for year in range(firstyear,lastyear+1) :
            x = (year - firstyear) * width + (year - firstyear + 1) * spacing
            # external funding
            y = external_fundinginyear[year - firstyear] * height
            print (r'    \fill[gray] (', x, 'pt, 0)', file = texfile)
            print (r'      -- (', x, 'pt,', y, 'pt)', file = texfile)
            print (r'      -- (', x + width, 'pt,', y, 'pt)', file = texfile)
            print (r'      -- (', x + width, 'pt,0pt);', file = texfile)
            # internal funding
            y2 = (internal_fundinginyear[year - firstyear]
                + external_fundinginyear[year - firstyear]) * height
            #print (r'    \path[pattern color=gray,pattern=north east lines] (',
            print (r'    \fill[lightgray] (', x, 'pt,', y, 'pt)',
                file = texfile)
            print (r'      -- (', x, 'pt,', y2, 'pt)', file = texfile)
            print (r'      -- (', x + width, 'pt,', y2, 'pt)', file = texfile)
            print (r'      -- (', x + width, 'pt,', y, 'pt);', file = texfile)
            # horizontal axis
            print (r'    \node[rotate=290] at (', x + width/1.7, 'pt,-3ex) {',
                year, '};', file = texfile)
        # Legend
        print (r'    \fill[gray] (', right * 72 + 10, 'pt,',
            top * 72 - 10, 'pt)', file = texfile)
        print (r'      -- ++(10pt,0pt) -- ++(0pt,10pt) -- ++(-10pt,0pt)',
            '-- cycle;', file = texfile)
        print (r'    \node[black,right] at (', right * 72 + 23, 'pt,',
            top * 72 - 4, 'pt) { external };', file = texfile)
        print (r'    \fill[lightgray] (', right * 72 + 10, 'pt,',
            top * 72 - 25, 'pt)', file = texfile)
        print (r'      -- ++(10pt,0pt) -- ++(0pt,10pt) -- ++(-10pt,0pt)',
            '-- cycle;', file = texfile)
        print (r'    \node[black,right] at (', right * 72 + 23, 'pt,',
            top * 72 - 19, 'pt) { internal };', file = texfile)
        # Draw box around plot (last so lines are on top of everything)
        print (r'    \draw (0,0) -- (', right, 'in,0)', file = texfile)
        print (r'                -- (', right, 'in,', top, 'in)',
            file = texfile)
        print (r'                -- (0,', top, 'in) -- cycle;',
            file = texfile)
        print (r'  \end{tikzpicture}\par', file = texfile)

##############################################################################

    def CV_numpages (filename) : # {{{2

        ''' Finds the length of the CV portion of the dossier, in pages, based
            on code I inserted into the dossier.'''

        # If we got a tex file, find its aux file
        if filename[-3:] == 'tex' :
            filename = filename[:-3] + 'aux'
        auxfile = open(filename,'r')
        for line in auxfile :
            if re.search('CV-last-page',line) :
                page = int(line.split('{')[-1].split('}')[0])
                return page
        else :
            raise KeyError('Token "CV-last-page" not found in file' + filename)

##############################################################################
## MAIN SUBROUTINE ##
##############################################################################

    ## LaTeX document preamble {{{2
    texfile = open (filename, 'w')
    data.texfile = texfile
    data.texfile_name = filename
    if numbers :
        print (r'\documentclass[11pt,longform,twoside,openright]{MU-dossier}',
            file = texfile)
    else :
        print (r'\documentclass[11pt,longform,twoside,openright,hidenumbers]',
            '{MU-dossier}', sep = '', file = texfile)
    write_preamble (texfile)
    print (r'\usepackage[final]{microtype}', file = texfile) # TODO: should this be in the global preamble?
    print (r'\usepackage{needspace}', file = texfile)
    print (r'\usepackage{pdfpages}', file = texfile)
    print (r'\usepackage{longtable}', file = texfile)
    print (r'\usepackage{tikz}', file = texfile)
    print (r'\usetikzlibrary{patterns}', file = texfile)
    set_typeface (texfile, typeface)
    #print (r'\usepackage[colorlinks,linkcolor=black,urlcolor=black,bookmarksnumbered,pdfusetitle]{hyperref}',
    print (r'\usepackage[hidelinks,bookmarksnumbered,pdfusetitle,pdfpagelabels]{hyperref}',
        file = texfile)
    # BEGIN These lines create commands that can be used
    # in the research and teaching statements. Counts will auto-update.
    data.count.setup_counts (data)
    print (r'\newcommand*{\PapersPublished}{' + \
        str(data.count.npubs) + '}', file = texfile)
    print (r'\newcommand*{\PapersSinceAppointment}{' + \
        str(data.count.npubs_post_appointment) + '}', file = texfile)
    # END
    print (r'\title{Dossier for Promotion and Tenure}', file = texfile)
    print (r'\author{' + data.professor.name + '}', file = texfile)
    #print (r'\colorlet{recent@employee}{DarkRed!15}', file = texfile)
    #print (r'\colorlet{recent@employee}{Green!15}', file = texfile)
    #print (r'\colorlet{recent@employee}{Sepia!15}', file = texfile)
    # MU Blue
    #print (r'\definecolor{recent}{cmyk}{0.65,0.09,0.00,0.53}', file = texfile)
    # MU Orange
    #print (r'\definecolor{recent}{cmyk}{0.05,0.71,1.0,0.23}', file = texfile)
    # MU Red
    print (r'\definecolor{recent}{cmyk}{0.16,0.97,0.86,0.54}', file = texfile)
    # MU Gold
    #print (r'\definecolor{recent}{cmyk}{0,0.25,0.90,0.05}', file = texfile)
    print (r'\colorlet{recent@employee}{recent!15}', file = texfile)
    #print (r'\definecolor{recent}{cmyk}{0.42,0.05,0.98,0.29}', file = texfile)
    #print (r'\colorlet{recent}{DarkRed}', file = texfile)
    #print (r'\colorlet{recent}{Green}', file = texfile)
    #print (r'\colorlet{recent}{DarkBlue}', file = texfile)
    #print (r'\colorlet{recent}{Sepia}', file = texfile)
    print (r'\begin{document}', file = texfile)
    #print (r'\frenchspacing', file = texfile)
    #print (r'\pagestyle{fancy}', file = texfile)
    if CV_only :
        # makes PDF outline go to subsection depth (default: section depth)
        print (r'\setcounter{tocdepth}{2}', file = texfile)
    else :
        print (r'\tableofcontents', file = texfile)
    ## Appointment Letters {{{2
        print (r'\chapter{Appointment Letters}', file = texfile)
        if os.path.isfile('offer-letter.pdf') :
            #print (r'\section{Offer Letter}', file = texfile)
            print (r'\section{Initial Appointment Letter}', file = texfile)
            print (r'\cleardoublepage', file = texfile)
            print (r'\includepdf[pages=-]{offer-letter.pdf}', file = texfile)
            print (r'\cleardoublepage', file = texfile)
        #if os.path.isfile('appointment-extension-1.pdf') :
        #    print (r'\section{Appointment Extension Letter (first year)}',
        #        file = texfile)
        #    print (r'\cleardoublepage', file = texfile)
        #    print (r'\includepdf[pages=-]{appointment-extension-1.pdf}',
        #        file = texfile)
        #    print (r'\cleardoublepage', file = texfile)
        #if os.path.isfile('appointment-extension-2.pdf') :
        #    print (r'\section{Appointment Extension Letter (second year)}',
        #        file = texfile)
        #    print (r'\cleardoublepage', file = texfile)
        #    print (r'\includepdf[pages=-]{appointment-extension-2.pdf}',
        #        file = texfile)
        #    print (r'\cleardoublepage', file = texfile)
        if os.path.isfile('appointment-extension-3.pdf') :
            #print (r'\section{Appointment Extension Letter (third year)}',
            print (r'\section{Mid-Probationary Review}',
                file = texfile)
            print (r'\cleardoublepage', file = texfile)
            print (r'\includepdf[pages=-]{appointment-extension-3.pdf}',
                file = texfile)
            print (r'\cleardoublepage', file = texfile)
#        if os.path.isfile('core-appointment-1.pdf') :
#            print (r'\section{Appointments as Core Faculty in Other Programs}',
#                file = texfile)
#            print (r'\cleardoublepage', file = texfile)
#            print (r'\includepdf[pages=-]{core-appointment-1.pdf}',
#                file = texfile)
#            print (r'\cleardoublepage', file = texfile)
#        if os.path.isfile('courtesy-appointment-1.pdf') :
#            print (r'\section{Appointments as Courtesy Faculty in Other Departments}',
#                file = texfile)
#            print (r'\cleardoublepage', file = texfile)
#            print (r'\includepdf[pages=-]{courtesy-appointment-1.pdf}',
#                file = texfile)
#            print (r'\cleardoublepage', file = texfile)
        if os.path.isfile('probationary-extension.pdf') :
            print (r'\section{Letter Extending the Probationary Period}',
                file = texfile)
            print (r'\cleardoublepage', file = texfile)
            print (r'\includepdf[pages=-]{probationary-extension.pdf}',
                file = texfile)
            print (r'\cleardoublepage', file = texfile)
        if os.path.isfile('post-tenure-review-1.pdf') :
            print (r'\section{Post-Tenure Reviews}',
                file = texfile)
            print (r'\cleardoublepage', file = texfile)
            print (r'\includepdf[pages=-]{post-tenure-review-1.pdf}',
                file = texfile)
            print (r'\cleardoublepage', file = texfile)
            for n in range(2,6) :
                if os.path.isfile('post-tenure-review-' + str(n) + '.pdf') :
                    print (r'\includepdf[pages=-]{post-tenure-review-' \
                        + str(n) + '.pdf}', file = texfile)

    # Department letters {{{2
        print (r'\chapter{Department Recommendation Letters and Procedures}',
            file = texfile)
        print (r'   \clearpage', file = texfile)
#        print (r'\section{Department Promotion and Tenure Guidelines}',
#            file = texfile)
#        print (r'   \clearpage', file = texfile)
#        print (r'\section{Department Committee Recommendation Letter}',
#            file = texfile)
#        print (r'   \clearpage', file = texfile)
#        print (r'\section{Department Chair Recommendation Letter}',
#            file = texfile)
#        print (r'   \clearpage', file = texfile)
#        print (r'\section{Comments from Tenured Faculty in the Department}',
#            file = texfile)
#        print (r'   \clearpage', file = texfile)
#        print (r'\section{Report on Process, Votes, and Appeals}',
#            file = texfile)
#        print (r'   \clearpage', file = texfile)
#        print (r'\section{Letters from Joint, Center, and Courtesy',
#            'Appointments}', file = texfile)
        # College letters {{{2
        print (r'\chapter{College Recommendation Letters and Procedures}',
            file = texfile)
#        print (r'   \clearpage', file = texfile)
#        print (r'\section{College Committee Recommendation Letter}',
#            file = texfile)
#        print (r'   \clearpage', file = texfile)
#        print (r'\section{Report on Process, Votes, and Appeals}',
#            file = texfile)
#        print (r'   \clearpage', file = texfile)
#        print (r'\section{Dean Recommendation Letter}', file = texfile)

    ## TAB IV: FULL CV (includes subheadings below) {{{2
    print (r'\setcounter{chapter}{3}%', file = texfile)
    print (r'\chapter{Curriculum Vitae}', file = texfile)
    print (r'\vspace{-2.5ex}', file = texfile)
    print (r'\bibliographystyle{CV}', file = texfile)
    if bibliography is not None :
        #papers = [pub.key for pub in data.publication]
        #papers = ['CV'] + list(set(papers))
        #try :
        #    papers.remove(None)
        #except ValueError :
        #    pass
        #keys = ','.join(papers)
        #print (r'\nocite{' + keys + '}', file = texfile)
        print (r'\nocite{CV}', file = texfile)
        print (r"\providecommand{\enquote}[1]{``#1''}", file = texfile)
        print (r'\providecommand{\url}[1]{\texttt{#1}}', file = texfile)
        print (r'\providecommand{\urlprefix}[1]{URL }', file = texfile)
        print (r'\nobibliography{' + bibliography + '}', file = texfile)
    # Print header (name, rank, serial number)
    data.professor.write (texfile)

    # SUMMARY {{{3
    print (r'\section{Summary}', file = texfile)
    # Education summary {{{4
    print (r'\begin{education}', file = texfile)
    #for degree in reversed(data.degree) :
    for degree in sorted(reversed(data.degree), key = lambda x: x.order) :
        if not degree.postdoc :
            degree.write (texfile)
    print (r'\end{education}', file = texfile)

    # Appointment summary {{{4
    if sum(x.end_date is None for x in data.jobhistory) == 1 :
        print (r'\subsection{Current University Appointment}', file = texfile)
    elif sum(x.end_date is None for x in data.jobhistory) >= 2 :
        print (r'\subsection{Current University Appointments}', file = texfile)
    if sum(x.end_date is None for x in data.jobhistory) >= 1 :
        print (r'\begin{experience}', file = texfile)
        for appt in reversed(data.jobhistory) :
            if appt.end_date is None :
                appt.write_appt (texfile)
        print (r'\end{experience}', file = texfile)
#    print (r'\vspace{0ex}%', file = texfile)

    # Statistics Summary {{{4
    if len(data.publication) > 0 :
        print (r'\subsection{Publication Statistics}', file = texfile)
        data.count.setup_counts (data)
        data.print_statistics_summary (texfile)
        data.plot_publications_vs_time (texfile)
        data.plot_citations_vs_time (texfile)

    # Teaching ratings {{{4
        # compute average
    means = {'content': 0.0, 'delivery': 0.0, 'environment': 0.0,
        'assessment': 0.0, 'effectiveness': 0.0, 'composite': 0.0,
        'composite_AB': 0.0, 'mean_GPA': 0.0}
    nstudents = 0
    nresponses = 0
    ncourses = 0
    for course in data.course :
        if course.school != constants.SCHOOL :
            continue
        # only counts as a course if we actually have scores back
        if course.content_score is not None :
            ncourses += 1
        if course.students is not None and course.responses is not None :
            nstudents += course.students
        if course.responses is not None :
            nresponses += course.responses
            means['content'] += course.responses * course.content_score
            means['delivery'] += course.responses * course.delivery_score
            means['environment'] += course.responses * course.environment_score
            means['assessment'] += course.responses * course.assessment_score
            means['effectiveness'] += course.responses * course.effectiveness_score
            means['composite'] += course.responses * course.composite_score
            means['composite_AB'] += course.responses * course.composite_AB_score
            means['mean_GPA'] += course.responses * course.mean_GPA
    for i in means :
        try :
            means[i] = means[i] / nresponses
        except ZeroDivisionError :
            means[i] = 0.0
    if len(data.course) > 0 :
        print (r'\subsection{University Student Evaluations (' + \
            str(nresponses) + '/' + str(nstudents), 'students responding,',
                ncourses, 'courses)}',
            file = texfile)
        print (r'\begin{quote}', file = texfile)
        print (r'\begin{description}', file = texfile)
        print (r'   \setlength{\parskip}{4.5pt plus 2pt minus 3.5pt}',
            file = texfile) # ADDED LINE
        print (r'   \item [Content/Structure]', ('%0.02f' % means['content']),
            '/ 5.0', file = texfile)
        print (r'   \item [Delivery]', ('%0.02f' % means['delivery']), '/ 5.0',
            file = texfile)
        print (r'   \item [Environment]', ('%0.02f' % means['environment']),
            '/ 5.0', file = texfile)
        print (r'   \item [Assessment]', ('%0.02f' % means['assessment']),
            '/ 5.0', file = texfile)
        print (r'   \item [Effectiveness]', ('%0.02f' % means['effectiveness']),
            '/ 5.0', file = texfile)
        print (r'   \item [Composite]', ('%0.02f' % means['composite']),
            '/ 5.0', file = texfile)
        print (r'   \item [Composite (students expecting A/B)]',
            ('%0.02f' % means['composite_AB']), '/ 5.0', file = texfile)
        print (r'   \item [Mean GPA]', ('%0.02f' % means['mean_GPA']), '/ 4.0',
            file = texfile)
        print (r'\end{description}', file = texfile)
        print (r'\end{quote}', file = texfile)

    # Research funding source summary {{{4
    funding_sources = []
    for grant in data.grant :
        if grant.awarded :
            funding_sources.append(grant.source.split(',')[0])
    if len(funding_sources) > 0 :
        print (r'\subsection{Research Funding Sources}', file = texfile)
        print (', '.join(sorted(set(funding_sources))), file = texfile)

    # Service summary {{{4
    if sum([item.end is None and isinstance(item, LocalService) \
            for item in data.service]) > 0 :
        print (r'\subsection{Current University Service}', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        print (r'   \setlength{\itemsep}{0.20ex}', file = texfile) # ADDED LINE
        #print (r'   \setlength{\itemsep}{4.5pt plus 2pt minus 3.5pt}',
        #    file = texfile) # ADDED LINE
        for item in data.service :
            if item.end is None and isinstance(item, LocalService) :
                item.write (texfile)
        print (r'\end{CVitemize}', file = texfile)
    if sum([item.end is None and isinstance(item,NonLocalService) \
            for item in data.service]) > 0 :
        print (r'\subsection{Current Regional~/ National~/ International '
            'Service}', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for item in data.service :
            if item.end is None and isinstance(item, NonLocalService) :
                item.write (texfile)
        print (r'\end{CVitemize}', file = texfile)

#    print (r'\clearpage', file = texfile)

    # BACKGROUND INFORMATION {{{3
    print (r'\section{Background Information}', file = texfile)
    # Education {{{4
    print (r'\begin{education}', file = texfile)
    #for degree in reversed(data.degree) :
    for degree in sorted(reversed(data.degree), key = lambda x: x.order) :
        if not degree.postdoc :
            degree.write (texfile, longform = True)
    print (r'\end{education}', file = texfile)

    # Job history {{{4
    if len(data.jobhistory) != 0 :
        print (r'\subsection{Professional Experience}', file = texfile)
        print (r'\begin{experience}', file = texfile)
        if isinstance(data.jobhistory, (list,tuple)) :
            for job in reversed(data.jobhistory) :
                job.write (texfile)
        else :
            data.jobhistory.write (texfile)
        print (r'\end{experience}', file = texfile)

    # TEACHING {{{3
    print (r'\section{Teaching}', file = texfile)
    if len(data.course) > 0 :
        print (r'\subsection{Teaching Experience}', file = texfile)
        print (r'\begin{flushleft}', file = texfile)
        print (r'\noindent', file = texfile)
    schools = [data.course[s].school for s in range(len(data.course)-1,0,-1)]
    schools = remove_duplicates (schools)
    # Courses {{{4
    for school in schools :
        print (school, file = texfile)
        courselevels = []
        for course in reversed(data.course) :
            if course.school == school :
                #if course.level not in courselevels :
                #    courselevels.append(course.level)
                if type(course) not in courselevels :
                    courselevels.append(type(course))
        #courselevels.sort()
        for level in courselevels : # {{{5
            if level is UndergraduateCourse :
                print (r'  \begin{courselist}{Undergraduate Courses}\nopagebreak',
                    file = texfile)
            elif level is GraduateCourse :
                print (r'  \begin{courselist}{Graduate Courses}\nopagebreak',
                    file = texfile)
            elif level is TeachingAssistantship :
                print (r'  \begin{courselist}{Teaching Assistantships}\nopagebreak',
                    file = texfile)
            else :
                print ("I don't know about that kind of teaching (" \
                    + str(level) + ")", file = texfile)
                raise TypeError
            existing_course_numbers = []
            existing_course_strings = []
            existing_course_count = []
            #for course in reversed(data.course) : # {{{6
            for course in sorted(data.course, key=lambda x: x.number) : # {{{6
                if isinstance(course, level) and course.school == school :
                    if course.number not in existing_course_numbers :
                        existing_course_numbers.append(course.number)
                        existing_course_count.append(1)
                        if course.guest :
                            existing_course_strings.append(r'    \item '
                                + course.title + ' (' + course.number + ')'
                                + ' (guest lecturer)')
                        else :
                            existing_course_strings.append(r'    \item ' +
                                course.title + ' (' + course.number + ')')
                    else :
                        i = existing_course_numbers.index(course.number)
                        existing_course_count[i] = existing_course_count[i] + 1
            for i in range(len(existing_course_strings)) : # {{{6
                if existing_course_count[i] > 2 :
                    print (existing_course_strings[i],
                        '(' + tocardinal(existing_course_count[i]) + ' times)',
                        file = texfile)
                elif existing_course_count[i] == 2 :
                    print (existing_course_strings[i], '(twice)',
                        file = texfile)
                else :
                    print (existing_course_strings[i], file = texfile)
            print (r'  \end{courselist}', file = texfile)
    if len(data.course) > 0 :
        print (r'\end{flushleft}', file = texfile)

    # Courses Developed {{{4
    ndeveloped = 0
    for course in data.course :
        if course.developed :
            ndeveloped += 1
    if ndeveloped > 0 :
        print (r'\subsection{Courses Developed or Redeveloped}', file = texfile)
        print (r'\begin{CVrevnumerate}', file = texfile)
        for course in reversed(data.course) :
            if course.developed :
                print (r'   \item', course.number + ',', course.title,
                    '(' + course.school + ',',
                    str(course.credits) + '~credits)', '--', file = texfile)
                if isinstance(course, GraduateCourse) :
                    print (r'   graduate course', file = texfile)
                elif isinstance(course,UndergraduateCourse) :
                    print (r'   undergraduate course', file = texfile)
        print (r'\end{CVrevnumerate}', file = texfile)

    # Students {{{4
    if len(data.employee) > 0 :
        print (r'\subsection{Research Supervision and Advising}',
            file = texfile)

    employees_advised (data, texfile, heading = r'\subsubsection')

    teaching_responsibilities (data, texfile)

    # Teaching Awards, Grants, Publications, and Presentations {{{4
    teaching_awards (data, texfile)
    # Awards earned by students {{{4
    #any_awards = False
    #for award in data.award :
    #    if award.student is not None :
    #        any_awards = True
    #        break
    #if any_awards :
    something_to_print = False
    if hide_pre_tenure :
        if data.count.student_awards_post_tenure > 0 :
            print (r'\subsection{Awards Earned by Students',
                '(only those post-tenure are listed)}', file = texfile)
            something_to_print = True
    elif hide_pre_appointment :
        if data.count.student_awards_post_appointment > 0 :
            print (r'\subsection{Awards Earned by Students',
                '(only those post-appointment are listed)}', file = texfile)
            something_to_print = True
    else :
        if data.count.student_awards > 0 :
            print (r'\subsection{Awards Earned by Students}', file = texfile)
            something_to_print = True
    if something_to_print :
        print (r'\begin{CVitemize}', file = texfile)
        for award in reversed(data.award) :
            if award.student is not None :
                if hide_pre_tenure and not award.post_tenure :
                    continue
                if hide_pre_appointment and not award.post_appointment :
                    continue
                award.write (texfile)
        print (r'\end{CVitemize}', file = texfile)
    # 4}}}

    print_teaching_grants (data, texfile, separate = False, long = False)
    student_theses (data, texfile, subdivide = False)
    teaching_publications (data, texfile)
    teaching_presentations (data, texfile)

    #course_evaluations (data, texfile)

    # Professional Development {{{4
    if len(data.teaching_development) > 0 :
        print (r'\subsection{Professional Development in Teaching}',
            file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for item in reversed(data.teaching_development) :
            print (r'\item', item, file = texfile)
        print (r'\end{CVitemize}', file = texfile)

    student_engagement (data, texfile)
    # extension_activities (data, texfile) TODO

    # RESEARCH {{{3
    print (r'\section{Research}', file = texfile)

    # Research Awards {{{4
    research_awards = False
    for award in data.award :
        if not award.teaching and award.student is None :
            research_awards = True
            break
    if research_awards :
        print (r'\subsection{Research Awards and Honors}', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for award in reversed(data.award) :
            if isinstance(award, ResearchAward) and award.student is None :
                award.write (texfile)
        print (r'\end{CVitemize}', file = texfile)

    # Research Grants {{{4
    research_grants = False
    funded_grants = False
    pending_grants = False
    rejected_grants = False
    for grant in data.grant :
        if not grant.teaching :
            research_grants = True
            if grant.awarded :
                funded_grants = True
            elif grant.rejected :
                rejected_grants = True
            else :
                pending_grants = True
            if research_grants and funded_grants and rejected_grants \
                    and pending_grants :
                break # stop looking...
    if research_grants :
        print (r'\subsection{Grants and Contracts}', file = texfile)
        if funded_grants :
            print (r'\subsubsection{Funded Contracts}', file = texfile)
            print (r'\begin{grantlist}', file = texfile)
            for grant in reversed(data.grant) :
                if grant.awarded and not grant.teaching :
                    #grant.write (texfile)
                    grant.write_condensed (texfile)
            print (r'\end{grantlist}', file = texfile)
        if pending_grants :
            #print (r'\penalty -1000%', file = texfile)
            print (r'\subsubsection{Pending Proposals and Letters of Intent}',
                file = texfile)
            print (r'\begin{grantlist}', file = texfile)
            for grant in reversed(data.grant) :
                if not grant.rejected and not grant.awarded \
                        and not grant.teaching :
                    #grant.write (texfile)
                    grant.write_condensed (texfile)
            print (r'\end{grantlist}', file = texfile)
        if show_rejected and rejected_grants :
            print (r'\subsubsection{Rejected Proposals and Letters of Intent}',
                file = texfile)
            print (r'\begin{grantlist}', file = texfile)
            for grant in reversed(data.grant) :
                if grant.rejected and not grant.teaching :
                    #grant.write (texfile)
                    grant.write_condensed (texfile)
            print (r'\end{grantlist}', file = texfile)

    # Invited Talks {{{4
    ninvited = 0
    for talk in data.presentation :
        if isinstance(talk, InvitedTalk) \
                and (show_interviews or not isinstance(talk, Interview)) :
            ninvited += 1
    if ninvited > 0 :
        if show_interviews :
            print (r'\subsection{Invited Presentations}', file = texfile)
        else :
            print (r'\subsection{Invited Presentations (excludes interviews)}',
                file = texfile)
        print (r'\begin{CVrevnumerate}', file = texfile)
        for talk in reversed(data.presentation) :
            if isinstance(talk, InvitedTalk) \
                    and (show_interviews or not isinstance(talk, Interview)) :
                talk.write (texfile, show_presenter = False)
        print (r'\end{CVrevnumerate}', file = texfile)

    # Publications {{{4
    if len(data.publication) > 0 :
        print (r'\subsection{Publications and Presentations}', file = texfile)
        if any([isinstance(x,Postdoc) for x in data.employee]) :
            print (r'''\emph{Graduate students and postdocs in my research
                group are identified in \emph{italics}, while undergraduate
                students in my group are indicated by a \emph{\textsf{different
                typeface}}; the corresponding author is indicated with an
                asterisk (*).}''', file = texfile)
        else :
            print (r'''\emph{Graduate students in my research group are
                identified in \emph{italics}, while undergraduate students in
                my group are indicated by a \emph{\textsf{different typeface}};
                the corresponding author is indicated with an asterisk
                (*).}''', file = texfile)
        print (r'\frenchspacing', file = texfile)
    # Articles
    something_to_print = False
    if hide_pre_tenure :
        if data.count.narticles_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Journal Articles (only',
                'those post-tenure are listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.narticles,
                ']', sep = '', file = texfile)
            something_to_print = True
    elif hide_pre_appointment :
        if data.count.narticles_post_appointment > 0 :
            print (r'\subsubsection{Peer-Reviewed Journal Articles (only',
                'those post-appointment are listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.narticles,
                ']', sep = '', file = texfile)
            something_to_print = True
    else :
        if data.count.narticles > 0 :
            print (r'\subsubsection{Peer-Reviewed Journal Articles}',
                file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            something_to_print = True
    if something_to_print :
        for pub in reversed(data.publication) :
            if hide_pre_tenure and not pub.post_tenure :
                continue
            if hide_pre_appointment and not pub.post_appointment :
                continue
            if pub.peer_reviewed and isinstance(pub,JournalArticle) \
                    and pub.status == constants.PUBLISHED \
                    and not pub.teaching :
                pub.write (texfile)
                #pub.write_citations (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)
    if data.count.naccepted > 0 :
        print (r'\paragraph*{Articles In Press}', file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for pub in data.publication :
            if pub.peer_reviewed and isinstance(pub,JournalArticle) \
                    and pub.status == constants.ACCEPTED and not pub.teaching :
                pub.write (texfile)
                #pub.write_citations (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    if data.count.nsubmitted > 0 :
        print (r'\paragraph*{Articles Currently Under Review}', file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for pub in data.publication :
            if pub.peer_reviewed and isinstance(pub,JournalArticle) and \
                  pub.status == constants.SUBMITTED and not pub.teaching :
                pub.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    if data.count.ninprep > 0 :
        print (r'\paragraph*{Articles in Preparation}', file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for pub in data.publication :
            if pub.peer_reviewed and isinstance(pub,JournalArticle) \
                    and pub.status == constants.UNSUBMITTED \
                    and not pub.teaching  :
                pub.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    # Books
    something_to_print = False
    if hide_pre_tenure :
        if data.count.nbooks_post_tenure > 0 :
            print (r'\subsubsection{Books (only those post-tenure are listed)}',
                file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.nbooks, ']',
                sep = '', file = texfile)
            something_to_print = True
    elif hide_pre_appointment :
        if data.count.nbooks_post_appointment > 0 :
            print (r'\subsubsection{Books (only those post-appointment are',
                'listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.nbooks, ']',
                sep = '', file = texfile)
            something_to_print = True
    else :
        if data.count.nbooks > 0 :
            print (r'\subsubsection{Books}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            something_to_print = True
    if something_to_print :
        for pub in reversed(data.publication) :
            if hide_pre_tenure and not pub.post_tenure :
                continue
            if hide_pre_appointment and not pub.post_appointment :
                continue
            if isinstance(pub,Book) and not pub.teaching :
                pub.write (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)
    # Book chapters
    something_to_show = False
    if hide_pre_tenure :
        if data.count.nchapters_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Book Chapters',
                '(only those post-tenure are listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.nchapters, ']',
                sep = '', file = texfile)
            something_to_show = True
    elif hide_pre_appointment :
        if data.count.nchapters_post_appointment > 0 :
            print (r'\subsubsection{Peer-Reviewed Book Chapters',
                '(only those post-tenure are listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.nchapters, ']',
                sep = '', file = texfile)
            something_to_show = True
    else :
        if data.count.nchapters > 0 :
            print (r'\subsubsection{Peer-Reviewed Book Chapters}',
                file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            something_to_show = True
    if something_to_show :
        for pub in reversed(data.publication) :
            if isinstance(pub,BookChapter) and pub.peer_reviewed \
                    and pub.status == constants.PUBLISHED \
                    and not pub.teaching :
                pub.write (texfile)
                #pub.write_citations (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)
    if data.count.nchapaccepted > 0 :
        print (r'\paragraph*{Book Chapters in Press}', file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for pub in reversed(data.publication) :
            if isinstance(pub,BookChapter) and pub.peer_reviewed and \
                    pub.status == constants.ACCEPTED :
                pub.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    if data.count.nchapsubmitted > 0 :
        print (r'\paragraph*{Book Chapters Currently Under Review}',
            file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for pub in reversed(data.publication) :
            if isinstance(pub,BookChapter) and pub.peer_reviewed and \
                    pub.status == constants.SUBMITTED :
                pub.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    if data.count.nchapinprep > 0 :
        print (r'\paragraph*{Book Chapters in Preparation}', file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for pub in reversed(data.publication) :
            if isinstance(pub,BookChapter) and pub.peer_reviewed and \
                    pub.status == constants.UNSUBMITTED :
                pub.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    # Conference Proceedings
    something_to_print = False
    if hide_pre_tenure :
        if data.count.nproceedings_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Conference Proceedings',
                '(only those post-tenure are listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.nproceedings, ']',
                sep = '', file = texfile)
            something_to_print = True
    elif hide_pre_appointment :
        if data.count.nproceedings_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Conference Proceedings',
                '(only those post-appointment are listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.nproceedings, ']',
                sep = '', file = texfile)
            something_to_print = True
    else :
        if data.count.nproceedings > 0 :
            print (r'\subsubsection{Peer-Reviewed Conference Proceedings}',
                file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            something_to_print = True
    if something_to_print :
        for paper in reversed(data.publication) :
            if isinstance(paper,ConferenceProceedings) \
                    and paper.peer_reviewed and not paper.teaching \
                    and paper.status == constants.PUBLISHED :
                if hide_pre_tenure and not paper.post_tenure :
                    continue
                if hide_pre_appointment and not paper.post_appointment :
                    continue
                paper.write (texfile)
                #paper.write_citations (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)
    if data.count.nprocaccepted > 0 :
        print (r'\paragraph*{Conference Proceedings In Press}',
            file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for paper in data.publication :
            if paper.peer_reviewed \
                    and isinstance(paper,ConferenceProceedings) \
                    and paper.status == constants.ACCEPTED :
                paper.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    if data.count.nprocsubmitted > 0 :
        print (r'\paragraph*{Conference Proceedings Currently Under Review}',
            file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for paper in data.publication :
            if paper.peer_reviewed \
                    and isinstance(paper,ConferenceProceedings) \
                    and paper.status == constants.SUBMITTED :
                paper.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    if data.count.nprocinprep > 0 :
        print (r'\paragraph*{Conference Proceedings in Preparation}',
            file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for paper in data.publication :
            if paper.peer_reviewed \
                    and isinstance(paper,ConferenceProceedings) \
                    and paper.status == constants.UNSUBMITTED :
                paper.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    # Non-refereed proceedings
    something_to_print = False
    if hide_pre_tenure :
        if data.count.nproc_notreviewed_post_tenure > 0 :
            print (r'\subsubsection{Non-Peer-Reviewed Conference Proceedings',
                '(only those post-tenure are listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.nproc_notreviewed,
                ']', sep = '', file = texfile)
            something_to_print = True
    elif hide_pre_appointment :
        if data.count.nproc_notreviewed_post_appointment > 0 :
            print (r'\subsubsection{Non-Peer-Reviewed Conference Proceedings',
                '(only those post-appointment are listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.nproc_notreviewed,
                ']', sep = '', file = texfile)
            something_to_print = True
    else :
        if data.count.nproc_notreviewed > 0 :
            print (r'\subsubsection{Non-Peer-Reviewed Conference Proceedings}',
                file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            something_to_print = True
    if something_to_print :
        for paper in data.publication :
            if hide_pre_tenure and not paper.post_tenure :
                continue
            if hide_pre_appointment and not paper.post_appointment :
                continue
            if not paper.peer_reviewed \
                    and isinstance(paper,ConferenceProceedings) \
                    and not paper.teaching \
                    and paper.status == constants.PUBLISHED :
                paper.write (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)
    if data.count.nproc_notreviewed_inprep > 0 :
        print (r'\paragraph*{Conference Proceedings in Preparation}',
            file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for paper in data.publication :
            if paper.peer_reviewed \
                    and isinstance(paper,ConferenceProceedings) \
                    and paper.status == constants.UNSUBMITTED :
                paper.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    # Other publications
    something_to_show = False
    if hide_pre_tenure :
        if data.count.nother_post_tenure > 0 :
            print (r'\subsubsection{Other Publications',
                '(only those post-tenure are listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.nother_post_tenure,
                ']', sep = '', file = texfile)
            something_to_show = True
    elif hide_pre_appointment :
        if data.count.nother_post_appointment > 0 :
            print (r'\subsubsection{Other Publications',
                '(only those post-appointment are listed)}', file = texfile)
            print (r'\begin{CVrevnumerate}[',
                data.count.nother_post_appointment, ']',
                sep = '', file = texfile)
            something_to_show = True
    else :
        if data.count.nother > 0 :
            print (r'\subsubsection{Other Publications}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            something_to_show = True
    if something_to_show :
        for pub in reversed(data.publication) :
            if hide_pre_tenure and not pub.post_tenure :
                continue
            if hide_pre_appointment and not pub.post_appointment :
                continue
            if not pub.peer_reviewed \
                    and not isinstance(pub,(Book,ConferenceProceedings)) :
                pub.write (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)

    # Patents {{{4
    if len(data.patent) > 0 :
        print (r'\subsubsection{Patents}', file = texfile)
        print (r'\begin{CVrevnumerate}', file = texfile)
        for patent in reversed(data.patent) :
            patent.write (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)

    # Information Disclosures TODO {{{4
    # Do this when you get one...
    # Presentations and Posters {{{4
    if separate_posters :
        something_to_print = False
        if hide_pre_tenure and data.count.oral_post_tenure > 0 :
            print (r'\subsubsection{Oral Presentations (only those',
                'post-tenure are shown; presenter is underlined)}',
                file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.oral, ']',
                sep = '', file = texfile)
            something_to_print = True
        elif hide_pre_appointment \
              and data.count.oral_post_appt_pre_tenure \
                + data.count.oral_post_tenure > 0 :
            print (r'\subsubsection{Oral Presentations (only those',
                'post-appointment are shown; presenter is underlined)}',
                file = texfile)
            print (r'\begin{CVrevnumerate}[', data.count.oral, ']',
                sep = '', file = texfile)
            something_to_print = True
        else :
            if data.count.oral > 0 :
                print (r'\subsubsection{Oral Presentations',
                    '(presenter is underlined)}', file = texfile)
                print (r'\begin{CVrevnumerate}', file = texfile)
                something_to_print = True
        if something_to_print :
            for pres in reversed(data.presentation) :
                if pres.teaching :
                    continue
                if hide_pre_tenure and not pres.post_tenure :
                    continue
                if hide_pre_appointment and not pres.post_appointment :
                    continue
                if not isinstance(pres,Poster) :
                    pres.write (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        # Posters
        something_to_print = False
        if hide_pre_tenure :
            if data.count.poster_post_tenure > 0 :
                print (r'\subsubsection{Posters (only those post-tenure',
                    'are listed; presenter is underlined)}', file = texfile)
                print (r'\begin{CVrevnumerate}[', data.count.poster, ']',
                    sep = '', file = texfile)
                something_to_print = True
        elif hide_pre_appointment :
            if data.count.poster_post_tenure \
              + data.count.poster_post_appt_pre_tenure > 0 :
                print (r'\subsubsection{Posters (only those post-appointment',
                    'are listed; presenter is underlined)}', file = texfile)
                print (r'\begin{CVrevnumerate}[', data.count.poster, ']',
                    sep = '', file = texfile)
                something_to_print = True
        else :
            if data.count.poster > 0 :
                print (r'\subsubsection{Posters (presenter is underlined)}',
                    file = texfile)
                print (r'\begin{CVrevnumerate}', file = texfile)
                something_to_print = True
        if something_to_print :
            for pres in reversed(data.presentation) :
                if pres.teaching :
                    continue
                if hide_pre_tenure and not pres.post_tenure :
                    continue
                if hide_pre_appointment and not pres.post_appointment :
                    continue
                if isinstance(pres,Poster) :
                    pres.write (texfile, poster_note = '')
            print (r'\end{CVrevnumerate}', file = texfile)
    else : # don't separate posters
        something_to_print = False
        if hide_pre_tenure and data.count.poster_post_tenure > 0 :
            print (r'\subsubsection{Presentations and Posters (only those',
                'post-tenure are listed; presenter is underlined)}',
                file = texfile)
            something_to_print = True
        elif hide_pre_appointment and data.count.poster_post_appt_pre_tenure \
                + data.count.poster_post_tenure > 0 :
            print (r'\subsubsection{Presentations and Posters (only those',
                'post-appointment are listed; presenter is underlined)}',
                file = texfile)
            something_to_print = True
        elif data.count.poster > 0 :
            print (r'\subsubsection{Presentations and Posters',
                '(presenter is underlined)}', file = texfile)
            something_to_print = True
        if something_to_print :
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pres in reversed(data.presentation) :
                if not pres.teaching :
                    pres.write (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)

    # Popular Press Coverage {{{4
    if show_news and len(data.news) > 0 :
        print (r'\subsubsection{Press Coverage}', file = texfile)
        print (r'\begin{CVrevnumerate}', file = texfile)
        for news in reversed(data.news) :
            news.write (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)
    
#    print (r'\nonfrenchspacing', file = texfile)

    # SERVICE {{{3
    print (r'\section{Service}', file = texfile)

    # Society Memberships {{{4
    if len(data.society) > 0 :
        print (r'\subsection{Professional Societies}',
            file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for society in reversed(data.society) :
            if society.abbr is None :
                print (r'  \item', society.name + ',', file = texfile)
            else :
                print (r'  \item', society.name, '(' + society.abbr + '),',
                    file = texfile)
            if isinstance(society.dates, (list,tuple)) :
                print (', '.join(society.dates), file = texfile)
            elif society.dates is not None :
                print (society.dates, file = texfile)
            if not society.active :
                print (r'(inactive)', file = texfile)
            
        print (r'\end{CVitemize}', file = texfile)

    # Regional/National/International Service {{{4
    if len(data.session) + len(data.panel) + len(data.journal_review) \
            + sum( isinstance(x,NonLocalService) for x in data.service ) > 0 :
        print (r'\subsection{Regional, National, and International Service}',
            file = texfile)
    # Conference organizing / etc.
    if len(data.session) > 0 :
        print (r'''\subsubsection{Regional, National, and International
            Conferences, Workshops, and Meetings}''', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for conference in reversed(data.session) :
            conference.write(texfile)
        print (r'\end{CVitemize}', file = texfile)
    # Proposal Review {{{5
    if len(data.panel) > 0 :
        print (r'\subsubsection{Proposal Review}', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for panel in reversed(data.panel) :
            panel.write (texfile)
        print (r'\end{CVitemize}', file = texfile)
    # Manuscript Review {{{5
    if len(data.journal_review) > 0 :
        reviews = remove_duplicates(data.journal_review)
        for review in reviews :
            review.count = 0
        for jreview in data.journal_review :
            for review in reviews :
                if review.journal == jreview.journal :
                    review.recent = review.recent or jreview.recent
                    review.count += 1
                    if jreview.earliest < review.earliest :
                        review.earliest = jreview.earliest
                    if jreview.latest > review.latest :
                        review.latest = jreview.latest
        #reviews.reverse()
        #reviews = sorted(reviews, key=lambda x: x.latest, reverse = True)
        print (r'\subsubsection{Manuscript Review}', file = texfile)
        #print (r'\begin{CVitemize}', file = texfile)
        journals = []
        for journal in reviews :
            #journal.write (texfile, print_count=False)
            ##journals.append(r'\emph{' + journal.journal + '} (' \
            ##    + str(journal.count) + ')')
            journals.append(r'\emph{' + journal.journal + '}')
        journals.sort()
        print (', '.join(journals), file=texfile)
        #print (r'\end{CVitemize}', file = texfile)
    # Other Regional/National/International Service {{{5
    if any ( isinstance(x, NonLocalService) for x in data.service ) :
        print (r'\subsubsection{Other Regional, National, and International',
            'Service}', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for activity in reversed(data.service) :
            if isinstance(activity, NonLocalService) :
                activity.write (texfile)
        print (r'\end{CVitemize}', file = texfile)

    # University/College/Department Service {{{5
    if any( isinstance(service, LocalService) for service in data.service ) :
        print (r'\subsection{University, College, and Department Service}',
            file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for service in reversed(data.service) :
            if isinstance(service, LocalService) :
                service.write (texfile)
        print (r'\end{CVitemize}', file = texfile)

    # make a marker for the end of the CV
    print (r'\makeatletter\write\@auxout{',
        r'\noexpand\newlabel{CV-last-page}{{\thesection}{\arabic{page}}}',
        r'}\makeatother',
        sep = '', file = texfile)

    if not CV_only :

    ## TAB V: TEACHING {{{2
        print (r'\chapter{Teaching and the Scholarship of Teaching}',
            file = texfile)
        print (r'\let\oldthesection\thesection \renewcommand*{\thesection}{\Alph{section}}', file = texfile)
        print (r'\section{Summary of Teaching Achievements}',
            file = texfile)
        # Statement on Teaching {{{3
        # Warn the user if this is longer than one page        
        print (r'\newcounter{teachingstatement}', file = texfile)
        print (r'\setcounter{teachingstatement}{\value{page}}', file = texfile)
        if os.path.isfile ('teaching-statement.tex') :
            print (r'\clearpage', file = texfile)
            print (r'\subsection{Statement on Teaching}', file = texfile)
            print (r'\addtolength{\parindent}{1em}\noindent', file = texfile)
            print (r'\input{teaching-statement}', file = texfile)
        elif os.path.isfile ('teaching-statement.pdf') :
            print (r'\includepdf{teaching-statement.pdf}',
                file = texfile)
        print (r'\ifnum\value{teachingstatement}<\value{page}', file=texfile)
        print (r'''  \ClassWarningNoLine{MU-Dossier}{Teaching statement\space
            is more than one page long.}''', file = texfile)
        print (r'\fi', file = texfile)
        # 3}}}

        teaching_responsibilities (data, texfile, level = 2)

        # Use of instructional technology {{{3
        if len(data.technology) > 0 :
            print (r'\subsection{Use of Instructional Technology}',
                file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for item in data.technology :
                print (r'\item', item, file = texfile)
            print (r'\end{CVitemize}', file = texfile)

        # Noteworthy teaching-related accomplishments # {{{3
        print (r'''\subsection{Noteworthy Teaching-Related
            Accomplishments}''', file = texfile)
        teaching_awards (data, texfile, level = 3)
        print_teaching_grants (data, texfile, level = 3, separate = True,
            long = True)
        teaching_publications (data, texfile, level = 2, subdivide = True)
        teaching_presentations (data, texfile, level = 3)
        student_theses (data, texfile, level = 3, subdivide = True,
            show_committee=True)

        course_evaluation_table (data, texfile, level = 1) # {{{3
        print (r'\par\noindent', file = texfile)
        if os.path.isfile ('teaching-eval-interpretation.tex') :
            #print (r'\begin{em}%', file = texfile)
            print (r'\input{teaching-eval-interpretation.tex}', file = texfile)
            #print (r'\end{em}', file = texfile)
        elif os.path.isfile ('teaching-eval-interpretation.pdf') :
            print (r'\includepdf[pages=-]{teaching-eval-interpretation.pdf}',
                file = texfile)

        # Student Advising {{{3
        print (r'\cleardoublepage', file = texfile)
        print (r'\section{Summary of Student Advising}',
            file = texfile)
        # Awards earned by students {{{4
        any_awards = False
        for award in data.award :
            if award.student is not None :
                any_awards = True
                break
        if any_awards :
            print (r'\subsection{Awards Earned by Students}', file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for award in reversed(data.award) :
                if award.student is not None :
                    award.write (texfile)
            print (r'\end{CVitemize}', file = texfile)

        # List of current and former students {{{4
        employees_advised (data, texfile, heading=r'\subsection')
#        for current in [True,False] :
#            if current :
#                prefix = 'Current '
#            else :
#                prefix = 'Past '
#            for level in [VISITING_PROF,POSTDOC,DOCTORAL,MASTERS,UNDERGRADUATE,DISSERTATION_COMMITTEE] :
#                written = False
#                if level == VISITING_PROF : # {{{4
#                    continue
#                    print (r'\subsection{' + prefix + 'Visiting Scholars}',
#                        file = texfile)
#                elif level == POSTDOC : # {{{4
#                    written = False
#                    if any(data.employee[i].level == POSTDOC and
#                           data.employee[i].current == current
#                             for i in range(len(data.employee))) :
#                        print (r'\subsection{' + prefix 
#                          + 'Post-Doctoral Scholars}', file = texfile)
#                        #print (r'\begin{tabular}{l l l l l}', file = texfile)
#                        #print (r'Name & Field & Start Date & Project & Funding',
#                        #    r'\\ \hline', file = texfile)
#                        print (r'\begin{CVrevnumerate}', file = texfile)
#                        written = True
#                    for postdoc in reversed(data.employee) :
#                        if postdoc.level == POSTDOC and postdoc.current == current :
#                            postdoc.write (texfile, print_address = True)
#                    if written :
#                        #print (r'\end{tabular}', file = texfile)
#                        print (r'\end{CVrevnumerate}', file = texfile)
#
#                elif level == DOCTORAL or level == MASTERS : # {{{4
#                    written = False
#                    if any(data.employee[i].level == level and
#                           data.employee[i].current == current
#                           for i in range(len(data.employee))) :
#                        if level == DOCTORAL :
#                            print (r'\subsection{' + prefix
#                                + 'Doctoral Students}', file = texfile)
#                        else :
#                            print (r'\subsection{' + prefix
#                                + "Master's Students}", file = texfile)
#                        #print (r'\begin{tabularx}{\linewidth}{l l L l} \hline',
#                        #    file = texfile)
#                        #print (r'Name & Degree Sought & Funding Source &',
#                        #    r'Graduation \\ \hline', file = texfile)
#                        print (r'\begin{CVrevnumerate}', file = texfile)
#                        written = True
#                    for student in reversed(data.employee) :
#                        if student.level == level and \
#                                student.current == current :
#                            student.write (texfile, print_funding = True,
#                                print_address = True)
#                    if written :
#                        #print (r'  \hline', file = texfile)
#                        #print (r'\end{tabularx}', file = texfile)
#                        print (r'\end{CVrevnumerate}', file = texfile)
#                        written = False
#
#                elif level == UNDERGRADUATE : # {{{4
#                    written = False
#                    if any(data.employee[i].level == level and
#                           data.employee[i].current == current
#                           for i in range(len(data.employee))) :
#                        print (r'\subsection{' + prefix +
#                            'Undergraduate Students}', file = texfile)
#                        #print (r'\begin{tabularx}{\linewidth}{P{1.5in} l l L} \hline',
#                        #    file = texfile)
#                        #print (r'Name & Major & Graduation & Project \\ \hline',
#                        #    file = texfile)
#                        print (r'\begin{CVrevnumerate}', file = texfile)
#                        written = True
#                    for student in reversed(data.employee) :
#                        if student.level == level and \
#                                student.current == current :
#                            student.write (texfile, print_funding = True,
#                                print_address = True)
#                    if written :
#                        #print (r'  \hline', file = texfile)
#                        #print (r'\end{tabularx}', file = texfile)
#                        print (r'\end{CVrevnumerate}', file = texfile)
#                elif level == DISSERTATION_COMMITTEE : # {{{4
#                    written = False
#                    if any(data.employee[i].level == level and
#                           data.employee[i].current == current
#                           for i in range(len(data.employee))) :
#                        print (r'\subsection{' + prefix +
#                            'Thesis/Dissertation Committee Memberships}',
#                            file = texfile)
#                        print (r'\begin{CVrevnumerate}', file=texfile)
#                        written = True
#                    for student in reversed(data.employee) :
#                        if student.level == level \
#                                and student.current == current :
#                            student.write (texfile, print_funding = False,
#                                print_address = True)
#                    if written :
#                        print (r'\end{CVrevnumerate}', file = texfile)

        # Peer Reviews {{{3
        print (r'\cleardoublepage', file = texfile)
        print (r'\section{Peer Teaching Reviews}', file = texfile)
        print (r'\cleardoublepage', file = texfile)
        if os.path.isfile ('peer-teaching-review-1.pdf') :
            print (r'\includepdf[pages=-]{peer-teaching-review-1}',
                file = texfile)
            print (r'\cleardoublepage', file = texfile)
        else :
            print (r'\cleardoublepage', file = texfile)
            print (r'\addtocounter{page}{2}', file = texfile)
        if os.path.isfile ('peer-teaching-review-2.pdf') :
            print (r'\includepdf[pages=-]{peer-teaching-review-2}',
                file = texfile)
            print (r'\cleardoublepage', file = texfile)
        else : # "Fake it" by inserting an extra two pages
            print (r'\cleardoublepage', file = texfile)
            print (r'\addtocounter{page}{2}', file = texfile)
        if os.path.isfile ('peer-teaching-review-3.pdf') :
            print (r'\includepdf[pages=-]{peer-teaching-review-3}',
                file = texfile)
            print (r'\cleardoublepage', file = texfile)
        else : # "Fake it" by inserting an extra two pages
            print (r'\cleardoublepage', file = texfile)
            print (r'\addtocounter{page}{2}', file = texfile)

        student_engagement (data, texfile, level = 1) # {{{3

        # extension_activities (data, texfile) # {{{3 TODO

        # Sample teaching publications {{{3
        if os.path.isfile('teaching-sample-1.pdf') :
            print (r'\includepdf[pages=-]{teaching-sample-1.pdf',
                file = texfile)
        if os.path.isfile('teaching-sample-2.pdf') :
            print (r'\includepdf[pages=-]{teaching-sample-2.pdf',
                file = texfile)

    ## TAB VI: RESEARCH {{{2
        print (r'\chapter{Research and Scholarship}', file = texfile)
        print (r'\section{Statement of Scholarly Accomplishments}', # {{{3
            file = texfile)
        if os.path.isfile ('research-statement.tex') :
            print (r'\noindent', file = texfile)
            print (r'\input{research-statement}', file = texfile)

        print (r'\cleardoublepage', file = texfile)
        print (r'\section{Bibliographic List of Scholarly Products}', # {{{3
            file = texfile)
#        # Journal statistics summary {{{3
#        if os.path.isfile ('journal-statistics.tex') :
#            print (r'\input{journal-statistics}', file = texfile)
#        elif os.path.isfile ('journal-statistics.pdf') :
#            print (r'\includepdf[pages=-]{journal-statistics}', file = texfile)

        # Bibliography (pre- and post-appointment/tenure) {{{3
        #print (r'\subsection{Publications and Presentations}', file = texfile)
        # author ordering information {{{4
        print (r'''\noindent
    Author ordering for publications is generally determined as
    follows:
    \begin{CVenumerate}
      \item The first author is the individual who contributed the most overall
        to the writing of the manuscript.  This person may or may not have
        participated in the actual research.
      \item The final author is, generally speaking, the head of the project
        (group author), except in cases in which that person is the first
        author.
      \item Remaining authors are generally listed in decreasing order of their
        contributions to the writing and scientific content of the manuscript.
      \item Students are generally listed before more senior personnel,
        except in cases in which multiple authors contributed significantly to the
        writing (as opposed to the research).
      \item If multiple authors have similar contributions to the manuscript,
        similar involvement in the research, and similar rank, they are often
        listed in groups by institution or in alphabetical order by last name.
    \end{CVenumerate}''', file = texfile)
        ## Publication statistics {{{4
        print (r'\subsection{Publication Statistics}', file=texfile)
        # Rehash of journal publication statistics
        data.print_statistics_summary (texfile, show_pubs_since_appt = True)
        data.plot_publications_vs_time (texfile)
        data.plot_citations_vs_time (texfile, show_wos = True, show_google = True)
        # Department and College comparison
#        if os.access ("pub-vs-average.pdf", os.R_OK) :
#            print (r'''\emph{The following plots show papers and citations per
#    year for me as well as the average in the chemical engineering program,
#    the newly-constituted Department of Biomedical, Biological, and Chemical
#    Engineering (BBCE), and the College of Engineering as a whole. Citations
#    are to papers written in the 2014--2019 window, cited by other papers
#    written in the same window. The data are from Scopus. It should be noted
#    that the data have not been filtered to remove citable items that are not
#    ordinary, peer-reviewed publications (e.g., prefaces to special issues,
#    editorials), and that publications not indexed by Scopus are not
#    included. Citation counts have not been filtered for self-citations.}''',
#                file=texfile)
#            print (r'\begin{center}', file=texfile)
#            print (r'   \includegraphics[height=3in,width=0.9\linewidth,keepaspectratio]{pub-vs-average}',
#                file = texfile)
#            print (r'\end{center}', file = texfile)
    #
        if any([isinstance(x,Postdoc) for x in data.employee]) :
            print (r'''\par\noindent\emph{In the lists that follow, students
                and postdocs in my research group are identified in
                \emph{italics}, while undergraduate students in my group
                are indicated by a \emph{\textsf{different font}}; the
                corresponding author is indicated with an asterisk (*).}''',
                file = texfile)
        else :
            print (r'''\par\noindent\emph{In the lists that follow, students
                in my research group are identified in \emph{italics}, while
                undergraduate students in my group are indicated by a
                \emph{\textsf{different font}}; the corresponding author is
                indicated with an asterisk (*).}''', file = texfile)
        print (r'\frenchspacing', file = texfile)

        # Articles {{{4
        if data.count.narticles + data.count.nsubmitted + data.count.ninprep \
                + data.count.naccepted > 0 :
            print (r'\subsection{Journal Articles}',
                file = texfile)
        if data.count.ninprep > 0 :
            print (r'\subsubsection{Articles in Preparation}',
                file = texfile)
            print (r'\begin{CVenumerate}', file = texfile)
            for pub in data.publication :
                if pub.peer_reviewed and isinstance(pub,JournalArticle) \
                        and pub.status == constants.UNSUBMITTED :
                    pub.write (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVenumerate}', file = texfile)
        if data.count.nsubmitted > 0 :
            print (r'\subsubsection{Recently Submitted Articles}',
                file = texfile)
            print (r'\begin{CVenumerate}', file = texfile)
            for pub in data.publication :
                if pub.peer_reviewed and isinstance(pub,JournalArticle) \
                        and pub.status == constants.SUBMITTED :
                    pub.write (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVenumerate}', file = texfile)
        if data.count.naccepted :
            print (r'\subsubsection{Accepted/In-Press Articles}',
                file = texfile)
            print (r'\begin{CVenumerate}', file = texfile)
            for pub in data.publication :
                if pub.peer_reviewed and isinstance(pub,JournalArticle) \
                        and pub.status == constants.ACCEPTED :
                    pub.write (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVenumerate}', file = texfile)
        if data.count.narticles_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Journal Articles',
                '(Post-Tenure)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if pub.peer_reviewed and isinstance(pub,JournalArticle) \
                        and pub.status == constants.PUBLISHED \
                        and not pub.teaching and pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.narticles_post_appointment \
                - data.count.narticles_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Journal Articles',
                '(Post-Appointment)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if pub.peer_reviewed and isinstance(pub,JournalArticle) \
                        and pub.status == constants.PUBLISHED \
                        and not pub.teaching \
                        and pub.post_appointment and not pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.narticles - data.count.narticles_post_appointment > 0 :
            print (r'\subsubsection{Peer-Reviewed Journal Articles',
                '(Pre-Appointment)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if pub.peer_reviewed and isinstance(pub,JournalArticle) \
                        and pub.status == constants.PUBLISHED \
                        and not pub.teaching \
                        and not pub.post_appointment and not pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)

        # Books {{{4
        if data.count.nbooks > 0 :
            print (r'\subsection{Books}', file = texfile)
        if data.count.nbooks_post_tenure > 0 :
            print (r'\subsubsection{Books (Post-Tenure)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if isinstance(pub,Book) and not pub.teaching \
                      and pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.nbooks_post_appointment \
                - data.count.nbooks_post_tenure > 0 :
            print (r'\subsubsection{Books (Post-Appointment)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if isinstance(pub,Book) and not pub.teaching \
                      and not pub.post_tenure and pub.post_appointment :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.nbooks - data.count.nbooks_post_appointment > 0 :
            print (r'\subsubsection{Books (Pre-Appointment)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if isinstance(pub,Book) and not pub.teaching \
                      and not pub.post_tenure and not pub.post_appointment :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)

        # Book Chapters {{{4
        if data.count.nchapters + data.count.nchapinprep \
                + data.count.nchapaccepted + data.count.nchapsubmitted > 0 :
            print (r'\subsection{Book Chapters}', file = texfile)
        if data.count.nchapters_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Book Chapters',
                '(Post-Tenure)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if isinstance(pub,BookChapter) and pub.peer_reviewed \
                        and pub.status == constants.PUBLISHED \
                        and pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.nchapters_post_appointment \
                - data.count.nchapters_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Book Chapters',
                '(Post-Appointment)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if isinstance(pub,BookChapter) and pub.peer_reviewed \
                        and pub.status == constants.PUBLISHED \
                        and pub.post_appointment and not pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.nchapters - data.count.nchapters_post_appointment \
                - data.count.nchapters_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Book Chapters',
                '(Pre-Appointment)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if isinstance(pub,BookChapter) and pub.peer_reviewed and \
                        pub.status == constants.PUBLISHED and \
                        not pub.post_appointment and not pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)

        # Proceedings {{{4
        if data.count.nproceedings + data.count.nprocinprep \
                + data.count.nprocaccepted + data.count.nprocsubmitted \
                + data.count.nproc_notreviewed_inprep > 0 :
            print (r'\subsection{Conference Proceedings}', file = texfile)
        if data.count.nprocinprep > 0 :
            print (r'\subsubsection{Conference Proceedings in Preparation}',
                file = texfile)
            print (r'\begin{CVenumerate}', file = texfile)
            for pub in data.publication :
                if pub.peer_reviewed \
                        and isinstance(pub, ConferenceProceedings) \
                        and pub.status == constants.UNSUBMITTED :
                    pub.write (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVenumerate}', file = texfile)
        if data.count.nprocsubmitted > 0 :
            print (r'\subsubsection{Recently Submitted Conference Proceedings}',
                file = texfile)
            print (r'\begin{CVenumerate}', file = texfile)
            for pub in data.publication :
                if pub.peer_reviewed \
                        and isinstance(pub,ConferenceProceedings) \
                        and pub.status == constants.SUBMITTED :
                    pub.write (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVenumerate}', file = texfile)
        if data.count.nproceedings_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Conference Proceedings',
                '(Post-Tenure)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if isinstance(pub,ConferenceProceedings) \
                        and pub.peer_reviewed \
                        and pub.status == constants.PUBLISHED \
                        and pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.nproceedings_post_appointment \
                - data.count.nproceedings_post_tenure > 0 :
            print (r'\subsubsection{Peer-Reviewed Conference Proceedings',
                '(Post-Appointment)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if isinstance(pub, ConferenceProceedings) \
                        and pub.peer_reviewed \
                        and pub.status == constants.PUBLISHED \
                        and not pub.post_tenure and pub.post_appointment :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.nproceedings \
                - data.count.nproceedings_post_appointment > 0 :
            print (r'\subsubsection{Peer-Reviewed Conference Proceedings',
                '(Pre-Appointment)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed (data.publication) :
                if isinstance(pub, ConferenceProceedings) \
                        and pub.peer_reviewed \
                        and pub.status == constants.PUBLISHED \
                        and not pub.post_appointment :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)

        # Non-reviewed conference proceedings
        if data.count.nproc_notreviewed_post_tenure > 0 :
            print (r'''\subsubsection{Non-Peer-Reviewed Conference Proceedings
                (Post-Tenure)}''', file / texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if not pub.teaching and not pub.peer_reviewed \
                        and isinstance(pub,ConferenceProceedings) \
                        and pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.nproc_notreviewed_post_appointment \
                - data.count.nproc_notreviewed_post_tenure > 0 :
            print (r'''\subsubsection{Non-Peer-Reviewed Conference Proceedings
                (Post-Appointment)}''', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if not pub.teaching and not pub.peer_reviewed \
                        and isinstance(pub,ConferenceProceedings) \
                        and pub.post_appointment and not pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.nproc_notreviewed \
                - data.count.nproc_notreviewed_post_appointment > 0 :
            print (r'''\subsubsection{Non-Peer-Reviewed Conference Proceedings
                (Pre-Appointment)}''', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if not pub.teaching and not pub.peer_reviewed \
                        and isinstance(pub,ConferenceProceedings) \
                        and not pub.post_appointment and not pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
                    pub.write_journal_stats (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)

        # Other, non-peer-reviewed publications {{{4
        if data.count.nother > 0 :
            print (r'\subsection{Other Non-Peer-Reviewed Publications}',
                file = texfile)
        if data.count.nother_post_tenure > 0 :
            print (r'\subsubsection{Other Non-Peer-Reviewed Publications',
                '(Post-Tenure)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if not pub.teaching and (not pub.peer_reviewed and \
                            not isinstance(pub,(Book,ConferenceProceedings))) \
                        and pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.nother_post_appointment \
                - data.count.nother_post_tenure > 0 :
            print (r'\subsubsection{Other Non-Peer-Reviewed Publications',
                '(Post-Appointment)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if not pub.teaching and (not pub.peer_reviewed and \
                            not isinstance(pub,(Book,ConferenceProceedings))) \
                        and pub.post_appointment and not pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.nother - data.count.nother_post_appointment > 0 :
            print (r'\subsubsection{Other Non-Peer-Reviewed Publications',
                '(Pre-Appointment)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pub in reversed(data.publication) :
                if not pub.teaching and (not pub.peer_reviewed and \
                            not isinstance(pub,(Book,ConferenceProceedings))) \
                        and not pub.post_appointment \
                        and not pub.post_tenure :
                    pub.write (texfile)
                    pub.write_citations (texfile)
                    pub.write_role (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)

        # Presentations and Posters (pre- and post-appointment/tenure) {{{3
        if data.count.oral + data.count.poster > 0 :
            print (r'\subsection{Oral and Poster Presentations}',
                file = texfile)
        if data.count.oral_post_tenure + data.count.poster_post_tenure > 0 :
            print (r'\subsubsection{Presentations and Posters',
                '(Post-Tenure; presenter is underlined)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pres in reversed(data.presentation) :
                if pres.post_tenure and not pres.teaching :
                    pres.write (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.oral_post_appt_pre_tenure \
                + data.count.poster_post_appt_pre_tenure > 0 :
            print (r'\subsubsection{Presentations and Posters',
                '(Post-Appointment; presenter is underlined)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pres in reversed(data.presentation) :
                if pres.post_appointment and not pres.post_tenure \
                        and not pres.teaching :
                    pres.write (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)
        if data.count.oral_pre_appt + data.count.poster_pre_appt > 0 :
            print (r'\subsubsection{Presentations and Posters',
                '(Pre-Appointment; presenter is underlined)}', file = texfile)
            print (r'\begin{CVrevnumerate}', file = texfile)
            for pres in reversed(data.presentation) :
                if not pres.post_appointment and not pres.teaching :
                    pres.write (texfile)
            print (r'\end{CVrevnumerate}', file = texfile)

        # Details on Grants and Contracts {{{3
        print (r'\cleardoublepage', file = texfile)
        print (r'\section{Details on Grants and Contracts}', file = texfile)

        # funding stats {{{4
        print (r'\subsection{Grant Summary}', file = texfile)
        proposed = 0.0
        funded = 0.0
        proposed_sc = 0.0
        proposed_external = 0.0
        proposed_external_sc = 0.0
        proposed_external_PI = 0.0
        proposed_external_PI_sc = 0.0
        funded_sc = 0.0
        funded_external = 0.0
        funded_external_sc = 0.0
        funded_external_PI = 0.0
        funded_external_PI_sc = 0.0
        for x in data.grant :
            try :
                external_amount = x.external_amount
                if external_amount is None :
                    external_amount = x.amount
                external_amount = float(external_amount)
                proposed += float(x.amount)
                if external_amount != 0 :
                    proposed_external += external_amount
                    if x.PI == constants.INVESTIGATOR :
                        proposed_external_PI += external_amount
                if x.shared_credit is not None :
                    proposed_sc += float(x.amount) * x.shared_credit / 100.0
                    if external_amount != 0 :
                        proposed_external_sc += \
                            external_amount * x.shared_credit / 100.0
                        if x.PI == constants.INVESTIGATOR :
                            proposed_external_PI_sc += \
                                external_amount * x.shared_credit / 100.0
                else : # assume it's 100% if no SC was listed
                    proposed_sc += float(x.amount)
                    if external_amount != 0 :
                        proposed_external_sc += external_amount
                        if x.PI == constants.INVESTIGATOR :
                            proposed_external_PI_sc += external_amount
                if x.awarded :
                    funded += float(x.amount)
                    if external_amount != 0 :
                        funded_external += external_amount
                    if x.shared_credit is not None :
                        funded_sc += float(x.amount) * x.shared_credit / 100.0
                        if external_amount != 0 :
                            funded_external_sc += \
                                external_amount * x.shared_credit / 100.0
                            if x.PI == constants.INVESTIGATOR :
                                proposed_external_PI_sc += \
                                    external_amount * x.shared_credit / 100.0
                    else : # assume it's 100% if no SC was listed
                        funded_sc += float(x.amount)
                        if external_amount != 0 :
                            funded_external_sc += external_amount
                            if x.PI == constants.INVESTIGATOR :
                                funded_external_PI_sc += external_amount
            except ValueError :
                raise
        try :
            print (r'\noindent', file = texfile)
            print ('   Proposals submitted: ',
                str(len(data.grant)), '; proposals funded: ',
                str(sum([x.awarded for x in data.grant])), ' (',
                format(float(sum([x.awarded for x in data.grant])) \
                    / len(data.grant) * 100, '.2f'), r'\%)',
                sep = '', file = texfile)
            print (r'\\ Amount proposed: \$', format(proposed, ',.0f'),
                r'; amount funded: \$', format(funded, ',.0f'), ' (',
                format(funded/proposed * 100, '.2f'), r'\%)',
                sep = '', file = texfile)
            print (r'\\ External proposals: \$',
                format(proposed_external, ',.0f'),
                r'; external funding: \$', format(funded_external, ',.0f'),
                ' (', format(funded_external/proposed_external * 100, '.2f'),
                r'\%)', sep = '', file = texfile)
            print (r'\\ Shared credit proposed: \$',
                format(proposed_sc, ',.0f'),
                r'; shared credit funded: \$', format(funded_sc, ',.0f'),
                ' (', format(funded_sc/proposed_sc * 100, '.2f'), r'\%)',
                sep = '', file = texfile)
            print (r'\\ External shared credit proposed: \$',
                format(proposed_external_sc, ',.0f'),
                r'; external shared credit funded: \$',
                format(funded_external_sc, ',.0f'), ' (',
                format(funded_external_sc/proposed_external_sc * 100, '.2f'),
                r'\%)', sep = '', file = texfile)
            print (r'\\ Ext.\ shared credit proposed as PI: \$',
                format(proposed_external_PI_sc, ',.0f'),
                r'; ext.\ shared credit funded as PI: \$',
                format(funded_external_PI_sc, ',.0f'), ' (',
                format(funded_external_PI_sc/proposed_external_PI_sc * 100,
                    '.2f'),
                r'\%)', sep = '', file = texfile)
    #        print (r'\begin{center}', file = texfile)
    #        generate_funding_graphic (texfile)#, top = 1.80)
    #        print (r'\end{center}', file = texfile)
        except ZeroDivisionError :
            print ('WARNING: Division by zero in funding summary.',
                file = sys.stderr)
            pass

        # List of grants {{{4
        nawarded = 0
        nawarded_federal = 0
        npending = 0
        npending_federal = 0
        nrejected = 0
        nrejected_federal = 0
        for grant in data.grant :
            if not grant.teaching :
                if grant.awarded :
                    nawarded += 1
                    if grant.federal :
                        nawarded_federal += 1
                elif grant.rejected :
                    nrejected += 1
                    if grant.federal :
                        nrejected_federal += 1
                else :
                    npending += 1
                    if grant.federal :
                        npending_federal += 1
        if nawarded_federal > 0 :
            print (r'\pagebreak[3]%', file = texfile)
            print (r'\subsection{Funded Federal Grants and Contracts}',
                file = texfile)
            print (r'\begin{grantlist}', file = texfile)
            for grant in reversed (data.grant) :
                if grant.awarded and grant.federal and not grant.teaching :
                    grant.write (texfile, show_description = True)
            print (r'\end{grantlist}', file = texfile)
        if nawarded - nawarded_federal > 0 :
            print (r'\pagebreak[3]%', file = texfile)
            print (r'\subsection{Funded Non-Federal Grants and Contracts}',
                file = texfile)
            print (r'\begin{grantlist}', file = texfile)
            for grant in reversed (data.grant) :
                if grant.awarded and not grant.federal and not grant.teaching :
                    grant.write (texfile, show_description = True)
            print (r'\end{grantlist}', file = texfile)
        if npending_federal > 0 :
            print (r'\pagebreak[2]', file = texfile)
            print (r'''\subsection{Pending Federal Proposals and Letters of
                    Intent}''', file = texfile)
            print (r'\begin{grantlist}', file = texfile)
            for grant in reversed (data.grant) :
                if not grant.awarded and grant.federal and not grant.rejected \
                        and not grant.teaching :
                    grant.write (texfile, show_description = True)
            print (r'\end{grantlist}', file = texfile)
        if npending - npending_federal > 0 :
            print (r'\pagebreak[2]', file = texfile)
            print (r'''\subsection{Pending Non-Federal Proposals and Letters
                    of Intent}''', file = texfile)
            print (r'\begin{grantlist}', file = texfile)
            for grant in reversed (data.grant) :
                if not grant.awarded and not grant.federal \
                        and not grant.rejected and not grant.teaching :
                    grant.write (texfile, show_description = True)
            print (r'\end{grantlist}', file = texfile)

        if show_rejected and nrejected > 0 :
            print (r'\subsection{Rejected Proposals and Letters of Intent}',
                file = texfile)
            print (r'\begin{grantlist}', file = texfile)
            for grant in reversed(data.grant) :
                if grant.rejected and not grant.teaching :
                    grant.write (texfile, show_description = True)
            print (r'\end{grantlist}', file = texfile)

#        # Sample publications {{{3
#        if any([os.path.isfile ('research-sample-1.pdf'), \
#                os.path.isfile ('research-sample-2.pdf'), \
#                os.path.isfile ('research-sample-3.pdf')]) :
#            print (r'\section{Sample Publications}', file = texfile)
#        if os.path.isfile ('research-sample-1.pdf') :
#            print (r'\includepdf[pages=-,pagecommand={\thispagestyle{plain}}]{research-sample-1}', file = texfile)
#        if os.path.isfile ('research-sample-2.pdf') :
#            print (r'\includepdf[pages=-,pagecommand={\thispagestyle{plain}}]{research-sample-2}', file = texfile)
#        if os.path.isfile ('research-sample-3.pdf') :
#            print (r'\includepdf[pages=-,pagecommand={\thispagestyle{plain}}]{research-sample-3}', file = texfile)
#
#        #3}}}
    #2}}}

        print (r'\let\thesection\oldthesection', file = texfile)
        print (r'\chapter{External Reviews}', file = texfile)

    ## Tab VIII: SERVICE {{{2
        print (r'\chapter{Service}', file = texfile)
        # Service awards {{{3
        if any (isinstance(x, ServiceAward) for x in data.award) :
            print (r'\section{Service Awards}', file=texfile)
            print (r'\begin{CVitemize}', file=texfile)
            for award in reversed(data.award) :
                if isinstance(award, ServiceAward) :
                    award.write(texfile)
            print (r'\end{CVitemize}', file=texfile)
        # Department service {{{3
        if any (isinstance(x, DepartmentService) for x in data.service) :
            print (r'\section{Department Service}', file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for service in reversed(data.service) :
                if isinstance(service, DepartmentService) :
                    service.write (texfile)
            print (r'\end{CVitemize}', file = texfile)
        # College service {{{3
        if any (isinstance(x, CollegeService) for x in data.service) :
            print (r'\section{College Service}', file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for service in reversed(data.service) :
                if isinstance(service, CollegeService) :
                    service.write (texfile)
            print (r'\end{CVitemize}', file = texfile)
        # University service {{{3
        if any( isinstance(x, UniversityService) for x in data.service) :
            print (r'\section{University Service}', file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for service in reversed(data.service) :
                if isinstance(service, UniversityService) :
                    service.write (texfile)
            print (r'\end{CVitemize}', file = texfile)
        # System-level service {{{3
        if any (isinstance(x, UniversitySystemService) for x in data.service) :
            print (r'\section{System-Level Service}', file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for service in reversed(data.service) :
                if isinstance(service, UniversitySystemService) :
                    service.write (texfile)
            print (r'\end{CVitemize}', file = texfile)

        services_and_sessions = [x for x in data.service \
            if isinstance(x, NonLocalService)]
        for service in services_and_sessions :
            service.year = service.start if type(service.start) is int else \
                int(service.start[-4:])
        services_and_sessions.extend(data.session)
        services_and_sessions.sort(key=lambda x: x.year)
        # Regional Service {{{3
        if any(isinstance(x, Regional) for x in services_and_sessions) :
            print (r'\section{Regional Service}',
                file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for activity in reversed(services_and_sessions) :
                if isinstance(activity, Regional) :
                    activity.write (texfile)
            print (r'\end{CVitemize}', file = texfile)
        # National Service {{{3
        if any(isinstance(x, National) for x in services_and_sessions) :
            print (r'\section{National Service}',
                file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for activity in reversed(services_and_sessions) :
                if isinstance(activity, National) :
                    activity.write (texfile)
            print (r'\end{CVitemize}', file = texfile)
        # International Service {{{3
        if any ( isinstance(service, International) for service in \
                services_and_sessions ) :
            print (r'\section{International Service}',
                file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for activity in reversed(data.service + data.session) :
                if isinstance(activity, International) :
                    activity.write (texfile)
            print (r'\end{CVitemize}', file = texfile)

    #2}}}
        # Professional societies {{{3
        if len(data.society) > 0 :
            print (r'\section{Membership in Professional Societies}',
                file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for society in reversed(data.society) :
                if society.abbr is None :
                    print (r'  \item', society.name + ',', file = texfile)
                else :
                    print (r'  \item', society.name, '(' + society.abbr + '),',
                        file = texfile)
                if isinstance(society.dates, (tuple,list)) :
                    print (', '.join(society.dates), file = texfile)
                elif society.dates is not None :
                    print (society.dates, file = texfile)
                else :
                    raise TypeError
#                if not society.active :
#                    print (r'(inactive)', file = texfile)
            print (r'\end{CVitemize}', file = texfile)
        # Proposal Review {{{3
        if len(data.panel) > 0 :
            print (r'\section{Proposal Review}', file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for panel in reversed(data.panel) :
                panel.write (texfile)
            print (r'\end{CVitemize}', file = texfile)
        # Manuscript Review {{{3
        if len(data.journal_review) > 0 :
            reviews = remove_duplicates(data.journal_review)
            for review in reviews :
                review.count = 0
            for jreview in data.journal_review :
                for review in reviews :
                    if review.journal == jreview.journal :
                        review.recent = review.recent or jreview.recent
                        review.count += 1
                        if jreview.earliest < review.earliest :
                            review.earliest = jreview.earliest
                        if jreview.latest > review.latest :
                            review.latest = jreview.latest
            reviews = sorted(reviews, key=lambda x: x.latest,
                reverse=True)
            print (r'\section{Manuscript Review}', file = texfile)
            print (r'\begin{CVitemize}', file = texfile)
            for journal in reviews :
                journal.write (texfile)
            print (r'\end{CVitemize}', file = texfile)        

            # Plot of reviews performed each year
            print (r'\begin{center}', file = texfile)
            data.plot_reviews_over_time(texfile, startyear = 2014)
            print (r'\end{center}', file = texfile)
        # 3}}}

    print (r'\end{document}', file = texfile)
    texfile.close()
    generate_pdf (filename)

    CV_pages = CV_numpages(filename)
    if CV_pages > constants.MAX_CV_PAGES :
        print ("WARNING: CV is", CV_pages, "pages, which is longer than the",
            "limit of", constants.MAX_CV_PAGES, file=sys.stderr)

# vim: foldmethod=marker
