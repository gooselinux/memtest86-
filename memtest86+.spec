%bcond_with update_grub

# Prevent stripping
%define __spec_install_post /usr/lib/rpm/brp-compress
# Turn off debuginfo package
%define debug_package %{nil}

Name:     memtest86+
Version:  4.00
Release:  2%{?dist}
License:  GPLv2
Summary:  Stand-alone memory tester for x86 and x86-64 computers
Group:    System Environment/Base
Source0:  http://www.memtest.org/download/%{version}/%{name}-%{version}.tar.gz
Source1:  memtest-setup
Source2:  new-memtest-pkg
URL:      http://www.memtest.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# require glibc-devel.i386 via this file:
BuildRequires: %{_includedir}/gnu/stubs-32.h
BuildRequires: compat-gcc-34
Requires: /sbin/grubby sed coreutils
ExclusiveArch: %{ix86} x86_64

%description
Memtest86+ is a thorough stand-alone memory test for x86 and x86-64 
architecture computers. BIOS based memory tests are only a quick 
check and often miss many of the failures that are detected by 
Memtest86+.

The ELF version should be used for booting from grub,
and avoids the following errors:
"Error 7: Loading below 1MB is not supported"
"Error 13: Invalid or unsupported executable format"
"Error 28: Selected item cannot fit into memory"

The script '%{_sbindir}/memtest-setup' can be run (as root)
to add the %{name} entry to your GRUB boot menu.

%prep
%setup -q 
sed -i -e's,0x10000,0x100000,' memtest.lds

%build
# Regular build flags not wanted for this binary
# Note: i486 minimum runtime arch
# It makes no sense to use smp flags here.
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/boot
mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}%{_sbindir}

# the ELF (memtest) version.
install -m644 memtest %{buildroot}/boot/elf-%{name}-%{version}

# the floppy (memtest.bin) version.
install -m644 memtest.bin %{buildroot}/boot/%{name}-%{version}

install -m755 %{SOURCE2} %{buildroot}/sbin/new-memtest-pkg
install -m755 %{SOURCE1} %{buildroot}%{_sbindir}/memtest-setup
sed -i 's/\r//' $RPM_BUILD_DIR/%{name}-%{version}/README

%if %{with update_grub}
%post -p /usr/sbin/memtest-setup
%endif

%preun
sed -i -e's,kernel --type=netbsd /elf-%{name}-%{version},kernel /elf-%{name}-%{version},' /boot/grub/grub.conf
/sbin/new-memtest-pkg --remove %{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
/boot/%{name}-%{version}
/boot/elf-%{name}-%{version}
/sbin/new-memtest-pkg
%{_sbindir}/memtest-setup


%changelog
* Tue Oct 13 2009 Jarod Wilson <jarod@redhat.com> - 4.00-2
- Fix memtest-setup on systems without a separate /boot
  filesystem (#528651)

* Tue Sep 29 2009 Jarod Wilson <jarod@redhat.com> - 4.00-1
- Update to new upstream release, v4.00
- Drop gcc4.2+ patch, merged upstream

* Mon Aug 17 2009 Jarod Wilson <jarod@redhat.com> - 2.11-11
- Fix runtime operation when built with gcc4.2+ (#442285)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 24 2009 Warren Togami <wtogami@redhat.com> - 2.11-9
- Fix uninstall to remove stanza from grub.conf

* Fri Apr 24 2009 Warren Togami <wtogami@redhat.com> - 2.11-8
- Bug #494157 rename elf binary so it doesn't accidentally copy the elf binary
  during livecd-creator
- Put scripts into CVS

* Sun Apr 05 2009 Paulo Roma <roma@lcg.ufrj.br> - 2.11-7
- adapted the spec file for building the elf and 
  the bin versions #494157

* Thu Apr 02 2009 Paulo Roma <roma@lcg.ufrj.br> - 2.11-6
- grub.conf will not be updated by default. The user
  will have to add and/or remove memtest86+ entries.
- No messages printed.

* Mon Mar 31 2009 Paulo Roma <roma@lcg.ufrj.br> - 2.11-5
- Changed postun for preun.
- Calling memtest-setup in case of updating grub.conf

* Mon Mar 11 2009 Paulo Roma <roma@lcg.ufrj.br> - 2.11-4
- Updated to 2.11
- Patched for booting from grub.
- Using memtest (ELF) instead of memtest.bin
- Changed memtest-setup for writing the correct grub entry.
- Removed obsolete patch memtest86+-2.10-fixflags.patch
- Created option update grub.conf

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 12 2008 Warren Togami <wtogami@redhat.com> - 2.10-1
- 2.10

* Thu Apr 03 2008 Warren Togami <wtogami@redhat.com> - 2.01-3
- Build with gcc34 for F9 (#437701)

* Tue Mar 04 2008 Peter Jones <pjones@redhat.com> - 2.01-2
- Don't install memtest86+ in bootloader configs on EFI platforms.

* Thu Feb 21 2008 Warren Togami <wtogami@redhat.com> - 2.01-1
- 2.01 major bugfix release

* Mon Feb 11 2008 Michal Schmidt <mschmidt@redhat.com> - 2.00-2
- forgot to cvs add the compilation patch.

* Mon Feb 11 2008 Michal Schmidt <mschmidt@redhat.com> - 2.00-1
- New upstream release: 2.00.
- Dropped boot time console configuration patches (already upstream).
- Fixed compilation on x86_64.

* Wed Oct 24 2007 Peter Jones <pjones@redhat.com> - 1.70-4
- Fix for mactel.

* Thu Oct 18 2007 Warren Togami <wtogami@redhat.com> - 1.70-3
- one more patch from mschmidt to allow configuration of parity and bits

* Wed Oct 17 2007 Warren Togami <wtogami@redhat.com> - 1.70-2
- mschmidt's boot time configuration of serial console (#319631)

* Thu Feb 08 2007 Florian La Roche <laroche@redhat.com> - 1.70-1
- update to 1.70

* Sat Feb 03 2007 Warren Togami <wtogami@redhat.com> - 1.65-6
- some spec cleanups (#226135)
- remove old Obsoletes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.65-4.1
- rebuild

* Tue Jun 27 2006 Florian La Roche <laroche@redhat.com> - 1.65-4
- make sure coreutils is installed for the preun script

* Thu Jun 08 2006 Jesse Keating <jkeating@redhat.com> - 1.65-3
- rebuilt for new buildsystem

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.65-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- make sure 32bit glibc-devel is installed (#170614)

* Sat Oct 01 2005 Warren Togami <wtogami@redhat.com> - 1.65-1
- 1.65

* Wed Jun 29 2005 Warren Togami <wtogami@redhat.com> - 1.60-1
- 1.60

* Mon Mar 28 2005 Warren Togami <wtogami@redhat.com> - 1.55.1-1
- 1.55.1 fixes K8

* Sun Mar 27 2005 Warren Togami <wtogami@redhat.com> - 1.55-1
- 1.55

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 19 2005 Warren Togami <wtogami@redhat.com> - 1.51-1
- 1.51

* Fri Jan 21 2005 Warren Togami <wtogami@redhat.com> - 1.50-1
- 1.50

* Sun Nov 28 2004 Warren Togami <wtogami@redhat.com> - 1.40-1
- 1.40
- remove arch patch, now upstream

* Tue Oct 26 2004 Warren Togami <wtogami@redhat.com> - 1.27-1
- 1.27

* Mon Oct 25 2004 Jeremy Katz <katzj@redhat.com> - 1.26-3
- allow building on all x86 arches
- pass appropriate compiler options to build on x86_64 as well (#136939)

* Wed Sep 02 2004 Warren Togami <wtogami@redhat.com> 1.26-1
- update to 1.26

* Sat Aug 28 2004 Warren Togami <wtogami@redhat.com> 1.25-1
- update to 1.25

* Mon Jun 28 2004 Warren Togami <wtogami@redhat.com>
- update to 1.20

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May 16 2004 Warren Togami <wtogami@redhat.com> 1.15-1
- update to 1.15

* Sun Feb 29 2004 Warren Togami <wtogami@redhat.com> 1.11-2
- switch to memtest86+ 1.11
- add boot loader setup script

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Oct 21 2003 Mike A. Harris <mharris@redhat.com> 3.0-3
- Pedantic spec file cleanups - s/Copyright/License/ and use _libdir instead of
  /usr/lib everywhere (even though it's currently x86 only)

* Tue Oct 21 2003 Jeremy Katz <katzj@redhat.com> 3.0-2
- fix perms (#107610)
- doesn't really require dev86 to build

* Thu Jul 21 2003 Michael Fulbright <msf@redhat.com>
- initial integration into distribution. Removed the scripts to install a
  entry in the boot loader for memtest for the moment, and relocated to under
  /usr/lib.

* Thu Apr 17 2003 Joe Szep <jszep@bu.edu>
- rebuilt for Doolittle final 

* Mon Feb  3 2003 Matthew Miller <mattdm@bu.edu>
- rebuild for doolittle
- patches to make build -- new gcc growing pains, I guess

* Tue Jul 30 2002 Matthew Miller <mattdm@bu.edu>
- added grubby stuff

* Tue Jul 30 2002 Dave Heistand <davidbh@bu.edu>
- updated source to v 3

* Thu Mar 7 2002 Dave Heistand <davidbh@bu.edu>
- updated source to 2.9, also changed setup -n
- to use %%{version}.

* Thu Nov  1 2001 Matthew Miller <mattdm@bu.edu>
- v 2.8a
- removed lilo-configuring scripts. need to figure out the best way to
  work with grub and RH 7.2 / BU Linux 2.5
- group -> System Environment/Base

* Mon Aug 20 2001 Matthew Miller <mattdm@bu.edu>
- v 2.7

* Wed Feb 14 2001 Matthew Miller <mattdm@bu.edu>
- v 2.5

* Fri Oct 06 2000 Matthew Miller <mattdm@bu.edu>
- v 2.4

* Thu Mar 23 2000 Matthew Miller <mattdm@bu.edu>
- changed so that lilo.conf isn't written if it already exists. This is
  important if you're including memtest86 in a distribution
- GPG key available from http://www.bu.edu/dsgsupport/linux/BULinux-GPG-KEY  
- changed name of lilo.conf backup file to something less likely to conflict
  with other backups

* Wed Mar 01 2000 Matthew Miller <mattdm@bu.edu>
- Updated to version 2.2
- Cosmetic changes to spec file
- updated Source: to reflect actual author's url

* Fri Dec 25 1998 Peter Soos <sp@osb.hu>

- Corrected the file attributes

* Mon Aug 17 1998 Peter Soos <sp@osb.hu>

- Moved to 1.4a

* Mon Jun 22 1998 Peter Soos <sp@osb.hu>

- Moved to 1.4

* Wed Dec 31 1997 Peter Soos <sp@osb.hu>

- Initial version
