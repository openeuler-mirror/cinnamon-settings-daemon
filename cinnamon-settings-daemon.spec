%global cinnamon_desktop_version 5.2.0

Name:           cinnamon-settings-daemon
Version:        5.2.0
Release:        1
Summary:        The daemon sharing settings from CINNAMON to GTK+/KDE applications
License:        GPLv2+ and LGPLv2+
URL:            https://github.com/linuxmint/%{name}
Source0:        https://github.com/linuxmint/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

ExcludeArch:   %{ix86}

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(cinnamon-desktop) >= %{cinnamon_desktop_version}
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libgnomekbd)
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(libnma)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(libxklavier)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(colord) >= 0.1.12
BuildRequires:  pkgconfig(lcms2) >= 2.2
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(ibus-1.0)
BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  docbook-style-xsl
BuildRequires:  intltool
BuildRequires:  libxslt
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(xorg-wacom)
BuildRequires:  pkgconfig(libwacom)

# add hard cinnamon-desktop required version due logind schema
Requires:       cinnamon-desktop%{?_isa} >= %{cinnamon_desktop_version}
Requires:       iio-sensor-proxy%{?_isa}

%description
A daemon to share settings from CINNAMON to other applications. It also
handles global keybindings, and many of desktop-wide settings.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       dbus-glib-devel

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson \
 -Duse_smartcard=disabled \
%ifarch s390 s390x %{?rhel:ppc ppc64}
 -Duse_wacom=disabled
%endif

%meson_build

%install
%meson_install

desktop-file-install --delete-original           \
  --dir %{buildroot}%{_sysconfdir}/xdg/autostart/  \
  %{buildroot}%{_sysconfdir}/xdg/autostart/*

desktop-file-install --delete-original           \
  --dir %{buildroot}%{_datadir}/applications/  \
  %{buildroot}%{_datadir}/applications/csd-automount.desktop
  
# Fix non-executable script
chmod a+x %{buildroot}%{_datadir}/cinnamon-settings-daemon-3.0/input-device-example.sh

# Delete csd symlinks
rm -rf %{buildroot}%{_libdir}/cinnamon-settings-daemon/

%files
%doc AUTHORS
%license COPYING COPYING.LIB
%{_bindir}/csd-*
%config %{_sysconfdir}/xdg/autostart/*
%{_libdir}/cinnamon-settings-daemon-3.0/
%{_libexecdir}/csd-a11y-keyboard
%{_libexecdir}/csd-a11y-settings
%{_libexecdir}/csd-automount
%{_libexecdir}/csd-background
%{_libexecdir}/csd-backlight-helper
%{_libexecdir}/csd-clipboard
%{_libexecdir}/csd-color
%{_libexecdir}/csd-cursor
%{_libexecdir}/csd-datetime-mechanism
%{_libexecdir}/csd-housekeeping
%{_libexecdir}/csd-input-helper
%{_libexecdir}/csd-keyboard
%{_libexecdir}/csd-locate-pointer
%{_libexecdir}/csd-media-keys
%{_libexecdir}/csd-mouse
%{_libexecdir}/csd-orientation
%{_libexecdir}/csd-power
%{_libexecdir}/csd-printer
%{_libexecdir}/csd-print-notifications
%{_libexecdir}/csd-screensaver-proxy
%{_libexecdir}/csd-sound
%{_libexecdir}/csd-xrandr
%{_libexecdir}/csd-xsettings
%{_libexecdir}/csd-list-wacom
%{_libexecdir}/csd-wacom
%{_libexecdir}/csd-wacom-osd
%{_datadir}/applications/csd-automount.desktop
%{_datadir}/cinnamon-settings-daemon/
%{_datadir}/dbus-1/system.d/org.cinnamon.SettingsDaemon.DateTimeMechanism.conf
%{_datadir}/dbus-1/system-services/org.cinnamon.SettingsDaemon.DateTimeMechanism.service
%{_datadir}/glib-2.0/schemas/org.cinnamon.settings-daemon*.xml
%{_datadir}/icons/hicolor/*/apps/csd-*
%{_datadir}/polkit-1/actions/org.cinnamon.settings*.policy

%files devel
%{_includedir}/cinnamon-settings-daemon-3.0/
%{_libdir}/pkgconfig/cinnamon-settings-daemon.pc
%{_datadir}/cinnamon-settings-daemon-3.0/

%changelog
* Fri May 6 2022 lin zhang <lin.zhang@turbolinux.com.cn> - 5.2.0-1
- Initial Packaging
