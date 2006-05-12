Summary: A fast, lightweight distributed source control management system 
Name: mercurial
Version: 0.9
Release: 1%{?dist}
License: GPL
Group: Development/Tools
URL: http://www.selenic.com/mercurial/
Source0: http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-devel asciidoc xmlto

%description
Mercurial is a fast, lightweight source control management system designed 
for efficient handling of very large distributed projects.

%prep
%setup -q

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


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.files
%defattr(-,root,root,-)
%doc CONTRIBUTORS README doc/hg.1.txt doc/hgmerge.1.txt doc/hgrc.5.txt
%{_mandir}/man*/*


%changelog
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

