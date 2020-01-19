Name:           tpm2-tss
Version:        1.0 
Release:        5%{?dist}
Summary:        TPM2.0 Software Stack

%global  pkg_prefix  TPM2.0-TSS

# The entire source code is under BSD except implementation.h and tpmb.h which
# is under TCGL(Trusted Computing Group License).
License:        BSD and TCGL
URL:            https://github.com/01org/TPM2.0-TSS
Source0:        https://github.com/01org/TPM2.0-TSS/archive/%{version}.tar.gz#/%{pkg_prefix}-%{version}.tar.gz
Source1:        resourcemgr.service
Source2:        resourcemgr.8

# RHEL only (resolves building on RHEL)
Patch0001: swap-pthread-check.patch
# RHEL only (enable install of test programs)
Patch0002: test-app.patch
# backport of upstream commit b0f09514467f3
Patch0003: Fix-memory-leaks-on-error-conditions-in-InitSysConte.patch
# backport of upstream commit b6ad056f2050b
Patch0004: avoid-potential-null-deref.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

# this package does not support big endian arch so far,
# and has been verified only on Intel platforms.
ExclusiveArch: %{ix86} x86_64

%description
tpm2-tss is a software stack supporting Trusted Platform Module(TPM) 2.0 system
APIs. It sits between TPM driver and applications, providing TPM2.0 specified
APIs for applications to access TPM module through kernel TPM drivers.

%prep
%autosetup -p1 -n %{pkg_prefix}-%{version}
./bootstrap


%build
%configure  --disable-static --disable-silent-rules
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -type f -name \*.la -delete
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}/
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_mandir}/man8/
install -m 0644 %{SOURCE2} %{buildroot}%{_mandir}/man8/

%clean
rm -rf %{buildroot}

%post
%systemd_post resourcemgr.service
/sbin/ldconfig

%preun
%systemd_preun resourcemgr.service

%postun
%systemd_postun resourcemgr.service
/sbin/ldconfig

%files
%doc README.md CHANGELOG.md 
%license LICENSE
%{_libdir}/libsapi.so.*
%{_libdir}/libtcti-device.so.*
%{_libdir}/libtcti-socket.so.*
%{_sbindir}/resourcemgr
%attr(644,root,root) %{_unitdir}/resourcemgr.service
%{_mandir}/man8/resourcemgr.8.gz

%package        devel
Summary:        Headers and libraries for building apps that use tpm2-tss 
Requires:       %{name}%{_isa} = %{version}-%{release}

%description    devel
This package contains headers and libraries required to build applications that
use tpm2-tss.

%files devel
%{_includedir}/sapi/
%{_includedir}/tcti/
%{_libdir}/libsapi.so
%{_libdir}/libtcti-device.so
%{_libdir}/libtcti-socket.so
%{_libdir}/pkgconfig/sapi.pc
%{_libdir}/pkgconfig/tcti-device.pc
%{_libdir}/pkgconfig/tcti-socket.pc

%package        utils
Summary:        Utilities for tpm2-tss
Requires:       %{name}%{_isa} = %{version}-%{release}

%description    utils
Utilities for tpm2-tss, such as testing features of
tpm device or simulator.

%files utils
%{_bindir}/tpmclient
%{_bindir}/tpmtest

%changelog
* Wed Jun 07 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 1.0-5
- Add manpage for resourcemgr
resolves: rhbz#1459635

* Mon Apr 03 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 1.0-4
- Clean up potential null deref
- Clean up memory leaks
- Inrease release version to 4

* Fri Mar 10 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 1.0-3
- Add systemd unit for resourcemgr
- Add utils subpackage
- Add Makefile.am patch to install test programs
- Add patch to swap out AX_PTHREAD for different check
- Increase release version to 3
resolves: rhbz#1275027 - Add TPM 2.0 System API (SAPI) library

* Mon Dec 12 2016 Sun Yunying <yunying.sun@intel.com> - 1.0-2
- Remove global macro pkg_version to avoid duplicate of version
- Use ExclusiveArch instead of ExcludeArch
- Use less wildcard in %files section to be more specific
- Add trailing slash at end of added directory in %file section
- Remove autoconf/automake/pkgconfig(cmocka) from BuildRequires
- Increase release version to 2

* Fri Dec 2 2016 Sun Yunying <yunying.sun@intel.com> - 1.0-1
- Initial version of the package
