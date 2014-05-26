#
# Conditional build:
%bcond_with		qt4     # Enable Qt4 support (this will disable all Qt3 support)

%define		rel	0.1
%define		svnrev		1229013
Summary:	Interface and abstraction library for Qt and Trinity
Name:		libtqtinterface
Version:	3.5.12
Release:	2.%{svnrev}.%{rel}
License:	GPL v2
Group:		X11/Libraries
#Source0:	http://mirror.its.uidaho.edu/pub/trinity/releases/%{version}/dependencies/tqtinterface-%{version}.tar.gz
Source0:	tqtinterface-%{version}-r%{svnrev}.tar.bz2
# Source0-md5:	c510477499087356ca795b78a16fb972
URL:		http://trinity.pearsoncomputing.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	qt-devel
BuildRequires:	sed >= 4.0
Obsoletes:	tqtinterface < 3.5.12-2.1229013
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package includes libraries that abstract the underlying Qt system
from the actual Trinity code, allowing easy, complete upgrades to new
versions of Qt.

It also contains various functions that have been removed from newer
versions of Qt, but are completely portable and isolated from other
APIs such as Xorg. This allows the Trinity project to efficiently
perform certain operations that are infeasible or unneccessarily
difficult when using pure Qt4 or above.

%package devel
Summary:	Header files for libtqtinterface library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libtqtinterface
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	tqtinterface-devel < 3.5.12-2.1229013

%description devel
Header files for libtqtinterface library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libtqtinterface.

%prep
%setup -qc
mv tqtinterface/* .

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DQT_VERSION=3 \
	-DQT_INCLUDE_DIR=%{_includedir}/qt \
	-DQT_LIBRARY_DIR=%{_libdir} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkgconfig
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtqt.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtqt.so.*.*.*
%ghost %attr(755,root,root) %{_libdir}/libtqt.so.4

%files devel
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_bindir}/convert_qt_tqt1
%attr(755,root,root) %{_bindir}/convert_qt_tqt2
%attr(755,root,root) %{_bindir}/convert_qt_tqt3
%attr(755,root,root) %{_bindir}/dcopidl-tqt
%attr(755,root,root) %{_bindir}/dcopidl2cpp-tqt
%attr(755,root,root) %{_bindir}/dcopidlng-tqt
%attr(755,root,root) %{_bindir}/mcopidl-tqt
%attr(755,root,root) %{_bindir}/moc-tqt
%attr(755,root,root) %{_bindir}/tmoc
%attr(755,root,root) %{_bindir}/tqt-replace
%attr(755,root,root) %{_bindir}/tqt-replace-stream
%attr(755,root,root) %{_bindir}/uic-tqt
%dir %{_includedir}/tqt
%{_includedir}/tqt/tq*.h
%dir %{_includedir}/tqt/Qt
%dir %{_includedir}/tqt/Qt/*.h
%{_pkgconfigdir}/tqt.pc
%{_libdir}/libtqt.so
