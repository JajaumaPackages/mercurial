Summary: A fast, lightweight distributed source control management system 
Name: mercurial
Version: 0.9.4
Release: 4%{?dist}
License: GPL
Group: Development/Tools
URL: http://www.selenic.com/mercurial/
Source0: http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
Patch0: mercurial-install-contrib.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-devel asciidoc xmlto
Provides: hg = %{version}-%{release}

%description
Mercurial is a fast, lightweight source control management system designed 
for efficient handling of very large distributed projects.
 
%prep
%setup -q
%patch0 -p1

%build
python ./setup.py build

# not built by default.  kind of lame
pushd doc ; make man ; popd

%install
rm -rf $RPM_BUILD_ROOT
python ./setup.py install -O1 --root=$RPM_BUILD_ROOT --record=%{name}.files

# and we have to install the man pages
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1 $RPM_BUILD_ROOT/%{_mandir}/man5
install -m 0644 doc/hg.1 $RPM_BUILD_ROOT/%{_mandir}/man1/hg.1
install -m 0644 doc/hgmerge.1 $RPM_BUILD_ROOT/%{_mandir}/man1/hgmerge.1
install -m 0644 doc/hgrc.5 $RPM_BUILD_ROOT/%{_mandir}/man5/hgrc.5
install -m 0644 doc/hgignore.5 $RPM_BUILD_ROOT/%{_mandir}/man5/hgignore.5

# Set up a system-wide hgrc that says where the hgk script went:
mkdir -p $RPM_BUILD_ROOT/etc/mercurial
cat - >$RPM_BUILD_ROOT/etc/mercurial/hgrc << EOF
[hgk]
path=/usr/share/mercurial/contrib/hgk
EOF

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.files
%defattr(-,root,root,-)
%doc CONTRIBUTORS README contrib/sample.hgrc
%{_sysconfdir}/mercurial
%{_mandir}/man*/*

%changelog
* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-4
- remove %{_datadir}/contrib stuff for now

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-3
- Fix mercurial-install-contrib.patch (/usr/share/mercurial->/usr/share/mercurial/contrib)

* Wed Aug 29 2007 Jonathan Shapiro <shap@eros-os.com> - 0.9.4-2
- update to 0.9.4-2
- install contrib directory
- set up required path for hgk
- install man5 man pages

* Thu Aug 23 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-1
- update to 0.9.4

* Wed Jan  3 2007 Jeremy Katz <katzj@redhat.com> - 0.9.3-1
- update to 0.9.3
- remove asciidoc files now that we have them as manpages

* Mon Dec 11 2006 Jeremy Katz <katzj@redhat.com> - 0.9.2-1
- update to 0.9.2

* Mon Aug 28 2006 Jeremy Katz <katzj@redhat.com> - 0.9.1-2
- rebuild

* Tue Jul 25 2006 Jeremy Katz <katzj@redhat.com> - 0.9.1-1
- update to 0.9.1

* Fri May 12 2006 Mihai Ibanescu <misa@redhat.com> - 0.9-1
- update to 0.9

* Mon Apr 10 2006 Jeremy Katz <katzj@redhat.com> - 0.8.1-1
- update to 0.8.1
- add man pages (#188144)

* Fri Mar 17 2006 Jeremy Katz <katzj@redhat.com> - 0.8-3
- rebuild

* Fri Feb 17 2006 Jeremy Katz <katzj@redhat.com> - 0.8-2
- rebuild

* Mon Jan 30 2006 Jeremy Katz <katzj@redhat.com> - 0.8-1
- update to 0.8

* Thu Sep 22 2005 Jeremy Katz <katzj@redhat.com> 
- add contributors to %%doc

* Tue Sep 20 2005 Jeremy Katz <katzj@redhat.com> - 0.7
- update to 0.7

* Mon Aug 22 2005 Jeremy Katz <katzj@redhat.com> - 0.6c
- update to 0.6c

* Tue Jul 12 2005 Jeremy Katz <katzj@redhat.com> - 0.6b
- update to new upstream 0.6b

* Fri Jul  1 2005 Jeremy Katz <katzj@redhat.com> - 0.6-1
- Initial build.

