# CVtools - a Python module for storing and generating career-long curricula vitarum.

Intended for academics, though other disciplines should be handled without
intervention. To get started:

```Python
import CVtools2
CVtools2.set_INVESTIGATOR([your name]) # used to embolden names in grants
CVtools2.set_AUTHOR([your full name]) # used to embolden names in
    # presentations and publications that don't have BibTeX keys
    # Can be a list or tuple if you use more than one name
CVtools2.set_SCHOOL([where you work now])
CV = CVtools2.CV_data()
```

You set your name with CV.professor = Professor() [see Professor class]

Now you use CV.append() to append degrees, publications, awards, etc. via
their respective classes.

At the end of your CV input file, append this:

```Python
if __name__ == '__main__' :
    CVtools2.write_CV([arguments])
    CVtools2.write_Dossier([arguments])
    CVtools2.write_NSF_Biosketch([arguments])
```

These will actually create the CV (short form), a dossier (long form), and
a biosketch that approximates NSF's form (two pages).
This package should accompany the file MU-dossier.cls, the LaTeX class that
provides the formatting specification for the aforementioned three files.

**Important:**
The NSF biosketch is a very good approximation to what NSF uses,
but it is not currently accepted by NSF, as they use certain metadata that are
not included in the PDFs created here.

You can also include BibTeX entries using the 'key' field. The entry should look something like this:
```BibTeX
@config{CV,
    author = "John Cleese"
}
...
@article{Spam2017,
    author = "Cleese, John and Chapman, Graham and Idle, Eric and
        Gilliam, Terry and Jones, Terry and Palin, Michael",
    student = "Idle, Eric",
    undergraduate = "Palin, Michael",
    corauth = "Cleese, John",
}
```
The entry above would render John Cleese (the CV author) in bold with a star next to his name (as he is the corresponding author). It would also identify Eric Idle as a graduate student and Michael Palin as an undergraduate student. This requires the "CV.bst" or "CV-short.bst" files to function properly.
