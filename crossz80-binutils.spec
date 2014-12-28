Summary:	Cross Z80 GNU binary utility development utilities - binutils
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - Z80 binutils
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - Z80 binutils
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla Z80 - binutils
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - Z80 binutils
Summary(tr.UTF-8):	GNU geliştirme araçları - Z80 binutils
Name:		crossz80-binutils
Version:	2.23.1
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	ftp://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2
# Source0-md5:	33adb18c3048d057ac58d07a3f1adb38
Patch0:		tc-z80.c.diff
URL:		http://sources.redhat.com/binutils/
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	perl-tools-pod
BuildRequires:	texinfo
%ifarch sparc sparc32
BuildRequires:	sparc32
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		z80-unknown-coff
%define		arch		%{_prefix}/%{target}

%description
Binutils is a collection of binary utilities, including:
- ar - create, modify and extract from archives,
- nm - lists symbols from object files,
- objcopy - copy and translate object files,
- objdump - display information from object files,
- ranlib - generate an index for the contents of an archive,
- size - list the section sizes of an object or archive file,
- strings - list printable strings from files,
- strip - discard symbols,
- c++filt - a filter for demangling encoded C++ symbols,
- addr2line - convert addresses to file and line,
- nlmconv - convert object code into an NLM.

This package contains the cross version for Z80.

%description -l pl.UTF-8
Pakiet binutils zawiera zestaw narzędzi umożliwiających kompilację
programów. Znajdują się tutaj między innymi assembler, konsolidator
(linker), a także inne narzędzia do manipulowania binarnymi plikami
programów i bibliotek.

Ten pakiet zawiera wersję skrośną generującą kod dla procesora Z80.

%prep
%setup -q -n binutils-%{version}
%patch0 -p1

%build
cp /usr/share/automake/config.sub .

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
%ifarch sparc
sparc32 \
%endif
./configure \
	--disable-shared \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--host=%{_target_platform} \
	--build=%{_target_platform} \
	--target=%{target} \
	--with-gnu-ld \
	--with-gnu-as \
	--enable-install-libbfd

# We have to regenerate headers after patching.
%{__make} configure-host \
	tooldir=%{_prefix} \
	EXEEXT=""

%{__make} -C bfd headers \
	tooldir=%{_prefix} \
	EXEEXT=""

%{__make} all \
	tooldir=%{_prefix} \
	EXEEXT=""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{*dlltool,*nlmconv,*windres}.1

rm -f $RPM_BUILD_ROOT%{_datadir}/locale/*/LC_MESSAGES/*.mo
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a
rm -rf $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/%{target}-*
%dir %{arch}
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*
%dir %{arch}/lib
%dir %{arch}/lib/*
%{arch}/lib/*/*
%{_mandir}/man?/%{target}-*
