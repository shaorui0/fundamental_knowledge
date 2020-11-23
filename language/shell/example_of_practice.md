# example of practice

账户违规发现时效性监控


risk_user_stat.sh

```bash
#!/bin/bash

set -e  # 所有非 0 的返回状态都需要捕获
set -o pipefail  # 管道间错误需要捕获

if [ $# == 1 ] ; then
    INPUT_DATE=$(date -d $1 +%Y-%m-%d)
else
    INPUT_DATE=$(date +%Y-%m-%d)
fi

# 时间变量
END_DAY=${INPUT_DATE}
BEGIN_DAY=$(date +"%Y-%m-%d" -d "-7 days ${END_DAY}")
CVREMARK_DAY=$(date +"%Y%m%d" -d "${END_DAY}")

# 数据库配置
HOST="10.233.31.50"
PORT="7550"
USER="leizihe"
PASSWD="U3m7Aetf8T"

# hadoop配置
HADOOP_PATH="/home/work/bin/hadoop-client/hadoop/bin/hadoop"
CVREMARK_HDFS="hdfs://nmg01-mulan-hdfs.dmop.baidu.com:54310/app/ecom/aries/fengkong/zhukaiwen/cvremark"


#获取监察数据：userid，违规类型，是否A类，来源，批注占位，审核时间，推送时间
function get_jc()
{
    echo "get_jc start!"

    mysql -h${HOST} -P${PORT} -u${USER} -p${PASSWD} --default-character-set=utf8 -e "
    select
        task_id,
        user_id,
        task.product,
        first_source,
        reason_name,
        reason,
        task.violation_basis,
        task_type,
        audit_time,
        task.punish_type,
        quarter_consume,
        real_punish_amount,
        push_time
    from
        DF_Inspection.task
        left join
        DF_Inspection.violation_reason
        on
            task.violation_reason_third = violation_reason.reason_id
    where
        real_punish_type not in (0,10,11,12,20) and is_violation = 1
        and audit_time >= '${BEGIN_DAY}' and audit_time < '${END_DAY}'
    " > jc.data
    sed -i "1d" jc.data

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

    echo "get_jc end!"
}

# 获取批注数据
function download_cvremark()
{
    echo "download_cvremark begin!"
    ${HADOOP_PATH} fs -test -e ${CVREMARK_HDFS}/${CVREMARK_DAY}/
    if [ $? -eq 0 ]; then
        cvremark_count=$(${HADOOP_PATH} fs -ls  ${CVREMARK_HDFS}/${CVREMARK_DAY}/userid_karemark*| wc -l)
        if [ ${cvremark_count} -gt 5 ];then
            echo "${cvremark_count} greate than 5"
        else
            echo "${cvremark_count} less than 5"
        fi
        cvremark_count=$(${HADOOP_PATH} fs -ls  ${CVREMARK_HDFS}/${CVREMARK_DAY}/cvremark*| wc -l)
        if [ ${cvremark_count} -gt 5 ];then
            echo "${cvremark_count} greate than 5"
        else
            echo "${cvremark_count} less than 5"
        fi
        ${HADOOP_PATH} fs -cat ${CVREMARK_HDFS}/${CVREMARK_DAY}/* | sort -t $'\t' -k 4 > cvremark
        cat cvremark | iconv -fgbk -tutf8 > cvremark.utf8
        mv cvremark cvremark.gbk
        mv cvremark.utf8 cvremark
    else
        echo "cvremark file doesn't exist"
    fi
    echo "download_cvremark end!"
}

# 获取业审数据：userid, 违规类型, 是否A类, 来源, 批注占位, 审核时间，推送时间
function get_ys()
{
    echo "get_ys start!"

    # 提取时间范围内自动拒绝和二审拒绝的批注
    awk -F"\t" -v begin_day=${BEGIN_DAY} -v end_day=${END_DAY} '
    ($3 ~ /系统自动拒绝.*涉嫌窃取网民隐私/ || $3 ~ /系统自动拒绝.*涉嫌劫持百度流量/ || $3 ~ /来源.*是否连坐.*违规类型.*违规位置/) && $4>=begin_day && $4<end_day
    ' cvremark > ys.data
    # 按照账户ID去重，保留最后一条
    awk -F"\t" '{
        user_id = $1;
        reason_name = "";
        violation_type = "";
        first_source = "";
        remark = $3;
        push_time = "";
        audit_time = $4;
        s[$1] = user_id"\t"reason_name"\t"violation_type"\t"first_source"\t"remark"\t"audit_time"\t"push_time;
    } END {
        for(i in s)print s[i]
    }' ys.data > ys.txt

    mysql -h${HOST} -P${PORT} -u${USER} -p${PASSWD} --default-character-set=utf8 -e "
    select
        task_id,
        user_id,
        ys_task.product,
        first_source,
        reason_name,
        reason,
        ys_task.violation_basis,
        task_type,
        audit_time,
        ys_task.punish_type,
        quarter_consume,
        real_punish_amount,
        push_time
    from
        DF_Inspection.ys_task
        left join
        DF_Inspection.violation_reason
        on
            ys_task.violation_reason_third = violation_reason.reason_id
    where
        real_punish_type not in (0,10,11,12,20) and is_violation = 1
        and audit_time >= '${BEGIN_DAY}' and audit_time < '${END_DAY}'
    " > ys_jc.data
    sed -i "1d" ys_jc.data

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
    }' ys_jc.data > ys_jc.txt
    cat ys_jc.txt >> ys.txt

    # 批注为信用封禁的部分
    awk -F"\t" -v b=${BEGIN_DAY} -v e=${END_DAY} '($3~/来源:信用封禁;账户等级.*封禁前状态.*初始违规账户/) && $4>=b && $4<e' cvremark > fj.data
    awk -F"\t" 'ARGIND==1{b[$1]} ARGIND==2{if(!($1 in b)) s[$1]=$1"\t\t\t\t"$3"\t"$4"\t"} END{for(i in s)print s[i]}' ys.txt  fj.data > fj.txt

    cat fj.txt | python -c '
# -*- coding: utf-8 -*-
import sys

for line in sys.stdin:
    parts = line.strip("\n").split("\t")
    pz_list = parts[4].split(";")
    level = pz_list[1].split(":")[1]
    state_before_fj = pz_list[2].split(":")[1]
    if (level=="10101" and state_before_fj in ["2", "3"]) or (level == "10104" and state_before_fj in ["1", "2", "3"]):
        print "\t".join(parts)
    ' > fj_filte.txt
    cat fj_filte.txt >> ys.txt

    echo "get_ys end!"
}

#  生成1-7列  是否监察 userid, 违规类型, 是否A类, 来源, 批注占位, 审核时间, 推送时间
function merge_jc_ys()
{
    echo "merge_jc_ys start"
    # 按照时间倒排顺序
    cat jc.txt | sort -t $'\t' -rk6 > jc_sort
    # 整理业审数据，监察优先级高于业审
    #awk -F"\t" 'ARGIND==1{s[$1]=$1"\t"$2"\t"$3"\t"$4;audit_time[$1]=$6;push_time[$1]=$7}ARGIND==2{if($1 in s)print "监察\t"s[$1]"\t"$5"\t"$6"\t"push_time[$1];else print "非监察\t"$0}' jc_sort ys.txt > user_data.part1
    awk -F"\t" 'ARGIND==1{s[$1]=$1"\t"$2"\t"$3"\t"$4;audit_time[$1]=$6;push_time[$1]=$7}ARGIND==2{if($1 in s)print "监察\t"s[$1]"\t"$5"\t"audit_time[$1]"\t"push_time[$1];else print "非监察\t"$0}' jc_sort ys.txt > user_data.part1

    # 整理监察数据，(只在监察的数据)
    awk -F"\t" 'ARGIND==1{s[$2]=$0}ARGIND==2{if(!($1 in s))print "监察\t"$0}' user_data.part1 jc_sort > user_data.part2

    # 去重，保留最后一条记录，即时间最早的记录
    cat user_data.part1 user_data.part2 | sort -t $'\t' -k1,1r -k7,7r | awk -F"\t" '{s[$2]=$0}END{for(i in s)print s[i]}' > user_data.txt

    rm -f user_data.part1 user_data.part2

    cat user_data.txt | awk -F"\t" '{print $2}' > uid_list.${END_DAY}

    # 去除已推送账户
    #awk -F "\t" 'ARGIND==1{s[$1]}ARGIND==2{if(!($2 in s)) print $0}' userdone user_data.txt

    echo "merge_jc_ys end!"
}

# 更新source  列 5
function update_source()
{
    echo "update source start"

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

    echo "update source end"
}

# 更新业审的来源：对于来源为巡查反馈、监察反馈、手动录入-业审举报、手动录入-风控能力建设的需要去监察和意图平台查询流转前的原始来源
function update_origin_source()
{
    echo "update origin source start"

    mysql -h${HOST} -P${PORT} -u${USER} -p${PASSWD} --default-character-set=utf8 -e "
    select 
        task_id,
        user_id,
        task.product,
        first_source,
        reason_name,
        reason,
        task.violation_basis,
        task_type,
        audit_time,
        task.punish_type
    from
        DF_Inspection.task
        left join
        DF_Inspection.violation_reason
        on task.violation_reason_third=violation_reason.reason_id
    where
        real_punish_type in (10) and is_violation=1 and audit_time>='${BEGIN_DAY}' and audit_time<'${END_DAY}'
    order by audit_time desc" > origin_source
    sed -i "1d" origin_source


    mysql -h${HOST} -P${PORT} -u${USER} -p${PASSWD} --default-character-set=utf8 -e "
    select
        task_id,
        user_id,
        ys_task.product,
        first_source,
        reason_name,
        reason,
        ys_task.violation_basis,
        task_type,
        audit_time,
        ys_task.punish_type
    from
        DF_Inspection.ys_task
        left join
        DF_Inspection.violation_reason
        on
            ys_task.violation_reason_third=violation_reason.reason_id
    where
        real_punish_type in (10) and is_violation=1 and audit_time>='${BEGIN_DAY}' and audit_time<'${END_DAY}'
    " > origin_source_yt
    sed -i "1d" origin_source_yt
    cat origin_source_yt >> origin_source

    cat user_data.txt.source | python -c '
# -*- coding: utf-8 -*-
import sys
import re

# 更新追溯违规来源
# 把业审中的来源-巡查反馈 转变为真实的监察来源

#加载监察数据中 仅下线的违规来源
origin_source = {}
with open(sys.argv[1], "r") as f:
    for eachline in f:
        parts = eachline.strip("\n").split("\t")
        user_id = parts[1]
        source = parts[3]
        origin_source[user_id] = source

# 加载source_id 和source_name 的映射
source_dict = {}
with open(sys.argv[2],"r") as f:
    for eachline in f:
        parts = eachline.strip("\n").split("\t")
        source_dict[parts[0]] = parts[1]

for line in sys.stdin:
    parts = line.strip("\n").split("\t")
    userid = parts[1]
    source = parts[4]
    if (source == "巡查反馈") or (source == "监察反馈") or (source == "手动录入-业审举报") or (source == "手动录入-风控能力建设"):
        origin_source_id = origin_source.get(userid,"")
        origin_source_name = source_dict.get(origin_source_id,"")
        if origin_source_name :
            parts[4] = origin_source_name
    print "\t".join(parts)
' origin_source first_source.txt > user_data.txt.${END_DAY}
    echo "update origin source end"
}




function main()
{
    # download_cvremark

    get_jc

    get_ys

    merge_jc_ys

    update_source

    update_origin_source

}
```

## 近期首次点击时间

使用hive统计账户的首次计费时间
first_clk_stat.sh

```bash
#!/bin/bash

set -e  # 所有非 0 的返回状态都需要捕获
set -o pipefail  # 管道间错误需要捕获

if [ $# == 1 ] ; then
    INPUT_DATE=$(date -d $1 +%Y-%m-%d)
else
    INPUT_DATE=$(date +%Y-%m-%d)
fi

# 时间变量
END_DAY=${INPUT_DATE}
UID_TIMESTAMP=$(date +"%Y%m%d000001" -d "${END_DAY}")
BEGIN_TIMESTAMP=$(date +"%Y%m%d000000" -d "-10 days ${END_DAY}")
END_TIMESTAMP=$(date +"%Y%m%d000000" -d "${END_DAY}")

# hive配置
HIVE_PATH="/home/work/bin/hive-1.1.9/bin/hive"
LOCAL_INPATH="/home/work/tmp/wangdi17/20191222_zhiban/uid_list.${END_DAY}"
OUTPUT_HDFS="hdfs://nmg01-mulan-hdfs.dmop.baidu.com:54310//app/ecom/aries/galaxy/luhaichuan/fc_clk/${UID_TIMESTAMP}"

nohup /home/work/bin/hive-1.1.9/bin/hive -e "
SET hive.exec.max.created.files=1000000;
use risk_data;

load data local inpath '${LOCAL_INPATH}' into table risk_data_special.sme_new_user partition(time_stamp=${UID_TIMESTAMP});

INSERT OVERWRITE DIRECTORY '${OUTPUT_HDFS}'
select
    fc_clk.userid,
    min(fc_clk.clktime_t)
from
    (select userid from risk_data_special.sme_new_user where time_stamp='${UID_TIMESTAMP}') uid_list
    join
    (select * from dorado_hour where time_stamp>='${BEGIN_TIMESTAMP}' and time_stamp<'${END_TIMESTAMP}') fc_clk
    on
    fc_clk.userid = uid_list.userid
group by
    fc_clk.userid
" > logs/user_first_clk.log.${END_DAY} 2>&1 &
```

## 数据合并

merge_to_csv.sh

```bash
#!/bin/bash

set -e  # 所有非 0 的返回状态都需要捕获
set -o pipefail  # 管道间错误需要捕获

if [ $# == 1 ] ; then
    INPUT_DATE=$(date -d $1 +%Y-%m-%d)
else
    INPUT_DATE=$(date +%Y-%m-%d)
fi

# 时间变量
END_DAY=${INPUT_DATE}
UID_TIMESTAMP=$(date +"%Y%m%d000001" -d "${END_DAY}")

# hadoop配置
HADOOP_PATH="/home/work/bin/hadoop-client/hadoop/bin/hadoop"

# 下载速启数据
# cp ../suqi/all_data/data/suqi_report.csv .
# cp ../suqi/all_data/data/cdc_client.txt .

rm -rf uid_clktime.${END_DAY}
${HADOOP_PATH} fs -getmerge hdfs://nmg01-mulan-hdfs.dmop.baidu.com:54310/app/ecom/aries/galaxy/luhaichuan/fc_clk/${UID_TIMESTAMP} uid_clktime.${END_DAY}
sed -i 's/\x01/\t/g' uid_clktime.${END_DAY}

awk -v FS='\t' -v OFS='\t' '
ARGIND==1{
    reg_eff_time[$1] = $16"\t"$17;
}
ARGIND==2{
    if ($2 in reg_eff_time) {print $2,reg_eff_time[$2]}
}' cdc_client.txt user_data.txt.${END_DAY} > uid_regtime_efftime

awk -v FS='\t' -v OFS='\t' '
ARGIND==1{
    mteff_time[$1] = $36;
}
ARGIND==2{
    if ($1 in mteff_time) {print $0,mteff_time[$1];} else {print $0,"NULL";}
}' suqi_report.csv uid_regtime_efftime > uid_regtime_efftime_mtefftime

awk -v FS='\t' -v OFS='\t' '
ARGIND==1{
    clktime[$1] = $2;
}
ARGIND==2{
    if ($1 in clktime) {print $0,substr(clktime[$1];} else {print $0,"NULL";}
}' uid_clktime.${END_DAY} uid_regtime_efftime_mtefftime > uid_regtime_efftime_mtefftime_clktime

# 是否监察 userid, 违规类型, 是否A类, 来源, 批注占位, 审核时间，推送时间
awk -v FS='\t' -v OFS='\t' '
ARGIND==1{
    push_audit_time[$2] = $8"\t"$7;
    other_info[$2] = $1"\t"$3"\t"$4"\t"$5"\t"$6;
}
ARGIND==2{
    if ($1 in push_audit_time) {print other_info[$1],$0,push_audit_time[$1];}
}' user_data.txt.${END_DAY} uid_regtime_efftime_mtefftime_clktime > uid_regtime_efftime_mtefftime_clktime_pushtime_audittime

python -c '
# -*- coding: utf-8 -*-
import sys
import pandas as pd

if __name__ == "__main__":
    file_input = sys.argv[1]
    file_output = sys.argv[2]

    tmp_data = pd.read_csv(file_input, sep = "\t", header = None, encoding = "utf8")
    tmp_data.columns = ["是否监察","违规类型", "是否A类", "来源", "批注", "userid", "注册时间", "生效时间", "物料审核通过时间", "点击时间", "推送时间", "判罚/审核时间"]
    tmp_data.to_csv(file_output, index = None, encoding = "gbk")
' uid_regtime_efftime_mtefftime_clktime_pushtime_audittime result_${END_DAY}.csv
```
