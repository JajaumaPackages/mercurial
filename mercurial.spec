Summary: A fast, lightweight distributed source control management system 
Name: mercurial
Version: 0.6b
Release: 1%{?dist}
License: GPL
Group: Development/Tools
URL: http://www.selenic.com/mercurial/
Source0: http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-devel

%description
Mercurial is a fast, lightweight source control management system designed 
for efficient handling of very large distributed projects.

%prep
%setup -q

%build
python ./setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python ./setup.py install -O1 --root=$RPM_BUILD_ROOT --record=%{name}.files


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.files
%defattr(-,root,root,-)
%doc doc/FAQ.txt README doc/hg.1.txt


%changelog
* Tue Jul 12 2005 Jeremy Katz <katzj@redhat.com> - 0.6b
- update to new upstream 0.6b

* Fri Jul  1 2005 Jeremy Katz <katzj@redhat.com> - 0.6-1
- Initial build.

