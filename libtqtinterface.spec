# TODO
# - for some unknown reason to me it creates dead symlinks instead of libtqt shared library
#   libtool: install: /usr/bin/install -c -p .libs/libtqt.so.4.2.0 /tmp/xxx/usr/lib64/libtqt.so.4.2.0
#   /usr/bin/install: cannot stat `.libs/libtqt.so.4.2.0': No such file or directory
#
# Conditional build:
%bcond_with		qt4     # Enable Qt4 support (this will disable all Qt3 support)

Summary:	Interface and abstraction library for Qt and Trinity
Name:		libtqtinterface
Version:	3.5.12
Release:	0.1
License:	GPL v2
Group:		X11/Libraries
Source0:	http://mirror.its.uidaho.edu/pub/trinity/releases/%{version}/dependencies/tqtinterface-%{version}.tar.gz
# Source0-md5:	361c45961184f01f95d3b771138c8229
URL:		http://trinity.pearsoncomputing.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	qt-devel
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

%prep
%setup -qc
mv dependencies/tqtinterface/* .

%build
cp -p /usr/share/automake/config.sub admin
cp -p %{_aclocaldir}/libtool.m4 admin/libtool.m4.in
cp -p %{_datadir}/libtool/config/ltmain.sh admin/ltmain.sh
%{__make} -f admin/Makefile.common cvs

%configure \
	--%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
	--disable-final \
	--enable-closure \
%if "%{_lib}" == "lib64"
	--enable-libsuffix=64 \
%endif
	--%{!?with_qt4:dis}%{?with_qt4:en}able-qt4

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
