# pwn_debug
**pwn_debug** -- An auxiliary debugging tool for ctf pwns based on pwntools

## Content

* [Key Features](https://github.com/ray-cp/pwn_debug#key-features)
* [Usage](https://github.com/ray-cp/pwn_debug#usage)
* [Installation](https://github.com/ray-cp/pwn_debug#installation)
* [Release log](https://github.com/ray-cp/pwn_debug#release-log)


## Key Features
It mainly has four features:

* Support glibc source debugging no matter x86 or 64, easy to debug libc functions in source code mode such as malloc and free.
* Support different libc versions no  matter the host versions. for example, allow running libc 2.29 on ubuntu which originally runs  on libc 2.23.
* Support easily making breakpoints, no matter the PIE of the program is opened or not.
* Easy to use(i think, lol), you just need add a little thing based on your original pwntool script.



## Usage
There are four steps to use **pwn_debug**:

0. import the tool `from pwn_debug.pwn_debug import *`
1. Declare a pwn_debug object: `pdbg=pwn_debug("binary")`
2. Set the mode parameters, three mode in total: `debug`, `local` and `remote`. You don't need to Set all the three mode, just set the mode parameters which you wanna do.
3. Run the mode.
4. do what you used to do with pwntools.

### example
A typical example is shown as below:

```
from pwn_debug.pwn_debug import *

## step 1
pdbg=pwn_debug("binary")

pdbg.context.terminal=['tmux', 'splitw', '-h']

## step 2
pdbg.local("libc.so.6")
pdbg.debug("2.23")
pdbg.remote('34.92.96.238',10000)
## step 3
#p=pdbg.run("local")
#p=pdbg.run("debug")
p=pdbg.run("remote")

pdbg.bp(0x80489aa)

elf=pdbg.elf
print hex(elf.got['printf'])
print hex(elf.plt['printf'])

libc=pdbg.libc
print libc.symbols['system']
p.interactive()
```

As shown above, there are three mode in **pwn_debug**: `debug`, `local`, `remote`.

### debug mode

Function prototype:
```
def debug(self,libc_version,env={}):
```

`debug` mode means you wanna use the libc with debug symbol, which means debugging in glibc source mode. you can see the source code when you follow into libc funcion.

In `debug` mode, you just need to declare the `libc version` like `2.23` or `2.29`, **pwn_debug** will auto set the mode.

but one thing you need to know is that you must have the corresponding libc in your dir, you can download or compilt it follow the [Installation](https://github.com/ray-cp/pwn_debug#install-glibc-with-symbols).

the code is normally like below:
```
from pwn_debug.pwn_debug import *
pdbg=pwn_debug("binary")
pdbg.debug("2.23")
p=pdbg.run("debug")
pdbg.bp(0x80489aa)
p.interactive()
```

### local mode

Function prototype:
```
def local(self,libc_path="",ld_path="",env={}):
```

`local` mode means you wanna use the libc in your computer or the libc the organizer gives out.

Declare the mode with no parameter means that you wanna use libc in your host, which may be `/lib/x86_64-linux-gnu/libc.so.6` or `/lib/i386-linux-gnu/libc.so.6`.

If you wanna use the libc that the organizer gives out, you should give the corresponding path.

the code is normally like below:
```
from pwn_debug.pwn_debug import *
pdbg=pwn_debug("binary")
pdbg.local()
#pdbg.local("./libc.so.6")
#gdbp.local("./libc.so.6","ld.so")
p=pdbg.run("local")
pdbg.bp(0x80489aa)
p.interactive()
```

### remote mode

Function prototype:
```
def remote(self,host="",port="",libc_path="")
```

`remote` mode means you wanna do remote connect with the server.

if you do not give the libc path means you wanna use the libc version on your host.

the code is normally like below:
```
from pwn_debug.pwn_debug import *
pdbg=pwn_debug("binary")
pdbg.remote('10.10.10.1',1234)
#pdbg.remote('10.10.10.1',1234,'./libc.so.6')
p=pdbg.run("remote")
pdbg.bp(0x80489aa)
p.interactive()
```
note that the breakpoint `pdbg.bp` will not affect the remote connect, so you don't need to comment the line in `remote` mode.

### Anthor Component

* make breakpoint
`pwn_debug.bp` will auto recongnize the program's PIE is open or not, so you just need to give the address you wanna break.

The `pwn_debug.bp` also won't have effect on `remote` mode, so you don't need comment out the line if you in `remote` mode.

Function prototype:
```
 def bp(self,address_list=[],fork_follow="child",command=[]):
```
`address_list` means the address you wanna make the breakpoint.

`fork_follow` means the `fork-follow-mode` in gdb you wanna set, default is `chlid`.

`command` is the command you wanna set in gdb.

example:
```
from pwn_debug.pwn_debug import *
pdbg=pwn_debug("binary")
p=pdbg.run("local")
pdbg.bp(0x80489aa)
pdbg.bp([0x9aa,0x8aa])
pdbg.bp([0x9aa,0x8aa],'parent',['x/6gx $rdi', 'i r rax'])
```

* elf `pwn_debug.elf` is just equal to `ELF('binary')`

* libc `pwn_debug.libc` is just equal to `ELF('libc_path')`


## Installation

### Install pwn_debug
```
git clone https://github.com/ray-cp/pwn_debug.git
cd pwn_debug
python setup.py install 
# or python setup.py install --user
```

### Install glibc with symbols

It supposed two ways to get the glibc, one is compile the glibc from source, the other is download from my git. 

compile the glibc will not include the `libc.so` and `ld.so`, it includes all the `lib`, but somtimes we just need the `libc.so` and `ld.so`.

right now, i just give the way compile by yourself. for i don't finish the other way in my git.

you can compile a single glibc in one time or compile all the glibc in one time. compile a single glibc may take less time, compile all will take a lot of time. **advise you compile the glibc when you need**

right now, all the glibc version include `2.19`,`2.23`,`2.24`,`2.25`,`2.26`,`2.27`,`2.28`,`2.29`.

The script will download and compile the glibc into dir `/glibc`, which will use your root privilege. The dir is needed for **pwn_debug** `debug` mode need the dir.

compile a specific version.
```
# ./build.sh $(version)
./build.sh 2.23
```

compile all the version(no parameter means compile all)
```
# ./build.sh  
./build.sh 
```

## Release log

* 2019-04-30: v0.1 beta version
