#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_without	vala		# Vala binding

Summary:	GLib wrapper for libvirt library
Summary(pl.UTF-8):	Wrapper GLib dla biblioteki libvirt
Name:		libvirt-glib
Version:	2.0.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	ftp://libvirt.org/libvirt/glib/%{name}-%{version}.tar.gz
# Source0-md5:	b470b5524c29b61a8ce8e0d094e6c835
URL:		http://www.libvirt.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gobject-introspection-devel >= 1.36.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libvirt-devel >= 1.2.8
BuildRequires:	libxml2-devel >= 2.0.0
BuildRequires:	pkgconfig
%{?with_vala:BuildRequires:	vala >= 0.13}
Requires:	glib2 >= 1:2.36.0
Requires:	libvirt >= 1.2.8
Obsoletes:	python-libvirt-glib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GLib wrapper for libvirt library.

%description -l pl.UTF-8
Wrapper GLib dla biblioteki libvirt.

%package devel
Summary:	Header files for libvirt-glib library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libvirt-glib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36.0
Requires:	libvirt-devel >= 0.10.2
Requires:	libxml2-devel >= 2.0.0

%description devel
Header files for libvirt-glib library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libvirt-glib.

%package static
Summary:	Static libvirt-glib library
Summary(pl.UTF-8):	Statyczna biblioteka libvirt-glib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libvirt-glib library.

%description static -l pl.UTF-8
Statyczna biblioteka libvirt-glib.

%package apidocs
Summary:	libvirt-glib API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libvirt-glib
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libvirt-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libvirt-glib.

%package -n vala-libvirt-glib
Summary:	libvirt-glib API for Vala language
Summary(pl.UTF-8):	API libvirt-glib dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-libvirt-glib
libvirt-glib API for Vala language.

%description -n vala-libvirt-glib -l pl.UTF-8
API libvirt-glib dla języka Vala.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libvirt-gconfig-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirt-gconfig-1.0.so.0
%attr(755,root,root) %{_libdir}/libvirt-glib-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirt-glib-1.0.so.0
%attr(755,root,root) %{_libdir}/libvirt-gobject-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirt-gobject-1.0.so.0
%{_libdir}/girepository-1.0/LibvirtGConfig-1.0.typelib
%{_libdir}/girepository-1.0/LibvirtGLib-1.0.typelib
%{_libdir}/girepository-1.0/LibvirtGObject-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvirt-gconfig-1.0.so
%attr(755,root,root) %{_libdir}/libvirt-glib-1.0.so
%attr(755,root,root) %{_libdir}/libvirt-gobject-1.0.so
%{_datadir}/gir-1.0/LibvirtGConfig-1.0.gir
%{_datadir}/gir-1.0/LibvirtGLib-1.0.gir
%{_datadir}/gir-1.0/LibvirtGObject-1.0.gir
%{_includedir}/libvirt-gconfig-1.0
%{_includedir}/libvirt-glib-1.0
%{_includedir}/libvirt-gobject-1.0
%{_pkgconfigdir}/libvirt-gconfig-1.0.pc
%{_pkgconfigdir}/libvirt-glib-1.0.pc
%{_pkgconfigdir}/libvirt-gobject-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libvirt-gconfig-1.0.a
%{_libdir}/libvirt-glib-1.0.a
%{_libdir}/libvirt-gobject-1.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/Libvirt-gconfig
%{_gtkdocdir}/Libvirt-glib
%{_gtkdocdir}/Libvirt-gobject
%endif

%if %{with vala}
%files -n vala-libvirt-glib
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libvirt-gconfig-1.0.vapi
%{_datadir}/vala/vapi/libvirt-glib-1.0.vapi
%{_datadir}/vala/vapi/libvirt-gobject-1.0.deps
%{_datadir}/vala/vapi/libvirt-gobject-1.0.vapi
%endif
