## Virtual file systems
POSIX systems, such as Linux and Mac OSX (which is based on BSD) include several virtual filesystems that are mounted (available) as part of the file-system. Files inside these virtual filesystems do not exist on the disk; they are generated dynamically by the kernel when a process requests a directory listing.
Linux provides 3 main virtual filesystems
```
/dev  - A list of physical and virtual devices (for example network card, cdrom, random number generator)
/proc - A list of resources used by each process and (by tradition) set of system information
/sys - An organized list of internal kernel entities
```
## How do I find out what filesystems are currently available (mounted)?
Use `mount`
Using mount without any options generates a list (one filesystem per line) of mounted filesystems including networked, virtual and local (spinning disk / SSD-based) filesystems. Here is a typical output of mount

```
$ mount
/dev/mapper/cs241--server_sys-root on / type ext4 (rw)
proc on /proc type proc (rw)
sysfs on /sys type sysfs (rw)
devpts on /dev/pts type devpts (rw,gid=5,mode=620)
tmpfs on /dev/shm type tmpfs (rw,rootcontext="system_u:object_r:tmpfs_t:s0")
/dev/sda1 on /boot type ext3 (rw)
/dev/mapper/cs241--server_sys-srv on /srv type ext4 (rw)
/dev/mapper/cs241--server_sys-tmp on /tmp type ext4 (rw)
/dev/mapper/cs241--server_sys-var on /var type ext4 (rw)rw,bind)
/srv/software/Mathematica-8.0 on /software/Mathematica-8.0 type none (rw,bind)
engr-ews-homes.engr.illinois.edu:/fs1-homes/angrave/linux on /home/angrave type nfs (rw,soft,intr,tcp,noacl,acregmin=30,vers=3,sec=sys,sloppy,addr=128.174.252.102)
```
Notice that each line includes the filesystem type source of the filesystem and mount point.
To reduce this output we can pipe it into `grep` and only see lines that match a regular expression. 
```
>mount | grep proc  # only see lines that contain 'proc'
proc on /proc type proc (rw)
none on /proc/sys/fs/binfmt_misc type binfmt_misc (rw)
```

##Todo
```
$ sudo mount /dev/cdrom /media/cdrom
$ mount
$ mount | grep proc
```
Examples of virtual files in /proc:
```
$ cat /proc/sys/kernel/random/entropy_avail
$ hexdump /dev/random
$ hexdump /dev/urandom
```

##Differences between random and urandom?  
/dev/random is a file which contains pseudorandom number generator where the entropy is determined from environmental noise. Random is will block/wait until enough entropy is collected from the environment. 
 
/dev/urandom is like random, but differs in the fact that it allows for repetition (lower entropy threshold), thus wont block.

```
$ cat /proc/meminfo
$ cat /proc/cpuinfo
$ cat /proc/cpuinfo | grep bogomips

$ cat /proc/meminfo | grep Swap

$ cd /proc/self
$ echo $$; cd /proc/12345; cat maps
```
## How do I mount a disk image?
Suppose you had downloaded a bootable linux disk image...
```
wget http://cosmos.cites.illinois.edu/pub/archlinux/iso/2014.11.01/archlinux-2014.11.01-dual.iso
```
Before putting the filesystem on a CD, we can mount the file as a filesystem and explore its contents. Note, mount requires root access, so let's run it using sudo
```
$ mkdir arch
$ sudo mount -o loop archlinux-2014.11.01-dual.iso ./arch
$ cd arch
```
Before the mount command, the arch directory is new and obviously empty. After mounting, the contents of `arch/` will be drawn from the files and directories stored in the filesystem stored inside the `archlinux-2014.11.01-dual.iso` file.
The `loop` option is required because we want to mount a regular file not a block device such as a physical disk. 

The loop option wraps the original file as a block device - in this example we will find out below that the file system is provided under `/dev/loop0` : We can check the filesystem type and mount options by running the mount command without any parameters. We will pipe the output into `grep` so that we only see the relevant output line(s) that contain 'arch'
```
$ mount | grep arch
/home/demo/archlinux-2014.11.01-dual.iso on /home/demo/arch type iso9660 (rw,loop=/dev/loop0)
```
The iso9660 filesystem is a read-only filesystem originally designed for optical storage media (i.e. CDRoms). Attempting to change the contents of the filesystem will fail
```
$ touch arch/nocando
touch: cannot touch `/home/demo/arch/nocando': Read-only file system
```

