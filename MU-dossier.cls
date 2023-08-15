\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{MU-dossier}[2022/04/07 2.1
                           U. Missouri faculty dossier document class]

% 2.1:  Fixed bug related to scope of \cfoot, \lhead, etc. in \@makechapterhead
% 2.0:  Created "RPT" class to override the default chapter style and instead
%       create a dossier suitable for the call letter from 2021 and later
%       (work in progress)
% 1.16: Tweaked spacing (specifically the minus spacing) between Role and other
%       list items; also tweaked "plus" spacing between list items to even
%       out spacing on pages
% 1.15: Fixed "page 0.2" issue during table of contents
% 1.14: Created CVitemize, CVenumerate, and CVrevnumerate to have better
%       control of list spacing without breaking the optional argument to the
%       revnumerate environment
% 1.13: Added \interlinepenalty=1000 to revnumerate environments so that
%       bibliography entries will not break across pages unless absolutely
%       necessary
% 1.12: Changed \addcontentsline so it's only the page number, excluding
%       the chapter it's part of, that appears in the Contents, and made
%       \tableofcontents reset pages to roman numerals without a chapter
% 1.11: Added \role for use in dossiers, tweaked Contents and footers
% 1.10: Forgot to record changes before this version!

\hyphenation{Ken-nedy Am-herst}

% Conditionals for use later
\newif\iflong@form
\newif\ifshort@form
\newif\ifshow@allpubs
% Options
%\DeclareOption{10pt}{\def\text@size{10pt}}
%\DeclareOption{11pt}{\def\text@size{11pt}}
%\DeclareOption{12pt}{\def\text@size{12pt}}
%\DeclareOption{letterpaper}{\gdef\paper@size{letterpaper}}
%\DeclareOption{a4paper}{\gdef\paper@size{a4paper}}
%\DeclareOption{draft}{\gdef\rule@type{draft}}
%\DeclareOption{final}{\gdef\rule@type{final}}
\DeclareOption{RPT}{%
    \ExecuteOptions{longform}
    \AtEndOfClass{%
        \renewcommand*{\thechapter}{\Alph{chapter}}
%        \renewcommand{\chapter}{%
%            \cleardoublepage
%            \renewcommand{\footrulewidth}{0.5pt}
%            \pagestyle{fancy}%
%            \thispagestyle{plain}%
%            \setcounter{page}{1}%
%            \global\@topnum\z@
%            \rhead{\small\scshape\thesection.~FIXME}%
%            \lhead{\small\scshape\@author}%
%            \lfoot{\small\scshape\@date}%
%            \rfoot{\small \thepage}%
%            \cfoot{}
%        }
%        \let\section\subsection
%        \let\subsection\subsubsection
%        \let\subsubsection\paragraph
%        \let\paragraph\subparagraph
%        \stepcounter{tocdepth}%
%        \stepcounter{secnumdepth}%
%        \renewcommand*{\thesection}{\Alph{section}}%
    }
}
\DeclareOption{longform}{\long@formtrue\short@formfalse}
\DeclareOption{normalform}{\long@formfalse\short@formfalse}
\DeclareOption{shortform}{\short@formtrue\long@formfalse}
\DeclareOption{shownumbers}{\gdef\secnum@depth{7}}
\DeclareOption{hidenumbers}{\gdef\secnum@depth{-1}}
\DeclareOption{selectpubs}{\show@allpubsfalse}
\DeclareOption{allpubs}{\show@allpubstrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}

% Default options
\ExecuteOptions{11pt,normalform,letterpaper,shownumbers,final,allpubs,oneside,openany}
\ProcessOptions

% Based on the report class
%\LoadClass[\text@size,\paper@size,twoside,\rule@type]{report}
\LoadClass{report}

% Process show/hide numbers option...
\setcounter{secnumdepth}{\secnum@depth}

% Required packages
\RequirePackage{revnum}
%\RequirePackage{enumitem}
%\setlist[itemize]{itemsep=0.25ex}
%\setlist[enumerate]{itemsep=0.65ex}
%\setlist[revnumerate]{parsep=0.65ex}

\RequirePackage{fancyhdr}
\RequirePackage{comment}
\RequirePackage{lastpage}

% Page layout
\usepackage{calc}
\iflong@form
\usepackage[inner=1.25in,outer=1in,top=1in,bottom=1in]{geometry}
\else
\usepackage[margin=1.00in]{geometry}
\fi
\setlength{\parindent}{0pt}
\advance\headheight by 3pt%

%% Do NOT encourage (and in fact strongly DIScourage) page breaks before lists
\@beginparpenalty 500%

%\usepackage{hanging}

% Format text headings
\@secpenalty = -500%
\renewcommand{\section}{%
    \@startsection{section}{1}{\z@}%
                  {2.5ex \@plus 2.5ex \@minus 0.2ex}%
                  {1.5ex \@plus 0.2ex \@minus 0.2ex}%
                  %{\penalty-\@highpenalty\normalfont\bfseries\MakeUppercase}%
                  {\penalty-1500\normalfont\bfseries\MakeUppercase}%
}
\renewcommand{\thesection}{\arabic{section}}
\renewcommand{\subsection}{%
    \@startsection{subsection}{2}{\z@}%
                  {1.0ex \@plus 2.0ex \@minus 0.2ex}%
                  {1.0ex \@plus 0.75ex \@minus 0.2ex}%
                  {\penalty-\@medpenalty\normalfont\bfseries}%
}
%\renewcommand{\thesubsection}{\arabic{section}.\arabic{subsection}}
\renewcommand{\subsubsection}{%
    \@startsection{subsubsection}{3}{\z@}%
                  {1.0ex \@plus 1.5ex \@minus 0.2ex}%
                  {1.0ex \@plus 0.5ex \@minus 0.2ex}%
                  {\penalty-\@lowpenalty\normalfont}%
                  %{\normalfont\itshape}%
}
\renewcommand{\paragraph}{%
    \@startsection{paragraph}{4}{\z@}%
                  {1.0ex \@plus 1ex \@minus 0.2ex}%
                  {1.0ex \@plus 0.25ex \@minus 0.2ex}%
                  {\penalty-\@lowpenalty\normalfont}%
}

% "Chapters" are sections of the Dossier (tabs)
\renewcommand*{\thechapter}{\Roman{chapter}}
\setcounter{tocdepth}{1}

% Eliminate header on first page of each chapter
\fancypagestyle{plain}{%
    \fancyhead{}%
    \renewcommand{\headrulewidth}{0pt}%
}

%% Chapter definitions

% This resets the page counter every chapter and numbers IV-1 (etc.)
\iflong@form\renewcommand{\thepage}{\thechapter.\arabic{page}}\fi
\let\old@tableofcontents\tableofcontents
\renewcommand{\tableofcontents}{%
    \pagenumbering{roman}%
    \pagestyle{empty}
    \old@tableofcontents
    \cleardoublepage
    \iflong@form\renewcommand{\thepage}{\thechapter.\arabic{page}}\fi
    \pagestyle{empty}
}
\renewcommand\chapter{%
  % normally we would increment the chapter counter first, but since I am not
  % redefining \@chapter and I don't want to mess it up....
  % TODO: this should work for the first chapter too, but without messing
  % up the table of contents!
%  \ifnum\value{chapter}>0
%%    \expandafter\label{lastpage\the\numexpr\value{chapter}+1\relax}
%    \expandafter\label{lastpage\thechapter}
%  \fi
    \if@openright\cleardoublepage\else\clearpage\fi
    \pagestyle{fancy}%
    \setcounter{page}{1}%
%    \renewcommand{\headrulewidth}{0.0pt}
    \renewcommand{\footrulewidth}{0.5pt}
    \thispagestyle{plain}%
    \global\@topnum\z@
    \@afterindentfalse
    \secdef\@chapter\@schapter
}
\def\@makechapterhead#1{%
  \lhead{\small\scshape\@author}%
  \lfoot{\small\scshape\@date}%
  \rfoot{\small \thepage}%
  \cfoot{}%
  \rhead{\small\scshape\thechapter.~#1}%
  {\parindent \z@ \raggedright \normalfont
    \ifnum \c@secnumdepth >\m@ne
        \large\bfseries\thechapter\hskip 2.5ex \@plus 1ex \@minus 0.2ex%
    \fi
    \interlinepenalty\@M
    \large\bfseries #1\par\nobreak
    \vskip 10\p@
  }
}
\def\@makeschapterhead#1{%
  \lhead{\small\scshape\@author}%
  \lfoot{\small\scshape\@date}%
  \rfoot{\small \thepage}%
  \thispagestyle{empty}
  \cfoot{}%
  \rhead{\small\scshape #1}%
  {\parindent \z@ \raggedright
    \normalfont
    \interlinepenalty\@M
    \large\bfseries #1\par\nobreak
    \vskip 10\p@
  }%
}
\renewcommand*\l@chapter[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \vskip 1.0em \@plus\p@
    \setlength\@tempdima{2.5em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \leavevmode \bfseries
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      %#1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
      #1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss}\par
      \penalty\@highpenalty
    \endgroup
  \fi}

% Redefine addcontentsline so only the page number (not the chapter) is printed
% in the table of contents
\AtBeginDocument{%
  \@ifpackageloaded{hyperref}{%
     % Only one line of this changes (part about \contentsline)
     \def\addcontentsline#1#2#3{% toc extension, type, tag
       \begingroup
         \let\label\@gobble
         \ifx\@currentHref\@empty
           \Hy@Warning{%
             No destination for bookmark of \string\addcontentsline,%
             \MessageBreak destination is added%
           }%
           \phantomsection
         \fi
         \expandafter\ifx\csname toclevel@#2\endcsname\relax
           \begingroup
             \def\Hy@tempa{#1}%
             \ifx\Hy@tempa\Hy@bookmarkstype
               \Hy@WarningNoLine{%
                 bookmark level for unknown #2 defaults to 0%
               }%
             \else
               \Hy@Info{bookmark level for unknown #2 defaults to 0}%
             \fi
           \endgroup
           \expandafter\gdef\csname toclevel@#2\endcsname{0}%
         \fi
         \edef\Hy@toclevel{\csname toclevel@#2\endcsname}%
         \Hy@writebookmark{\csname the#2\endcsname}%
           {#3}%
           {\@currentHref}%
           {\Hy@toclevel}%
           {#1}%
         \ifHy@verbose
           \begingroup
             \def\Hy@tempa{#3}%
             \@onelevel@sanitize\Hy@tempa
             \let\temp@online\on@line
             \let\on@line\@empty
             \Hy@Info{%
               bookmark\temp@online:\MessageBreak
               thecounter {\csname the#2\endcsname}\MessageBreak
               text {\Hy@tempa}\MessageBreak
               reference {\@currentHref}\MessageBreak
               toclevel {\Hy@toclevel}\MessageBreak
               type {#1}%
             }%
           \endgroup
         \fi
         \addtocontents{#1}{%
           % The only change is here (\thepage -> \arabic{page})
           \protect\contentsline{#2}{#3}{\arabic{page}}{\@currentHref}%
         }%
       \endgroup
     }
  }{%
    \renewcommand*{\addcontentsline}[3]{%
      \addtocontents{#1}{\protect\contentsline{#2}{#3}{\arabic{page}}}}
  }
}

% Change separation between dots in Contents
\renewcommand*{\@dotsep}{4.5}

% Header for CV and related information
\newcommand{\highestdegree}[1]{\gdef\highest@degree{#1}}
\newcommand{\rank}[1]{\gdef\@rank{#1}}
\newcommand{\department}[1]{\gdef\@department{#1}}
\newcommand{\school}[1]{\gdef\@school{#1}}
\newcommand{\office}[1]{\gdef\@office{#1}}
\newcommand{\address}[1]{\gdef\@address{#1}}
\newcommand{\phone}[1]{\gdef\@phone{#1}}
\newcommand{\email}[1]{\gdef\@email{#1}}
\newcommand{\makeCVtitle}{%
  \hbox{}\hfill\textbf{\iflong@form\else\Large\fi\@author, \highest@degree}\hfill\hbox{}\\[0.25\baselineskip]
  \textit{\@rank, Department of \@department, \@school, \@office, \@address ;
    \@phone ; \@email
  }
  \vskip 2ex%
}

\newenvironment{education}
    {\subsection{Education}\par
     \vskip -1.0ex%
     \setlength{\parskip}{0.25\baselineskip}
     \leftskip 2.5em%
     \setlength{\parindent}{-2.5em}%
    }{}

\newenvironment{experience}%
    {%\subsection{Professional Experience}%
     \renewcommand*\descriptionlabel[1]{\hspace\labelsep
                              \normalfont ##1}%
     \begin{description}%
     \let\olditem\item
     \renewcommand{\item}[2][]{\olditem [##1] \textbf{##2},}
    }
    {\let\item\olditem
     \end{description}}

\newenvironment{courselist}[1]%
    {\nopagebreak\par\noindent
%     \begin{minipage}{\linewidth}
     \vbox{}%
%     \vspace{-0.75ex}%
     \hspace{2.0em}#1
     \begin{list}{}{%
        \@beginparpenalty\@highpenalty%
        \setlength{\leftmargin}{6.0em}%
        \setlength{\topsep}{0pt}%
        \setlength{\itemsep}{0pt}%
        \setlength{\parsep}{0pt}%
        \setlength{\parskip}{0pt}%
        \setlength{\itemindent}{-2.0em}%
     }%
    }{\end{list}%\end{minipage}
      \par%\vspace{2pt}%
    }

\newenvironment{grantlist}
    {\begin{revnumerate}
      \setlength{\itemindent}{-1.3em}%
      \setlength{\leftskip}{1.3em}% thank you, http://www.wkiri.com/today/?p=76
      \setlength{\listparindent}{-1.3em}%
      \setlength{\parindent}{\listparindent}%
    }
    {\end{revnumerate}}

\newenvironment{role}
    {\begin{trivlist}%
      \vspace{-1.70ex}%
      \setlength{\itemindent}{-1.3em}%
      \setlength{\leftskip}{1.3em}% thank you, http://www.wkiri.com/today/?p=76
      \setlength{\listparindent}{-1.3em}%
      \setlength{\parindent}{\listparindent}%
      \item}
    {\vspace{-1.70ex}\relax
     \end{trivlist}\relax}

\newsavebox{\trash}%
\newenvironment{longformonly}%
    {\iflong@form\else\begin{lrbox}{\trash}\begin{minipage}{\textwidth}\mbox{}\fi}%
    {\iflong@form\else\end{minipage}\end{lrbox}\fi}

\newenvironment{notonshortform}%
    {\ifshort@form\begin{lrbox}{\trash}\begin{minipage}{\textwidth}\mbox{}\fi}%
    {\ifshort@form\end{minipage}\end{lrbox}\fi}

\newenvironment{notonlongform}%
    {\iflong@form\begin{lrbox}{\trash}\begin{minipage}{\textwidth}\mbox{}\fi}%
    {\iflong@form\end{minipage}\end{lrbox}\fi}

\clubpenalty=10000
\widowpenalty=10000

%%% Tweak list separations %%
\newenvironment{CVitemize}{%
    \begin{itemize}\itemsep\z@ plus 0.25ex\interlinepenalty=1000\relax}{\end{itemize}}
\newenvironment{CVenumerate}{%
    \begin{enumerate}\itemsep\z@ plus 0.25ex\interlinepenalty=1000\relax}{\end{enumerate}}
\newenvironment{CVrevnumerate}[1][-1]{%
    \begin{revnumerate}[#1]\itemsep\z@ plus 0.25ex\interlinepenalty=1000\relax}{\end{revnumerate}}
