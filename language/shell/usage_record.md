[很全的参考文档](https://github.com/skywind3000/awesome-cheatsheets/blob/master/languages/bash.sh)

# shell语法
TAG: 工具

## 头处理
```sh
#!/bin/bash
set -e  # 所有非 0 的返回状态都需要捕获
set -o pipefail  # 管道间错误需要捕获
```


## 日期
```sh
# 如果没有输入日期（argv[1]），采用当前日期
if [ $# == 1 ] ; then
    INPUT_DATE=$(date -d $1 +%Y-%m-%d)
else
    INPUT_DATE=$(date +%Y-%m-%d)
fi
# 时间变量
END_DAY=${INPUT_DATE} 
BEGIN_DAY=$(date +"%Y-%m-%d" -d "-7 days ${END_DAY}") # 知识点：七天前
CVREMARK_DAY=$(date +"%Y%m%d" -d "${END_DAY}")
```


## 2>&1
https://stackoverflow.com/questions/818255/in-the-shell-what-does-21-mean

将标准错误输出到标准输出

## &
命令最后表示**后台运行**

## main function
function download_cvremark()
{
    ...
}
function main()
{
    download_cvremark
}

## 用户创建
sudo useradd -m username

useradd work
passwd work

添加work用户的sudo权限
$ visudo

## 用户切换
https://unix.stackexchange.com/questions/3568/how-to-switch-between-users-on-one-terminal

$ whoami
user1
$ su - user2
Password:
$ whoami
user2
$ exit
logout

## 磁盘

du -h --max-depth=1
du -sh test_dir
## 内存

ps aux --sort -rss
ps -ef | grep te_main
ps -eaf

## netstat
netstat -tunpl | grep 端口号
## chmod
sudo chmod u=rwx,g=rwx,o=rwx file_name

## shell中嵌套python
数据处理，cat infile为要处理的数据。argv[1]为参考数据。
```sh
cat user_data.txt | python -c '
# -*- coding: utf-8 -*-
import sys
import re
# 把监察的来源id转为文本,非监察来源做正则匹配后解析
source_dict = {}
with open(sys.argv[1],"r") as f:
    for eachline in f:
        parts = eachline.strip("\n").split("\t")
        source_dict[parts[0]] = parts[1]
for line in sys.stdin:
    parts = line.strip("\n").split("\t")
    if parts[4]:
        parts[4] = source_dict.get(parts[4],"")
    elif re.search(r"来源.*是否连坐.*违规类型.*违规位置", parts[5]):
        try:
            parts_new = parts[5].strip("\n").split(";")
            parts[4] = parts_new[0].split(":")[1]
        except Exception as e:
            print e
    elif re.search(r"来源.*账户等级.*封禁前状态.*初始违规账户", parts[5]):
        try:
            parts_new = parts[5].strip("\n").split(";")
            parts[4] = parts_new[0].split(":")[1]
        except Exception as e:
            print e
    elif re.search(r"系统自动拒绝", parts[5]):
        parts[4] = "系统"
    print "\t".join(parts)
    ' first_source.txt > user_data.txt.source
```


## 例行化 crontab
[参考](https://man.linuxde.net/crontab)
查看任务
- crontab -u username -l
- crontab -l

编辑任务
- crontab -e



## 参看文件某行是否存在某句话
```
FILE=/home/shaorui02/hello
LOCAL_LOG=log

if grep -Fxq "$FILE: No such file or directory" $LOCAL_LOG # 文件不存在
then
    echo file not exist
else
    echo file exist
fi

#grep -Fxq "hello" hello
```
搜索文件内容
```
grep -r def_galaxy_w .
grep mulan *.sh
```

找到脏数据 + 删除脏数据

```
cat file | grep -n xxx
grep -r xxx file
sed '1473d' file
```

grep -v aaa | grep bbb 匹配不含'aaa'但包含'bbb'的行


#使用''包裹特殊符号
grep '"type":6' 202006*/audit_trace.log

## nohup
> no hang up不挂断
退出帐户时该进程不会结束
使用:`nohup sh load_fin_acct_renew_log_da.sh 2019-08-15 &`
`nohup command >/dev/null 2>&1 &` 不会创建nohup.out，linux有个黑洞的机制

## hadoop 
> get src dst
hadoop fs -get hdfs://nmg01-khan-hdfs.dmop.baidu.com:54310/app/ecom/aries/fengkong/tianzhu/qe/data/user_org_acs_info/pdate=2020-04-26/data user_org_acs_info_final.txt_from_hdfs_04-26


## here doc
1. 配合cat使用，保存到环境变量
sql=$(cat <<EOF
        select * 
        from db_cdc_publish.prod_uc_acct_sec_info 
        where pdate='${PDATE};
quit;
EOF
)
~/.jumbo/bin/queryengine  --sessionconf engine=wing -e "${sql}"


## diff
`diff -c user_org_acs_info_final.txt_from_hdfs_04-21_before100 user_org_acs_info_final.txt.2020-04-21_before100`


## head
显示头1000行
`head -n 100 party_agent_ka_info_da.txt`

显示1000行到3000行
`cat filename| head -n 3000 | tail -n +1000`

## scp
Linux scp 命令用于 Linux 之间复制文件和目录。
scp 是 secure copy 的缩写, scp 是 linux 系统下基于 ssh 登陆进行安全的远程文件拷贝命令。
scp 是加密的，rcp 是不加密的，scp 是 rcp 的加强版。

`scp -r /usr/local/hbase-2.1.3 root@h02:/usr/local/`

## sort

sort -t $'\t' -k 2 mt_feed_addtime > sr_mt_feed_addtime
sort -t $'\t' -rk 2 mt_feed_addtime > sr_mt_feed_addtime

## awk
打印某列
head temp_cdc.utf8 | awk -F"\t" '{print $8"}' 

awk中打印引号
echo test | awk '{print"sed '\'1d''\''"}'

去重
cat user_data.part1 user_data.part2 | sort -t $'\t' -k3,3r | awk -F"\t" '{s[$2]=$0}END{for(i in s)print s[i]}' > user_data.txt

循环打印
awk 'BEGIN { for (i = 1; i <= 64; ++i) print"/app/ecom/fengkong/aka/bp/meteor_sequence/aka-ad-output-trad-fc-pipe/20200923/2240/pipe-" i }'

```sh
awk -v FS='\t' -v OFS='\t' '
ARGIND==1{
    user_name_map[$1] = $2;
}
ARGIND==2{
    user_id = $1;
    opt_name = $5;
    if($1 in user_name_map) {user_name = user_name_map[user_id];}
    else {user_name = "NULL";}

    result_map[user_id] = user_id"\t"user_name"\t"opt_name
}
ARGIND==3{
    user_id = $1;
    opt_name = $7;
    if($1 in user_name_map) {user_name = user_name_map[user_id];}
    else {user_name = "NULL";}

    result_map[user_id] = user_id"\t"user_name"\t"opt_name
}
END{for(i in result_map)print result_map[i]}
' cdc_clent.txt user_opt_map ka_org_acs_info > result
```

## find 
find . -name user_optional_license_day.log.wf.20200701000000

## grep 
### xargs
从标准输入获取一个作为参数
ls | xargs grep hdfs --color


## 日期循环

给一个start，给一个end
```sh
#!/bin/bash

set -u  # 使用的变量必须提前定义过
set -e  # 所有非 0 的返回状态都需要捕获
set -o pipefail  # 管道间错误需要捕获


#help info
if [ $# == 2 ] ; then
    start_date="$1"
    end_date="$2"
else
    start_date=$(date -d "1 day ago" +%Y-%m-%d)
    end_date=$(date -d "1 day ago" +%Y-%m-%d)
fi

start_sec=$(date -d ${start_date} +%s)
end_sec=$(date -d ${end_date} +%s)
interval_days=$(( (end_sec - start_sec) / 86400 )) # 一天有 86400 秒

for((i=0; i<=interval_days; i++)); do
    date_string="${start_date} +${i} days"
    #cur_date="$(date -d "${date_string}" +%F)"
    cur_date="$(date -d "${date_string}" +%Y-%m-%d)"
    echo $cur_date
done
```

#### python对应功能

```py
from datetime import date, timedelta

start_date = date(2020, 6, 1)
end_date = date(2020, 7, 21)
delta = timedelta(days=1)
while start_date <= end_date:
    print (start_date.strftime("%Y%m%d"))
    start_date += delta
```

## split
将文件平等划分
split -l 10000 file.txt

---

# awk的使用

TAG: 工具

## 【双文件】参考文件 + 处理文件
典型应用就是**去重**。

### case1
```sh
# 总的形式
awk -v FS='\t' -v OFS='\t' ' 
ARGIND==1{
    push_audit_time[$2] = $8"\t"$7;
    other_info[$2] = $1"\t"$3"\t"$4"\t"$5"\t"$6;
}
ARGIND==2{
    if ($1 in push_audit_time) {print other_info[$1],$0,push_audit_time[$1];}
}' infile1 infile2 > outfile

```

【代码解析】
- FS='\t' OFD='\t' 输入、输出解析格式，以'\t'分列
- infile1解析存入memory（hash table），infile2判断：是否存在infile1中（hash check）
- $0为整行，$1-n：以\t分割的列。验证方式`head file | awk -F"\t" '{print $1"\t"$2}' `

【问题】
1. 如果我需要任务的添加某行？
2. 在设计时如何『占位』？
    一般source_file都是从各种数据库中获取（不然也就不需要进行文本处理了）。
    - 【数据处理流程】mysql(which info do you want?) -> csv -> delete file line -> infile(FS=" ")=>outfile(OFS="\t")

### case2

【代码】
```sh
awk -v FS='\t' -v OFS='\t' '{
        violation_basis = $7;
        task_type = $8;
        punish_type = $10;
        user_id = $2;
        reason_name = $5;
        violation_type = "";
        first_source = $4;
        remark = "";
        audit_time = $9;
        push_time = $13;
        if (violation_basis ~ /1/) {
            reason_name = $5; violation_type = "A类";
        }
        else if (violation_basis=="NULL" || task_type==1 || task_type==2) {
            if (punish_type==5) {reason_name = "一线自查(严重)";}
            else if (punish_type==6) {reason_name = "一线自查(feed)";}
            else if (punish_type==7) {reason_name = "一线自查(一般)";}
            else if (punish_type==8) {reason_name = "一线自查(其他)";}
            else {reason_name = "一线自查";}
            violation_type = "";
        }
        else {
            reason_name = $5; violation_type = "非A类";
        }
        print user_id, reason_name, violation_type, first_source, remark, audit_time, push_time;
    }' jc.data > jc.txt
```

【解析】
- 设计时规定好了每个$n格式什么含义，在这里解析以后，将各列数据赋值给arg，利用print直接打印好，中间是处理流程（行文本处理），""为初始化。

【知识点】
这里学习如何在shell上写if-else，其实本身这里也可通过python来处理`print('\t'.join(parts))`



# sed

sed -i "1d" file 去掉第一行
sed '1,3d' sr_mt_feed_addtime 去掉第一到第n行

sed '1,70d' sr_mt_feed_addtime 去掉第一到第n行

去掉最后一行？
本地替换字符串
sed -i 's/\x01/\t/g' uid_clktime.${END_DAY}

sed -i '/pattern to match/d' ./infile # 删除包含某个字符串的某行，**inplace**

# nohup
nohup sh run.sh 2>&1 &
【TODO】why？


# for loop

```bash
for j in {0..5}
do
    for i in {0..96}
    do
        #echo "hadoop fs -copySeqFileToLocal /app/ecom/fengkong/aka/bp/meteor_sequence/aka-ad-output-fc-pipe/20201009/15${j}0/pipe-$i/pipe-$i-20201009-15${j}000.log 20201009-15${j}000_$i"
        # :00
        hadoop fs -copySeqFileToLocal /app/ecom/fengkong/aka/bp/meteor_sequence/aka-ad-output-fc-pipe/20201009/15${j}0/pipe-$i/pipe-$i-20201009-15${j}000.log 20201009-15${j}000_$i

        # :05
        hadoop fs -copySeqFileToLocal /app/ecom/fengkong/aka/bp/meteor_sequence/aka-ad-output-fc-pipe/20201009/15${j}0/pipe-$i/pipe-$i-20201009-150500.log 20201009-150500_$i
    done
done
```

---

- ls 
  - ls -al(ll)

- user
  - useradd -m sr -s /bin/bush #控制脚本    自动建立用户登录目录
  - userdel
  - su #super user
  - passwd sr #(user) 设置password

- li
  - ln (Unix) The ln command is a standard Unix command utility used to create a **hard link or a symbolic link** (symlink) to an existing file.
  建立一个link（硬链接或符号链接），文件系统里面的东西。
- pwd

- touch
  - touch readme.md

- echo
  - echo hello > a.txt #重定向

- man

- chmod
  - chmod o-r hello.c #（除掉读权限）
	-	chmod o+r hello.c

- whereis
  - whereis gdb
  - whereis gcc

- touch
  - touch foo.txt


- cat 
  - cat hello.c


- sudo  
  - sudo su **进入root**

- nslookup
  - nslookup www.baidu.com


- telnet 
  - telnet www.aol.com 80

- curl
  - 模拟POST
```
  curl -H "Content-Type: application/json" -X POST -d '{"user_name": "shaorui02", "show_name": "测试标签_1","desc": "测试","first_level": "一级分类","second_level": "二级分类","sentiment": "正向","query": "{\"bool\":{\"filter\":{\"match_all\":{\"_tag\":[\"101\"]}}}}"}' http://127.0.0.1:8088/portrait/tagset

  //【问题】曾经碰到登录界面导致POST不成功
  //【问】如果有登录界面怎么办？
```
[diff curl and wget](https://stackoverflow.com/questions/34648633/what-is-the-difference-between-curl-and-wget-below)
- nc  (netcat)
  > a simple Unix utility that **reads and writes data across network** connections, using the TCP or UDP protocol. It is designed to be a reliable "back-end" tool that can be used directly or driven by other programs and scripts.

- dd 创建一定大小的文件
  > dd is a command-line utility for Unix and Unix-like operating systems whose primary purpose is to **convert and copy files**. On Unix, device drivers for hardware (such as hard disks) and special device files appear in the file system just like normal files; dd can also read and/or write from/to these files, provided that function is implemented in their respective driver.
  dd if=/dev/zero of=hello.txt bs=100M count=1
```
if =输入文件(或设备名称)。
of =输出文件(或设备名称)。
ibs = bytes 一次读取bytes字节，即读入缓冲区的字节数。
skip = blocks 跳过读入缓冲区开头的ibs*blocks块。
obs = bytes 一次写入bytes字节，即写 入缓冲区的字节数。
bs = bytes 同时设置读/写缓冲区的字节数(等于设置obs和obs)。
cbs = bytes 一次转换bytes字节。
count = blocks 只拷贝输入的blocks块。
conv = ASCII 把EBCDIC码转换为ASCII码。
conv = ebcdic 把ASCII码转换为EBCDIC码。
conv = ibm 把ASCII码转换为alternate EBCDIC码。
conv = blick 把变动位转换成固定字符。
conv = ublock 把固定们转换成变动位
conv = ucase 把字母由小写变为大写。
conv = lcase 把字母由大写变为小写。
conv = notrunc 不截短输出文件。
conv = swab 交换每一对输入字节。
conv = noerror 出错时不停止处理。
conv = sync 把每个输入记录的大小都调到ibs的大小(用ibs填充)。
```
- diff -u

- tar
  - 解压
    - tar -xf all.tar -C ./all     *.tar*
    - tar -xzf all.tar.gz -C ./all   *.tar.gz*

  - 压缩
    - tar -cvf /home/www/images.tar /home/www/images *仅打包，不压缩*
    - tar -zcvf /home/www/images.tar.gz /home/www/images *打包后，以gzip压缩*
    tar -cvf shaorui_galaxy_khan.tar  /home/work/sf-galaxy/*  --exclude=*log* --exclude=*data*

  - tar.gz
  		tar -cvf bible.tar the_holy.txt  （压缩）
  		tar -c(创建)z(压缩)vf bible.tar.gz the_holy_bible.txt
      tar -xvf bible.tar.gz  ~/
  			i. 解压 
  				1) 到当前（直接）
  				2) 指定
  					tar   zxvf    test.tgz  -C  指定目录
  					比如将/source/kernel.tgz解压到  /source/linux-2.6.29 目录
  					tar  zxvf  /source/kernel.tgz  -C /source/ linux-2.6.29
  			ii. 压缩，生成(文件夹---》tar)
  				tar -cvf /home/www/images.tar /home/www/images ← 仅打包，不压缩
  				 tar -zcvf /home/www/images.tar.gz /home/www/images ← 打包后，以gzip压缩
  			iii. 目录压缩到文件
  				将指定目录压缩到指定文件
  				比如将linux-2.6.29 目录压缩到  kernel.tgz
          tar czvf   kernel.tgz   linux-2.6.29

- mount 挂载
  - mount - mount a filesystem
  想象u盘插入，
```
All  files  accessible  in a Unix system are arranged in one big tree,
the file hierarchy, rooted at /.  These files can be spread  out  over
several  devices.   The  mount command serves to attach the filesystem
found on some device to the big file tree.  Conversely, the  umount(8)
command  will  detach it again.  The filesystem is used to control how
data is stored on the device or provided in a virtual way  by  network
or another services.
```
linux（或者说操作系统，本身对每个文件系统的访问是需要挂载的。windows则是自动管理的）
- .bashrc(run command)


- ps
  > 查看正在运行的进程
  ps aux --sort -rss 查看内存使用情况

- du
  du -h --max-depth=1
  查看磁盘使用情况

- fg Foreground
	> 将后台中的命令调至前台继续运行
- Bg Background
	> 将一个在后台暂停的命令，变成继续执行

- history---记录在案（.bash_history） #命令行
  - history > 20190102_id.txt


---

#工具

# vim
  - 批量
    - search：:/pattern n(next word) N(pre) noh(close highlight)
    - 查找替换 全局替换:% s/XXX/YYY/g.
    - 注释：v + ctrl+v(line) + I + // + esc
    - 反注释: v + 选择 + d
  - copy/format clipboard: shift+ins + gg=G
  - movement
    - n上/下...up/down n line
      - 推广到首尾(file/line)


  - vimdiff file1 file2
    - ？还没找到具体使用需求 


---

### user control
sudo useradd -m olivia
sudo passwd olivia
addgroup readers
less /etc/group

sudo usermod -a -G readers nathan
sudo chown -R :readers /READERS 
sudo chown -R myuser . # 当前用户能写
sudo chmod -R g-w /READERS
sudo chmod -R o-x /READERS

- Using access control lists
  >  setfacl - set file access control lists
  - sudo setfacl -m g:readers:rx -R /DATA  # only read
  - sudo setfacl -m g:editors:rwx -R /DATA # read and write


---

#工具

-  gprofil (profile tool)
https://www.howtoforge.com/tutorial/how-to-install-and-use-profiling-tool-gprof/

- valgrind (memory leak)
    g++ memoryLeak.cc -o memoryLeak.exe -g  //-o目标程序 -g产生调试信息
    valgrind --tool=memcheck --leak-check=full ./memoryLeak.exe



---

### 库文件 和 头文件 路径配置
	  > 默认lib库路径是 ： /usr/local/lib/
          
	  > 默认头文件的位置： /usr/local/include/log4cpp        
- 库文件
  - 临时
    - export LD_LIBRARY_PATH=/opt/gtk/lib:$LD_LIBRARY_PATH
    - echo $LD_LIBRARY_PATH
  - sudo vim /etc/ld.so.config
    - 添加路径
    - sudo ldconfig
- 头文件
  - vim .bashrc 
  - 添加 export CPLUS_INCLUDE_PATH=~/netProgramming/muduo/muduo/base:$CPLUS_INCLUDE_PATH
 
