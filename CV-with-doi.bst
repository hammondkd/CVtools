%%
%% This is file `CV.bst',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% merlin.mbs  (with options: `head,seq-no,nm-init,ed-au,ed-rev,jnrlst,yr-par,xmth,tit-qq,atit-u,trtit-b,vol-bf,vnum-sp,volp-sp,num-xser,numser,jnm-x,add-pub,edby,edbyy,pp,xedn,etal-it,url,url-nl,nfss,{}')
%% physjour.mbs  (with options: `seq-no,nm-init,ed-au,ed-rev,jnrlst,yr-par,xmth,tit-qq,atit-u,trtit-b,vol-bf,vnum-sp,volp-sp,num-xser,numser,jnm-x,add-pub,edby,edbyy,pp,xedn,etal-it,url,url-nl,nfss,{}')
%% geojour.mbs  (with options: `seq-no,nm-init,ed-au,ed-rev,jnrlst,yr-par,xmth,tit-qq,atit-u,trtit-b,vol-bf,vnum-sp,volp-sp,num-xser,numser,jnm-x,add-pub,edby,edbyy,pp,xedn,etal-it,url,url-nl,nfss,{}')
%% photjour.mbs  (with options: `seq-no,nm-init,ed-au,ed-rev,jnrlst,yr-par,xmth,tit-qq,atit-u,trtit-b,vol-bf,vnum-sp,volp-sp,num-xser,numser,jnm-x,add-pub,edby,edbyy,pp,xedn,etal-it,url,url-nl,nfss,{}')
%% merlin.mbs  (with options: `tail,seq-no,nm-init,ed-au,ed-rev,jnrlst,yr-par,xmth,tit-qq,atit-u,trtit-b,vol-bf,vnum-sp,volp-sp,num-xser,numser,jnm-x,add-pub,edby,edbyy,pp,xedn,etal-it,url,url-nl,nfss,{}')
%% ----------------------------------------
%% *** Compromise between ACS, APS, and Elsevier Journal Styles ***
%% 
%% Copyright 1994-2005 Patrick W Daly
 % ===============================================================
 % IMPORTANT NOTICE:
 % This bibliographic style (bst) file has been generated from one or
 % more master bibliographic style (mbs) files, listed above.
 %
 % This generated file can be redistributed and/or modified under the terms
 % of the LaTeX Project Public License Distributed from CTAN
 % archives in directory macros/latex/base/lppl.txt; either
 % version 1 of the License, or any later version.
 % ===============================================================
 % Name and version information of the main mbs file:
 % \ProvidesFile{merlin.mbs}[2005/10/17 4.14 (PWD, AO, DPC)]
 %   For use with BibTeX version 0.99a or later
 %-------------------------------------------------------------------
 % This bibliography style file is intended for texts in ENGLISH
 % This is a numerical citation style, and as such is standard LaTeX.
 % It requires no extra package to interface to the main text.
 % The form of the \bibitem entries is
 %   \bibitem{key}...
 % Usage of \cite is as follows:
 %   \cite{key} ==>>          [#]
 %   \cite[chap. 2]{key} ==>> [#, chap. 2]
 % where # is a number determined by the ordering in the reference list.
 % The order in the reference list is that by which the works were originally
 %   cited in the text, or that in the database.
 %---------------------------------------------------------------------

ENTRY
  { address
    author
    booktitle
    chapter
    doi
    edition
    editor
    eid
    howpublished
    institution
    journal
    key
    month
    note
    number
    organization
    pages
    publisher
    school
    series
    title
    type
    url
    volume
    year
    student
  }
  {}
  { label }
INTEGERS { output.state before.all mid.sentence after.sentence after.block }
FUNCTION {init.state.consts}
{ #0 'before.all :=
  #1 'mid.sentence :=
  #2 'after.sentence :=
  #3 'after.block :=
}
STRINGS { s t cv.author studentname }
FUNCTION {output.nonnull}
{ 's :=
  output.state mid.sentence =
    { ", " * write$ }
    { output.state after.block =
        { add.period$ write$
          newline$
% line removed by KDH to remove extra space after periods
%          "\newblock " write$
        }
        { output.state before.all =
            'write$
            { add.period$ " " * write$ }
          if$
        }
      if$
      mid.sentence 'output.state :=
    }
  if$
  s
}
FUNCTION {output}
{ duplicate$ empty$
    'pop$
    'output.nonnull
  if$
}
FUNCTION {output.check}
{ 't :=
  duplicate$ empty$
    { pop$ "empty " t * " in " * cite$ * warning$ }
    'output.nonnull
  if$
}
FUNCTION {fin.entry}
{ add.period$
  write$
  newline$
}

% New functions added by Karl H.
INTEGERS { numstudents studentsleft studentidx }
FUNCTION {config}
{ author duplicate$ empty$
    { "The CV entry should define the author of your CV" warning$ pop$ }
    %{ purify$ 'cv.author := }
    { #1 "{f.~}{vv~}{ll}{, jj}" format.name$
      purify$ 'cv.author :=
    }
    if$
  % 10/10/2021 Added the following code to remove the LaTeX Warning
  % "Citation `CV' undefined on input line X."
  "\makeatletter" write$ newline$
  "\AtEndDocument{\immediate\write\@auxout{\noexpand\bibcite{" write$
  cite$ "}{}}}" * write$ newline$
  "\makeatother" write$ newline$
}
FUNCTION {process.configs.only}
{
    "config" type$ =
    { call.type$ }
    'skip$
    if$
}
FUNCTION {process.non.configs}
{
    "config" type$ =
    'skip$
    { call.type$ }
    if$
}
FUNCTION {highlight}
{ duplicate$ empty$
    { pop$ "" }
    { "\textbf{" swap$ * "}" * }
  if$
}
FUNCTION {highlight.if.cv.author}
{ duplicate$ purify$ cv.author =
    { highlight }
    'skip$
  if$
}
FUNCTION {highlight.student}
{ duplicate$ empty$
    { pop$ "" }
    { "\emph{" swap$ * "}" * }
  if$
}
FUNCTION {highlight.if.student}
{ 'studentname :=
  duplicate$ studentname =
    %{ highlight.student } % removed so students are normal on biosketches
    'skip$
    'skip$
  if$
}
FUNCTION {highlight.student.authors}
{ student empty$ 'skip$ {
    #1 'studentidx :=
    student num.names$ 'numstudents :=
    numstudents 'studentsleft :=
    { studentsleft #0 > }
    { student studentidx  "{f.~}{vv~}{ll}{, jj}" format.name$
      highlight.if.student
      studentidx #1 + 'studentidx :=
      studentsleft #1 - 'studentsleft :=
    }
    while$
  } if$
}
% End Added Functions

FUNCTION {new.block}
{ output.state before.all =
    'skip$
    { after.block 'output.state := }
  if$
}
FUNCTION {new.sentence}
{ output.state after.block =
    'skip$
    { output.state before.all =
        'skip$
        { after.sentence 'output.state := }
      if$
    }
  if$
}
FUNCTION {add.blank}
{  " " * before.all 'output.state :=
}

FUNCTION {date.block}
{
  new.block
}

FUNCTION {not}
{   { #0 }
    { #1 }
  if$
}
FUNCTION {and}
{   'skip$
    { pop$ #0 }
  if$
}
FUNCTION {or}
{   { pop$ #1 }
    'skip$
  if$
}
FUNCTION {non.stop}
{ duplicate$
   "}" * add.period$
   #-1 #1 substring$ "." =
}

FUNCTION {new.block.checka}
{ empty$
    'skip$
    'new.block
  if$
}
FUNCTION {new.block.checkb}
{ empty$
  swap$ empty$
  and
    'skip$
    'new.block
  if$
}
FUNCTION {new.sentence.checka}
{ empty$
    'skip$
    'new.sentence
  if$
}
FUNCTION {new.sentence.checkb}
{ empty$
  swap$ empty$
  and
    'skip$
    'new.sentence
  if$
}
FUNCTION {field.or.null}
{ duplicate$ empty$
    { pop$ "" }
    'skip$
  if$
}
FUNCTION {emphasize}
{ duplicate$ empty$
    { pop$ "" }
    { "\emph{" swap$ * "}" * }
  if$
}
FUNCTION {bolden}
{ duplicate$ empty$
    { pop$ "" }
    { "\textbf{" swap$ * "}" * }
  if$
}
FUNCTION {tie.or.space.prefix}
{ duplicate$ text.length$ #3 <
    { "~" }
    { " " }
  if$
  swap$
}

FUNCTION {capitalize}
{ "u" change.case$ "t" change.case$ }

FUNCTION {space.word}
{ " " swap$ * " " * }
 % Here are the language-specific definitions for explicit words.
 % Each function has a name bbl.xxx where xxx is the English word.
 % The language selected here is ENGLISH
FUNCTION {bbl.and}
{ "and"}

FUNCTION {bbl.etal}
{ "et~al." }

FUNCTION {bbl.editors}
{ "editors" }

FUNCTION {bbl.editor}
{ "editor" }

FUNCTION {bbl.edby}
{ "edited by" }

FUNCTION {bbl.edition}
{ "edition" }

FUNCTION {bbl.volume}
{ "volume" }

FUNCTION {bbl.of}
{ "of" }

FUNCTION {bbl.number}
{ "number" }

FUNCTION {bbl.nr}
{ "no." }

FUNCTION {bbl.in}
{ "in" }

FUNCTION {bbl.pages}
{ "pp." }

FUNCTION {bbl.page}
{ "p." }

FUNCTION {bbl.chapter}
{ "chapter" }

FUNCTION {bbl.techrep}
{ "Technical Report" }

FUNCTION {bbl.mthesis}
{ "Thesis" }
%{ "Master's thesis" }

FUNCTION {bbl.phdthesis}
{ "Dissertation" }
%{ "Ph.D. dissertation" }

MACRO {jan} {"January"}

MACRO {feb} {"February"}

MACRO {mar} {"March"}

MACRO {apr} {"April"}

MACRO {may} {"May"}

MACRO {jun} {"June"}

MACRO {jul} {"July"}

MACRO {aug} {"August"}

MACRO {sep} {"September"}

MACRO {oct} {"October"}

MACRO {nov} {"November"}

MACRO {dec} {"December"}

 %-------------------------------------------------------------------
 % Begin module:
 % \ProvidesFile{physjour.mbs}[2002/01/14 2.2 (PWD)]
MACRO {aa}{"Astronomy and Astrophysics"}
MACRO {aasup}{"Astronomy and Astrophysics, Supplement Series"}
MACRO {aj}{"Astronomical Journal"}
MACRO {aph} {"Acta Physica"}
MACRO {advp} {"Advances in Physics"}
MACRO {ajp} {"American Journal of Physics"}
MACRO {ajm} {"American Journal of Mathematics"}
MACRO {amsci} {"American Scientist"}
MACRO {anofd} {"Annals of Fluid Dynamics"}
MACRO {am} {"Annals of Mathematics"}
MACRO {ap} {"Annals of Physics"}
MACRO {adp} {"Annalen der Physik"}
MACRO {ao} {"Applied Optics"}
MACRO {apl} {"Applied Physics Letters"}
MACRO {app} {"Astroparticle Physics"}
MACRO {apj} {"Astrophysical Journal"}
MACRO {apjsup} {"Astrophysical Journal Supplement"}
MACRO {apss} {"Astrophysics and Space Science"}
MACRO {araa} {"Annual Review of Astronomy and Astrophysics"}
MACRO {baas} {"Bulletin of the American Astronomical Society"}
MACRO {baps} {"Bulletin of the American Physical Society"}
MACRO {cmp} {"Communications in Mathematical Physics"}
MACRO {cpam} {"Communications on Pure and Applied Mathematics"}
MACRO {cppcf} {"Comments on Plasma Physics and Controlled Fusion"}
MACRO {cpc} {"Computer Physics Communications"}
MACRO {cqg} {"Classical and Quantum Gravity"}
MACRO {cra} {"Comptes Rendus des S{\'e}ances de l'Acad{\'e}mie des Sciences A"}
MACRO {fed} {"Fusion Engineering and Design"}
MACRO {ft} {"Fusion Technology"}
MACRO {grg} {"General Relativity and Gravitation"}
MACRO {ieeens} {"IEEE Transactions on Nuclear Science"}
MACRO {ieeeps} {"IEEE Transactions on Plasma Science"}
MACRO {ijimw} {"International Journal of Infrared and Millimeter Waves"}
MACRO {ip} {"Infrared Physics"}
MACRO {irp} {"Infrared Physics"}
MACRO {jap} {"Journal of Applied Physics"}
MACRO {jasa} {"Journal of the Acoustical Society of America"}
MACRO {jcp} {"Journal of Computational Physics"}
MACRO {jetp} {"Soviet Physics--JETP"}
MACRO {jfe} {"Journal of Fusion Energy"}
MACRO {jfm} {"Journal of Fluid Mechanics"}
MACRO {jmp} {"Journal of Mathematical Physics"}
MACRO {jne} {"Journal of Nuclear Energy"}
MACRO {jnec} {"Journal of Nuclear Energy, Part C: Plasma Physics, Accelerators, Thermonuclear Research"}
MACRO {jnm} {"Journal of Nuclear Materials"}
MACRO {jpc} {"Journal of Physical Chemistry"}
MACRO {jpp} {"Journal of Plasma Physics"}
MACRO {jpsj} {"Journal of the Physical Society of Japan"}
MACRO {jsi} {"Journal of Scientific Instruments"}
MACRO {jvst} {"Journal of Vacuum Science and Technology"}
MACRO {nat} {"Nature"}
MACRO {nature} {"Nature"}
MACRO {nedf} {"Nuclear Engineering and Design/Fusion"}
MACRO {nf} {"Nuclear Fusion"}
MACRO {nim} {"Nuclear Instruments and Methods"}
MACRO {nimpr} {"Nuclear Instruments and Methods in Physics Research"}
MACRO {np} {"Nuclear Physics"}
MACRO {npb} {"Nuclear Physics B"}
MACRO {nt/f} {"Nuclear Technology/Fusion"}
MACRO {npbpc} {"Nuclear Physics B (Proceedings Supplements)"}
MACRO {inc} {"Il Nuovo Cimento"}
MACRO {nc} {"Nuovo Cimento"}
MACRO {pf} {"Physics of Fluids"}
MACRO {pfa} {"Physics of Fluids A: Fluid Dynamics"}
MACRO {pfb} {"Physics of Fluids B: Plasma Physics"}
MACRO {pl} {"Physics Letters"}
MACRO {pla} {"Physics Letters A"}
MACRO {plb} {"Physics Letters B"}
MACRO {prep} {"Physics Reports"}
MACRO {pnas} {"Proceedings of the National Academy of Sciences of the USA"}
MACRO {pp} {"Physics of Plasmas"}
MACRO {ppcf} {"Plasma Physics and Controlled Fusion"}
MACRO {phitrsl} {"Philosophical Transactions of the Royal Society of London"}
MACRO {prl} {"Physical Review Letters"}
MACRO {pr} {"Physical Review"}
MACRO {physrev} {"Physical Review"}
MACRO {pra} {"Physical Review A"}
MACRO {prb} {"Physical Review B"}
MACRO {prc} {"Physical Review C"}
MACRO {prd} {"Physical Review D"}
MACRO {pre} {"Physical Review E"}
MACRO {ps} {"Physica Scripta"}
MACRO {procrsl} {"Proceedings of the Royal Society of London"}
MACRO {rmp} {"Reviews of Modern Physics"}
MACRO {rsi} {"Review of Scientific Instruments"}
MACRO {science} {"Science"}
MACRO {sciam} {"Scientific American"}
MACRO {sam} {"Studies in Applied Mathematics"}
MACRO {sjpp} {"Soviet Journal of Plasma Physics"}
MACRO {spd} {"Soviet Physics--Doklady"}
MACRO {sptp} {"Soviet Physics--Technical Physics"}
MACRO {spu} {"Soviet Physics--Uspeki"}
MACRO {st} {"Sky and Telescope"}
 % End module: physjour.mbs
 %-------------------------------------------------------------------
 % Begin module:
 % \ProvidesFile{geojour.mbs}[2002/07/10 2.0h (PWD)]
MACRO {aisr} {"Advances in Space Research"}
MACRO {ag} {"Annales Geophysic\ae"}
MACRO {anigeo} {"Annali di Geofisica"}
MACRO {angl} {"Annals of Glaciology"}
MACRO {andmet} {"Annalen der Meteorologie"}
MACRO {andgeo} {"Annales de Geophysique"}
MACRO {andphy} {"Annales de Physique"}
MACRO {afmgb} {"Archiv f\^^b{u}r Meteorologie, Geophysik und Bioklimatologie"}
MACRO {ass}{"Astrophysics and Space Science"}
MACRO {atph} {"Atm\'osphera"}
MACRO {aao} {"Atmosphere-Ocean"}
MACRO {atenv} {"Atmospheric Environment"}
MACRO {aujag} {"Australian Journal of Agricultural Research"}
MACRO {aumet} {"Australian Meteorological Magazine"}
MACRO {blmet} {"Boundary-Layer Meteorology"}
MACRO {bams} {"Bulletin of the American Meteorological Society"}
MACRO {cch} {"Climatic Change"}
MACRO {cdyn} {"Climate Dynamics"}
MACRO {cbul} {"Climatological Bulletin"}
MACRO {cap} {"Contributions to Atmospheric Physics"}
MACRO {dsr} {"Deep-Sea Research"}
MACRO {dhz} {"Deutsche Hydrographische Zeitschrift"}
MACRO {dao} {"Dynamics of Atmospheres and Oceans"}
MACRO {eco} {"Ecology"}
MACRO {empl}{"Earth, Moon and Planets"}
MACRO {envres} {"Environmental Research"}
MACRO {envst} {"Environmental Science and Technology"}
MACRO {ecms} {"Estuarine and Coastal Marine Science"}
MACRO {expa}{"Experimental Astronomy"}
MACRO {geoint} {"Geofisica Internationale"}
MACRO {geopub} {"Geofysiske Publikasjoner"}
MACRO {geogeo} {"Geologiya i Geofizika"}
MACRO {gafd} {"Geophysical and Astrophysical Fluid Dynamics"}
MACRO {gfd} {"Geophysical Fluid Dynamics"}
MACRO {geomag} {"Geophysical Magazine"}
MACRO {georl} {"Geophysical Research Letters"}
MACRO {grl} {"Geophysical Research Letters"}
MACRO {ga} {"Geophysica"}
MACRO {gs} {"Geophysics"}
MACRO {ieeetap} {"IEEE Transactions on Antennas and Propagation"}
MACRO {ijawp} {"International Journal of Air and Water Pollution"}
MACRO {ijc} {"International Journal of Climatology"}
MACRO {ijrs} {"International Journal of Remote Sensing"}
MACRO {jam} {"Journal of Applied Meteorology"}
MACRO {jaot} {"Journal of Atmospheric and Oceanic Technology"}
MACRO {jatp} {"Journal of Atmospheric and Terrestrial Physics"}
MACRO {jastp} {"Journal of Atmospheric and Solar-Terrestrial Physics"}
MACRO {jce} {"Journal of Climate"}
MACRO {jcam} {"Journal of Climate and Applied Meteorology"}
MACRO {jcm} {"Journal of Climate Meteorology"}
MACRO {jcy} {"journal of Climatology"}
MACRO {jgr} {"Journal of Geophysical Research"}
MACRO {jga} {"Journal of Glaciology"}
MACRO {jh} {"Journal of Hydrology"}
MACRO {jmr} {"Journal of Marine Research"}
MACRO {jmrj} {"Journal of Meteorological Research, Japan"}
MACRO {jm} {"Journal of Meteorology"}
MACRO {jpo} {"Journal of Physical Oceanography"}
MACRO {jra} {"Journal de Recherches Atmospheriques"}
MACRO {jaes} {"Journal of the Aeronautical Sciences"}
MACRO {japca} {"Journal of the Air Pollution Control Association"}
MACRO {jas} {"Journal of the Atmospheric Sciences"}
MACRO {jmts} {"Journal of the Marine Technology Society"}
MACRO {jmsj} {"Journal of Meteorological Society of Japan"}
MACRO {josj} {"Journal of the Oceanographical Society of Japan"}
MACRO {jwm} {"Journal of Weather Modification"}
MACRO {lao} {"Limnology and Oceanography"}
MACRO {mwl} {"Mariners Weather Log"}
MACRO {mau} {"Mausam"}
MACRO {meteor} {"``Meteor'' Forschungsergebnisse"}
MACRO {map} {"Meteorology and Atmospheric Physics"}
MACRO {metmag} {"Meteorological Magazine"}
MACRO {metmon} {"Meteorological Monographs"}
MACRO {metrun} {"Meteorologische Rundschau"}
MACRO {metzeit} {"Meteorologische Zeitschrift"}
MACRO {metgid} {"Meteorologiya i Gidrologiya"}
MACRO {mwr} {"Monthly Weather Review"}
MACRO {nwd} {"National Weather Digest"}
MACRO {nzjmfr} {"New Zealand Journal of Marine and Freshwater Research"}
MACRO {npg} {"Nonlinear Processes in Geophysics"}
MACRO {om} {"Oceanography and Meteorology"}
MACRO {ocac} {"Oceanologica Acta"}
MACRO {oceanus} {"Oceanus"}
MACRO {paleoc} {"Paleoceanography"}
MACRO {pce} {"Physics and Chemistry of the Earth"}
MACRO {pmg} {"Papers in Meteorology and Geophysics"}
MACRO {ppom} {"Papers in Physical Oceanography and Meteorology"}
MACRO {physzeit} {"Physikalische Zeitschrift"}
MACRO {pps} {"Planetary and Space Science"}
MACRO {pss} {"Planetary and Space Science"}
MACRO {pag} {"Pure and Applied Geophysics"}
MACRO {qjrms} {"Quarterly Journal of the Royal Meteorological Society"}
MACRO {quatres} {"Quaternary Research"}
MACRO {rsci} {"Radio Science"}
MACRO {rse} {"Remote Sensing of the Environment"}
MACRO {rgeo} {"Reviews of Geophysics"}
MACRO {rgsp} {"Reviews of Geophysics and Space Physics"}
MACRO {rdgeo} {"Revista de Geofisica"}
MACRO {revmeta} {"Revista Meteorologica"}
MACRO {sgp}{"Surveys in Geophysics"}
MACRO {sp} {"Solar Phys."}
MACRO {ssr} {"Space Science Review"}
MACRO {tellus} {"Tellus"}
MACRO {tac} {"Theoretical and Applied Climatology"}
MACRO {tagu} {"Transactions, American Geophysical Union (EOS)"}
MACRO {wrr} {"Water Resources Research"}
MACRO {weather} {"Weather"}
MACRO {wafc} {"Weather and Forecasting"}
MACRO {ww} {"Weatherwise"}
MACRO {wmob} {"World Meteorological Organization Bulletin"}
MACRO {zeitmet} {"Zeitschrift f\^^b{u}r Meteorologie"}
 % End module: geojour.mbs
 %-------------------------------------------------------------------
 % Begin module:
 % \ProvidesFile{photjour.mbs}[1999/02/24 2.0b (PWD)]

MACRO {appopt} {"Applied Optics"}
MACRO {bell} {"Bell Systems Technical Journal"}
MACRO {ell} {"Electronics Letters"}
MACRO {jasp} {"Journal of Applied Spectroscopy"}
MACRO {jqe} {"IEEE Journal of Quantum Electronics"}
MACRO {jlwt} {"Journal of Lightwave Technology"}
MACRO {jmo} {"Journal of Modern Optics"}
MACRO {josa} {"Journal of the Optical Society of America"}
MACRO {josaa} {"Journal of the Optical Society of America~A"}
MACRO {josab} {"Journal of the Optical Society of America~B"}
MACRO {jdp} {"Journal de Physique"}
MACRO {oc} {"Optics Communications"}
MACRO {ol} {"Optics Letters"}
MACRO {phtl} {"IEEE Photonics Technology Letters"}
MACRO {pspie} {"Proceedings of the Society for Photo-Optical Instruments Engineers"}
MACRO {sse} {"Solid-State Electronics"}
MACRO {sjot} {"Soviet Journal of Optical Technology"}
MACRO {sjqe} {"Soviet Journal of Quantum Electronics"}
MACRO {sleb} {"Soviet Physics--Lebedev Institute Reports"}
MACRO {stph} {"Soviet Physics--Technical Physics"}
MACRO {stphl} {"Soviet Technical Physics Letters"}
MACRO {vr} {"Vision Research"}
MACRO {zph} {"Zeitschrift f\^^b{u}r Physik"}
MACRO {zphb} {"Zeitschrift f\^^b{u}r Physik~B"}
MACRO {zphd} {"Zeitschrift f\^^b{u}r Physik~D"}

MACRO {CLEO} {"Conf. on Lasers and Electro-Optics"}
MACRO {ASSL} {"Advanced Solid State Lasers"}
MACRO {OSA}  {"Optical Society of America"}
 % End module: photjour.mbs
%% Copyright 1994-2005 Patrick W Daly
MACRO {acmcs} {"ACM Computing Surveys"}

MACRO {acta} {"Acta Informatica"}

MACRO {cacm} {"Communications of the ACM"}

MACRO {ibmjrd} {"IBM Journal of Research and Development"}

MACRO {ibmsj} {"IBM Systems Journal"}

MACRO {ieeese} {"IEEE Transactions on Software Engineering"}

MACRO {ieeetc} {"IEEE Transactions on Computers"}

MACRO {ieeetcad}
 {"IEEE Transactions on Computer-Aided Design of Integrated Circuits"}

MACRO {ipl} {"Information Processing Letters"}

MACRO {jacm} {"Journal of the ACM"}

MACRO {jcss} {"Journal of Computer and System Sciences"}

MACRO {scp} {"Science of Computer Programming"}

MACRO {sicomp} {"SIAM Journal on Computing"}

MACRO {tocs} {"ACM Transactions on Computer Systems"}

MACRO {tods} {"ACM Transactions on Database Systems"}

MACRO {tog} {"ACM Transactions on Graphics"}

MACRO {toms} {"ACM Transactions on Mathematical Software"}

MACRO {toois} {"ACM Transactions on Office Information Systems"}

MACRO {toplas} {"ACM Transactions on Programming Languages and Systems"}

MACRO {tcs} {"Theoretical Computer Science"}
FUNCTION {bibinfo.check}
{ swap$
  duplicate$ missing$
    {
      pop$ pop$
      ""
    }
    { duplicate$ empty$
        {
          swap$ pop$
        }
        { swap$
          pop$
        }
      if$
    }
  if$
}
FUNCTION {bibinfo.warn}
{ swap$
  duplicate$ missing$
    {
      swap$ "missing " swap$ * " in " * cite$ * warning$ pop$
      ""
    }
    { duplicate$ empty$
        {
          swap$ "empty " swap$ * " in " * cite$ * warning$
        }
        { swap$
          pop$
        }
      if$
    }
  if$
}
FUNCTION {write.url}
{ url empty$
    { skip$ }
    { "\newline\urlprefix\url{" url * "}" * write$ newline$ }
  if$
}

STRINGS  { bibinfo}
INTEGERS { nameptr namesleft numnames }

FUNCTION {format.names}
{ 'bibinfo :=
  duplicate$ empty$ 'skip$ {
  's :=
  "" 't :=
  #1 'nameptr :=
  s num.names$ 'numnames :=
  numnames 'namesleft :=
    { namesleft #0 > }
    { s nameptr
      "{f.~}{vv~}{ll}{, jj}"
      format.name$
      % Added line by Karl H.
      highlight.if.cv.author
      bibinfo bibinfo.check
      % Line added by Karl H.
      highlight.student.authors
      't :=
      nameptr #1 >
        {
          namesleft #1 >
            { ", " * t * }
            {
              s nameptr "{ll}" format.name$ duplicate$ "others" =
                { 't := }
                { pop$ }
              if$
              numnames #2 >
                { "," * }
                'skip$
              if$
              t "others" =
                {
                  " " * bbl.etal emphasize *
                }
                {
                  bbl.and
                  space.word * t *
                }
              if$
            }
          if$
        }
        't
      if$
      nameptr #1 + 'nameptr :=
      namesleft #1 - 'namesleft :=
    }
  while$
  } if$
}
FUNCTION {format.names.ed}
{
  format.names
}
FUNCTION {format.authors}
{ author "author" format.names
}
FUNCTION {get.bbl.editor}
{ editor num.names$ #1 > 'bbl.editors 'bbl.editor if$ }

FUNCTION {format.editors}
{ editor "editor" format.names duplicate$ empty$ 'skip$
    {
      "," *
      " " *
      get.bbl.editor
      *
    }
  if$
}
FUNCTION {format.note}
{
 note empty$
    { "" }
    { note #1 #1 substring$
      duplicate$ "{" =
        'skip$
        { output.state mid.sentence =
          { "l" }
          { "u" }
        if$
        change.case$
        }
      if$
      note #2 global.max$ substring$ * "note" bibinfo.check
    }
  if$
}
FUNCTION {format.doi}
{
    doi "doi" bibinfo.check
    duplicate$ empty$
        { pop$ "" }
        { "\doi{" swap$ * "}" * }
    if$
}

FUNCTION {format.title}
{ title
  "title" bibinfo.check
  duplicate$ empty$ 'skip$
    {
      "\enquote{" swap$ *
      add.period$ "}" *
    }
  if$
}
FUNCTION {output.bibitem}
{ newline$
  "\bibitem{" write$
  cite$ write$
  "}" write$
  newline$
  ""
  before.all 'output.state :=
}

FUNCTION {n.dashify}
{
  't :=
  ""
    { t empty$ not }
    { t #1 #1 substring$ "-" =
        { t #1 #2 substring$ "--" = not
            { "--" *
              t #2 global.max$ substring$ 't :=
            }
            {   { t #1 #1 substring$ "-" = }
                { "-" *
                  t #2 global.max$ substring$ 't :=
                }
              while$
            }
          if$
        }
        { t #1 #1 substring$ *
          t #2 global.max$ substring$ 't :=
        }
      if$
    }
  while$
}

FUNCTION {word.in}
{ bbl.in capitalize
  " " * }

FUNCTION {format.date}
{
  ""
  duplicate$ empty$
  year  "year"  bibinfo.check duplicate$ empty$
    { swap$ 'skip$
        { "there's a month but no year in " cite$ * warning$ }
      if$
      *
    }
    { swap$ 'skip$
        {
          swap$
          " " * swap$
        }
      if$
      *
    }
  if$
  duplicate$ empty$
    'skip$
    {
      before.all 'output.state :=
    " (" swap$ * ")" *
    }
  if$
}
FUNCTION {format.btitle}
{ title "title" bibinfo.check
  duplicate$ empty$ 'skip$
    {
      emphasize
    }
  if$
}
FUNCTION {either.or.check}
{ empty$
    'pop$
    { "can't use both " swap$ * " fields in " * cite$ * warning$ }
  if$
}
FUNCTION {format.bvolume}
{ volume empty$
    { "" }
    { bbl.volume volume tie.or.space.prefix
      "volume" bibinfo.check * *
      series "series" bibinfo.check
      duplicate$ empty$ 'pop$
        { swap$ bbl.of space.word * swap$
          emphasize * }
      if$
      "volume and number" number either.or.check
    }
  if$
}
FUNCTION {format.number.series}
{ volume empty$
    { number empty$
        { series field.or.null }
        { series empty$
            { number "number" bibinfo.check }
            { output.state mid.sentence =
                { bbl.number }
                { bbl.number capitalize }
              if$
              number tie.or.space.prefix "number" bibinfo.check * *
              bbl.in space.word *
              series "series" bibinfo.check *
            }
          if$
        }
      if$
    }
    { "" }
  if$
}

FUNCTION {format.edition}
{ edition duplicate$ empty$ 'skip$
    {
      output.state mid.sentence =
        { "l" }
        { "t" }
      if$ change.case$
      "edition" bibinfo.check
      " " * bbl.edition *
    }
  if$
}
INTEGERS { multiresult }
FUNCTION {multi.page.check}
{ 't :=
  #0 'multiresult :=
    { multiresult not
      t empty$ not
      and
    }
    { t #1 #1 substring$
      duplicate$ "-" =
      swap$ duplicate$ "," =
      swap$ "+" =
      or or
        { #1 'multiresult := }
        { t #2 global.max$ substring$ 't := }
      if$
    }
  while$
  multiresult
}
FUNCTION {format.pages}
{ pages duplicate$ empty$ 'skip$
    { duplicate$ multi.page.check
        {
          bbl.pages swap$
          n.dashify
        }
        {
          bbl.page swap$
        }
      if$
      tie.or.space.prefix
      "pages" bibinfo.check
      * *
    }
  if$
}
FUNCTION {format.journal.pages}
{ pages duplicate$ empty$ 'pop$
    { swap$ duplicate$ empty$
        { pop$ pop$ format.pages }
        {
          ": " *
          swap$
          n.dashify
          "pages" bibinfo.check
          *
        }
      if$
    }
  if$
}
FUNCTION {format.journal.eid}
{ eid "eid" bibinfo.check
  duplicate$ empty$ 'pop$
    { swap$ duplicate$ empty$ 'skip$
      {
          ": " *
      }
      if$
      swap$ *
    }
  if$
}
FUNCTION {format.vol.num.pages}
{ volume field.or.null
  duplicate$ empty$ 'skip$
    {
      "volume" bibinfo.check
    }
  if$
  bolden
  number "number" bibinfo.check duplicate$ empty$ 'skip$
    {
      swap$ duplicate$ empty$
        { "there's a number but no volume in " cite$ * warning$ }
        'skip$
      if$
      swap$
      "~(" swap$ * ")" *
    }
  if$ *
  eid empty$
    { format.journal.pages }
    { format.journal.eid }
  if$
}

FUNCTION {format.chapter.pages}
{ chapter empty$
    'format.pages
    { type empty$
        { bbl.chapter }
        { type "l" change.case$
          "type" bibinfo.check
        }
      if$
      chapter tie.or.space.prefix
      "chapter" bibinfo.check
      * *
      pages empty$
        'skip$
        { ", " * format.pages * }
      if$
    }
  if$
}

FUNCTION {format.booktitle}
{
  booktitle "booktitle" bibinfo.check
  emphasize
}
FUNCTION {format.in.ed.booktitle}
{ format.booktitle duplicate$ empty$ 'skip$
    {
      editor "editor" format.names.ed duplicate$ empty$ 'pop$
        {
          get.bbl.editor
          swap$ "," *
          " " * swap$ *
          swap$
          "," *
          " " * swap$
          * }
      if$
      word.in swap$ *
    }
  if$
}
FUNCTION {empty.misc.check}
{ author empty$ title empty$ howpublished empty$
  month empty$ year empty$ note empty$
  and and and and and
    { "all relevant fields are empty in " cite$ * warning$ }
    'skip$
  if$
}
FUNCTION {format.thesis.type}
{ type duplicate$ empty$
    'pop$
    { swap$ pop$
      "t" change.case$ "type" bibinfo.check
    }
  if$
}
FUNCTION {format.tr.number}
{ number "number" bibinfo.check
  type duplicate$ empty$
    { pop$ bbl.techrep }
    'skip$
  if$
  "type" bibinfo.check
  swap$ duplicate$ empty$
    { pop$ "t" change.case$ }
    { tie.or.space.prefix * * }
  if$
}
FUNCTION {format.article.crossref}
{
  key duplicate$ empty$
    { pop$
      journal duplicate$ empty$
        { "need key or journal for " cite$ * " to crossref " * crossref * warning$ }
        { "journal" bibinfo.check emphasize word.in swap$ * }
      if$
    }
    { word.in swap$ * " " *}
  if$
  " \cite{" * crossref * "}" *
}
FUNCTION {format.crossref.editor}
{ editor #1 "{vv~}{ll}" format.name$
  "editor" bibinfo.check
  editor num.names$ duplicate$
  #2 >
    { pop$
      "editor" bibinfo.check
      " " * bbl.etal
      emphasize
      *
    }
    { #2 <
        'skip$
        { editor #2 "{ff }{vv }{ll}{ jj}" format.name$ "others" =
            {
              "editor" bibinfo.check
              " " * bbl.etal
              emphasize
              *
            }
            {
             bbl.and space.word
              * editor #2 "{vv~}{ll}" format.name$
              "editor" bibinfo.check
              *
            }
          if$
        }
      if$
    }
  if$
}
FUNCTION {format.book.crossref}
{ volume duplicate$ empty$
    { "empty volume in " cite$ * "'s crossref of " * crossref * warning$
      pop$ word.in
    }
    { bbl.volume
      capitalize
      swap$ tie.or.space.prefix "volume" bibinfo.check * * bbl.of space.word *
    }
  if$
  editor empty$
  editor field.or.null author field.or.null =
  or
    { key empty$
        { series empty$
            { "need editor, key, or series for " cite$ * " to crossref " *
              crossref * warning$
              "" *
            }
            { series emphasize * }
          if$
        }
        { key * }
      if$
    }
    { format.crossref.editor * }
  if$
  " \cite{" * crossref * "}" *
}
FUNCTION {format.incoll.inproc.crossref}
{
  editor empty$
  editor field.or.null author field.or.null =
  or
    { key empty$
        { format.booktitle duplicate$ empty$
            { "need editor, key, or booktitle for " cite$ * " to crossref " *
              crossref * warning$
            }
            { word.in swap$ * }
          if$
        }
        { word.in key * " " *}
      if$
    }
    { word.in format.crossref.editor * " " *}
  if$
  " \cite{" * crossref * "}" *
}
FUNCTION {format.org.or.pub}
{ 't :=
  ""
  address empty$ t empty$ and
    'skip$
    {
      address "address" bibinfo.check *
      t empty$
        'skip$
        { address empty$
            'skip$
            { ": " * }
          if$
          t *
        }
      if$
    }
  if$
}
FUNCTION {format.publisher.address}
{ publisher "publisher" bibinfo.warn format.org.or.pub
}

FUNCTION {format.organization.address}
{ organization "organization" bibinfo.check format.org.or.pub
}

FUNCTION {article}
{ output.bibitem
  format.authors "author" output.check
  new.block
  format.title "title" output.check
  new.block
  crossref missing$
    {
      journal
      "journal" bibinfo.check
      emphasize
      "journal" output.check
      add.blank
      format.vol.num.pages output
      format.date "year" output.check
    }
    { format.article.crossref output.nonnull
      format.pages output
    }
  if$
  new.block
  format.note output
  new.block
  format.doi output
  fin.entry
  write.url
}
FUNCTION {book}
{ output.bibitem
  author empty$
    { format.editors "author and editor" output.check
    }
    { format.authors output.nonnull
      crossref missing$
        { "author and editor" editor either.or.check }
        'skip$
      if$
    }
  if$
  new.block
  format.btitle "title" output.check
  crossref missing$
    { format.bvolume output
      new.block
      new.sentence
      format.number.series output
      format.publisher.address output
    }
    {
      new.block
      format.book.crossref output.nonnull
    }
  if$
  format.edition output
  format.date "year" output.check
  new.block
  format.note output
  fin.entry
  write.url
}
FUNCTION {booklet}
{ output.bibitem
  format.authors output
  new.block
  format.title "title" output.check
  new.block
  howpublished "howpublished" bibinfo.check output
  address "address" bibinfo.check output
  format.date output
  new.block
  format.note output
  fin.entry
  write.url
}

FUNCTION {inbook}
{ output.bibitem
  author empty$
    { format.editors "author and editor" output.check
    }
    { format.authors output.nonnull
      crossref missing$
        { "author and editor" editor either.or.check }
        'skip$
      if$
    }
  if$
  new.block
  format.title "title" output.check
  new.block
  format.in.ed.booktitle "booktitle" output.check
  crossref missing$
    {
      format.bvolume output
      format.chapter.pages "chapter and pages" output.check
      new.block
      new.sentence
      format.number.series output
      format.publisher.address output
    }
    {
      format.chapter.pages "chapter and pages" output.check
      new.block
      format.book.crossref output.nonnull
    }
  if$
  format.edition output
  format.date "year" output.check
  new.block
  format.note output
  fin.entry
  write.url
}

FUNCTION {incollection}
{ output.bibitem
  format.authors "author" output.check
  new.block
  format.title "title" output.check
  new.block
  crossref missing$
    { format.in.ed.booktitle "booktitle" output.check
      format.bvolume output
      format.chapter.pages output
      new.sentence
      format.number.series output
      format.publisher.address output
      format.edition output
      format.date "year" output.check
    }
    { format.incoll.inproc.crossref output.nonnull
      format.chapter.pages output
    }
  if$
  new.block
  format.note output
  new.block
  format.doi output
  fin.entry
  write.url
}
FUNCTION {inproceedings}
{ output.bibitem
  format.authors "author" output.check
  new.block
  format.title "title" output.check
  new.block
  crossref missing$
    { format.in.ed.booktitle "booktitle" output.check
      format.bvolume output
      format.pages output
      new.sentence
      format.number.series output
      publisher empty$
        { format.organization.address output }
        { organization "organization" bibinfo.check output
          format.publisher.address output
        }
      if$
      format.date "year" output.check
    }
    { format.incoll.inproc.crossref output.nonnull
      format.pages output
    }
  if$
  new.block
  format.note output
  fin.entry
  write.url
}
FUNCTION {conference} { inproceedings }
FUNCTION {manual}
{ output.bibitem
  author empty$
    { organization "organization" bibinfo.check
      duplicate$ empty$ 'pop$
        { output
          address "address" bibinfo.check output
        }
      if$
    }
    { format.authors output.nonnull }
  if$
  new.block
  format.btitle "title" output.check
  author empty$
    { organization empty$
        {
          address new.block.checka
          address "address" bibinfo.check output
        }
        'skip$
      if$
    }
    {
      organization address new.block.checkb
      organization "organization" bibinfo.check output
      address "address" bibinfo.check output
    }
  if$
  format.edition output
  format.date output
  new.block
  format.note output
  fin.entry
  write.url
}

FUNCTION {mastersthesis}
{ output.bibitem
  format.authors "author" output.check
  new.block
  format.btitle
  "title" output.check
  new.block
  bbl.mthesis format.thesis.type output.nonnull
  school "school" bibinfo.warn output
  address "address" bibinfo.check output
  format.date "year" output.check
  new.block
  format.note output
  fin.entry
  write.url
}

FUNCTION {misc}
{ output.bibitem
  format.authors output
  title howpublished new.block.checkb
  format.title output
  howpublished new.block.checka
  howpublished "howpublished" bibinfo.check output
  format.date output
  new.block
  format.note output
  fin.entry
  write.url
  empty.misc.check
}
FUNCTION {phdthesis}
{ output.bibitem
  format.authors "author" output.check
  new.block
  format.btitle
  "title" output.check
  new.block
  bbl.phdthesis format.thesis.type output.nonnull
  school "school" bibinfo.warn output
  address "address" bibinfo.check output
  format.date "year" output.check
  new.block
  format.note output
  fin.entry
  write.url
}

FUNCTION {proceedings}
{ output.bibitem
  editor empty$
    { organization "organization" bibinfo.check output
    }
    { format.editors output.nonnull }
  if$
  new.block
  format.btitle "title" output.check
  format.bvolume output
  editor empty$
    { publisher empty$
        'skip$
        {
          new.sentence
          format.number.series output
          format.publisher.address output
        }
      if$
    }
    { publisher empty$
        {
          new.sentence
          format.organization.address output }
        {
          new.sentence
          organization "organization" bibinfo.check output
          format.publisher.address output
        }
      if$
     }
  if$
      format.date "year" output.check
  new.block
  format.note output
  fin.entry
  write.url
}

FUNCTION {techreport}
{ output.bibitem
  format.authors "author" output.check
  new.block
  format.btitle
  "title" output.check
  new.block
  format.tr.number output.nonnull
  institution "institution" bibinfo.warn output
  address "address" bibinfo.check output
  format.date "year" output.check
  new.block
  format.note output
  fin.entry
  write.url
}

% EDITED BY KARL
FUNCTION {unpublished}
{ output.bibitem
  format.authors "author" output.check
  new.block
  format.title "title" output.check
  journal missing$
    {}
    { new.block
      journal
      "journal" bibinfo.check
      emphasize
      "journal" output.check
      add.blank
      pages missing$
        {}
        { format.vol.num.pages output }
      if$
    }
    if$
  %format.date output
  format.date "year" output.check
  new.block
  format.note "note" output.check
  fin.entry
  write.url
}

FUNCTION {default.type} { misc }
READ
STRINGS { longest.label }
INTEGERS { number.label longest.label.width }
FUNCTION {initialize.longest.label}
{ "" 'longest.label :=
  #1 'number.label :=
  #0 'longest.label.width :=
}
FUNCTION {longest.label.pass}
{ number.label int.to.str$ 'label :=
  number.label #1 + 'number.label :=
  label width$ longest.label.width >
    { label 'longest.label :=
      label width$ 'longest.label.width :=
    }
    'skip$
  if$
}

EXECUTE {initialize.longest.label}
ITERATE {longest.label.pass}
FUNCTION {begin.bib}
{  preamble$ empty$
    'skip$
    { preamble$ write$ newline$ }
  if$
  "\frenchspacing"
  write$ newline$
  "\providecommand{\enquote}[1]{``#1''}"
  write$ newline$
  "\providecommand{\url}[1]{\texttt{#1}}"
  write$ newline$
  "\providecommand{\urlprefix}{URL }"
  write$ newline$
  "\providecommand{\doi}{DOI }"
  write$ newline$
  "\begin{thebibliography}{"  longest.label  * "}" *
  write$ newline$
}
EXECUTE {begin.bib}
EXECUTE {init.state.consts}
ITERATE {process.configs.only}
ITERATE {process.non.configs}
%ITERATE {call.type$}
FUNCTION {end.bib}
{ newline$
  "\end{thebibliography}" write$ newline$
}
EXECUTE {end.bib}
%% End of customized bst file
%%
%% End of file `CV.bst'.
