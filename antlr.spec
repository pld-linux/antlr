# TODO: Move antlr-java to separate package ?

Summary:	ANother Tool for Language Recognition
Summary(pl):	Jeszcze jedno narz�dzie do rozpoznawania j�zyka
Name:		antlr
Version:	2.7.4
Release:	1
License:	Public Domain
Group:		Development/Tools
Source0:	http://www.antlr.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	33df7cdc8e80447cdd78607c76f02bac
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
PCCTS) to narz�dzie j�zykowe dostarczaj�ce szkielet do tworzenia
program�w rozpoznaj�cych j�zyki, kompilator�w, translator�w z opis�w
gramatycznych obejmuj�cych Jav�, C# lub C++. ANTLR jest popularne
poniewa� jest �atwe do zrozumienia, pot�ne, elastyczne, generuje
wyj�cie czytelne dla cz�owieka i jest dost�pne z pe�nymi �r�d�ami.
ANTLR ma �wietne wsparcie dla tworzenia drzew, przechodzenia po
drzewach oraz translacji.

%prep
%setup -q

%build
#export CLASSPATH=$RPM_BUILD_DIR/%{name}-%{version}

cp /usr/share/automake/config.sub scripts

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
%doc doc/*
%attr(755,root,root) %{_bindir}/antlr
%attr(755,root,root) %{_bindir}/antlr-config
%attr(755,root,root) %{_bindir}/antlr-java
%{_includedir}/%{name}
%{_libdir}/libantlr.a
%{_datadir}/%{name}-2.7.3
