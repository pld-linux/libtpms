#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	Library providing Trusted Platform Module (TPM) functionality
Summary(pl.UTF-8):	Biblioteka zapewniająca funkcjonalność modułu TPM (Trusted Platform Module)
Name:		libtpms
Version:	0.9.4
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/stefanberger/libtpms/tags
Source0:	https://github.com/stefanberger/libtpms/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7428f3d36d5385507b69b82d0fa9d6bb
Patch0:		%{name}-x32.patch
URL:		https://github.com/stefanberger/libtpms
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1.6
BuildRequires:	libtool >= 2:2
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library providing TPM functionality for VMs. Targeted for
integration into Qemu.

%description -l pl.UTF-8
Biblioteka zapewniająca funkcjonalność TPM dla maszyn wirtualnych.
Głównym przeznaczeniem jest integracja z Qemu.

%package devel
Summary:	Header files for libtpms library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libtpms
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libtpms library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libtpms.

%package static
Summary:	Static libtpms library
Summary(pl.UTF-8):	Statyczna biblioteka libtpms
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libtpms library.

%description static -l pl.UTF-8
Statyczna biblioteka libtpms.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-openssl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# add private dependency on libcrypto if not already there
! grep -Eq '^(Requires|Libs\.private)' $RPM_BUILD_ROOT%{_pkgconfigdir}/libtpms.pc || exit 1
echo 'Libs.private: -lcrypto' >> $RPM_BUILD_ROOT%{_pkgconfigdir}/libtpms.pc

# ...to make .la file completely obsolete
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtpms.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES CREDITS LICENSE README
%attr(755,root,root) %{_libdir}/libtpms.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtpms.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtpms.so
%{_includedir}/libtpms
%{_pkgconfigdir}/libtpms.pc
%{_mandir}/man3/TPMLIB_*.3*
%{_mandir}/man3/TPM_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtpms.a
%endif
