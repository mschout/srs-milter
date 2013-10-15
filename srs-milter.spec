Summary:        Milter (mail filter) for SRS
Name:           srs-milter
Version:        0.0.2
Release:        1%{?dist}
License:        GPL
Group:          System Environment/Daemons
URL:            https://github.com/flowerysong/srs-milter
Source0:        https://github.com/flowerysong/srs-milter/archive/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  sendmail-devel
BuildRequires:  libspf2-devel
BuildRequires:  libsrs2-devel
Requires:   libspf2
Requires:   libsrs2

Requires(pre):      /usr/bin/getent, /usr/sbin/groupadd, /usr/sbin/useradd, /usr/sbin/usermod
Requires(post):     /sbin/chkconfig
Requires(post):     /sbin/service
Requires(preun):    /sbin/chkconfig, initscripts
Requires(postun):   initscripts

%description
The srs-milter package is an implementation of the SRS standard
that tries to fix problems caused by SPF in case of forwarded mail

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
make %{?_smp_mflags} -C src

%install
make DESTDIR=%{buildroot} install -C src
install -D -m0755 srs-milter.init %{buildroot}%{_initrddir}/srs-milter
install -D -m0644 srs-milter.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/srs-milter
install -d -m0755 %{buildroot}%{_localstatedir}/lib/srs-milter

%pre
/usr/bin/getent group srs-milter >/dev/null || /usr/sbin/groupadd -r srs-milter
/usr/bin/getent passwd srs-milter >/dev/null || \
        /usr/sbin/useradd -r -g srs-milter -d %{_localstatedir}/lib/srs-milter \
        -s /sbin/nologin -c "SRS Milter" srs-milter
# Fix homedir for upgrades
/usr/sbin/usermod --home %{_localstatedir}/lib/srs-milter srs-milter &>/dev/null
exit 0

%post
/sbin/chkconfig --add srs-milter || :

%preun
if [ $1 -eq 0 ]; then
    %{_initrddir}/srs-milter stop &>/dev/null || :
    /sbin/chkconfig --del srs-milter || :
fi

%postun
%{_initrddir}/srs-milter condrestart &>/dev/null || :

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
%config(noreplace) %{_sysconfdir}/sysconfig/srs-milter
%{_initrddir}/srs-milter
%{_sbindir}/srs-milter
%dir %attr(-,srs-milter,srs-milter) %{_localstatedir}/lib/srs-milter

%changelog
* %(date "+%a %b %d %Y") (Automated RPM build) - %{version}-%{release}
- See git log for actual changes.
