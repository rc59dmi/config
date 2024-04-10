Name:           rc59dmi-update-services
Packager:       rc59dmi
Vendor:         rc59dmi
Version:        0.8
Release:        1%{?dist}
Summary:        Automatic updates for rpm-ostree and flatpak
License:        MIT
URL:            https://github.com/rc59dmi/config

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Supplements:    rpm-ostree flatpak

Source0:        rc59dmi-update-services.tar.gz

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^rc59dmi%-", ""); print(t)}

%description
Adds systemd units and configuration files for enabling automatic updates in rpm-ostree and flatpak

%prep
%setup -q -c -T

%build

mkdir -p -m0755 %{buildroot}%{_datadir}/%{VENDOR}

tar xf %{SOURCE0} -C %{buildroot}%{_datadir}/%{VENDOR} --strip-components=1

# rpm-ostreed.conf cannot be installed in /etc as it'd conflict with upstream 
# rpm-ostree package
tar xf %{SOURCE0} -C %{buildroot} --strip-components=2 --exclude etc/rpm-ostreed.conf


%post
%systemd_post flatpak-system-update.timer
%systemd_user_post flatpak-user-update.timer


%preun
%systemd_preun flatpak-system-update.timer
%systemd_user_preun flatpak-user-update.timer


%files
%dir %attr(0755,root,root) %{_datadir}/%{VENDOR}/%{sub_name}
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/lib/systemd/system-preset/10-flatpak-system-update.preset
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/lib/systemd/system/flatpak-system-update.service
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/lib/systemd/system/flatpak-system-update.timer
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/lib/systemd/user-preset/10-flatpak-user-update.preset
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/lib/systemd/user/flatpak-user-update.service
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/lib/systemd/user/flatpak-user-update.timer
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/%{_sysconfdir}/systemd/system/rpm-ostreed-automatic.timer.d/override.conf
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/%{_sysconfdir}/systemd/system/rpm-ostreed-automatic.service.d/override.conf
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/%{_sysconfdir}/rpm-ostreed.conf
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system-preset/10-flatpak-system-update.preset
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system/flatpak-system-update.service
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/system/flatpak-system-update.timer
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/user-preset/10-flatpak-user-update.preset
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/user/flatpak-user-update.service
%attr(0644,root,root) %{_exec_prefix}/lib/systemd/user/flatpak-user-update.timer
%attr(0644,root,root) %{_exec_prefix}/%{_sysconfdir}/systemd/system/rpm-ostreed-automatic.timer.d/override.conf
%attr(0644,root,root) %{_exec_prefix}/%{_sysconfdir}/systemd/system/rpm-ostreed-automatic.service.d/override.conf



%changelog
* Wed Apr 10 2024 Dušan Simić <dusan.simic@dmi.uns.ac.rs> - 0.1
- Add flatpak update service and rpm-ostree config based on UBlue
