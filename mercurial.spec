Summary: A fast, lightweight distributed source control management system 
Name: mercurial
Version: 1.0
Release: 4%{?dist}
License: GPLv2
Group: Development/Tools
URL: http://www.selenic.com/mercurial/
Source0: http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
Source1: mercurial-site-start.el
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-devel asciidoc xmlto
Requires: python
Provides: hg = %{version}-%{release}

%description
Mercurial is a fast, lightweight source control management system designed
for efficient handling of very large distributed projects.

Quick start: http://www.selenic.com/mercurial/wiki/index.cgi/QuickStart
Tutorial: http://www.selenic.com/mercurial/wiki/index.cgi/Tutorial
Extensions: http://www.selenic.com/mercurial/wiki/index.cgi/CategoryExtension

%package emacs
Summary:	Mercurial version control system support for Emacs
Group:		Applications/Editors
Requires:	hg = %{version}-%{release}, emacs-common

%description emacs
%{summary}.

%package hgk
Summary:	Hgk interface for mercurial
Group:		Development/Tools
Requires:	hg = %{version}-%{release}, tk

%description hgk
A Mercurial extension for displaying the change history graphically
using Tcl/Tk.  Displays branches and merges in an easily
understandable way and shows diffs for each revision.  Based on
gitk for the git SCM.

See http://www.selenic.com/mercurial/wiki/index.cgi/UsingHgk for more
documentation.

%prep
%setup -q

%build
make all

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --root $RPM_BUILD_ROOT --prefix %{_prefix} --record=%{name}.files
make install-doc DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}

install contrib/hgk          $RPM_BUILD_ROOT%{_bindir}
install contrib/convert-repo $RPM_BUILD_ROOT%{_bindir}/mercurial-convert-repo
install contrib/hg-ssh       $RPM_BUILD_ROOT%{_bindir}
install contrib/git-viz/{hg-viz,git-rev-tree} $RPM_BUILD_ROOT%{_bindir}

bash_completion_dir=$RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
mkdir -p $bash_completion_dir
install -m 644 contrib/bash_completion $bash_completion_dir/mercurial.sh

zsh_completion_dir=$RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
mkdir -p $zsh_completion_dir
install -m 644 contrib/zsh_completion $zsh_completion_dir/_mercurial

lisp_dir=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
mkdir -p $lisp_dir
install -m 644 contrib/mercurial.el $lisp_dir
xlisp_dir=$RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp
mkdir -p $xlisp_dir
install -m 644 contrib/mercurial.el $xlisp_dir
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

mkdir -p $lisp_dir/site-start.d/ && install -m644 %SOURCE1 $lisp_dir/site-start.d/
mkdir -p $xlisp_dir/site-start.d/ && install -m644 %SOURCE1 $xlisp_dir/site-start.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.files
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING doc/README doc/hg*.txt doc/hg*.html doc/ja *.cgi contrib/*.fcgi
%doc %attr(644,root,root) %{_mandir}/man?/hg*.gz
%doc %attr(644,root,root) contrib/*.svg contrib/*.hgrc
%{_sysconfdir}/bash_completion.d/mercurial.sh
%{_datadir}/zsh/site-functions/_mercurial
%{_bindir}/hg-ssh
%{_bindir}/hg-viz
%{_bindir}/git-rev-tree
%{_bindir}/mercurial-convert-repo
%dir %{_sysconfdir}/mercurial
%dir %{_sysconfdir}/mercurial/hgrc.d

%files emacs
%{_datadir}/emacs/site-lisp/mercurial.el
%{_datadir}/xemacs/site-packages/lisp/mercurial.el
%{_datadir}/emacs/site-lisp/site-start.d/*
%{_datadir}/xemacs/site-packages/lisp/site-start.d/*

%files hgk
%{_bindir}/hgk

#%check
#cd tests && python run-tests.py

%changelog
* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-4
- Rename mercurial-site-start -> mercurial-site-start.el

* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-3
- Incorprate suggestions from hopper@omnifarious.org

* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-2
- Add site-start

* Tue Mar 25 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-1
- Update to 1.0
- Disable check for now - 1 test fails
- Move emacs to separate package
- Add check

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-7
- Autorebuild for GCC 4.3

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-6
- rpmlint fixes

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-5
- /etc/mercurial/hgrc.d missing

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-3
- Fix to last change

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-2
- mkdir /etc/mercurial/hgrc.d for plugins

* Tue Oct 23 2007  <ndbecker2@gmail.com> - 0.9.5-2
- Bump tag to fix confusion

* Mon Oct 15 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-1
- Sync with spec file from mercurial

* Sat Sep 22 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-8
- Just cp contrib tree.
- Revert install -O2

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-7
- Change setup.py install to -O2 to get bytecompile on EL-4

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-6
- Revert last change.

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-5
- Use {ghost} on contrib, otherwise EL-4 build fails

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-4
- remove {_datadir}/contrib stuff for now

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

