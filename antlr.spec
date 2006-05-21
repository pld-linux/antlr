%include /usr/lib/rpm/macros.java
# TODO: 
#  *  Add a csharp bindings subpacakge (feel free to do it)
#  *  Package the Emacs an Jedit modes
#
# Conditional build:
%bcond_with	javac	# use javac instead of gcj
#
Summary:	ANother Tool for Language Recognition
Summary(pl):	Jeszcze jedno narzêdzie do rozpoznawania jêzyka
Name:		antlr
Version:	2.7.5
Release:	3
License:	Public Domain
Group:		Development/Tools
Source0:	http://www.antlr.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	1ef201f29283179c8e5ab618529cac78
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.antlr.org/
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	python
%if !%{with javac}
BuildRequires:	gcc-java
BuildRequires:	jar
# gij is in gcc-java in Ac
Requires:	gcc-java
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

%package -n python-%{name}
Summary:	ANTLR runtime library for Python
Group:		Libraries/Python
%pyrequires_eq	python-modules

%description -n python-%{name}
ANTLR (ANother Tool for Language Recognition) runtime library for Python.

%prep
%setup -q
%patch0 -p1 

%build
unset CLASSPATH || :
unset JAVA_HOME || :

%{?with_javac:export JAVA_HOME=%{java_home}}

cp -f /usr/share/automake/config.sub scripts

%configure \
	%{?with_javac:CLASSPATH=`pwd` --with-javac=javac} \
	%{!?with_javac:--with-javac=gcj}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{py_sitescriptdir}/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/antlr.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

%{__sed} -i -e "s,ANTLR_JAR=.*,ANTLR_JAR=\"%{_javadir}/antlr-%{version}.jar\",g" $RPM_BUILD_ROOT%{_bindir}/antlr

mv $RPM_BUILD_ROOT{%{_datadir}/%{name}-%{version}/*.py,%{py_sitescriptdir}/%{name}}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}
rm -f $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}/*.py

rm -f $RPM_BUILD_ROOT%{_sbindir}/pyantlr.sh
rm -f $RPM_BUILD_ROOT%{_libdir}/antlr*

# TODO: install where Emacs and JEdit will look for that
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/*.{xml,el}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/antlr
%attr(755,root,root) %{_bindir}/antlr-config
%{_includedir}/%{name}
%{_libdir}/libantlr.a
%{_datadir}/%{name}*
# Don't separate it, antlr binary won't work without it
%{_javadir}/*.jar

%files -n python-%{name}
%{py_sitescriptdir}/%{name}
