%define debug_package %{nil}

# Package namespaces
%global ns_name ea
%global ns_dir /opt/cpanel
%global _scl_prefix %ns_dir

%scl_package %scl

# This makes the ea-php<ver>-build macro stuff work
%scl_package_override

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

# Starting with PHP 5.6, the IonCube loader needs to be loaded first
%if "%{php_version}" < "5.6"
%global inifile ioncube.ini
%else
%global inifile 01-ioncube.ini
%endif

Name:    %{?scl_prefix}php-ioncube6
Vendor:  cPanel, Inc.
Summary: Experimental v6 Loader for ionCube-encoded PHP files
Version: 6.0.4
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 3
Release: %{release_prefix}%{?dist}.cpanel
License: Redistributable
Group:   Development/Languages
URL:     http://www.ioncube.com/loaders.php

# There is a different distribution archive per architecture.  The
# archive contains the license file, so no need to have it as a
# separate source file.
Source: http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_%{archive_arch}.tar.gz

BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Provides:      %{?scl_prefix}ioncube = 6
Conflicts:     %{?scl_prefix}ioncube >= 7, %{?scl_prefix}ioncube < 6
Conflicts:     %{?scl_prefix}php-ioncube
Conflicts:     %{?scl_prefix}php-ioncube5

# Don't provide extensions as shared library resources
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}

%description
The experimental v6 ionCube Loader enables use of ionCube-encoded PHP files running
under PHP %{php_version}.

%prep
%setup -q -n ioncube

%build
# Nothing to do here, since it's a binary distribution.

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

# The module itself
install -d -m 755 $RPM_BUILD_ROOT%{php_extdir}
install -m 755 ioncube_loader_lin_%{php_version}.so $RPM_BUILD_ROOT%{php_extdir}

# The ini snippet
install -d -m 755 $RPM_BUILD_ROOT%{php_inidir}
cat > $RPM_BUILD_ROOT%{php_inidir}/%{inifile} <<EOF
; Enable Experimental v6 IonCube Loader extension module
zend_extension="%{php_extdir}/ioncube_loader_lin_%{php_version}.so"
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt
%config(noreplace) %{php_inidir}/%{inifile}
%{php_extdir}/ioncube_loader_lin_%{php_version}.so

%changelog
* Mon Jan 30 2017 Dan Muey <dan@cpanel.net> - 6.0.4-3
- EA-5837: updated vendor field

* Mon Oct 03 2016 Edwin Buck <e.buck@cpanel.net> 6.0.4-2
- EA-5286: Reworked conflicts to conflict with other ioncube releases.

* Fri Sep 20 2016 Edwin Buck <e.buck@cpanel.net> 6.0.4-1
- Initial packaging
