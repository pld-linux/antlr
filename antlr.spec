# TODO:
#  *  add python bcond
#  *  add an axamples subpackage (and python-examples as well)
#
# Conditional build:
%bcond_without	gcj	# use javac instead of GCJ
%bcond_without	dotnet	# don't build .NET modules
#
%{?with_dotnet:%include	/usr/lib/rpm/macros.mono}
#
Summary:	ANother Tool for Language Recognition
Summary(pl):	Jeszcze jedno narz�dzie do rozpoznawania j�zyka
Name:		antlr
Version:	2.7.5
Release:	4.1
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
%{?with_dotnet:BuildRequires:	mono-csharp}
Conflicts:	pccts < 1.33MR33-6
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ANTLR, ANother Tool for Language Recognition, (formerly PCCTS) is a
language tool that provides a framework for constructing recognizers,
compilers, and translators from grammatical descriptions containing
Java, C#, or C++ actions. ANTLR is popular because it is easy to
understand, powerful, flexible, generates human-readable output, and
comes with complete source. ANTLR provides excellent support for tree
construction, tree walking, and translation.

%description -l pl
ANTLR (ANother Tool for Language Recognition; poprzednio znane jako
PCCTS) to narz�dzie j�zykowe dostarczaj�ce szkielet do tworzenia
program�w rozpoznaj�cych j�zyki, kompilator�w, translator�w z opis�w
gramatycznych obejmuj�cych Jav�, C# lub C++. ANTLR jest popularne
poniewa� jest �atwe do zrozumienia, pot�ne, elastyczne, generuje
wyj�cie czytelne dla cz�owieka i jest dost�pne z pe�nymi �r�d�ami.
ANTLR ma �wietne wsparcie dla tworzenia drzew, przechodzenia po
drzewach oraz translacji.

%package -n dotnet-antlr
Summary:	.NET support for ANTLR
Summary(pl):	Modu�y j�zyka .NET dla biblioteki ANTLR
Group:		Libraries

%description -n dotnet-antlr
.NET support for ANTLR.

%description -n dotnet-antlr -l pl
Modu�y j�zyka .NET dla biblioteki ANTLR.

%package -n python-antlr
Summary:	Python support for ANTLR
Summary(pl):	Modu�y j�zyka Python dla biblioteki ANTLR
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-antlr
Python support for ANTLR.

%description -n python-antlr -l pl
Modu�y j�zyka Python dla biblioteki ANTLR.

%package examples
Summary:	Examples of ANTLR usage
Summary(pl):	Przyk�adowe programy u�ywaj�ce ANTLR
Group:		Development
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description examples
Examples of ANTLR usage.

%description examples -l pl
Przyk�adowe programy u�ywaj�ce ANTLR.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub scripts

%configure \
	--enable-cxx \
	%{?with_dotnet:--enable-csharp} \
	%{!?with_gcj:CLASSPATH=`pwd` --with-javac=javac} \
	%{?with_gcj:--with-javac=gcj --with-jar=fastjar}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{py_sitescriptdir}/%{name},%{_prefix}/lib/mono/%{name},%{_examplesdir}/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/antlr.jar \
	$RPM_BUILD_ROOT%{_javadir}
install $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/*.py \
	$RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}
cp -Rf examples/{cpp,csharp,java,python} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name} -name Makefile -exec rm -f {} \;

%{?with_dotnet:install lib/*.dll $RPM_BUILD_ROOT%{_prefix}/lib/mono/%{name}}

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}
rm $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}/*.py

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

%if %{with dotnet}
%files -n dotnet-antlr
%defattr(644,root,root,755)
%{_prefix}/lib/mono/%{name}/*.dll
%endif

%files -n python-antlr
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{name}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}
