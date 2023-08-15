def create_new_user (author='Donald F. Duck', school='Disney University') :
    field = author.split()
    new_author = field[0][0] + '.'
    for i in range(1,len(field)-1) :
        new_author += '~' + field[i][0] + '.'
    new_author += ' ' + field[-1]
    new_investigator = field[0] + ' ' + field[-1]
    print ('#! /usr/bin/python3 -B')
    print ('\nfrom CVtools import *')
    print ('# Used to embolden names in presentations, committees,',
        'non-BibTeX papers')
    print ('AUTHOR =', repr(new_author))
    print ('set_AUTHOR (AUTHOR)\n')
    print ('# Used to embolden names in grants')
    print ('INVESTIGATOR =', repr(new_investigator))
    print ('set_INVESTIGATOR (INVESTIGATOR)\n')
    print ('set_SCHOOL (', repr(school), ')', sep='')
    print ('set_SCOPUS_API_KEY (None)')
    print ('set_WOS_USERNAME (None)')
    print ('set_WOS_PASSWORD (None)')
    print ('''\n# These should always be False on entry; set them True at appropriate points
#set_POST_TENURE (False)
#set_POST_APPOINTMENT (False)''')
    print ('\nCV = CV_data()')

    print ('## Command-line options {' + r'''{{1
import argparse
import os
import sys
parser = argparse.ArgumentParser(
    prog = os.path.basename(sys.argv[0]),
    description = 'Generates a CV, biosketch, and/or dossier for ' \
        + str(INVESTIGATOR).replace('~',' '),
)
parser.add_argument('-v','--verbose', action='store_true', dest='verbose',
    default=False, help='Give more verbose output')
parser.add_argument('--highlight', action='store', dest='highlight',
    metavar='key', default=None,
    help='BibTeX key or DOI indicating which publication to highlight in the citations plot (default: None)')
parser.add_argument('--CV-only', action='store_true', dest='CV_only',
    default=False, help='Generate only the CV rather than the entire dossier')

cmd_args = parser.parse_args()
''')

    print ('## Personal information {' + '{{1\n'
        'CV.professor = Professor(\n',
        '    name =', repr(author) + ',\n',
        '    highest_degree = "Ph.D.",\n',
        '    rank = "Assistant Professor",\n',
        '    department = "Department of Chemical Engineering",\n',
        '    school =', repr(school) + ',\n',
        '    office = 1313 Disneyland DR,\n',
        '    city = "Anaheim",\n',
        '    state = "CA",\n',
        '    zipcode = 92802,\n',
        '    phone = "+1 714 555 3825",\n',
        '    email = "donald@disney.edu",\n',
        '    website = "https://mickey.disney.com/donald/"\n',
        ')\n')
    print ('CV.research_interests = []\n')

    print ('\n*** Now use CV.append() to add items to your CV. ***')

    print (20*' ', '.')
    print (20*' ', '.')
    print (20*' ', '.')
    print ('\nif __name__ == "__main__" :')
    print ('    write_CV(CV, "', field[0], '-CV.tex",\n',
      '        bibliography=None, typeface=None,\n',
      '        show_interviews=False,\n',
      '        show_posters=False,\n',
      '        show_presentations=False\n    )', sep='')
    print ('\n    write_Dossier(CV, "', field[0], '-Dossier.tex",\n',
      '        bibliography=None, typeface=None,\n',
      '        show_interviews=True,\n',
      '        separate_posters=True\n',
      '        show_rejected=False,\n',
      '        show_news=False,\n',
      '        CV_only = cmd_args.CV_only,\n',
      '        hide_pre_appointment = True,\n',
      '        hide_pre_tenure = True,\n    )', sep='')

    print ('\n^^^ paste the above code into a file, then start CV-ing! ^^^')

if __name__ == '__main__' :
    create_new_user()
