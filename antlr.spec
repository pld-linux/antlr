# TODO: Move antlr-java to separate package ?

%define		_snap	20030911

Summary:	ANother Tool for Language Recognition
Summary(pl):	Jeszcze jedno narzêdzie do rozpoznawania jêzyka
Name:		antlr
Version:	2.7.3
Release:	0.%{_snap}.5
License:	Public Domain
Group:		Development/Tools
#Source0:	http://www.antlr.org/download/%{name}-%{version}.tar.gz
#Source0:	http://wwwhome.cs.utwente.nl/~klaren/antlr/%{name}-%{_snap}.tar.gz
Source0:	%{name}-%{_snap}.tar.gz
# Source0-md5:	de00ded0f1922587bb24628152fc3f62
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-runscript.patch
URL:		http://www.antlr.org/
BuildRequires:	gcc-java
BuildRequires:	gcc-java-tools
# BuildRequires:	jar
# BuildRequires:	jdk
# Requires:	jre
Conflicts:	pccts < 1.33MR33-6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ANTLR, ANother Tool for Language Recognition, (formerly PCCTS) is a language
tool that provides a framework for constructing recognizers, compilers, and
translators from grammatical descriptions containing Java, C#, or C++ actions.
ANTLR is popular because it is easy to understand, powerful, flexible,
generates human-readable output, and comes with complete source. ANTLR provides
excellent support for tree construction, tree walking, and translation. 

%description -l pl
ANTLR (ANother Tool for Language Recognition; poprzednio znane jako
PCCTS) to narzêdzie jêzykowe dostarczaj±ce szkielet do tworzenia
programów rozpoznaj±cych jêzyki, kompilatorów, translatorów z opisów
gramatycznych obejmuj±cych Javê, C# lub C++. ANTLR jest popularne
poniewa¿ jest ³atwe do zrozumienia, potê¿ne, elastyczne, generuje
wyj¶cie czytelne dla cz³owieka i jset dostêpne z pe³nymi ¼ród³ami.
ANTLR ma ¶wietne wsparcie dla tworzenia drzew, przechodzenia po
drzewach oraz translacji.

%prep
%setup -q -n %{name}-%{_snap}
%patch0 -p1
%patch1 -p1

%build
export CLASSPATH=$RPM_BUILD_DIR/%{name}-%{_snap}

%configure \
    --enable-gcj

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc RIGHTS
%attr(755,root,root) %{_bindir}/antlr
%attr(755,root,root) %{_bindir}/antlr-config
#%%attr(755,root,root) %{_bindir}/antlr-java
%{_includedir}/%{name}
%{_libdir}/libantlr.a
%{_datadir}/%{name}-%{version}
