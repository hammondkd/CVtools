import datetime
from .tex2pdf import generate_pdf, write_preamble, set_typeface
from .constants import DEPT_TEACHING_AVERAGE, PUBLISHED, ACCEPTED, INPRESS, \
    SUBMITTED, UNSUBMITTED
from . import constants
from .utilities import remove_duplicates, tocardinal
from .course import UndergraduateCourse, GraduateCourse, TeachingAssistantship
from .employee import GraduateCommittee, VisitingProfessor, MastersStudent, \
    DoctoralStudent, GraduateStudent
from .presentation import InvitedTalk, Interview, Poster
from .service import NonLocalService, LocalService

def write_CV (data, filename, bibliography = None, typeface = None,
    show_research_interests = True, show_posters = True,
    show_interviews = False, separate_posters = True,
    show_presentations = True) :

    '''Generates a CV. This is the "short" form, appropriate for most
       purposes. By default, it shows research interests, interviews (as
       invited talks), and presentations; it also by default separates oral
       and poster presentations into separate lists rather than combining the
       two.'''

    constants.IDENTIFY_MINIONS = False

    texfile = open (filename, 'w')
    data.texfile = texfile
    data.texfile_name = filename
    # LateX Preamble # {{{2
    print(r'\documentclass[11pt,letterpaper,hidenumbers]{MU-dossier}',
        file = texfile)
    write_preamble (texfile)
    set_typeface (texfile, typeface)
    # Header/Footer
    print (r'\usepackage{lastpage}', file = texfile)
    print (r'\pagestyle{fancy}', file = texfile)
    print (r'\thispagestyle{plain}', file = texfile)
    print (r'\lhead{\small\textsc{' + data.professor.name + ',',
        data.professor.highest_degree + '}}', file = texfile)
    print (r'\rhead{\small\textsc{Curriculum Vitae}}', file = texfile)
    print (r'\makeatletter\lfoot{\small\itshape\@date}\makeatother',
        file = texfile)
    print (r'\cfoot{}', file = texfile)
    print (r'\rfoot{\small Page~\thepage\space of \pageref{LastPage}}',
        file = texfile)
    print (r'\begin{document}', file = texfile)
    print (r'\frenchspacing', file = texfile)
    print (r'\bibliographystyle{CV-short}', file = texfile)
    if bibliography is not None :
        print (r'\nocite{CV}', file = texfile)
        print (r"\providecommand{\enquote}[1]{``#1''}", file = texfile)
        print (r'\providecommand{\url}[1]{\texttt{#1}}', file = texfile)
        print (r'\providecommand{\urlprefix}[1]{URL }', file = texfile)
        print (r'\nobibliography{' + bibliography + '}', file = texfile)
    # Print personal information (name, rank, serial number) {{{2
    data.professor.write (texfile, large = True)

    # Academic Appointments (will cause problems if empty!) {{{2
    if len(data.jobhistory) != 0 :
        print (r'\subsection{Academic Appointments}', file = texfile)
        print (r'\begin{experience}', file = texfile)
        if isinstance(data.jobhistory, (list,tuple)) :
            for job in reversed(data.jobhistory) :
                if job.onCV :
                    job.write (texfile)
        else :
            data.jobhistory.write (texfile)
        print (r'\end{experience}', file = texfile)

    # Education {{{2
    print (r'\begin{education}', file = texfile)
    # FIXME does this need to be reversed(sorted()) or can it stay?
    for degree in sorted(reversed(data.degree), key = lambda x: x.order) :
        if not degree.postdoc :
            degree.write (texfile, longform=True)
    print (r'\end{education}', file = texfile)

    # Research interests {{{2
    if len(data.research_interests) > 0 and show_research_interests :
        print (r'\subsection{Research Interests}', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for interest in data.research_interests :
            print (r'  \item', interest, file = texfile)
        print (r'\end{CVitemize}', file = texfile)

    # Summary {{{2
    print (r'\subsection{Publication and Teaching Statistics}', file = texfile)
    data.print_condensed_statistics_summary (texfile)
    mean = 0.0
    nresponses = 0
    for course in data.course :
        if course.responses is not None :
            nresponses += course.responses
            mean += course.responses * course.composite_score
    try :
        mean = mean / nresponses
    except ZeroDivisionError :
        mean = 0.0
    print (r'\\ Composite teaching evaluation:',
        str(round(mean,2)) + '/5.0', file = texfile)
    print ('      (department average:', str(DEPT_TEACHING_AVERAGE) + ')',
        file = texfile)

    # Teaching {{{2
    print (r'\section{Teaching}', file = texfile)
    # Teaching awards {{{3
    if sum([x.teaching for x in data.award]) > 0 :
        print (r'\subsection{Teaching Awards and Honors}', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for award in reversed(data.award) :
            if award.teaching :
                award.write (texfile)
        print (r'\end{CVitemize}', file = texfile)
    # Courses {{{3
    print (r'\subsection{Courses Taught (includes guest lectures, as noted)}',
        file = texfile)
    schools = [data.course[s].school for s in range(len(data.course)-1,0,-1)]
    schools = remove_duplicates (schools)
    for school in schools :
        print (school, file = texfile)
        courselevels = []
        if any(isinstance(x,UndergraduateCourse) and x.school == school \
                for x in data.course) :
            courselevels.append(UndergraduateCourse)
        if any(isinstance(x,GraduateCourse) and x.school == school \
                for x in data.course) :
            courselevels.append(GraduateCourse)
        if any(isinstance(x,TeachingAssistantship) and x.school == school\
                for x in data.course) :
            courselevels.append(TeachingAssistantship)
        for level in courselevels : # {{{3
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
                    + str(level) + ")", file = sys.stderr)
                raise TypeError
            existing_course_numbers = []
            existing_course_strings = []
            existing_course_count = []
            for course in reversed(data.course) :
                if isinstance(course, level) and course.school == school :
                    if course.number not in existing_course_numbers :
                        existing_course_numbers.append(course.number)
                        existing_course_count.append(1)
                        if course.guest :
                            existing_course_strings.append(r'    \item '
                                + course.number + ': ' + course.title 
                                + ' (guest lecturer)')
                        else :
                            existing_course_strings.append(r'    \item '
                                 + course.number + ': ' + course.title)
                    else :
                        i = existing_course_numbers.index(course.number)
                        existing_course_count[i] = existing_course_count[i] + 1
            for i in range(len(existing_course_strings)) :
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
    # Current and Former Research Students {{{3
    if len(data.employee) != 0 :
        print (r'\subsection{Current and Former Research Group Members}',
            file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for student in data.employee :
            if not isinstance(student, (GraduateCommittee,VisitingProfessor)) :
                if student.middle is None :
                    full_name = student.first + ' ' + student.last
                else :
                    full_name = student.first + ' ' + student.middle + ' ' \
                        + student.last
                print (r'  \item', student.salutation, full_name + ',',
                    student.description(), file = texfile)
        print (r'\end{CVenumerate}', file = texfile)

    # Research {{{2
    print (r'\section{Research}', file = texfile)
    # Research awards {{{3
    if sum([(not x.teaching and x.student is None) for x in data.award]) > 0 :
        print (r'\subsection{Research Awards}', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for award in reversed(data.award) :
            if not award.teaching and award.student is None :
                award.write (texfile)
        print (r'\end{CVitemize}', file = texfile)

    # Invited Talks {{{3
    if sum([isinstance(x,InvitedTalk) \
            and (show_interviews or not isinstance(x,Interview)) \
            for x in data.presentation]) > 0 :
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

    # Publications {{{3
    if sum([x.peer_reviewed and x.status == PUBLISHED \
            for x in data.publication]) > 0 :
        print (r'\subsection{Peer-Reviewed Publications}', file = texfile)
        print (r'\begin{CVrevnumerate}', file = texfile)
        for paper in reversed(data.publication) :
            if paper.peer_reviewed and paper.status == PUBLISHED :
                paper.write (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)

    if sum([x.peer_reviewed and x.status == ACCEPTED \
            for x in data.publication] ) > 0 :
        print (r'\paragraph*{Accepted Manuscripts}', file = texfile)
        print (r'\begin{CVrevnumerate}', file = texfile)
        for paper in reversed(data.publication) :
            if paper.peer_reviewed and paper.status == ACCEPTED :
                paper.write (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)

    if sum([x.peer_reviewed and x.status == SUBMITTED \
            for x in data.publication] ) > 0 :
        print (r'\paragraph*{Submitted Manuscripts}', file = texfile)
        print (r'\begin{CVrevnumerate}', file = texfile)
        for paper in reversed(data.publication) :
            if paper.peer_reviewed and paper.status == SUBMITTED :
                paper.write (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)

    # Student theses/dissertations {{{3
    ntheses = 0
    ndissertations = 0
    for student in data.employee :
        if isinstance(student,MastersStudent) and not student.current \
                and (student.title is not None or student.key is not None) :
            ntheses += 1
        if isinstance(student,DoctoralStudent) and not student.current \
                and (student.title is not None or student.key is not None) :
            ndissertations += 1
    if ntheses > 0 and ndissertations == 0 :
        print (r'\subsection{Student Theses}',
            file = texfile)
    elif ndissertations > 0 and ntheses == 0 :
        print (r'\subsection{Student Dissertations}',
            file = texfile)
    elif ntheses + ndissertations > 0 :
        print (r'\subsection{Student Theses and Dissertations}',
            file = texfile)
    if ntheses + ndissertations > 0 :
        print (r'\begin{CVrevnumerate}', file = texfile)
        graduates = [x for x in data.employee if x.defense is not None]
        graduates.sort(reverse = True, key = lambda x: \
                datetime.datetime.strptime(x.defense, '%m/%d/%Y'))
        for student in graduates :
            if isinstance(student,GraduateStudent) \
                    and not student.current :
                student.write_thesis_or_dissertation (texfile)
        print (r'\end{CVrevnumerate}', file = texfile)
    # Presentations {{{3
    npresent = 0
    nposter = 0
    noral = 0
    for talk in data.presentation :
        if talk.teaching :
            continue
        npresent += 1
        if isinstance(talk,Poster) :
            nposter += 1
        else :
            noral += 1
    if show_presentations : # I assume posters are only present if talks are
        if not separate_posters :
            if show_posters and npresent > 0 :
                print (r'\subsection{Presentations and Posters}',
                    file = texfile)
            elif noral > 0 :
                print (r'\subsection{Oral Presentations}', file = texfile)
            if noral > 0 or (show_posters and npresent > 0) :
                print (r'\begin{CVrevnumerate}', file = texfile)
                for talk in reversed(data.presentation) :
                    if talk.teaching :
                        continue
                    if show_posters or not isinstance(talk,Poster) :
                        talk.write (texfile, show_students = False,
                            show_presenter = False, short = True)
                print (r'\end{CVrevnumerate}', file = texfile)
        else :
            if noral > 0 :
                print (r'\subsection{Oral Presentations}', file = texfile)
                print (r'\begin{CVrevnumerate}', file = texfile)
                for talk in reversed(data.presentation) :
                    if talk.teaching :
                        continue
                    if not isinstance(talk,Poster) :
                        talk.write (texfile, show_students = False,
                            show_presenter = False, short = True)
                print (r'\end{CVrevnumerate}', file = texfile)
            if show_posters and nposter > 0 :
                print (r'\subsection{Poster Presentations}', file = texfile)
                print (r'\begin{CVrevnumerate}', file = texfile)
                for pres in reversed(data.presentation) :
                    if pres.teaching :
                        continue
                    if isinstance(pres,Poster) :
                        pres.write (texfile, show_presenter = False,
                            show_students = False, short = True,
                            poster_note = '')
                print (r'\end{CVrevnumerate}', file = texfile)

    # Grants {{{3
    if sum([x.awarded for x in data.grant]) > 0 :
        print (r'\subsection{Funded Grants and Contracts}', file = texfile)
        print (r'  \begin{CVrevnumerate}', file = texfile)
        for grant in reversed(data.grant) :
            if grant.awarded :
                grant.write_condensed (texfile)
        print (r'  \end{CVrevnumerate}', file = texfile)

    # Service {{{2
    print (r'\section{Service Activities}', file = texfile)
    # Student engagement {{{3
    print (r'\subsection{Student Engagement}', file = texfile)
    if len(data.student_engagement) > 0 :
        print (r'\begin{CVitemize}', file = texfile)
        for item in reversed(data.student_engagement) :
            print (r'  \item', item, file = texfile)
        print (r'\end{CVitemize}', file = texfile)

    # National & International Meetings
    if len(data.session) > 0 :
        print (r'''\subsection{Regional, National, and International
            Conferences, Workshops, and Meetings}''', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for conference in reversed(data.session) :
            conference.write(texfile)
        print (r'\end{CVitemize}', file = texfile)

    # Professional societies {{{3
    if len(data.society) > 0 :
        print (r'\subsection{Professional Society Memberships}',
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
        print (r'\end{CVitemize}', file = texfile)

    # Proposal Review {{{3
    if len(data.panel) > 0 :
        print (r'\subsection{Proposal Review}', file = texfile)
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
        #reviews = sorted(reviews, key=lambda x: x.latest)
        print (r'\subsection{Manuscript Review}', file = texfile)
        #print (r'\begin{CVitemize}', file = texfile)
        journals = []
        for journal in sorted(reviews) :
            #journal.write (texfile, print_count = False)
            journals.append(r'\emph{' + journal.journal + '}')
        print (', '.join(journals), file=texfile)
        #print (r'\end{CVitemize}', file = texfile)

    # Other Regional/National/International Service {{{3
    if any ( isinstance(service, NonLocalService) \
            for service in data.service) :
        print (r'\subsection{Other Regional, National, and International',
            'Service}', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for activity in reversed(data.service) :
            if isinstance(activity, NonLocalService) :
                activity.write (texfile)
        print (r'\end{CVitemize}', file = texfile)

    # Local service {{{3
    if any (isinstance(service, LocalService) for service in data.service) :
        print (r'\subsection{University, College, and Department Service}',
            file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for service in reversed(data.service) :
            if isinstance(service, LocalService) :
                service.write (texfile)
        print (r'\end{CVitemize}', file = texfile)
    # 3}}}

    # 2}}}

    print(r'\end{document}', file = texfile)
    texfile.close()
    generate_pdf (filename)
