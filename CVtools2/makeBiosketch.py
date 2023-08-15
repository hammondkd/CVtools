from .tex2pdf import generate_pdf, write_preamble, set_typeface
from .recent import set_SHOW_RECENT
from .utilities import datestring2year

def write_NSF_Biosketch (data, filename, # {{{1
        bibliography = None, typeface = 'Times') :

    '''Generates a biographical sketch suitable for an NSF proposal, based on
       the new requirements (updated 05/01/2020).'''

    set_SHOW_RECENT (False)
    texfile = open (filename, 'w')
    data.texfile = texfile
    data.texfile_name = filename
    # LaTeX preamble {{{2
    print (r'\documentclass[11pt,shortform,numbers]{MU-dossier}',
        file = texfile)
    write_preamble (texfile)
    set_typeface (texfile, typeface)
    print (r'\usepackage{lastpage}', file = texfile)
    print (r'\usepackage{booktabs}', file = texfile)
#    print (r'\setlength{\emergencystretch}{1.25em}', file = texfile)
    print (r'\renewcommand*{\thesection}{(\lowercase{\alph{section}})}',
        file = texfile)
    # header and footer
    print (r'\pagestyle{plain}', file = texfile)
    print (r'\lhead{}\rhead{}\chead{}', file=texfile)
    print (r'\cfoot{}\lfoot{BS-\thepage\ of \pageref{LastPage}}', file=texfile)
    print (r'\author{' + data.professor.name + '}', file = texfile)
    print (r'\title{NSF Biosketch 20-1}', file = texfile)
    print (r'\usepackage[hidelinks,bookmarksnumbered,pdfusetitle]{hyperref}',
        file = texfile)
    print (r'\setcounter{secnumdepth}{1}', file = texfile)
    print (r'\setcounter{tocdepth}{2}', file = texfile)
    print (r'\begin{document}', file = texfile)
    if bibliography is not None :
        print (r'\bibliographystyle{CV-with-doi}%', file = texfile)
        print (r'\nocite{CV}%', file = texfile)
        print (r"\providecommand{\enquote}[1]{``#1''}%", file = texfile)
        print (r"\let\newblock\relax", file = texfile)
        print (r'\nobibliography{' + bibliography + '}%', file = texfile)
    print (r'\pdfbookmark{NSF BIOGRAPHICAL SKETCH}{}%', file = texfile)
    # 1}}}
    # Now start actually writing stuff
    print (r'\begin{tabularx}{\linewidth}{@{}l}', file = texfile)
    print (r'\multicolumn{1}{c}{\bfseries NSF BIOGRAPHICAL SKETCH} \\',
        file = texfile)
    names = data.professor.name.split()
    print (r'  \toprule', file = texfile)
    print (r'NAME: ', names[-1], ', ', names[0], r' \\', sep='', file=texfile)
#    print (r'  \midrule\midrule', file = texfile)
    print (r'\multicolumn{1}{@{}p{\linewidth}}{POSITION TITLE \& INSTITUTION: ',
        data.professor.rank, ', ', data.professor.school, r'} \\',
        sep='', file = texfile)
    print (r'  \bottomrule', file = texfile)
    print (r'\end{tabularx}', file = texfile)
    #print (r'\multicolumn{5}{@{}l}{\bfseries (a) PROFESSIONAL PREPARATION} \\',
    #    file = texfile)
    print (r'\section{PROFESSIONAL PREPARATION}', file = texfile)
    print (r'\begin{tabularx}{\linewidth}{L|l|l|l|l}', file = texfile)
    #print (r'  \specialrule{\lightrulewidth}{0pt}{0pt}', file = texfile)
    #print (r'  \toprule', file = texfile)
    print (r'  \specialrule{\heavyrulewidth}{0pt}{0pt}', file = texfile)
    print (r'''\multicolumn{1}{c|}{\scriptsize INSTITUTION}
        & \multicolumn{1}{c|}{\scriptsize LOCATION}
        & \multicolumn{1}{c|}{\scriptsize MAJOR / AREA OF STUDY}
        & \multicolumn{1}{c|}{\scriptsize DEGREE}% (if applicable)
        & \multicolumn{1}{c}{\scriptsize YEAR} \\''', file = texfile)
    print (r'  \specialrule{\lightrulewidth}{0pt}{0pt}', file = texfile)
    # They want this in chronological order
    for degree in data.degree :
        print (degree.school, '&', degree.address, '&', degree.major, '&',
            degree.degree, '&', degree.year, r'\\', file = texfile)
    print (r'\end{tabularx}', file = texfile)
    #print (r'\\[1ex]', file = texfile)
    #print (r'\multicolumn{2}{l}{\bfseries (b)~APPOINTMENTS} \\', file=texfile)
    print (r'\section{APPOINTMENTS}', file = texfile)
    print (r'\begin{tabularx}{\linewidth}{l L}', file = texfile)
    for appt in reversed(data.jobhistory) :
        if appt.academic :
            if appt.end_date is None :
                end = 'present'
            else :
                end = datestring2year(appt.end_date)
            if datestring2year(appt.start_date) == end :
                print ('    ', datestring2year(appt.start_date),
                    '&', file = texfile)
            else :
                print ('    ', datestring2year(appt.start_date) + '--' + end,
                    '&', file = texfile)
            print ('  ', appt.title + ',', appt.unit + ',', appt.employer + ',',
                appt.location,
                r'\\', file = texfile)
    print (r'\end{tabularx}', file = texfile)
#    print (r'\\[1ex]', file = texfile)
    # Products
    print (r'\section{PRODUCTS}', file = texfile)
    if any([x.most_significant for x in data.publication]) :
        print (r'\subsection{Products Most Closely Related to the Proposed',
            'Project}', file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for pub in reversed(data.publication) :
            if pub.most_significant :
                pub.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    if any([x.significant for x in data.publication]) :
        print (r'\subsection{Other Significant Products, Whether or Not',
            'Related to the Proposed Project}', file = texfile)
        print (r'\begin{CVenumerate}', file = texfile)
        for pub in reversed(data.publication) :
            if pub.significant :
                pub.write (texfile)
        print (r'\end{CVenumerate}', file = texfile)
    # Synergistic Activities {{{2
    print (r'\section{SYNERGISTIC ACTIVITIES}', file = texfile)
    if len(data.synergistic) > 0 :
        print (r'\begin{CVenumerate}', file = texfile)
        for item in data.synergistic :
            print (r'  \item', item, file = texfile)
        print (r'\end{CVenumerate}', file = texfile)

    # wrap it up
    print (r'\end{document}', file = texfile)
    texfile.close()
    generate_pdf (filename)

##############################################################################

def write_old_Biosketch (data, filename, bibliography = None, # {{{1
        typeface = None, show_collaborators = False) :

    '''Generates a biographical sketch suitable for an NSF or DOE grant.
       If show_collaborators is True, include a list of collaborators, suitable
       for a DOE grant or other proposal.'''

    texfile = open (filename, 'w')
    data.texfile = texfile
    data.texfile_name = filename
    # LaTeX document preamble {{{2
    print (r'\documentclass[12pt,shortform,hidenumbers]{MU-dossier}', file = texfile)
    write_preamble (texfile)
    set_typeface (texfile, typeface)
    # Page numbers are section f in NSF proposals
    print (r'\renewcommand*{\thepage}{F--\arabic{page}}', file = texfile)
    # End
    print (r'\author{' + data.professor.name + '}', file = texfile)
    print (r'\begin{document}', file = texfile)
    print (r'\bibliographystyle{CV-with-doi}', file = texfile)
    if bibliography is not None :
        papers = [pub.key for pub in data.publication]
        papers = ['CV'] + list(set(papers))
        papers.remove(None)
        keys = ','.join(papers)
        print (r'\nocite{CV}', file = texfile)
        print (r"\providecommand{\enquote}[1]{``#1''}", file = texfile)
        print (r"\let\newblock\relax", file = texfile)
        print (r'\nobibliography{' + bibliography + '}', file = texfile)

    # Name and Degree {{{2
    data.professor.write_address (texfile)

    # Education and Training / Professional Preparation {{{2
    print (r'\subsection{Education and Training}', file = texfile)
    print (r'  \newlength{\origtabcolsep}', file = texfile)
    print (r'  \setlength{\origtabcolsep}{\tabcolsep}', file = texfile)
    print (r'  \setlength{\tabcolsep}{0.0em}', file = texfile)
    print (r'\begin{tabularx}{\linewidth}{L s s s}', file = texfile)
    # They want this in chronological order
    for degree in data.degree :
        if degree.longschool is None :
            school = degree.school
        else :
            school = degree.longschool
        print (school, '&', degree.address, '&', degree.major, '&',
            degree.degree + ',', degree.year, r'\\', file = texfile)
    print (r'\end{tabularx}', file = texfile)

    # Appointments {{{2
    #print (r'\subsection{Academic Appointments}', file = texfile)
    print (r'\subsection{Research and Professional Experience}', file=texfile)
    print (r'\begin{tabularx}{\linewidth}{L l}', file = texfile)
    for appt in reversed(data.jobhistory) :
        if appt.academic :
            if appt.end_date is None :
                end = 'present'
            else :
                end = str(appt.end_date)
            print ('  ', appt.title + ',', appt.unit + ',', appt.employer,
                '&', file = texfile)
            if str(appt.start_date) == end :
                print ('    ', str(appt.start_date), r'\\', file = texfile)
            else :
                print ('    ', str(appt.start_date) + '--' + end, r'\\',
                    file = texfile)
    print (r'\end{tabularx}', file = texfile)
    print (r'  \setlength{\tabcolsep}{6.0pt} % the default', file = texfile)

    # Publications {{{2
    if any([x.most_significant or x.significant for x in data.publication]) :
        print (r'\subsection{Publications}', file = texfile)
    if any([x.most_significant for x in data.publication]) :
        print (r'\subsubsection{Most-Closely-Related Publications}',
            file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for pub in reversed(data.publication) :
            if pub.most_significant :
                pub.write (texfile)
        print (r'\end{CVitemize}', file = texfile)

    if any([x.significant for x in data.publication]) :
        print (r'\subsubsection{Other Select Publications (of',
            sum(1 for y in filter(lambda x: x.peer_reviewed and \
                    x.status in [PUBLISHED,ACCEPTED], data.publication)),
                'total)}', file = texfile)
        print (r'\begin{CVitemize}', file = texfile)
        for pub in reversed(data.publication) :
            if pub.significant :
                pub.write (texfile)
        print (r'\end{CVitemize}', file = texfile)

    # Synergistic Activities {{{2
    print (r'\subsection{Synergistic Activities}', file = texfile)
    if len(data.synergistic) > 0 :
        print (r'\begin{CVitemize}', file = texfile)
        for item in data.synergistic :
            print (r'  \item', item, file = texfile)
        print (r'\end{CVitemize}', file = texfile)

    # Collaborators {{{2
    if show_collaborators :
        # update collaborators based on grants and publications
        data.update_collaborators(bibliography)
        # remove those longer ago than 2 years
        collab = filter(lambda x: x.year >= datetime.datetime.now().year - 2,
            data.collaborator)
        collab = list(collab)
        print (r'\par\textbf{Collaborators (' +
            str(len(collab)) + ')}\quad', file = texfile)
        if len(collab) > 0 :
            collab = sorted(collab, key=lambda c: c.last)
            for i in range(len(collab)-1) :
                # assuming you don't have two collaborators with the same
                # first AND last name...remove duplicates
                if i > 0 and all([collab[i].first == collab[i-1].first, \
                        collab[i].last == collab[i-1].last]) :
                    continue
                print (str(collab[i]) + ',', file = texfile)
            if all([collab[-1].first != collab[-2].first, \
                    collab[-1].last != collab[-2].last]) :
                print (str(collab[-1]), file = texfile)
#            for person in collab :
#                if person is collab[-1] :
#                    print (str(person), file = texfile)
#                else :
#                    print (str(person) + ',', file = texfile)

##############################################################################

        # Advisors {{{3
        def advisor_string (degree) :
            if degree.advisor is None :
                return None
            line = ''
            if isinstance(degree.advisor, str) or len(degree.advisor) == 1 :
                line += r'\par\vspace{1.0ex}\textbf{Doctorate' \
                    ' Advisor (1)}\quad '
            else :
                line += r'\par\vspace{1.0ex}\textbf{Doctorate' \
                    ' Advisors (' + str(len(degree.advisor)) + ')}\quad '
            if isinstance(degree.advisor, (list,tuple)) :
                arr = []
                for i in range(len(degree.advisor)) :
                    if degree.advisor_address is None :
                        arr.append(degree.advisor[i] + ' ('
                            + degree.school + ', ' + degree.address + ')')
                    else :
                        arr.append(degree.advisor[i] + ' ('
                            + degree.advisor_address[i] + ')')
                line += list2string(arr)
            elif isinstance(degree.advisor, str) :
                if degree.advisor_address is None :
                    line += degree.advisor + ' (' + degree.school \
                        + ', ' + degree.address + ')'
                else :
                    line += degree.advisor + ' (' + degree.advisor_address + ')'
            else :
                raise TypeError
            return line

##############################################################################

        # Assemble list of advisors # {{{3
        advisor_lines = []
        for degree in data.degree :
            if degree.degree in DOCTORATES or degree.degree == 'Postdoc' \
                  or (degree.degree in MASTERS and degree.advisor is not None) :
                advisor_lines.append( advisor_string(degree) )
        advisor_lines = remove_duplicates (advisor_lines)
        for line in advisor_lines :
            print (line, file = texfile)

    #if show_collaborators :
        # Students {{{3
        nformerstudents = 0
        for student in data.employee :
            if isinstance(student, GraduateStudent) and not student.current :
                nformerstudents += 1
        print (r'\vspace{1.0ex}\par\vspace{1.0ex}\textbf{Graduate ',
            'Students Advised (', nformerstudents, ')}\quad',
            sep = '', file = texfile)
        if nformerstudents > 0 :
            nstudent = 0
            for student in data.employee :
                if isinstance (student, GraduateStudent) \
                        and not student.current :
                    print (student.first, student.last, file = texfile)
                    nstudent += 1
                    if student.present_address is None :
                        present_address = 'unaffiliated'
                    else :
                        present_address = student.present_address
                    if nstudent != nformerstudents :
                        print ('(' + present_address + '),', file = texfile)
                    else :
                        print ('(' + present_address + ')', file = texfile)
        else : # no former students
            print ('-none-', file = texfile)

        # Postdocs {{{3
        npostdocs = 0
        for minion in data.employee :
            if isinstance (minion, Postdoc) :
                npostdocs += 1
        print (r'\par\textbf{Postdoctoral Scholars Sponsored ('
            + str(npostdocs) + ')}\quad', file = texfile)
        if npostdocs > 0 :
            nstudent = 0
            for student in data.employee :
                if isinstance (student, Postdoc) :
                    print (student.first, student.last)
                    nstudent += 1
                    if student.present_address is not None :
                        if nstudent != nformerstudents :
                            print ('(' + student.present_address + '),',
                                file = texfile)
                        else :
                            print ('(' + student.present_address + ')',
                                file = texfile)
        else : # no former students
            print ('-none-', file = texfile)

        # 3}}}
    # end if show_collaborators 2}}}

    print (r'\end{document}', file = texfile)
    texfile.close()
    generate_pdf (filename)
