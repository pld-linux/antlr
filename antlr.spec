Summary:	ANother Tool for Language Recognition
Summary(pl):	TODO
Name:		antlr
Version:	2.7.2
Release:	1
License:	Public Domain
Group:		Development/Tools
Source0:	http://www.antlr.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	d67ffcaba6b2cedd99601b9052f63957
Patch0:		%{name}-classpath.patch
URL:		http://www.antlr.org/
BuildRequires:	jar
Conflicts:	pccts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ANTLR, ANother Tool for Language Recognition, (formerly PCCTS) is a language
tool that provides a framework for constructing recognizers, compilers, and
translators from grammatical descriptions containing Java, C#, or C++ actions.
ANTLR is popular because it is easy to understand, powerful, flexible,
generates human-readable output, and comes with complete source. ANTLR provides
excellent support for tree construction, tree walking, and translation. 

%description -l pl
TODO.

%prep
%setup -q
%patch0 -p1

%build

export CLASSPATH=$RPM_BUILD_DIR/%{name}-%{version}/antlr.jar

%configure

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
%{_includedir}/%{name}
%{_libdir}/libantlr.a
%{_datadir}/%{name}-%{version}
