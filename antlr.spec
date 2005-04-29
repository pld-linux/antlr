# TODO: 
#  *  Add a csharp bindings subpackage (feel free to do it)
#  *  Package the python bindings as subpackage as well
#
# Conditional build:
%bcond_without	gcj	# use javac instead of GCJ
#
Summary:	ANother Tool for Language Recognition
Summary(pl):	Jeszcze jedno narzêdzie do rozpoznawania jêzyka
Name:		antlr
Version:	2.7.5
Release:	4
License:	Public Domain
Group:		Development/Tools
Source0:	http://www.antlr.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	1ef201f29283179c8e5ab618529cac78
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-remove-ugly-gcj-hack.patch
URL:		http://www.antlr.org/
BuildRequires:	automake
%if %{with gcj}
BuildRequires:	gcc-java >= 5:4.0.0
BuildRequires:	gcc-java-tools >= 5:4.0.0
Requires:	/usr/bin/gij
%else
BuildRequires:	jar
BuildRequires:	jdk
Requires:	jre
%endif
Conflicts:	pccts < 1.33MR33-6
BuildRequires:	sed >= 4.0
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
wyj¶cie czytelne dla cz³owieka i jest dostêpne z pe³nymi ¼ród³ami.
ANTLR ma ¶wietne wsparcie dla tworzenia drzew, przechodzenia po
drzewach oraz translacji.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub scripts

%configure \
	%{!?with_gcj:CLASSPATH=`pwd` --with-javac=javac} \
	%{?with_gcj:--with-javac=gcj --with-jar=fastjar}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/antlr.jar \
	$RPM_BUILD_ROOT%{_javadir}

%{__sed} -i -e "s,ANTLR_JAR=.*,ANTLR_JAR=\"%{_javadir}/antlr.jar\",g" $RPM_BUILD_ROOT%{_bindir}/antlr

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/antlr
%attr(755,root,root) %{_bindir}/antlr-config
%{_includedir}/%{name}
%{_libdir}/libantlr.a
# Dont separate it, antlr binary wont work without it
%{_javadir}/*.jar
