# TODO: Move antlr-java to separate package ?
#
# Conditional build:
%bcond_with	javac	# use javac instead of gcj
#
Summary:	ANother Tool for Language Recognition
Summary(pl):	Jeszcze jedno narzêdzie do rozpoznawania jêzyka
Name:		antlr
Version:	2.7.4
Release:	2
License:	Public Domain
Group:		Development/Tools
Source0:	http://www.antlr.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	33df7cdc8e80447cdd78607c76f02bac
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
PCCTS) to narzêdzie jêzykowe dostarczaj±ce szkielet do tworzenia
programów rozpoznaj±cych jêzyki, kompilatorów, translatorów z opisów
gramatycznych obejmuj±cych Javê, C# lub C++. ANTLR jest popularne
poniewa¿ jest ³atwe do zrozumienia, potê¿ne, elastyczne, generuje
wyj¶cie czytelne dla cz³owieka i jest dostêpne z pe³nymi ¼ród³ami.
ANTLR ma ¶wietne wsparcie dla tworzenia drzew, przechodzenia po
drzewach oraz translacji.

%prep
%setup -q

%build
#export CLASSPATH=$RPM_BUILD_DIR/%{name}-%{version}

cp -f /usr/share/automake/config.sub scripts

%configure \
	%{?with_javac:CLASSPATH=`pwd`} \
	%{!?with_javac:--enable-gcj}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javalibdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/%{name}-2.7.3/antlr.jar $RPM_BUILD_ROOT%{_javalibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/antlr
%attr(755,root,root) %{_bindir}/antlr-config
%{!?with_javac:%attr(755,root,root) %{_bindir}/antlr-java}
%{_includedir}/%{name}
%{_libdir}/libantlr.a
%{_javalibdir}/*.jar
