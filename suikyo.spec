#
# Conditional build:
%bcond_without	emacs		# Emacs binding
%bcond_without	xemacs		# XEmacs binding
#
Summary:	Romaji-Hiragana conversion library
Summary(pl.UTF-8):	Biblioteka konwersji romaji-hiragana
Name:		suikyo
Version:	2.1.0
Release:	1
License:	GPL v2
Group:		Libraries
#Source0:	http://taiyaki.org/suikyo/src/%{name}-%{version}.tar.gz
Source0:	http://prime.sourceforge.jp/src/%{name}-%{version}.tar.gz
# Source0-md5:	d33d713c57522f5c28323e19b3f635b2
URL:		http://taiyaki.org/suikyo/
%{?with_emacs:BuildRequires:	emacs}
BuildRequires:	ruby
%{?with_xemacs:BuildRequires:	xemacs}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Suikyo is a Romaji-Hiragana conversion library based on DFA
(Deterministic finate state) automaton.

%description -l pl.UTF-8
Suikyo to biblioteka konwersji romaji-hiragana oparta na
deterministycznym automacie skończonym (DFA).

%package -n ruby-suikyo
Summary:	Ruby binding of suikyo
Summary(pl.UTF-8):	Wiązanie języka Ruby do suikyo
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n ruby-suikyo
Ruby binding of suikyo.

%description -n ruby-suikyo -l pl.UTF-8
Wiązanie języka Ruby do suikyo.

%package -n emacs-suikyo
Summary:	Emacs binding of suikyo
Summary(pl.UTF-8):	Wiązanie Emacsa do suikyo
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
Requires:	emacs

%description -n emacs-suikyo
Emacs binding of suikyo.

%description -n emacs-suikyo -l pl.UTF-8
Wiązanie Emacsa do suikyo.

%package -n xemacs-suikyo
Summary:	XEmacs binding of suikyo
Summary(pl.UTF-8):	Wiązanie XEmacsa do suikyo
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
Requires:	xemacs

%description -n xemacs-suikyo
XEmacs binding of suikyo.

%description -n xemacs-suikyo -l pl.UTF-8
Wiązanie XEmacsa do suikyo.

%prep
%setup -q

%build
%configure \
	--with-rubydir=%{ruby_rubylibdir}
%{__make}

cd elisp/src

%if %{with emacs}
emacs -no-site-file -q -batch -f batch-byte-compile *.el
for i in *.elc; do
	mv $i $i.emacs
done
%endif

%if %{with xemacs}
xemacs -no-site-file -q -batch -f batch-byte-compile *.el
for i in *.elc; do
	mv $i $i.xemacs
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

# omit elisp
%{__make} install-am \
	DESTDIR=$RPM_BUILD_ROOT
for d in conv-table ruby ; do
%{__make} -C $d install \
	DESTDIR=$RPM_BUILD_ROOT
done

%if %{with emacs}
%{__make} -C elisp install \
	suikyoelsrcdir=%{_datadir}/emacs/site-lisp/suikyo \
	etcdir=%{_datadir}/emacs/site-lisp/site-start.d
for f in elisp/src/*.elc.emacs ; do
	cp -p $f $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/suikyo/${f%.emacs}
done
sed -i -e 's,concat "/[^"]*",concat "%{_datadir}/emacs/site-lisp",' $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/init-suikyo.el
%endif

%if %{with xemacs}
%{__make} -C elisp install \
	suikyoelsrcdir=%{_datadir}/xemacs/xemacs-packages/suikyo \
	etcdir=%{_datadir}/xemacs/site-packages/lisp/site-start.d
for f in elisp/src/*.elc.xemacs ; do
	cp -p $f $RPM_BUILD_ROOT%{_datadir}/xemacs/xemacs-packages/lisp/suikyo/${f%.xemacs}
done
sed -i -e 's,concat "/[^"]*",concat "%{_datadir}/xemacs/xemacs-packages/lisp",' $RPM_BUILD_ROOT%{_datadir}/xemacs/site-packages/lisp/site-start.d/init-suikyo.el
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README doc/index.html
%{_datadir}/suikyo
%{_pkgconfigdir}/suikyo.pc

%files -n ruby-suikyo
%defattr(644,root,root,755)
%doc contrib/uniq.rb ruby/ChangeLog ruby/doc/index.html
%{ruby_rubylibdir}/suikyo

%if %{with emacs}
%files -n emacs-suikyo
%defattr(644,root,root,755)
%doc elisp/ChangeLog
%{_datadir}/emacs/site-lisp/suikyo
%{_datadir}/emacs/site-lisp/site-start.d/init-suikyo.el
%endif

%if %{with xemacs}
%files -n xemacs-suikyo
%doc elisp/ChangeLog
%defattr(644,root,root,755)
%{_datadir}/xemacs/xemacs-packages/lisp/suikyo
%{_datadir}/xemacs/site-packages/lisp/site-start.d/init-suikyo.el
%endif
