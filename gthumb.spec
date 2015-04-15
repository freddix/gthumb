Summary:	An image viewer and browser for GNOME
Name:		gthumb
Version:	3.4.0
Release:	1
License:	GPL v2
Vendor:		GNOME
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/pub/gnome/sources/gthumb/3.4/%{name}-%{version}.tar.xz
# Source0-md5:	c920d76705094141a339c97b9df8d3e7
URL:		http://live.gnome.org/gthumb
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk+-update-icon-cache
BuildRequires:	gtk+3-devel
BuildRequires:	intltool
BuildRequires:	libexif-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libgphoto2-devel
BuildRequires:	libiptcdata-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libraw-devel
BuildRequires:	libsoup-gnome-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libwebp-devel
BuildRequires:	libxml2-devel
BuildRequires:	xorg-libXtst-devel
BuildRequires:	xorg-libXxf86vm-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires:	gsettings-desktop-schemas
Suggests:	brasero
Suggests:	dcraw
Suggests:	gstreamer-plugins-base
Suggests:	gstreamer-plugins-good
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gThumb lets you browse your hard disk, showing you thumbnails of image
files. It also lets you view single files (including GIF animations),
add comments to images, organize images in catalogs, print images,
view slideshows, set your desktop background, and more.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-clutter		\
	--disable-libbrasero		\
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/GConf
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}

gtk-update-icon-cache -ft $RPM_BUILD_ROOT%{_datadir}/%{name}/icons/hicolor

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/extensions
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/%{name}/extensions/*.so
%{_libdir}/%{name}/extensions/*.extension
%{_datadir}/gthumb
%{_datadir}/glib-2.0/schemas/*.xml
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/*/apps/*.svg
%{_mandir}/man1/gthumb.1*

