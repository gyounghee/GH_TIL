## putty

1. putty 다운로드   
[putty 다운로드 페이지](https://www.chiark.greenend.org.uk/~sgtatham/putty/releases/0.76.html)  
`putty-64bit-0.76-installer.msi`   →  클릭하여 설치

2. putty 다운로드 후 putty 설정   
* putty 실행  
``` 
Host Name : 192.168.10.2
Saved Session : test
```
입력한 후 save  
→ 다음에 putty 실행할 때 load함으로써 편하게 사용하기 위함


## vagrant
1. vagrant 다운로드  
[vagrant download](https://www.vagrantup.com/)


2. vagrant > spark-in-action.box 다운로드  
[spark-in-action.box download](https://app.vagrantup.com/anassbo/boxes/spark-in-action-box)


3. vagrant설치하면 ~/HashiCorp/Vagrant 파일 자동생성   
  - ~/HashiCorp/Vagrant 안에  spark-in-action.box 넣기


4. 제어판 > 시스템 환경 변수 편집 > 환경변수 
- 사용자 변수에  
 `변수명 : VAGRANT_HOME` / `값 : C:\HashiCorp\Vagrant` 추가   
  [ 값에 해당하는 경로는 다를 수 있음 ]


5. cmd에서 spark-in-action.box가 들어있는 Vagrant파일로 경로를 설정하고   
```vagrant box add --name manning/spark-in-action spark-in-action.box``` 입력
- 가상환경 만드는 코드였던 것 같음..  


6. VagrantFile 생성   
```vagrant init manning/spark-in-action```

7. vagrant up
- vagrant up이 잘 실행되면 가상환경이 실행된 것
  - 만약 안될 시 VagrantFile을 HashiCorp로 뺴거나
  - cmd를 `관리자 실행 권한`으로 열고 vagrant up 하기

## vagrant와 putty 연결
```
# vagrant up이 잘 실행된 것을 확인한 후 putty의 test를 load하고 open 

# login id : spark  또는 vagrant   
# password : spark  또는 vagrant   

# 만약 vagrant로 할 경우 `sudo su - spark` 인가.. 로 vagrant에서 spark로 변경 가능
```

## **vagrant와 putty 종료시키기**

cmd에서 꼭 
```
vagrant halt
```
해준 후, putty 종료 시켜야 함.

.  
.  
.  
.  
.  
.  

vagrant 다운로드 후 과정 참고
```
Microsoft Windows [Version 10.0.22000.434]
(c) Microsoft Corporation. All rights reserved.

C:\Users\user>cd ..

C:\Users>cd ..

C:\>cd HashiCorp

C:\HashiCorp>cd Vagrant

C:\HashiCorp\Vagrant>vagrant box add --name manning/spark-in-action spark-in-action.box
==> box: Box file was not detected as metadata. Adding it directly...
==> box: Adding box 'manning/spark-in-action' (v0) for provider:
    box: Unpacking necessary files from: file://C:/HashiCorp/Vagrant/spark-in-action.box
    box:
==> box: Successfully added box 'manning/spark-in-action' (v0) for 'virtualbox'!

C:\HashiCorp\Vagrant>
C:\HashiCorp\Vagrant>vagrant init manning/spark-in-action
The user that is running Vagrant doesn't have the proper permissions
to write a Vagrantfile to the specified location. Please ensure that
you call `vagrant init` in a location where the proper permissions
are in place to create a Vagrantfile.

C:\HashiCorp\Vagrant>
C:\HashiCorp\Vagrant>vagrant up
A Vagrant environment or target machine is required to run this
command. Run `vagrant init` to create a new Vagrant environment. Or,
get an ID of a target machine from `vagrant global-status` to run
this command on. A final option is to change to a directory with a
Vagrantfile and to try again.

C:\HashiCorp\Vagrant>vagrant init manning/spark-in-action
The user that is running Vagrant doesn't have the proper permissions
to write a Vagrantfile to the specified location. Please ensure that
you call `vagrant init` in a location where the proper permissions
are in place to create a Vagrantfile.

C:\HashiCorp\Vagrant>
C:\HashiCorp\Vagrant>cd ..

C:\HashiCorp>vagrant init manning/spark-in-action
A `Vagrantfile` has been placed in this directory. You are now
ready to `vagrant up` your first virtual environment! Please read
the comments in the Vagrantfile as well as documentation on
`vagrantup.com` for more information on using Vagrant.

C:\HashiCorp>
C:\HashiCorp>vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Importing base box 'manning/spark-in-action'...
==> default: Matching MAC address for NAT networking...
==> default: Setting the name of the VM: HashiCorp_default_1644249074876_60878
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
    default: Adapter 2: hostonly
    default: Adapter 3: bridged
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: password
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
    default: The guest additions on this VM do not match the installed version of
    default: VirtualBox! In most cases this is fine, but in rare cases it can
    default: prevent things such as shared folders from working properly. If you see
    default: shared folder errors, please make sure the guest additions within the
    default: virtual machine match the version of VirtualBox you have installed on
    default: your host and reload your VM.
    default:
    default: Guest Additions Version: 4.3.36
    default: VirtualBox Version: 6.1
==> default: Setting hostname...
==> default: Configuring and enabling network interfaces...
==> default: Mounting shared folders...
    default: /vagrant => C:/HashiCorp

C:\HashiCorp>vagrant ssh -- -l spark
==> default: The machine you're attempting to SSH into is configured to use
==> default: password-based authentication. Vagrant can't script entering the
==> default: password for you. If you're prompted for a password, please enter
==> default: the same password you have configured in the Vagrantfile.
vagrant@127.0.0.1's password:
vagrant@127.0.0.1's password:
Welcome to Ubuntu 14.04.4 LTS (GNU/Linux 3.13.0-85-generic x86_64)

 * Documentation:  https://help.ubuntu.com/

 System information disabled due to load higher than 1.0

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

119 packages can be updated.
71 updates are security updates.

New release '16.04.7 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


Last login: Thu Apr 21 12:10:21 2016 from 10.0.2.2
vagrant@spark-in-action:~$ sudo su
root@spark-in-action:/home/vagrant# sudo su -spark
Cannot execute park: No such file or directory
root@spark-in-action:/home/vagrant# sudo su - spark
spark@spark-in-action:~$ vagrant halt
The program 'vagrant' is currently not installed. You can install it by typing:
sudo apt-get install vagrant
spark@spark-in-action:~$ logout
root@spark-in-action:/home/vagrant# exit;
exit
vagrant@spark-in-action:~$ exit;
logout
Connection to 127.0.0.1 closed.

C:\HashiCorp>vagrant halt
==> default: Attempting graceful shutdown of VM...

C:\HashiCorp>vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
    default: Adapter 2: hostonly
    default: Adapter 3: bridged
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: password
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
    default: The guest additions on this VM do not match the installed version of
    default: VirtualBox! In most cases this is fine, but in rare cases it can
    default: prevent things such as shared folders from working properly. If you see
    default: shared folder errors, please make sure the guest additions within the
    default: virtual machine match the version of VirtualBox you have installed on
    default: your host and reload your VM.
    default:
    default: Guest Additions Version: 4.3.36
    default: VirtualBox Version: 6.1
==> default: Setting hostname...
==> default: Configuring and enabling network interfaces...
==> default: Mounting shared folders...
    default: /vagrant => C:/HashiCorp
==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> default: flag to force provisioning. Provisioners marked to run always will still run.

C:\HashiCorp>Vagrant ssh - -l spark
An invalid option was specified. The help for this command
is available below.

Usage: vagrant ssh [options] [name|id] [-- extra ssh args]

Options:

    -c, --command COMMAND            Execute an SSH command directly
    -p, --plain                      Plain mode, leaves authentication up to user
    -t, --[no-]tty                   Enables tty when executing an ssh command (defaults to true)
        --[no-]color                 Enable or disable color output
        --machine-readable           Enable machine readable output
    -v, --version                    Display Vagrant version
        --debug                      Enable debug output
        --timestamp                  Enable timestamps on log output
        --debug-timestamp            Enable debug output with timestamps
        --no-tty                     Enable non-interactive output
    -h, --help                       Print this help

C:\HashiCorp>Vagrant ssh - -l spark
An invalid option was specified. The help for this command
is available below.

Usage: vagrant ssh [options] [name|id] [-- extra ssh args]

Options:

    -c, --command COMMAND            Execute an SSH command directly
    -p, --plain                      Plain mode, leaves authentication up to user
    -t, --[no-]tty                   Enables tty when executing an ssh command (defaults to true)
        --[no-]color                 Enable or disable color output
        --machine-readable           Enable machine readable output
    -v, --version                    Display Vagrant version
        --debug                      Enable debug output
        --timestamp                  Enable timestamps on log output
        --debug-timestamp            Enable debug output with timestamps
        --no-tty                     Enable non-interactive output
    -h, --help                       Print this help

C:\HashiCorp>vagrant ssh -- -l spark
==> default: The machine you're attempting to SSH into is configured to use
==> default: password-based authentication. Vagrant can't script entering the
==> default: password for you. If you're prompted for a password, please enter
==> default: the same password you have configured in the Vagrantfile.
vagrant@127.0.0.1's password:
vagrant@127.0.0.1's password:
vagrant@127.0.0.1's password:
vagrant@127.0.0.1: Permission denied (publickey,password).

C:\HashiCorp>vagrant halt
==> default: Attempting graceful shutdown of VM...

C:\HashiCorp>vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
    default: Adapter 2: hostonly
    default: Adapter 3: bridged
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: password
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
    default: The guest additions on this VM do not match the installed version of
    default: VirtualBox! In most cases this is fine, but in rare cases it can
    default: prevent things such as shared folders from working properly. If you see
    default: shared folder errors, please make sure the guest additions within the
    default: virtual machine match the version of VirtualBox you have installed on
    default: your host and reload your VM.
    default:
    default: Guest Additions Version: 4.3.36
    default: VirtualBox Version: 6.1
==> default: Setting hostname...
==> default: Configuring and enabling network interfaces...
==> default: Mounting shared folders...
    default: /vagrant => C:/HashiCorp
==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> default: flag to force provisioning. Provisioners marked to run always will still run.

C:\HashiCorp>vagrant ssh -- -l spark
==> default: The machine you're attempting to SSH into is configured to use
==> default: password-based authentication. Vagrant can't script entering the
==> default: password for you. If you're prompted for a password, please enter
==> default: the same password you have configured in the Vagrantfile.
vagrant@127.0.0.1's password:
Welcome to Ubuntu 14.04.4 LTS (GNU/Linux 3.13.0-85-generic x86_64)

 * Documentation:  https://help.ubuntu.com/

 System information disabled due to load higher than 1.0

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

119 packages can be updated.
71 updates are security updates.

New release '16.04.7 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


Last login: Mon Feb  7 15:52:58 2022 from 10.0.2.2
vagrant@spark-in-action:~$

```

