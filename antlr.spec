# TODO:
#  - add python bcond
#  - package the Emacs and Jedit modes
#    %{_datadir}/%{name}-%{version}/antlr-jedit.xml
#    %{_datadir}/%{name}-%{version}/antlr-mode.el
#
# NOTE:
#  - next version is packaged as antlr3.spec. Please, do not upgrade this spec
#    to 3.
#
# Conditional build:
%bcond_with	gcj	# use GCJ instead of javac
%bcond_without	dotnet	# don't build .NET modules
%bcond_without	java	# don't build Java at all
#
%{?with_dotnet:%include	/usr/lib/rpm/macros.mono}
#
%ifarch x32
%undefine	with_dotnet
%endif
#
Summary:	ANother Tool for Language Recognition
Summary(pl.UTF-8):	Jeszcze jedno narzędzie do rozpoznawania języka
Name:		antlr
Version:	2.7.7
Release:	14
License:	Public Domain
Group:		Development/Tools
Source0:	http://www.antlr2.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	01cc9a2a454dd33dcd8c856ec89af090
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-strcasecmp.patch
Patch2:		%{name}-gentoo.patch
URL:		http://www.antlr2.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
%{?with_dotnet:BuildRequires:	mono-csharp}
BuildRequires:	python
BuildRequires:	sed >= 4.0
%if %{with java}
%if %{with gcj}
BuildRequires:	java-gcj-compat-devel
%else
BuildRequires:	jar
BuildRequires:	jdk
Requires:	jpackage-utils
%endif
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

%description -l pl.UTF-8
ANTLR (ANother Tool for Language Recognition; poprzednio znane jako
PCCTS) to narzędzie językowe dostarczające szkielet do tworzenia
programów rozpoznających języki, kompilatorów, translatorów z opisów
gramatycznych obejmujących Javę, C# lub C++. ANTLR jest popularne
ponieważ jest łatwe do zrozumienia, potężne, elastyczne, generuje
wyjście czytelne dla człowieka i jest dostępne z pełnymi źródłami.
ANTLR ma świetne wsparcie dla tworzenia drzew, przechodzenia po
drzewach oraz translacji.

%package -n dotnet-antlr
Summary:	.NET support for ANTLR
Summary(pl.UTF-8):	Moduły języka .NET dla biblioteki ANTLR
Group:		Libraries

%description -n dotnet-antlr
.NET support for ANTLR.

%description -n dotnet-antlr -l pl.UTF-8
Moduły języka .NET dla biblioteki ANTLR.

%package -n python-antlr
Summary:	Python runtime support for ANTLR-generated parsers
Summary(pl.UTF-8):	Moduł uruchomieniowy języka Python dla analizatorów ANTLR
Group:		Libraries/Python
%pyrequires_eq	python-libs

%description -n python-antlr
Python runtime support for ANTLR-generated parsers.

%description -n python-antlr -l pl.UTF-8
Moduł uruchomieniowy języka Python dla analizatorów wygenerowanych
przez ANTLR.

%package examples
Summary:	Examples of ANTLR usage
Summary(pl.UTF-8):	Przykładowe programy używające ANTLR
Group:		Development
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description examples
Examples of ANTLR usage.

%description examples -l pl.UTF-8
Przykładowe programy używające ANTLR.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.sub scripts
%{__autoconf}
%configure \
	%{?with_dotnet:CSHARPC=/usr/bin/mcs --enable-csharp} \
	%{!?with_dotnet:--disable-csharp} \
	--enable-cxx \
	%{?with_java:CLASSPATH=`pwd` --with-java=java --with-javac=javac --with-jar=jar} \
	%{!?with_java:--disable-java} \

CXXFLAGS="%{rpmcxxflags}" \
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{py_sitescriptdir}/%{name},%{_prefix}/lib/mono/%{name},%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/*.py \
	$RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/antlr.py
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}
# module installer
%{__rm} $RPM_BUILD_ROOT%{_sbindir}/pyantlr.sh

%if %{with java}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/antlr.jar \
	$RPM_BUILD_ROOT%{_javadir}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/antlr.jar
%endif
%{__sed} -i -e "s,ANTLR_JAR=.*,ANTLR_JAR=\"%{_javadir}/antlr.jar\",g" $RPM_BUILD_ROOT%{_bindir}/antlr

%if %{with dotnet}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/*.dll $RPM_BUILD_ROOT%{_prefix}/lib/mono/%{name}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/antlr.*.dll
%endif

cp -Rf examples/{cpp,csharp,java,python} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} -name Makefile -exec rm -f {} \;

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.{html,gif,jpg}
%attr(755,root,root) %{_bindir}/antlr
%attr(755,root,root) %{_bindir}/antlr-config
%{_includedir}/%{name}
%{_libdir}/libantlr.a
# Don't separate it, antlr binary won't work without it
%if %{with java}
%{_javadir}/antlr.jar
%endif

%if %{with dotnet}
%files -n dotnet-antlr
%defattr(644,root,root,755)
%dir %{_prefix}/lib/mono/%{name}
%{_prefix}/lib/mono/%{name}/antlr.astframe.dll
%{_prefix}/lib/mono/%{name}/antlr.runtime.dll
%endif

%files -n python-antlr
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{name}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
