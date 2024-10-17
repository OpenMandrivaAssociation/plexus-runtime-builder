# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global parent plexus
%global subname runtime-builder

Name:           %{parent}-%{subname}
Version:        1.0
Release:        0.6.a9
Summary:        Plexus Component Descriptor Creator
License:        MIT
Group:          Development/Java
URL:            https://plexus.codehaus.org/
# svn export svn://svn.plexus.codehaus.org/plexus/tags/plexus-runtime-builder-1.0-alpha-9 plexus-runtime-builder/
# tar czf plexus-runtime-builder-1.0-alpha-9.tar.gz plexus-runtime-builder/
Source0:        %{name}-src.tar.gz
Patch0:         0001-Fix-ArtifactResolutionException.patch

BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  apache-commons-codec
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  maven2 >= 2.0.4
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-release-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven2-common-poms
BuildRequires:  maven-wagon
BuildRequires:  plexus-appserver
BuildRequires:  plexus-archiver
BuildRequires:  plexus-container-default
BuildRequires:  plexus-utils
BuildRequires:  plexus-velocity
BuildRequires:  plexus-xmlrpc
BuildRequires:  tomcat6-servlet-2.5-api
BuildRequires:  velocity
BuildRequires:  xmlrpc

Requires:       apache-commons-codec
Requires:       jakarta-commons-httpclient
Requires:       maven2-common-poms
Requires:       maven-wagon
Requires:       plexus-appserver
Requires:       plexus-archiver
Requires:       plexus-container-default
Requires:       plexus-utils
Requires:       plexus-velocity
Requires:       plexus-xmlrpc
Requires:       velocity
Requires:       xmlrpc

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2


%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}

%patch0 -p1 -b .sav

%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

# FIXME: Ignoring text failures for now
# this is due to fact that test ignore artifact in local repo for some reason
mvn-jpp -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 target/*.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{parent}/%{subname}.jar
%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/%{parent} %{subname}
%add_to_maven_depmap plexus %{name} %{version} JPP/%{parent} %{subname}

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml \
  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-%{subname}.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}

cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}


%post
%update_maven_depmap

%postun
%update_maven_depmap

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%files
%defattr(-,root,root,-)
%{_javadir}/plexus
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*


