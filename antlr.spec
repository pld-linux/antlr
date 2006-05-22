# TODO:
#  *  update java stuff
#  *  add python bcond
#  *  package the Emacs and Jedit modes
#
# Conditional build:
%bcond_without	gcj	# use javac instead of GCJ
%bcond_without	dotnet	# don't build .NET modules
#
%{?with_dotnet:%include	/usr/lib/rpm/macros.mono}
#
Summary:	ANother Tool for Language Recognition
Summary(pl):	Jeszcze jedno narzêdzie do rozpoznawania jêzyka
Name:		antlr
Version:	2.7.6
Release:	0.9
License:	Public Domain
Group:		Development/Tools
Source0:	http://www.antlr.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	17d8bf2e814f0a26631aadbbda8d7324
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-csharp.patch
URL:		http://www.antlr.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
%{?with_dotnet:BuildRequires:	mono-csharp}
BuildRequires:	python
BuildRequires:	sed >= 4.0
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
PCCTS) to narzêdzie jêzykowe dostarczaj±ce szkielet do tworzenia
programów rozpoznaj±cych jêzyki, kompilatorów, translatorów z opisów
gramatycznych obejmuj±cych Javê, C# lub C++. ANTLR jest popularne
poniewa¿ jest ³atwe do zrozumienia, potê¿ne, elastyczne, generuje
wyj¶cie czytelne dla cz³owieka i jest dostêpne z pe³nymi ¼ród³ami.
ANTLR ma ¶wietne wsparcie dla tworzenia drzew, przechodzenia po
drzewach oraz translacji.

%package -n dotnet-antlr
Summary:	.NET support for ANTLR
Summary(pl):	Modu³y jêzyka .NET dla biblioteki ANTLR
Group:		Libraries

%description -n dotnet-antlr
.NET support for ANTLR.

%description -n dotnet-antlr -l pl
Modu³y jêzyka .NET dla biblioteki ANTLR.

%package -n python-antlr
Summary:	Python runtime support for ANTLR-generated parsers
Summary(pl):	Modu³ uruchomieniowy jêzyka Python dla analizatorów ANTLR
Group:		Libraries/Python
%pyrequires_eq	python-libs

%description -n python-antlr
Python runtime support for ANTLR-generated parsers.

%description -n python-antlr -l pl
Modu³ uruchomieniowy jêzyka Python dla analizatorów wygenerowanych
przez ANTLR.

%package examples
Summary:	Examples of ANTLR usage
Summary(pl):	Przyk³adowe programy u¿ywaj±ce ANTLR
Group:		Development
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description examples
Examples of ANTLR usage.

%description examples -l pl
Przyk³adowe programy u¿ywaj±ce ANTLR.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub scripts
%{__autoconf}
%configure \
	--enable-cxx \
	%{?with_dotnet:--enable-csharp} \
	%{!?with_dotnet:--disable-csharp} \
	%{!?with_gcj:CLASSPATH=`pwd` --with-java=java --with-javac=javac --with-jar=jar} \
	%{?with_gcj:--with-java=gij --with-javac=gcj --with-jar=fastjar}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{py_sitescriptdir}/%{name},%{_prefix}/lib/mono/%{name},%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/antlr.jar \
	$RPM_BUILD_ROOT%{_javadir}
install $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/*.py \
	$RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}
cp -Rf examples/{cpp,csharp,java,python} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} -name Makefile -exec rm -f {} \;

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
%{_examplesdir}/%{name}-%{version}
