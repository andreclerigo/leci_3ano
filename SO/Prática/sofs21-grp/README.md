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

where **XXXXX** must be your project id.

******

## Compiling the code

In a terminal, enter the **build** directory of your project

```
cd XXXXX/sofs21/build
```

Then compile the code

```
cmake ../src
make
```

If you prefer ninja, instead of make

```
cmake -G Ninja ../src
ninja
```

******

## Generating documentation

The code is documented in **doxygen**. So, you can easily generate **html** documentation pages.

```
cd XXXXX/sofs21/doc
doxygen
firefox html/index.html &
```

Of course, you can change firefox by your favourite browser.

******

## Editable source files

When editing your code, take into attention the following:

- Folder **src/grp_src** is the only one containing source code to be edited by the groups.

- Only files with termination **.cpp** are to be edited.

- There is a single function per file, with the exception of proposals for internal auxiliary functions in some cases.

- Please do not change the signature of the functions, nor delete the call to soProbe.

- We assume that only files with termination **.cpp** inside **src/grp_src** subfolders are editable by the groups. Thus, any changes to the other files can produce indesirable behavior during our tests, since we will use our version of them.

******

## Testing the code

The following sequence of commands, where XXXXX is your project's id, allows you to create a support file and format it as a **sofs** file system

```
cd XXXXX/sofs21/bin
./createDisk /tmp/dsk 1000      # /tmp/dsk will be a disk with 1000 blocks
./mksofs /tmp/dsk               # format the disk as a sofs21 file system
```
Now, you can use the _showblock_ application to see its contents. For instance,

```
./showblock /tmp/dsk -s 0
```
prints the superblock. Use option -h to see other options.

******

## Script files

We encourage the use o bash script functions to facilitate the test of your code.
In folder **scripts**, 3 files were added to propose an approach on how to create and use these functions:

- **sofs21.sh** is the entry point, creating some required environment variables and sourcing the other script files.

- **msg.sh** just declare 3 auxiliary functions.

- **basic.sh** declare functions to create a sofs21 disk \(c), format it (f), call the showblock tool (s), and build your code (m).

To activate these functions, just execute command **source «path-to-sofs21.sh»**, where «path-to-sofs21.sh» is a absolute or relative path to file **sofs21.sh**.

