#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_without	vala		# Vala binding
#
Summary:	GLib wrapper for libvirt library
Summary(pl.UTF-8):	Wrapper GLib dla biblioteki libvirt
Name:		libvirt-glib
Version:	0.0.8
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	ftp://libvirt.org/libvirt/glib/%{name}-%{version}.tar.gz
# Source0-md5:	cc0913fdf1011558e81e7de4b00c7d1f
Patch0:		%{name}-pc.patch
URL:		http://www.libvirt.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	gobject-introspection-devel >= 0.10.8
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	libtool
BuildRequires:	libvirt-devel >= 0.9.10
BuildRequires:	libxml2-devel >= 2.0.0
BuildRequires:	pkgconfig
%{?with_vala:BuildRequires:	vala >= 0.13}
Requires:	glib2 >= 1:2.22.0
Requires:	libvirt >= 0.9.10
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
Requires:	glib2-devel >= 1:2.22.0
Requires:	libvirt-devel >= 0.9.10
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

%description apidocs
API documentation for libvirt-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libvirt-glib.

%package -n python-libvirt-glib
Summary:	Python bindings for libvirt-glib library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libvirt-glib
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-libvirt-glib
Python bindings for libvirt-glib library.

%description -n python-libvirt-glib -l pl.UTF-8
Wiązania Pythona do biblioteki libvirt-glib.

%package -n vala-libvirt-glib
Summary:	libvirt-glib API for Vala language
Summary(pl.UTF-8):	API libvirt-glib dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description -n vala-libvirt-glib
libvirt-glib API for Vala language.

%description -n vala-libvirt-glib -l pl.UTF-8
API libvirt-glib dla języka Vala.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir} \
	%{__enable_disable apidocs gtk-doc} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.{a,la}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
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

%files -n python-libvirt-glib
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/libvirtglibmod.so
%{py_sitedir}/libvirtglib.py[co]

%if %{with vala}
%files -n vala-libvirt-glib
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libvirt-gconfig-1.0.vapi
%{_datadir}/vala/vapi/libvirt-glib-1.0.vapi
%{_datadir}/vala/vapi/libvirt-gobject-1.0.deps
%{_datadir}/vala/vapi/libvirt-gobject-1.0.vapi
%endif
