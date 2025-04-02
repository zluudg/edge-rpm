%define cli_version 0.5
%define hellosrcdist_version 1.0.1
%define debug_package %{nil}


Name:           tapir-edge
Version:        1.0.0
Release:        1%{?dist}
Group:          dnstapir/edge
Summary:        DNSTAPIR EDGE
License:        BSD
URL:            https://www.github.com/zluudg/edge-rpm
BuildRequires:  golang
BuildRequires:  make
BuildRequires:  systemd
BuildRequires: systemd-rpm-macros
%{?sysusers_requires_compat}
Source0:        https://github.com/zluudg/cli/archive/refs/tags/v%{cli_version}.tar.gz
Source1:        https://github.com/zluudg/hellosrcdist/archive/refs/tags/v%{hellosrcdist_version}.tar.gz
Source2:        tapir-edm.service
Source3:        tapir-pop.service
Source4:        tapir-renew.service
Source5:        tapir-renew.timer
Source6:        tapir-edge.sysusers
%description
An attempt at packaging this thing

%prep
%setup -n cli-%{cli_version}
%setup -T -D -b 1 -n hellosrcdist-%{hellosrcdist_version}
%build
make
cd %{_builddir}
cd cli-%{cli_version}
make

%install
cd %{_builddir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_bindir}
install -m 0644 -D %{SOURCE6} %{buildroot}%{_sysusersdir}/tapir-edge.conf
mkdir -p %{buildroot}%{_sysconfdir}/dnstapir/
mkdir -p %{buildroot}%{_sysconfdir}/dnstapir/certs/
mkdir -p %{buildroot}%{_localstatedir}/log/dnstapir/
install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}
install -p -m 0755 cli-%{cli_version}/tapir-cli %{buildroot}%{_bindir}/tapir-cli
install -p -m 0755 hellosrcdist-%{hellosrcdist_version}/bin/hellosrcdist %{buildroot}%{_bindir}/hellosrcdist
touch %{buildroot}%{_localstatedir}/log/dnstapir/tapir-pop.log 
touch %{buildroot}%{_localstatedir}/log/dnstapir/pop-dnsengine.log 
touch %{buildroot}%{_localstatedir}/log/dnstapir/pop-mqtt.log 
touch %{buildroot}%{_localstatedir}/log/dnstapir/pop-policy.log 

%files
%attr(0664,tapir-edge,tapir-edge) %{_sysusersdir}/tapir-edge.conf
%attr(0775,tapir-edge,tapir-edge) %{_bindir}/tapir-cli
%attr(0775,tapir-edge,tapir-edge) %{_bindir}/hellosrcdist
%attr(0660,tapir-edge,tapir-edge) %{_localstatedir}/log/dnstapir/tapir-pop.log 
%attr(0660,tapir-edge,tapir-edge) %{_localstatedir}/log/dnstapir/pop-dnsengine.log 
%attr(0660,tapir-edge,tapir-edge) %{_localstatedir}/log/dnstapir/pop-mqtt.log 
%attr(0660,tapir-edge,tapir-edge) %{_localstatedir}/log/dnstapir/pop-policy.log 
%attr(0660,tapir-edge,tapir-edge) %dir %{_localstatedir}/log/dnstapir/
%attr(0660,tapir-edge,tapir-edge) %dir %{_sysconfdir}/dnstapir
%attr(0660,tapir-edge,tapir-edge) %dir %{_sysconfdir}/dnstapir/certs
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/tapir-edm.toml
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/tapir-pop.yaml
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/tapir-cli.yaml
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/pop-outputs.yaml
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/pop-policy.yaml
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/pop-sources.yaml
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/rpz-serial.yaml 
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/certs/ca.crt
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/certs/tls.crt
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/certs/validation-keys.json
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/certs/tls.key
%attr(0660,tapir-edge,tapir-edge) %ghost %{_sysconfdir}/dnstapir/certs/datakey-priv.json
%attr(0644,tapir-edge,root) %{_unitdir}/tapir-pop.service
%attr(0644,tapir-edge,root) %{_unitdir}/tapir-edm.service
%attr(0644,tapir-edge,root) %{_unitdir}/tapir-renew.service
%attr(0644,tapir-edge,root) %{_unitdir}/tapir-renew.timer

%pre
%sysusers_create_compat %{SOURCE5}

%post
%systemd_post tapir-pop.service
%systemd_post tapir-edm.service
%systemd_post tapir-renew.service
%systemd_post tapir-renew.timer

%preun
%systemd_post tapir-pop.service
%systemd_post tapir-edm.service
%systemd_post tapir-renew.service
%systemd_post tapir-renew.timer

%postun
%systemd_post tapir-pop.service
%systemd_post tapir-edm.service
%systemd_post tapir-renew.service
%systemd_post tapir-renew.timer

%check

%changelog
%autochangelog
