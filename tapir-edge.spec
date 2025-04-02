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
#BuildRequires: systemd-units
#BuildRequires: systemd-devel
#BuildRequires(post): systemd-units
#BuildRequires(preun): systemd-units
#BuildRequires(postun): systemd-units
Source0:        https://github.com/zluudg/cli/archive/refs/tags/v%{cli_version}.tar.gz
Source1:        https://github.com/zluudg/hellosrcdist/archive/refs/tags/v%{hellosrcdist_version}.tar.gz
Source2:        tapir-edm.service
Source3:        tapir-pop.service
Source4:        tapir-renew.service
Source5:        tapir-edge.sysusers
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
install -m 0644 -D %{SOURCE5} %{buildroot}%{_sysusersdir}/tapir-edge.conf
mkdir -p %{buildroot}%{_sysconfdir}/dnstapir/
mkdir -p %{buildroot}%{_sysconfdir}/dnstapir/certs/
mkdir -p %{buildroot}%{_localstatedir}/log/dnstapir/
install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}
install -p -m 0755 cli-%{cli_version}/tapir-cli %{buildroot}%{_bindir}/tapir-cli
install -p -m 0755 hellosrcdist-%{hellosrcdist_version}/bin/hellosrcdist %{buildroot}%{_bindir}/hellosrcdist
touch %{buildroot}%{_localstatedir}/log/dnstapir/tapir-pop.log 
touch %{buildroot}%{_localstatedir}/log/dnstapir/pop-dnsengine.log 
touch %{buildroot}%{_localstatedir}/log/dnstapir/pop-mqtt.log 
touch %{buildroot}%{_localstatedir}/log/dnstapir/pop-policy.log 

%files
%{_bindir}/tapir-cli
%{_bindir}/hellosrcdist
%{_sysusersdir}/tapir-edge.conf
%dir %{_localstatedir}/log/dnstapir/
%dir %{_sysconfdir}/dnstapir
%dir %{_sysconfdir}/dnstapir/certs
%attr(0660,root,tapir-edge) %{_localstatedir}/log/dnstapir/
%attr(0664,root,tapir-edge) %{_sysconfdir}/dnstapir/
%attr(0660,root,tapir-edge) %{_sysconfdir}/dnstapir/certs/
%attr(0660,root,tapir-edge) %{_localstatedir}/log/dnstapir/tapir-pop.log 
%attr(0660,root,tapir-edge) %{_localstatedir}/log/dnstapir/pop-dnsengine.log 
%attr(0660,root,tapir-edge) %{_localstatedir}/log/dnstapir/pop-mqtt.log 
%attr(0660,root,tapir-edge) %{_localstatedir}/log/dnstapir/pop-policy.log 
%attr(0660,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/tapir-edm.toml
%attr(0660,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/tapir-pop.yaml
%attr(0660,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/tapir-cli.yaml
%attr(0660,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/pop-outputs.yaml
%attr(0660,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/pop-policy.yaml
%attr(0660,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/pop-sources.yaml
%attr(0660,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/rpz-serial.yaml 
%attr(0664,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/certs/ca.crt
%attr(0664,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/certs/tls.crt
%attr(0664,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/certs/validation-keys.json
%attr(0660,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/certs/tls.key
%attr(0660,root,tapir-edge) %ghost %{_sysconfdir}/dnstapir/certs/datakey-priv.json
%attr(0644,root,root) %{_unitdir}/tapir-pop.service
%attr(0644,root,root) %{_unitdir}/tapir-edm.service
%attr(0644,root,root) %{_unitdir}/tapir-renew.service

%post
%systemd_post tapir-pop.service
%systemd_post tapir-edm.service
%systemd_post tapir-renew.service
	
%preun
%systemd_post tapir-pop.service
%systemd_post tapir-edm.service
%systemd_post tapir-renew.service
	
%postun
%systemd_post tapir-pop.service
%systemd_post tapir-edm.service
%systemd_post tapir-renew.service

%changelog
%autochangelog
