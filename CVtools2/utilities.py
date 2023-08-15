import collections
import datetime
import re
from . import constants

def list2string (the_list) : # {{{1
    '''Convert a list of authors to a comma-separated list with "and" at the
       end.'''
    if the_list is None :
        return None
    if isinstance(the_list, str) :
        # It's already a string; just send it back
        return the_list
    if len(the_list) == 1 :
        return the_list[0]
    if len(the_list) == 2 :
        last_sep = ' and '
    else :
        last_sep = ', and '
    the_string = ', '.join(the_list[:-1]) + last_sep + the_list[-1]
    return the_string

##############################################################################

def datestring2year (thedate) : # {{{1
    if isinstance(thedate,int) :
        return str(thedate)
    elif isinstance(thedate,str) :
        while True :
            if thedate == 'present' :
                return thedate
            success = False
            try :
                year_date = datetime.datetime.strptime(thedate,'%Y')
                success = True
                break
            except ValueError :
                success = False
            try :
                year_date = datetime.datetime.strptime(thedate,'%m/%Y')
                success = True
                break
            except ValueError :
                success = False or success
            try :
                year_date = datetime.datetime.strptime(thedate,'%m/%d/%Y')
                success = True
                break
            except ValueError :
                success = False or success
        if success :
            year = str(int(datetime.datetime.strftime(year_date, '%Y')))
            return year
    raise ValueError ('thedate is ' + str(thedate))
    return None

##############################################################################

def datestring2monthyear (thedate) : # {{{1
    if isinstance(thedate,str) :
        if thedate == 'present' :
            return thedate
        success = False
        try :
            year_date = datetime.datetime.strptime(thedate,'%Y')
            success = True
        except ValueError :
            success = False
        try :
            year_date = datetime.datetime.strptime(thedate,'%m/%Y')
            success = True
        except ValueError :
            success = False or success
        try :
            year_date = datetime.datetime.strptime(thedate,'%m/%d/%Y')
            success = True
        except ValueError :
            success = False or success
        if success :
            year = datetime.datetime.strftime(year_date, '%Y')
            month = datetime.datetime.strftime(year_date, '%B')
            return str(month) + ' ' + str(year)
    raise ValueError ('thedate is ' + str(thedate))
    return None

##############################################################################

def remove_duplicates (values) : # {{{1
    return list(collections.OrderedDict.fromkeys(values))

##############################################################################

def any_entries_match (list1, list2) : # {{{1
    if is_instance (list1, str) :
        if is_instance (list2, str) :
            # both are strings
            return list1 == list2
        else :
            # 2 is a list, 1 is a string
            return list1 in list2
    else :
        if is_instance (list2, str) :
            # 2 is a string, 1 is a list
            return list2 in list1
        else :
            # 1 and 2 both iterables
            return any(x in list1 for x in list2)

##############################################################################

def tocardinal (num, recurse=False) : # {{{1
    'Converts an integer to a cardinal number'
    if num < 0 :
        return 'negative ' + tocardinal(-num)
    elif num == 0 :
        if recurse :
            return ''
        else :
            return 'zero'
    elif num == 1 :
        return 'one'
    elif num == 2 :
        return 'two'
    elif num == 3 :
        return 'three'
    elif num == 4 :
        return 'four'
    elif num == 5 :
        return 'five'
    elif num == 6 :
        return 'six'
    elif num == 7 :
        return 'seven'
    elif num == 8 :
        return 'eight'
    elif num == 9 :
        return 'nine'
    elif num == 10 :
        return 'ten'
    elif num == 11 :
        return 'eleven'
    elif num == 12 :
        return 'twelve'
    elif num == 13 :
        return 'thirteen'
    elif num == 14 :
        return 'fourteen'
    elif num == 15 :
        return 'fifteen'
    elif num == 18 :
        return 'eighteen'
    elif ( num > 15 and num < 20 ) :
        return tocardinal(num-10,True) + 'teen'
    elif ( num == 20 ) :
        return 'twenty'
    elif ( num > 20 and num < 30 ) :
        return 'twenty-' + tocardinal(num-20,True)
    elif ( num == 30 ) :
        return 'thirty'
    elif ( num > 30 and num < 40 ) :
        return 'thirty-' + tocardinal(num-30,True)
    elif ( num == 40 ) :
        return 'forty'
    elif ( num > 40 and num < 50 ) :
        return 'forty-' + tocardinal(num-40,True)
    elif ( num == 50 ) :
        return 'fifty'
    elif ( num > 50 and num < 60 ) :
        return 'fifty-' + tocardinal(num-50,True)
    elif ( num == 60 ) :
        return 'sixty'
    elif ( num > 60 and num < 70 ) :
        return 'sixty-' + tocardinal(num-60,True)
    elif ( num == 70 ) :
        return 'seventy'
    elif ( num > 70 and num < 80 ) :
        return 'seventy-' + tocardinal(num-70,True)
    elif ( num == 80 ) :
        return 'eighty'
    elif ( num > 80 and num < 90 ) :
        return 'eighty-' + tocardinal(num-80,True)
    elif ( num == 90 ) :
        return 'ninety'
    elif ( num > 90 and num < 100 ) :
        return 'ninety-' + tocardinal(num-90,True)
    elif ( num == 100 ) :
        return 'one hundred'
    elif ( num > 100 and num < 1000 ) :
        return tocardinal(num / 100,True) + ' hundred ' + \
               tocardinal(num % 100,True)
    elif ( num > 1000 and num < 1000000 ) :
        return tocardinal(num / 1000) + ' thousand ' + \
               tocardinal(num % 1000,True)
    elif ( num == 1000000 ) :
        return 'one million'
    elif ( num >= 1000000 and num < 1000000000 ) :
        return tocardinal(num / 1000000) + ' million ' + \
               tocardinal(num % 1000000, True)
    elif ( num >= 1000000000 and num < 1000000000000 ) :
        return tocardinal(num / 1000000000) + ' billion ' + \
               tocardinal(num % 1000000000,True)

##############################################################################

def toordinal (num) : # {{{1
    "Converts an integer to an ordinal number."
    if ( num == 1 ) :
        return 'once'
    elif ( num == 2 ) :
        return 'twice'
#    elif ( num == 3 ) :
#        return 'thrice'
    elif ( num < 11 and num >= 0 ) :
        return tocardinal(num) + ' times'
    else :
        return str(num) + ' times'

##############################################################################

def add_commas_to_number (num) : # {{{1
    toss = locale.setlocale (locale.LC_ALL, 'en_US')
    if isinstance(num, str) :
        return num
    else :
        return locale.format("%d", num, grouping=True)

##############################################################################

def markup_authors (authors, # {{{1
        CV_author = None, students = None, undergraduates = None,
        presenter = None, printand = True, initials = False, corauth = None,
        language = None) :

    '''Takes an author or list/tuple of authors and makes CV_author boldface,
       all students italic, and all presenters underlined. If printand is
       False, the word "and" is not printed. If initials is True, names are
       processed so that, for example, "John Stuart Smith" would become
       "J.~S. Smith" in the returned string. The optional argument "language"
       defaults to LaTeX, but can also be HTML. Passing with only one argument
       has the effect of reducing ["John T. Smith","Jane E. Doe",
          "Leif Erikson"] to "John T. Smith, Jane E. Doe, and Leif Erikson"'''

    # process language
    if language is None or language.lower() == "latex" :
        start_AUTHOR = r'\\textbf{'
        end_AUTHOR = r'}'
        start_student = r'\\emph{'
        end_student = r'}'
        start_UG = r'\\textsf{\\slshape '
        end_UG = r'}'
        start_presenter = r'\\uline{'
        end_presenter = r'}'
        tie = '~'
    elif language.lower() == "html" :
        start_AUTHOR = r'<b>'
        end_AUTHOR = r'</b>'
        start_student = r'<i>'
        end_student = r'</i>'
        start_UG = r'<span class="undergraduate">'
        end_UG = r'</span>'
        start_presenter = r'<span class="presenter">'
        end_presenter = r'</span>'
        tie = '&nbsp;'
    else :
        raise ValueError

    if CV_author is None :
        CV_author = constants.AUTHOR
    if isinstance(authors, str) :
        # BEGIN FIXME: This needs to change only names, not "note" fields
        # Make "Smith, John Thomas" into "John Thomas Smith" if necessary
        if re.match('[a-zA-Z]+,', authors) :
            #print ("BEFORE, authors=", authors)
            fields = authors.split(',')
            if len(fields) == 2 :
                authors = fields[1] + ' ' + fields[0]
        # END
        if initials :
            # Abbreviate author names (e.g., Karl -> K.; Karl D. -> K.~D.)
            names = authors.replace(tie,' ').replace('\.',' ').split()
            for i in range(len(names)-1) :
                if ( names[i] == '' ) :
                    continue
                # Don't change names in braces (like in BibTeX)
                elif ( names[i][0] != '{' ) :
                    # Look for, and split across, hyphens
                    if names[i].find('-') > 0 :
                        j = names[i].index('-')
                        names[i] = names[i][0] + '.' + '-' + names[i][j+1] + '.'
                    else :
                        names[i] = names[i][0] + '.'
                # Process braces
                else :
                    j = i
                    while not re.search('}',names[j]) :
                        j += 1
                    name = ' '.join(names[i:j+1])
                    names[i] = name
                    for k in range(i+1,j+1) :
                        names[k] = ''
            # remove empty strings we may have just inserted
            while '' in names :
                names.remove('')
            # A.~Person in the first case, I.~P. Freely in the second
            if len(names) == 2 :
                authors = tie.join(names[0:-1]) + tie + names[-1]
            else :
                authors = tie.join(names[0:-1]) + ' ' + names[-1]
        author_list = authors
        if constants.IDENTIFY_MINIONS :
            # Students are italicized
            if isinstance(students, (list,tuple)) :
                for student in students :
                    student_clean = markup_authors(student,initials=initials,
                        language=language)
                    if re.search (student_clean, author_list) :
                        author_list = re.sub(student_clean, start_student \
                            + student_clean + end_student, author_list)
            elif students is not None :
                student_clean = markup_authors(students,initials=initials,
                    language=language)
                if re.search (student_clean, author_list) :
                    author_list = re.sub(student_clean, start_student \
                        + student_clean + end_student, author_list)
            # Undergraduates are sans serif
            if isinstance(undergraduates, (list,tuple)) :
                for student in undergraduates :
                    student_clean = markup_authors(student,initials=initials,
                        language=language)
                    if re.search (student_clean, author_list) :
                        author_list = re.sub(student_clean,
                            start_UG + student_clean + end_UG, author_list)
            elif undergraduates is not None :
                student_clean = markup_authors(undergraduates,initials=initials,
                    language=language)
                if re.search (student_clean, author_list) :
                    author_list = re.sub(student_clean, 
                        start_UG + student_clean + end_UG, author_list)
        # Corresponding author has a pre-pended asterisk
        if corauth is not None :
            if isinstance(corauth, (list,tuple)) :
                for auth in corauth :
                    corauth_clean = markup_authors(auth, initials=initials,
                        CV_author='NULL', language=language)
                    if re.search (corauth_clean, author_list) :
                        author_list = re.sub(corauth_clean,
                            r'*' + corauth_clean, author_list)
            elif isinstance(corauth, str) :
                corauth_clean = markup_authors(corauth, initials=initials,
                    CV_author='NULL', language=language)
                if re.search (corauth_clean, author_list) :
                    author_list = re.sub(corauth_clean,
                        r'*' + corauth_clean, author_list)
        # CV author is in bold
        if isinstance(CV_author, (list,tuple)) :
            # sort it first (reverse order) to catch hyphenated last names
            CVauthor = list(CV_author)
            CVauthor.sort(reverse=True)
            for i in range(len(CVauthor)) :
                author_list = re.sub(CVauthor[i], start_AUTHOR \
                    + CVauthor[i] + end_AUTHOR, author_list)
        elif isinstance(CV_author, str) :
            author_list = re.sub(CV_author, start_AUTHOR + CV_author \
                + end_AUTHOR, authors)
        # Presenter is underlined
        if presenter is not None :
            if isinstance(presenter, (list,tuple)) :
                for p in presenter :
                    p_clean = markup_authors(p,initials=initials,
                        CV_author='NULL', language=language)
                    if re.search (p_clean, author_list) :
                        author_list = re.sub(p_clean, start_presenter \
                            + p_clean + end_presenter, author_list)
            elif isinstance(presenter, str) :
                presenter_clean = markup_authors(presenter, CV_author='NULL',
                    initials=initials, language=language)
                if re.search (presenter_clean, author_list) :
                    author_list = re.sub(presenter_clean, start_presenter \
                        + presenter_clean + end_presenter, author_list)
    elif authors is None :
        author_list = ''
    elif len(authors) == 0 :
        author_list = None
    elif len(authors) == 1 :
        author_list = markup_authors (authors[0], CV_author = CV_author,
            students = students, undergraduates = undergraduates,
            presenter = presenter, printand = printand, initials = initials,
            corauth = corauth, language=language)
    else :
        # Pass the author list to this function, each in turn, until we're
        # out of authors
        auth = list(authors)
        for i in range(len(auth)) :
            auth[i] = markup_authors (auth[i], CV_author = CV_author,
                students = students, undergraduates = undergraduates,
                presenter = presenter, printand = printand,
                initials = initials, corauth = corauth, language=language)
        if len(auth) == 2 :
            if printand :
                author_list = auth[0] + ' and ' + auth[1]
            else :
                author_list = ', '.join(auth)
        elif len(auth) > 2 :
            if printand :
                author_list = ', '.join(auth[0:-1])
                author_list = author_list + ', and ' + auth[-1]
            else :
                author_list = ', '.join(auth)
    return author_list

def yearlist2string (numlist) : # {{{1
    ''' Converts a list of years to a string. Example:
>> list2string([2018,2018,2018,2016,2015,2015])
"3*[2018] + [2016] + 2*[2015]"
'''
    if numlist is None :
        return None
    try :
        current = numlist[0]
    except IndexError :
        return ''
    n = 0
    smartlist = ''
    for year in numlist :
        if year == current :
            n += 1
            continue
        else :
            smartlist += str(n) + '*[' + str(current) + '] + '
            current = year
            n = 1
    smartlist += str(n) + '*[' + str(current) + ']'
    return smartlist
