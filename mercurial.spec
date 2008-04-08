Summary: A fast, lightweight distributed source control management system 
Name: mercurial
Version: 1.0
Release: 6%{?dist}
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

%define pkg mercurial
#%define pkgname Foo

# If the emacs-el package has installed a pkgconfig file, use that to determine
# install locations and Emacs version at build time, otherwise set defaults.
%if %($(pkg-config emacs) ; echo $?)
%define emacs_version 22.1
%define emacs_lispdir %{_datadir}/emacs/site-lisp
%define emacs_startdir %{_datadir}/emacs/site-lisp/site-start.d
%else
%define emacs_version %(pkg-config emacs --modversion)
%define emacs_lispdir %(pkg-config emacs --variable sitepkglispdir)
%define emacs_startdir %(pkg-config emacs --variable sitestartdir)
%endif

# If the xemacs-devel package has installed a pkgconfig file, use that to determine
# install locations and Emacs version at build time, otherwise set defaults.
%if %($(pkg-config xemacs) ; echo $?)
%define xemacs_version 21.5
%define xemacs_lispdir %{_datadir}/xemacs/site-packages
%define xemacs_startdir %{_datadir}/xemacs/site-packages/site-start.d
%else
%define xemacs_version %(pkg-config xemacs --modversion)
%define xemacs_lispdir %(pkg-config xemacs --variable sitepkglispdir)
%define xemacs_startdir %(pkg-config xemacs --variable sitestartdir)
%endif

%package -n emacs-%{pkg}
Summary:	Mercurial version control system support for Emacs
Group:		Applications/Editors
Requires:	hg = %{version}-%{release}, emacs-common
Requires:       emacs(bin) >= %{emacs_version}


%description -n emacs-%{pkg}
Contains byte compiled elisp packages for %{pkg}.
To get started: start emacs, load hg-mode with M-x hg-mode, and show 
help with C-c h h

%package -n emacs-%{pkg}-el
Summary:        Elisp source files for %{pkg} under GNU Emacs
Group:          Development/Tools
Requires:       emacs-%{pkg} = %{version}-%{release}

%description -n emacs-%{pkg}-el
This package contains the elisp source files for %{pkg} under GNU Emacs. You
do not need to install this package to run %{pkg}. Install the emacs-%{pkg}
package to use %{pkg} with GNU Emacs.

%package -n xemacs-%{pkg}
Summary:        Compiled elisp files to run %{pkg} under XEmacs
Group:          Development/Tools
Requires:       xemacs(bin) >= %{xemacs_version}

%description -n xemacs-%{pkg}
This package contains the byte compiled elisp packages to use %{pkg} with
XEmacs. 
To get started: start xemacs, load hg-mode with M-x hg-mode, and show 
help with C-c h h


%package -n xemacs-%{pkg}-el
Summary:        Elisp source files for %{pkg} under XEmacs
Group:          Development/Tools
Requires:       xemacs-%{pkg} = %{version}-%{release}

%description -n xemacs-%{pkg}-el
This package contains the elisp source files for %{pkg} under XEmacs. You do
not need to install this package to run %{pkg}. Install the xemacs-%{pkg}
package to use %{pkg} with XEmacs.

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

grep -v 'hgk.py*' < %{name}.files > %{name}-base.files
grep 'hgk.py*' < %{name}.files > %{name}-hgk.files

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

mkdir -p $RPM_BUILD_ROOT%{emacs_lispdir}
mkdir -p $RPM_BUILD_ROOT%{xemacs_lispdir}
pushd contrib
for file in mercurial.el mq.el; do
  emacs -batch --no-site-file -f batch-byte-compile $file
  install -m 644 $file ${file}c $RPM_BUILD_ROOT%{emacs_lispdir}
  rm ${file}c
  xemacs -batch -l mercurial.el --no-site-file -f batch-byte-compile $file
  install -m 644 $file ${file}c $RPM_BUILD_ROOT%{xemacs_lispdir}
  rm ${file}c
done
popd



mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

mkdir -p $RPM_BUILD_ROOT%{emacs_startdir} && install -m644 %SOURCE1 $RPM_BUILD_ROOT%{emacs_startdir}
mkdir -p $RPM_BUILD_ROOT%{xemacs_startdir} && install -m644 %SOURCE1 $RPM_BUILD_ROOT%{xemacs_startdir}

cat >hgk.rc <<EOF
[extensions]
# enable hgk extension ('hg help' shows 'view' as a command)
hgk=
EOF
install hgk.rc $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

install contrib/mergetools.hgrc $RPM_BUILD_ROOT%{_sysconfdir}/mercurial/hgrc.d

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-base.files
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING doc/README doc/hg*.txt doc/hg*.html doc/ja *.cgi contrib/*.fcgi
%doc %attr(644,root,root) %{_mandir}/man?/hg*.gz
%doc %attr(644,root,root) contrib/*.svg contrib/sample.hgrc
%{_sysconfdir}/bash_completion.d/mercurial.sh
%{_datadir}/zsh/site-functions/_mercurial
%{_bindir}/hg-ssh
%{_bindir}/hg-viz
%{_bindir}/git-rev-tree
%{_bindir}/mercurial-convert-repo
%dir %{_sysconfdir}/mercurial
%dir %{_sysconfdir}/mercurial/hgrc.d
%{_sysconfdir}/mercurial/hgrc.d/mergetools.hgrc

%files -n emacs-%{pkg}
%{emacs_lispdir}/*.elc
%{emacs_startdir}/*.el

%files -n emacs-%{pkg}-el
%{emacs_lispdir}/*.el

%files -n xemacs-%{pkg}
%{xemacs_lispdir}/*.elc
%{xemacs_startdir}/*.el

%files -n xemacs-%{pkg}-el
%{xemacs_lispdir}/*.el


%files hgk -f %{name}-hgk.files
%{_bindir}/hgk
%{_sysconfdir}/mercurial/hgrc.d/hgk.rc

#%check
#cd tests && python run-tests.py

%changelog
* Tue Apr  8 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-6
- fix to comply with emacs packaging guidelines

* Thu Mar 27 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-5
- Move hgk-related py files to hgk
- Put mergetools.hgrc in /etc/mercurial/hgrc.d
- Add hgk.rc and put in /etc/mercurial/hgrc.d

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

