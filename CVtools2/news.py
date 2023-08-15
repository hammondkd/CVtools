from .recent import Recent

class NewsCoverage (Recent) : # {{{1

    'Popular news coverage, such as appearing on the radio or television.'

    def __init__ (self, **args) :
        super().__init__(**args)
        try :
            self.author = args['author']
            self.title = args['title']
            self.source = args['source']
            self.date = args['date']
            self.year = args['year']
        except KeyError :
            traceback.print_stack()
            print ('KeyError: Missing required key word for Presentation',
                file = sys.stderr)
            raise SystemExit(1)

##############################################################################

    def write (self, texfile) :
        author_list = markup_authors (authors = self.author,
            CV_author = AUTHOR)
        print (r'\item', file = texfile)
        self.begin_recent(texfile)
        print (r'    ', author_list + ".", file = texfile)
        print ('   ``' + self.title + ".''", file = texfile)
        print (r'   \emph{' + self.source + '},', file = texfile)
        if re.match('[0-9]', self.date[-1]) :
            date_string = self.date + ', ' + str(self.year) + '.'
        else :
            date_string = self.date + ' ' + str(self.year) + '.'
        print (date_string, file = texfile)
        self.end_recent(texfile)
