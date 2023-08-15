import re
import os
import subprocess
import sys

def generate_pdf (filename, run_bibtex = True, run_once_only = False) : # {{{1

    'Generates a PDF from the given LaTeX input file.'

    (stem, extension) = os.path.splitext (filename)
    code = subprocess.Popen(['pdflatex','--interaction','batchmode',filename],
        stdout=subprocess.DEVNULL).wait()
    if code != 0 :
        print ('Error running pdflatex on', filename, '(first time)',
            file = sys.stderr)
        raise SystemExit (code)
    if run_bibtex :
        with open(stem + '.aux','r') as bibfile :
            if any(re.match(r'\\citation',line) for line in bibfile) :
                bibtex = subprocess.Popen(['bibtex','-terse',stem + '.aux'],
                    stdout = subprocess.DEVNULL)
                code = bibtex.wait()
                if code != 0 :
                    print ('WARNING: Error running bibtex on', stem + '.aux',
                        file = sys.stderr)
    if not run_once_only :
        code = subprocess.Popen(['pdflatex','--interaction','batchmode',
            filename], stdout=subprocess.DEVNULL).wait()
        if code != 0 :
            print ('Error running pdflatex on', filename, '(second time)',
                file = sys.stderr)
            raise SystemExit (code)
        code = subprocess.Popen(['pdflatex','--interaction','batchmode',
            filename], stdout=subprocess.DEVNULL).wait()
        if code != 0 :
            print ('Error running pdflatex on', filename, '(third time)',
                file = sys.stderr)
            raise SystemExit (code)

##############################################################################

def set_typeface (outfile, typeface) : # {{{1
    '''Translates typeface names from their usual names to the requisite LaTeX
       packages.'''
    if typeface is None or re.search('[Cc]omputer [Mm]odern', typeface) \
                        or re.search('[Mm]odern', typeface) :
        #typefacepackage = None
        typefacepackage = r'\usepackage{lmodern,textgreek}\let\gammaup\textgamma'
    elif re.search('[gG]aramond', typeface) :
        typefacepackage = r'''\usepackage[garamond]{mathdesign}
\usepackage{newtxtextgreek}
\usepackage[sf,mono=false,scale=1.05]{libertine}'''
    elif re.search('[uU]topia', typeface) :
        typefacepackage = r'''\usepackage[utopia]{mathdesign}
\usepackage{newtxtextgreek}'''
    elif re.search('[Tt]imes', typeface) :
        typefacepackage = r'\usepackage{txfonts,newtxtextgreek}'
    elif re.search('([Pp]alladio|[Pp]alatino)', typeface) :
        typefacepackage = r'\usepackage{pxfonts,newtxtextgreek}'
    elif re.search('([Bb]itstream|[Cc]harter|[Bb]itstream\s*[Cc]harter)',
            typeface) :
        typefacepackage = r'''\usepackage[charter]{mathdesign}
\usepackage{newtxtextgreek}
\usepackage[sf,mono=false,scale=1.05]{libertine}'''
    elif re.search('([Ll]ibertine)', typeface) :
        typefacepackage = r'\usepackage{libertine,textgreek}'
    elif re.search('([Bb]ookman)', typeface) :
        typefacepackage = r'\usepackage{bookman,textgreek}'
    else :
        raise ValueError('I do not know how to use the typeface ' + typeface)
    print (r'\usepackage[T1]{fontenc}', file = outfile)
    if typefacepackage is not None :
        print(typefacepackage, file = outfile)

##############################################################################

def write_preamble (texfile) : # {{{1
    'Generates the preamble to the LaTeX document.'
    print (r'\usepackage{textcomp}', file=texfile)
    print (r"\usepackage{amsmath}", file=texfile)
    print (r'\usepackage{url}', file = texfile)
    print (r"\usepackage[numbers]{natbib}", file=texfile) # Is this required because of how you highlight students/etc.? Check this!
    print (r"\usepackage{bibentry}", file=texfile)
    print (r'\usepackage{revnum}', file = texfile)
    print (r"\usepackage[normalem]{ulem}", file=texfile)
    print (r"\usepackage{tabularx,array}", file=texfile)
    print (r"\usepackage{colortbl}", file=texfile)
    print (r"\usepackage{refcount}", file=texfile)
    print (r"\usepackage{miller}", file=texfile)
    print (r'\newcommand*{\doi}{DOI: \begingroup \urlstyle{rm}\Url}',
        file = texfile)
    print (r'\newcommand*{\urlprefix}{URL: }', file = texfile)
    print (r'\newcommand*{\micro}{\textmu}', file = texfile)
    print (r'\newcommand*{\degrees}{\textdegree}', file = texfile)
    print (r"\usepackage[dvipsnames,svgnames,table]{xcolor}", file=texfile)
    print (r"\newcolumntype{L}{>{\hangindent=2em\hangafter=1\raggedright\arraybackslash}X}", file=texfile)
    print (r"\newcolumntype{C}{>{\centering\arraybackslash}X}", file=texfile)
    print (r"\newcolumntype{s}{>{\hspace{4pt}}l}", file=texfile)
    print (r"\newcolumntype{P}[1]{>{\raggedright\arraybackslash}p{#1}}", file=texfile)
    print (r'\colorlet{recent@employee}{white}', file = texfile)
    print (r'\colorlet{recent}{black}', file = texfile)
    print (r"\hyphenation{fusion iso-therm iso-therms Co-lum-bia Mas-sa-chu-setts Bio-molec-ular quad-ru-pole physi-sorption micro-porous meso-porous}", file=texfile)
    print (r'\setlength{\emergencystretch}{1ex}%', file = texfile)
