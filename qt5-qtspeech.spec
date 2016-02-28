%define major 5
%define libname %mklibname qtspeech %{major}
%define devname %mklibname qtspeech -d

Name:	qt5-qtspeech
Version:5.5.0
Release: 1
Source0: qtspeech-%{version}.tar.xz
Source100: %{name}.rpmlintrc
Summary: Qt text to speech library
URL: https://github.com/qtproject/qtspeech
License: GPL
Group: System/Libraries
BuildRequires: qmake5
BuildRequires: pkgconfig(speech-dispatcher)
BuildRequires: pkgconfig(Qt5Core)

%description
Qt text to speech library

%package -n %{libname}
Summary: Qt text to speech library
Group: System/Libraries

%description -n %{libname}
Qt text to speech library

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
Example code for the %{name} library

%prep
%setup -qn qtspeech-%{version}
%{_libdir}/qt5/bin/syncqt.pl \
	-version %{version} \
	-private \
	-module QtTextToSpeech

%qmake_qt5 *.pro


%build
%make

%install
make install install_docs INSTALL_ROOT="%{buildroot}"
find "%{buildroot}" -type f -name '*.prl' -exec sed -i -e '/^QMAKE_PRL_BUILD_DIR/d' {} \;

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/Qt5TextToSpeech
%{_libdir}/qt5/mkspecs/modules/*.pri
%{_libdir}/*.prl

%files examples
%{_libdir}/qt5/examples/speech