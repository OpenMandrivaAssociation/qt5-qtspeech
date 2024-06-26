%define major 5
%define libname %mklibname qtspeech %{major}
%define devname %mklibname qtspeech -d
%define beta %{nil}

Name: qt5-qtspeech
Version:	5.15.14
%if "%{beta}" != "%{nil}"
%define qttarballdir qtspeech-everywhere-src-%{version}-%{beta}
Source0: http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
Release:	0.%{beta}.1
%else
%define qttarballdir qtspeech-everywhere-opensource-src-%{version}
Source0: http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
Release:	1
%endif
Source100: %{name}.rpmlintrc
# From KDE
Patch1001:	0001-Reverse-list-of-voices-before-returning-from-Speech-.patch
Summary: Qt text to speech library
URL: https://github.com/qtproject/qtspeech
License: LGPL-2.1-with-Qt-Company-Qt-exception-1.1 or LGPL-3.0-with-Qt-Company-Qt-exception-1.1
Group: System/Libraries
BuildRequires: qmake5
BuildRequires: pkgconfig(speech-dispatcher)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: qt5-qtdoc
BuildRequires: qt5-qttools
BuildRequires: qdoc5 qt5-doc qt5-assistant
# For the Provides: generator
BuildRequires: cmake >= 3.11.0-1

%description
Qt text to speech library.

%package -n %{libname}
Summary: Qt text to speech library
Group: System/Libraries

%description -n %{libname}
Qt text to speech library.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package examples
Summary: Example code for the %{name} library
Group: Development/C
Requires: %{devname} = %{EVRD}
BuildRequires: pkgconfig(Qt5Widgets)

%description examples
Example code for the %{name} library.

%prep
%autosetup -n %(echo %{qttarballdir}|sed -e 's,-opensource,,') -p1
rm examples/*.pro

%{_libdir}/qt5/bin/syncqt.pl \
	-version %{version} \
	-module QtTextToSpeech

%qmake_qt5 *.pro


%build
%make_build
%make_build docs

%install
%make_install install_docs INSTALL_ROOT="%{buildroot}"
find "%{buildroot}" -type f -name '*.prl' -exec sed -i -e '/^QMAKE_PRL_BUILD_DIR/d' {} \;

mv examples %{buildroot}%{_libdir}/qt5/

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/qt5/plugins/texttospeech

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/Qt5TextToSpeech
%{_libdir}/qt5/mkspecs/modules/*.pri
%{_libdir}/*.prl
%doc %{_docdir}/qt5/qtspeech
%doc %{_docdir}/qt5/qtspeech.qch

%files examples
%{_libdir}/qt5/examples/speech
