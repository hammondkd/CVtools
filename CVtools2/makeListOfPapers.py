from .tex2pdf import write_preamble, set_typeface, generate_pdf
from . import constants

def write_List_of_Papers (data, filename, bibliography = None, 
        typeface = None) :

    'Generates a list of papers written by the author.'

    texfile = open(filename, 'w')
    data.texfile = texfile
    data.texfile_name = filename
    # Preamble
    print (r'\documentclass[12pt,notitlepage]{MU-dossier}', file = texfile)
#    print (r'\usepackage[margin=1in]{geometry}', file = texfile)
    write_preamble (texfile)
    set_typeface (texfile, typeface)
    print (r'\author{' + data.professor.name + '}', file = texfile)
    print (r'\title{Publications (with Abstracts)}', file = texfile)
    print (r'\begin{document}', file = texfile)
    print (r'\bibliographystyle{CV-with-abstract}', file = texfile)
    if bibliography is not None :
        print (r'\nocite{CV}', file = texfile)
        print (r"\providecommand{\enquote}[1]{``#1''}", file = texfile)
        print (r"\let\newblock\relax", file = texfile)
        print (r'\nobibliography{' + bibliography + '}', file = texfile)
    # Header
    print (r'\maketitle', file = texfile)
    print (r'''\noindent Graduate students in the group are denoted with
        \emph{italics}; undergraduate students are denoted with a
        \emph{\textsf{different typeface}}.
        The corresponding author is indicated with an asterisk (*).''',
        file = texfile)
    # Peer-reviewed publications
    print (r'\subsection*{Peer-Reviewed Publications (',
        sum(x.peer_reviewed and x.status \
                in (constants.ACCEPTED, constants.INPRESS, \
                    constants.PUBLISHED) for x in data.publication), ')}',
        sep = '', file = texfile)
    print (r'\begin{CVrevnumerate}', file = texfile)
    for pub in reversed(data.publication) :
        if pub.peer_reviewed and pub.status \
                in (constants.ACCEPTED, constants.INPRESS, \
                    constants.PUBLISHED) :
            pub.write (texfile, end='')
    print (r'\end{CVrevnumerate}', file = texfile)
    print (r'\end{document}', file = texfile)
    texfile.close()
    generate_pdf (filename)
