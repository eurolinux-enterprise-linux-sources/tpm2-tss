Name:           tpm2-tss
Version:        1.4.0
Release:        2%{?dist}
Summary:        TPM2.0 Software Stack

# The entire source code is under BSD except implementation.h and tpmb.h which
# is under TCGL(Trusted Computing Group License).
License:        BSD and TCGL
URL:            https://github.com/tpm2-software/tpm2-tss
Source0:        https://github.com/tpm2-software/tpm2-tss/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        60-tpm-udev.rules

Patch0:         autoconf-fixup.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  autoconf-archive
BuildRequires:  libtool
BuildRequires:  pkgconfig

Obsoletes:  %{name}-utils <= 1.1.0-1
# udev rules moved from tpm2-abrmd package
Conflicts:  tpm2-abrmd%{?_isa} <= 1.1.0-8%{?dist}

# this package does not support big endian arch so far,
# and has been verified only on Intel platforms.
ExclusiveArch: %{ix86} x86_64

%description
tpm2-tss is a software stack supporting Trusted Platform Module(TPM) 2.0 system
APIs. It sits between TPM driver and applications, providing TPM2.0 specified
APIs for applications to access TPM module through kernel TPM drivers.

%prep
%autosetup -p1 -n %{name}-%{version}
./bootstrap


%build
%configure --disable-static --disable-silent-rules
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -type f -name \*.la -delete

mkdir -p %{buildroot}%{_udevrulesdir}
install -m 0644 -D -t %{buildroot}/%{_udevrulesdir}/ %{SOURCE1}

%clean
rm -rf %{buildroot}

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{_libdir}/libsapi.so.*
%{_libdir}/libtcti-device.so.*
%{_libdir}/libtcti-socket.so.*
%{_udevrulesdir}/60-tpm-udev.rules

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
%{_mandir}/man3/Init*Tcti.3.gz
%{_mandir}/man7/tcti-*.7.gz

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Thu Sep 06 2018 Jerry Snitselaar <jsnitsel@redhat.com> - 1.4.0-2
- Add conflict for older tpm2-abrmd versions due to udev rules move.
resolves: rhbz#1626069

* Fri Jun 15 2018 Jerry Snitselaar <jsnitsel@redhat.com> - 1.4.0-1
- Rebase to 1.4.0 release
resolves: rhbz#1515116

* Thu Dec 14 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 1.3.0-2
- Fix package version in autoconf
resolves: rhbz#1463097

* Wed Dec 13 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 1.3.0-1
- Rebase to 1.3.0 release
resolves: rhbz#1463097

* Thu Aug 31 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 1.1.0-1
- Rebase to 1.1.0
resolves: rhbz#1463097

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
