# The **sofs21** file system supporting software

******
******

## Prerequisites

On Ubuntu you need the following packages installed: 
_build-essential_, _cmake_, _doxygen_, _libfuse-dev_, and _git_.

```
sudo apt install build-essential cmake doxygen libfuse-dev git
```
In other Linux distributions you need equivalent packages installed.

******

## Cloning the repo

In a directory of your choice, clone the project to your computer

```
cd «directory-of-your-choice»
git clone https://to-be-defined/XXXX
```
where **XXXX** must be your project id.

******

## Preparing the compilation environment

In a terminal, enter the base directory of your project, create the **build** directory,
and use _cmake_ to prepare _make_

```
cd «directory-of-your-choice»
cd XXXX
mkdir build
cd build
cmake ../src
```

If you prefer _ninja_, instead of _make_,

```
cd «directory-of-your-choice»
cd XXXX
mkdir build
cd build
cmake -G Ninja ../src
```

******

## Compiling the code

In a terminal, enter the **build** directory of your project and run _make_ or _ninja_

```
cd «directory-of-your-choice»
cd XXXX/build
make
```
or

```
cd «directory-of-your-choice»
cd XXXX/build
ninja
```
******

## Generating documentation

The code is documented in **doxygen**. So, you can easily generate **html** documentation pages.

```
cd «directory-of-your-choice»
cd XXXX/doc
doxygen
```
Then, you can display the pages running (inside the **doc** directory)

```
firefox html/index.html &
```

Of course, you can replace _firefox_ with your favourite browser.

******

## Editable source files

When editing your code, take into attention the following:

- Folder **src/grp_src** is the only one containing source code to be edited by the groups.

- Only files with termination **.cpp** are to be edited.

- There is a single function per file, with the exception of proposals for internal auxiliary functions in some cases.

- Please do not change the signature of the functions, nor delete the call to soProbe.

- Any changes to the other files can produce indesirable behavior during our tests, since we will use our version of them.

******

## Testing the code

The following sequence of commands, where XXXX is your project's id, allows you to create a support file and format it as a **sofs21** file system

```
cd «directory-of-your-choice»
cd XXXX/bin
./createDisk /tmp/dsk 1000      # /tmp/dsk will be a disk with 1000 blocks
./mksofs /tmp/dsk               # format the disk as a sofs21 file system
```
Now, you can use the _showblock_ application to see its contents.
For instance

```
./showblock /tmp/dsk -s 0
```
prints the superblock. Use option -h to see other options.

You can also, create a directory or use an existing one to mount the disk in that directory.

```
mkdir /tmp/mnt                  # our mount point
./sofsmount /tmp/dsk /tmp/mnt   # mount the disk in the mount point
```
Now, everything created inside the mount point will be stored in disk (the /tmp/dsk file). You can use the **showblock** tool to check that out.

******

## Script files

We encourage the use o bash script functions to facilitate the test of the code.
In folder **scripts**, a set of files, containing bash functions, exists to facilitate the test.

- **sofs21.sh** is the entry point, creating some required environment variables and sourcing the other script files.

- **msg.sh** just declare 3 auxiliary functions.

- **basic.sh** declare functions to create a sofs21 disk \(c), format it (f), call the showblock tool (s), call the testtool tool (tt), and build your code (m).

- **tt-tools.sh** declare functions interfacing with the testool. These are incomplete.

To activate these functions, on a terminal, just execute command **source «path-to-sofs21.sh»**, where «path-to-sofs21.sh» is a absolute or relative path to file **sofs21.sh**.
For instance, if you are in the base directory of the project

```
source scripts/sofs21.sh
```
As an example:

```
m         # go to the build directory and run make
c         # creates a disk with 1000 blocks (file /tmp/dsk)
f         # format the disk
s -s 0    # shows the superblock
s -i 1    # shows the first block of the inode table
s -h      # shows a help menu
```
no matter the directory where they are executed.


## Authors
[André Clérigo](https://github.com/andreclerigo)  
[Cláudio Asensio](https://github.com/ClaudioAsensio)  
[Diogo Jesus](https://github.com/diogopjesus)  
[Miguel Tavares](https://github.com/FastMiguel099)  
[Tiago Marques](https://github.com/Tiagura)  
[Pedro Rodrigues](https://github.com/pedromtrodrigues)  
