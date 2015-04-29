%define __jar_repack %{nil}

%define storm_user storm
%define storm_group storm
%define storm_user_home %{_var}/lib/storm
%define storm_home %{_prefix}/lib/storm
%define storm_log_dir %{_var}/log/storm
%define storm_pid_dir %{_var}/run/storm

Name:          storm
Version:       0.9.4
Release:       4%{dist}
BuildArch:     noarch
Summary:       Apache Storm Complex Event Processing    
Group:         Applications/Internet
License:       Apache License Version 2.0
URL:           https://storm.apache.org/
Source:        http://www.apache.org/dyn/closer.cgi/storm/apache-storm-0.9.4/apache-storm-0.9.4.tar.gz
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(pre): shadow-utils
Requires:      %{name}-conf = %{version}-%{release}
Source1:       init-storm
Source2:       sysconfig-storm
Source3:       storm.yaml
Source4:       logback.xml

%description
Storm is a distributed realtime computation system.
Similar to how Hadoop provides a set of general primitives for doing batch processing,
Storm provides a set of general primitives for doing realtime computation. Storm is simple,
can be used with any programming language, is used by many companies, and is a lot of fun to use!

Storm integrates with the queueing and database technologies you already use.
A Storm topology consumes streams of data and processes those streams in arbitrarily complex
ways, repartitioning the streams between each stage of the computation however needed.


%package conf
Summary: Apache Storm Configuration Files
Group:   Applications/Internet

%description conf
Configuration files for Apache Storm


%package examples
Summary:  Apache Storm Examples
Group:    Applications/Internet
Requires: %{name} = %{version}-%{release}

%description examples
storm-starter contains a variety of examples of using Storm.
If this is your first time working with Storm, check out these topologies first.


%package logviewer
Summary:  Apache Storm Logviewer
Group:    Applications/Internet
Requires: %{name} = %{version}-%{release}
Requires: %{name}-supervisor = %{version}-%{release}

%description logviewer
With the log viewer, you can easily access a specific worker's log in a web browser 
by clicking on a worker's port number right from Storm UI.
The logviewer daemon runs as a separate process on Storm supervisor nodes.


%package nimbus
Summary:  Apache Storm Nimbus
Group:    Applications/Internet
Requires: %{name} = %{version}-%{release}

%description nimbus
Communicate with Nimbus to submit code (packaged as a jar) and topologies for execution on the cluster.
Nimbus will take care of distributing that code around the cluster and assigning workers to run the topology.


%package supervisor
Summary:  Apache Storm Supervisor
Group:    Applications/Internet
Requires: %{name} = %{version}-%{release}

%description supervisor
The supervisor daemon is responsible for starting and stopping worker processes on that machine.


%package ui
Summary:  Apache Storm UI
Group:    Applications/Internet
Requires: %{name} = %{version}-%{release}

%description ui
The Storm UI - a site you can access from the browser that gives diagnostics on the cluster and topologies.


%prep
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%setup -q -n apache-%{name}-%{version}

# This SPEC build is only packaging
%build

%install
# Create the appropriate directories
%{__mkdir_p} %{buildroot}%{storm_home}
%{__mkdir_p} %{buildroot}%{storm_home}/init
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir_p} %{buildroot}%{_initddir}
%{__mkdir_p} %{buildroot}%{storm_pid_dir}
%{__mkdir_p} %{buildroot}%{_var}/lib/storm
%{__mkdir_p} %{buildroot}%{storm_log_dir}
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}-%{version}
%{__mkdir_p} %{buildroot}%{_bindir}

# Copy the storm files to the right places
%{__cp} -R * %{buildroot}%{storm_home}/.
%{__cp} %{SOURCE1} %{buildroot}%{storm_home}/init/init-storm
%{__cp} %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/storm
%{__cp} %{SOURCE3} %{buildroot}%{storm_home}/conf/storm.yaml
%{__cp} %{SOURCE4} %{buildroot}%{storm_home}/logback/cluster.xml
%{__mv} %{buildroot}%{storm_home}/{CHANGELOG.md,DISCLAIMER,LICENSE,NOTICE,README.markdown,SECURITY.md} %{buildroot}%{_docdir}/%{name}-%{version}/.

# Make convenient symlinks
%{__ln_s} -f %{storm_home}/logback %{buildroot}%{storm_home}/conf/logback
%{__ln_s} -f %{storm_home}/conf %{buildroot}%{_sysconfdir}/storm
%{__ln_s} -f %{storm_home}/bin/storm %{buildroot}%{_bindir}/storm
%{__ln_s} -f %{storm_log_dir} %{buildroot}%{storm_home}/logs
%{__ln_s} -f %{storm_pid_dir} %{buildroot}%{storm_home}/pids
%{__ln_s} -f %{storm_home}/init/init-storm %{buildroot}%{_initddir}/storm-logviewer
%{__ln_s} -f %{storm_home}/init/init-storm %{buildroot}%{_initddir}/storm-nimbus
%{__ln_s} -f %{storm_home}/init/init-storm %{buildroot}%{_initddir}/storm-supervisor
%{__ln_s} -f %{storm_home}/init/init-storm %{buildroot}%{_initddir}/storm-ui

# Edit config files for environment
%{__sed} -i "s,__STORM_USER__,%{storm_user},g" %{buildroot}%{_sysconfdir}/sysconfig/storm
%{__sed} -i "s,__STORM_HOME__,%{storm_home},g" %{buildroot}%{_sysconfdir}/sysconfig/storm
%{__sed} -i "s,__LOG_DIR__,%{storm_log_dir},g" %{buildroot}%{_sysconfdir}/sysconfig/storm
%{__sed} -i "s,__LOCAL_DIR__,%{storm_user_home},g" %{buildroot}%{storm_home}/conf/storm.yaml


%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%pre
getent group %{storm_group} >/dev/null || groupadd -r %{storm_group}
getent passwd %{storm_user} >/dev/null || /usr/sbin/useradd --comment="Apache Storm User" -M -r -g %{storm_group} --home %{storm_user_home} %{storm_user}

%files
%defattr(-,root,root,-)
%attr(-,%{storm_user},%{storm_group}) %{storm_user_home}
%attr(-,%{storm_user},%{storm_group}) %{storm_pid_dir}
%docdir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}
%dir %{storm_home}
%{storm_home}/RELEASE
%{storm_home}/bin
%{storm_home}/external
%{storm_home}/lib
%attr(755,root,root) %{storm_home}/init
%{storm_home}/logs
%{storm_home}/pids
%attr(755,-,-) %{_bindir}/storm
%attr(-,%{storm_user},%{storm_group}) %{storm_log_dir}


%files conf
%defattr(644,%{storm_user},%{storm_group},755)
%config %{_sysconfdir}/sysconfig/storm
%config %{_sysconfdir}/storm
%config %{storm_home}/conf
%config %{storm_home}/logback


%files examples
%defattr(-,root,root,-)
%{storm_home}/examples


%files logviewer
%defattr(755,root,root,-)
%{_initddir}/storm-logviewer


%files nimbus
%defattr(755,root,root,-)
%attr(755,-,-) %{_initddir}/storm-nimbus


%files supervisor
%defattr(755,root,root,-)
%attr(755,-,-) %{_initddir}/storm-supervisor


%files ui
%defattr(-,root,root,-)
%{storm_home}/public
%attr(755,-,-) %{_initddir}/storm-ui


%changelog
* Tue Apr 28 2015 Corey Shaw <corey.shaw@gmail.com> 0.9.4-1
- First build of SPEC
