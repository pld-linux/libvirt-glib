#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
%bcond_without	vala		# Vala binding

Summary:	GLib wrapper for libvirt library
Summary(pl.UTF-8):	Wrapper GLib dla biblioteki libvirt
Name:		libvirt-glib
Version:	5.0.0
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.libvirt.org/glib/%{name}-%{version}.tar.xz
# Source0-md5:	2e36b42b91bb98fac22321b5afc5a835
URL:		https://libvirt.org/
BuildRequires:	gcc >= 6:4.8
BuildRequires:	glib2-devel >= 1:2.48.0
BuildRequires:	gobject-introspection-devel >= 1.36.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libvirt-devel >= 2.3.0
BuildRequires:	libxml2-devel >= 1:2.9.1
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 0.13}
BuildRequires:	xz
Requires:	glib2 >= 1:2.48.0
Requires:	libvirt >= 2.3.0
Requires:	libxml2 >= 1:2.9.1
Obsoletes:	python-libvirt-glib < 1
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
Requires:	glib2-devel >= 1:2.48.0
Requires:	libvirt-devel >= 2.3.0
Requires:	libxml2-devel >= 1:2.9.1

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
BuildArch:	noarch

%description apidocs
API documentation for libvirt-glib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libvirt-glib.

%package -n vala-libvirt-glib
Summary:	libvirt-glib API for Vala language
Summary(pl.UTF-8):	API libvirt-glib dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
BuildArch:	noarch

%description -n vala-libvirt-glib
libvirt-glib API for Vala language.

%description -n vala-libvirt-glib -l pl.UTF-8
API libvirt-glib dla języka Vala.

%prep
%setup -q

%if %{with static_libs}
%{__sed} -i -e '/^libvirt_gconfig = / s/shared_library/library/' libvirt-gconfig/meson.build
%{__sed} -i -e '/^libvirt_glib = / s/shared_library/library/' libvirt-glib/meson.build
%{__sed} -i -e '/^libvirt_gobject = / s/shared_library/library/' libvirt-gobject/meson.build
%endif

%{__sed} -i -e "s/datadir, 'gtk-doc'/datadir, 'doc', 'gtk-doc'/" docs/libvirt-{gconfig,glib,gobject}/meson.build

%build
%meson build \
	%{!?with_apidocs:-Ddocs=disabled}
	%{!?with_vala:-Dvapi=disabled}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
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
%{_datadir}/vala/vapi/libvirt-gconfig-1.0.deps
%{_datadir}/vala/vapi/libvirt-gconfig-1.0.vapi
%{_datadir}/vala/vapi/libvirt-glib-1.0.deps
%{_datadir}/vala/vapi/libvirt-glib-1.0.vapi
%{_datadir}/vala/vapi/libvirt-gobject-1.0.deps
%{_datadir}/vala/vapi/libvirt-gobject-1.0.vapi
%endif
