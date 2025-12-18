# rpmbuild tries to run perl in /opt/nec/ve/bin/ and fails to get the perl version.
# To avoid this, specify the path to perl in the spec file.
%global __perl /usr/bin/perl
%define _prefix /opt/nec/ve/veos
%define _localstatedir /var/opt/nec/ve/veos
%define _sysconfdir  /etc/opt/nec
%define _ve_prefix  /opt/nec/ve

Name: veosinfo3
Version: 3.6.0
Release: 1%{?dist}
Summary: RPM library to interact with VEOS and VE specific 'sysfs'
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
Vendor:	NEC Corporation
BuildArch: x86_64
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: veos
Requires: libyaml

BuildRequires: log4c-devel
BuildRequires: systemd-devel
BuildRequires: veos >= 2.11
BuildRequires: veos-devel >= 2.11
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: protobuf-c
BuildRequires: protobuf-c-devel
BuildRequires: libyaml
BuildRequires: libyaml-devel
BuildRequires: libgudev1

%description
This library is responsible for interacting with 
VEOS and VE specific 'sysfs' to retrieve command
specific information.

%package devel
Summary: Development files for RPM library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Provides: %{_prefix}/include/veosinfo.h
Conflicts: veosinfo-devel

%description devel
Header files for the RPM Library.

%prep
%setup -q -n %{name}-%{version}

%build
./autogen.sh
%configure --prefix=%{_prefix} --localstatedir=%{_localstatedir} --sysconfdir=%{_sysconfdir} --with-ve-prefix=%{_ve_prefix}

make CFLAGS="%{optflags} $CFLAGS"

%install
make DESTDIR=%{buildroot} install
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libveosinfo.so.*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
