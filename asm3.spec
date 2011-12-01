%define gcj_support     0
%define section         free

Name:           asm3
Version:        3.2
Release:        %mkrel 0.0.7
Epoch:          0
Summary:        Code manipulation tool to implement adaptable systems
License:        BSD-style
URL:            http://asm.objectweb.org/
Group:          Development/Java
Source0:        http://download.fr2.forge.objectweb.org/asm/asm-%{version}.tar.gz
Source1:		asm-3.0.pom
Source2:		asm-analysis-3.0.pom
Source3:		asm-commons-3.0.pom
Source4:		asm-tree-3.0.pom
Source5:		asm-util-3.0.pom
Source6:		asm-xml-3.0.pom
Source7:		asm-MANIFEST.MF
BuildRequires:  ant
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  objectweb-anttask
BuildRequires:  zip
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ASM is a code manipulation tool to implement adaptable systems.

%package        javadoc
Summary:        Javadoc for %{name}
Group:                Development/Java

%description        javadoc
Javadoc for %{name}.

%prep
%setup -q -n asm-%{version}
%{__mkdir_p} test/lib
%{__perl} -pi -e 's|.*<attribute name="Class-path".*||' archive/asm-xml.xml

%build
export CLASSPATH=:
export OPT_JAR_LIST=:
%{ant} -Dobjectweb.ant.tasks.path=$(build-classpath objectweb-anttask) jar jdoc

# inject OSGi manifests
mkdir -p META-INF
cp %{SOURCE7} META-INF/MANIFEST.MF
zip -u output/dist/lib/all/asm-all-%{version}.jar META-INF/MANIFEST.MF

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}/%{name}

for jar in output/dist/lib/*.jar; do
newjar=${jar/asm-/%{name}-}
%{__install} -m 644 ${jar} \
%{buildroot}%{_javadir}/%{name}/`basename ${newjar}`
done

install -m 644 output/dist/lib/all/asm-all-%{version}.jar \
%{buildroot}%{_javadir}/%{name}/asm-all-%{version}.jar

(cd %{buildroot}%{_javadir}/%{name} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

#poms
%add_to_maven_depmap asm asm %{version} JPP/asm3 asm3
%add_to_maven_depmap asm asm-util %{version} JPP/asm3 asm3-util
%add_to_maven_depmap asm asm-analysis %{version} JPP/asm3 asm3-analysis
%add_to_maven_depmap asm asm-commons %{version} JPP/asm3 asm3-commons
%add_to_maven_depmap asm asm-tree %{version} JPP/asm3 asm3-tree
%add_to_maven_depmap asm asm-xml %{version} JPP/asm3 asm3-xml

install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 %{SOURCE1} \
    %{buildroot}%{_datadir}/maven2/poms/JPP.asm.pom
install -pm 644 %{SOURCE2} \
    %{buildroot}%{_datadir}/maven2/poms/JPP.asm-util.pom
install -pm 644 %{SOURCE3} \
    %{buildroot}%{_datadir}/maven2/poms/JPP.asm-analysis.pom
install -pm 644 %{SOURCE4} \
    %{buildroot}%{_datadir}/maven2/poms/JPP.asm-commons.pom
install -pm 644 %{SOURCE5} \
    %{buildroot}%{_datadir}/maven2/poms/JPP.asm-tree.pom
install -pm 644 %{SOURCE6} \
    %{buildroot}%{_datadir}/maven2/poms/JPP.asm-xml.pom

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a output/dist/doc/javadoc/user/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%{gcj_compile}

# fix end-of-line
%{__perl} -pi -e 's/\r$//g' README.txt

%clean
%{__rm} -rf %{buildroot}

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc README.txt
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%{_datadir}/maven2/poms/*
%config(noreplace) %{_mavendepmapfragdir}/*
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%dir %{_javadocdir}/%{name}

