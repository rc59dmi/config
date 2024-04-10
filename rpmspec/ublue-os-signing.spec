Name:           rc59dmi-signing
Packager:       rc59dmi
Vendor:         rc59dmi
Version:        0.1
Release:        1%{?dist}
Summary:        Signing files and keys for RC59 Fedora Remix
License:        MIT
URL:            https://github.com/rc59dmi/config

BuildArch:      noarch

Source0:        rc59dmi-signing.tar.gz

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^rc59dmi%-", ""); print(t)}

%description
Adds files and keys for signing RC59 images

%prep
%setup -q -c -T

%build
mkdir -p -m0755 %{buildroot}%{_datadir}/%{VENDOR}
mkdir -p -m0755 %{buildroot}%{_exec_prefix}/etc/containers/registries.d
mkdir -p -m0755 %{buildroot}%{_exec_prefix}/etc/pki

tar xf %{SOURCE0} -C %{buildroot}%{_datadir}/%{VENDOR} --strip-components=1
tar xf %{SOURCE0} -C %{buildroot} --strip-components=2

%files
%dir %attr(0755,root,root) %{_datadir}/%{VENDOR}/%{sub_name}
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/etc/containers/policy.json
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/etc/containers/registries.d/rc59dmi.yaml
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/etc/pki/containers/rc59dmi.pub
%attr(0644,root,root) %{_exec_prefix}/etc/containers/policy.json
%attr(0644,root,root) %{_exec_prefix}/etc/containers/registries.d/rc59dmi.yaml
%attr(0644,root,root) %{_exec_prefix}/etc/pki/containers/rc59dmi.pub

%changelog
* Wed Apr 10 2024 Dušan Simić <dusan.simic@dmi.uns.ac.rs> - 0.1
- Add package for signing files and keys
