%define release_number %(echo $RELEASE_NUMBER)
%define version_number %(echo $VERSION_NUMBER)

Name:     sniproxy-fang
Version:  %{version_number}
Release:  %{release_number}%{?dist}
Summary:  SniProxy Written in GoLang
Epoch:    7
Packager: Eliezer Croitoru <ngtech1ltd@gmail.com>>
Vendor:   NgTech Ltd
License:  3 Clause BSD
Group:    System Environment/Daemons
URL:      https://github.com/fangdingjun/sniproxy
Source0:  sniproxy-fang.service
Source1:  sniproxy-fang
Source2:  sniproxy-fang.sysconfig
Source3:  config.sample.yaml

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Requires: systemd-units
# Required to allow debug package auto creation
BuildRequires:  redhat-rpm-config
BuildRequires:  systemd-units

# Required to validate auto requires AutoReqProv: no
## aaaAutoReqProv: no

%description
Sniproxy by fangdingjun an opensource and public sniproxy written in GoLang.
Sources at: https://github.com/fangdingjun/sniproxy

%prep
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sniproxy-fang
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
install -m 644 %{SOURCE0} ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_bindir}/sniproxy-fang
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/sniproxy-fang
install -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/sniproxy-fang/config.sample.yaml

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %dir %{_sysconfdir}
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig
%config(noreplace) %{_sysconfdir}/sysconfig/sniproxy-fang
%config(noreplace) %{_sysconfdir}/sniproxy-fang/config.sample.yaml
%attr(755,root,root) %{_bindir}/sniproxy-fang

%{_unitdir}/sniproxy-fang.service

%pre
if ! /usr/bin/getent group sniproxy >/dev/null 2>&1; then
  /usr/sbin/groupadd -g 5006 sniproxy
fi

if ! /usr/bin/getent passwd sniproxy >/dev/null 2>&1 ; then
  /usr/sbin/useradd -g 5006 -u 5006 -m -d /home/sniproxy -r -s /sbin/nologin sniproxy >/dev/null 2>&1 || exit 1
fi

%post
%systemd_post sniproxy-fang.service

%preun
%systemd_preun sniproxy-fang.service

%postun
%systemd_postun_with_restart sniproxu-fang.service

%changelog
* Tue Jan 07 2020 Eliezer Croitoru <ngtech1ltd@gmail.com>
- Release 1.0.0  git commit: 2274aa2.
