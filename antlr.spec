# TODO: 
#  *  Add a csharp bindings subpacakge (feel free to do it)
#  *  Package the python bindings as subpackage as well
#
# Conditional build:
%bcond_with	javac	# use javac instead of gcj
#
Summary:	ANother Tool for Language Recognition
Summary(pl):	Jeszcze jedno narz�dzie do rozpoznawania j�zyka
Name:		antlr
Version:	2.7.5
Release:	2
License:	Public Domain
Group:		Development/Tools
Source0:	http://www.antlr.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	1ef201f29283179c8e5ab618529cac78
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.antlr.org/
BuildRequires:	automake
%if !%{with javac}
BuildRequires:	gcc-java
BuildRequires:	gcc-java-tools
%else
BuildRequires:	jar
BuildRequires:	jdk
Requires:	jre
%endif
Conflicts:	pccts < 1.33MR33-6
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	%{_datadir}/java

%description
ANTLR, ANother Tool for Language Recognition, (formerly PCCTS) is a language
tool that provides a framework for constructing recognizers, compilers, and
translators from grammatical descriptions containing Java, C#, or C++ actions.
ANTLR is popular because it is easy to understand, powerful, flexible,
generates human-readable output, and comes with complete source. ANTLR provides
excellent support for tree construction, tree walking, and translation. 

%description -l pl
ANTLR (ANother Tool for Language Recognition; poprzednio znane jako
PCCTS) to narz�dzie j�zykowe dostarczaj�ce szkielet do tworzenia
program�w rozpoznaj�cych j�zyki, kompilator�w, translator�w z opis�w
gramatycznych obejmuj�cych Jav�, C# lub C++. ANTLR jest popularne
poniewa� jest �atwe do zrozumienia, pot�ne, elastyczne, generuje
wyj�cie czytelne dla cz�owieka i jest dost�pne z pe�nymi �r�d�ami.
ANTLR ma �wietne wsparcie dla tworzenia drzew, przechodzenia po
drzewach oraz translacji.

%prep
%setup -q
%patch0 -p1 

%build
#export CLASSPATH=$RPM_BUILD_DIR/%{name}-%{version}

cp -f /usr/share/automake/config.sub scripts

%configure \
	%{?with_javac:CLASSPATH=`pwd` --with-javac=javac} \
	%{!?with_javac:--with-javac=gcj}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javalibdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/antlr.jar $RPM_BUILD_ROOT%{_javalibdir}

%{__sed} -i -e "s,ANTLR_JAR=.*,ANTLR_JAR=\"%{_javalibdir}/antlr.jar\",g" $RPM_BUILD_ROOT%{_bindir}/antlr

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
%{_javalibdir}/*.jar
