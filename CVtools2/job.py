from .utilities import list2string, datestring2year

class Job : # {{{1

    'Gives information about employment held by the CV author.'

    def __init__ (self, start_date, title, employer, location, # {{{2
            end_date = None, unit = None, supervisor = None,
            stitle = "Supervisor", academic = True, onCV = True, note = None) :
        self.start_date = start_date
        self.end_date = end_date
        self.title = title
        self.unit = list2string(unit)
        self.employer = employer
        self.location = location
        self.supervisor = list2string(supervisor)
        self.stitle = stitle
        self.academic = academic
        if not isinstance(academic, bool) :
            raise TypeError ('Job.academic must be True or False')
        self.onCV = onCV
        if not isinstance(onCV, bool) :
            raise TypeError ('Job.onCV must be True or False')
        self.note = note

##############################################################################

    def write_appt (self, texfile) : # {{{2
        if self.end_date is None :
            end_date = 'present'
        else :
            end_date = datestring2year(self.end_date)
        if datestring2year(self.start_date) == datestring2year(end_date) :
            date_range = datestring2year(self.start_date)
        else :
            date_range = str(datestring2year(self.start_date)) + '--' \
                + str(end_date)
        print (r'\item[' + date_range + ']{' + self.title + '}', file=texfile)
        if self.unit is not None :
            print (self.unit, file = texfile)

##############################################################################

    def write (self, texfile) : # {{{2
        if self.end_date is None :
            end_date = 'present'
        else :
            end_date = datestring2year(self.end_date)
        if datestring2year(self.start_date) == datestring2year(end_date) :
            date_range = datestring2year(self.start_date)
        else :
            date_range = str(datestring2year(self.start_date)) + '--' \
                + str(end_date)
        print (r'\item[' + date_range + ']{' + self.title + '}', file=texfile)
        if self.unit is not None :
            print (self.unit + ',', file=texfile)
        print (self.employer + ',', file=texfile)
        # Put the rest of the line in one string so we can easily test whether
        # to add a period at the end of the entry.
        rest = self.location
        if self.supervisor is not None :
            rest = rest + '; ' + self.stitle + ': ' + self.supervisor
        if self.note is not None :
            rest = rest + ' (' + self.note + ')'
        if rest[-1] != '.' :
            rest = rest + '.'
        print (rest, file=texfile)
