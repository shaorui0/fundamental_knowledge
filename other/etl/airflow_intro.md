# Airflow


## 为什么引入airflow？


### crontab解决了哪些问题？

一般的etl功能通过`.sh` + crontab。这种形式对付一般的例行任务是足够的，但是对于更加复杂的例行任务（各种数据集的依赖，任务报警、重试）以及一些扩展性需求（性能上的需求，比如并发），shell文件的复杂度会变的非常大。


其他依赖包括什么？
- 时间依赖，crontab自身支持例行时刻和间隔
- 外部系统依赖，需要shell自己调用接口
- 任务间的依赖，通常通过shell函数来完成

### 为什么需要Airflow？

任务调度不止是**工作流的执行**，还要包括：
- 日志记录
    - RD介入是否方便？
    - 日志形式是否直观？
- 任务报警
- 失败重试

### 额外的惊喜？

额外的，整个调度系统是否有比较好的伸缩性？比如并发机制（**多个调度任务能不能并发？甚至扩展到多机？**）。涉及到这些高级功能，一般的调度方式是很难满足了。


Airflow 同时拥有不错的**集群扩展能力**，可使用 CeleryExecuter 以及多个 Pool 来提高任务**并发度**。

### ETL上的实践

Airflow的理念，天然的适用于 ETL 过程。Airflow 本质是通过DAG来控制任务依赖，**有向无环图**保证了任务之间不会有循环依赖。

在现阶段的实践中，我们使用 Airflow 来同步各个数据源数据到数仓，同时定时执行一些批处理任务及带有数据依赖、资源依赖关系的计算脚本。

- Airflow 在 CeleryExecuter 下可以使用不同的用户启动 Worker，不同的 Worker 监听不同的 Queue，这样可以解决用户权限依赖问题。 Worker 也可以启动在多个不同的机器上，解决**机器依赖**的问题。

- Airflow 可以为任意一个 Task 指定一个抽象的 Pool，每个 Pool 可以指定一个 Slot 数。 每当一个 Task 启动时，就占用一个 Slot，当 Slot 数占满时，其余的任务就处于等待状态。这样就解决了**资源依赖**问题。



## Airflow的升级


### 涉及到pyenv和virtualenv的环境隔离

```
# 创建测试所需数据库

1. mysql: 
DF_Airflow_test;
DF_Airflow_Celery_test;
2. redis: 
10.26.149.41:7000 

# airflow 通用安装 e.g. py27 单机多版本注意要设置不同的家目录
mkdir airflow-1.10.10-py-2.7.14
cd airflow-1.10.10-py-2.7.14/
pyenv virtualenv 2.7.14  airflow-1.10.10-py-2.7.14
pyenv local airflow-1.10.12-py-2.7.14
export AIRFLOW_HOME=~/airflow-1.10.10-py-2.7.14
pip install  apache-airflow[mysql,celery]==1.10.12  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-2.7.txt"

# airflow 1.10.3 安装
pip install  apache-airflow==1.10.3   --use-feature=2020-resolver
# airflow 1.10.12 安装
## py3
pip install  apache-airflow[mysql]==1.10.12  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"
## py2
pip install  apache-airflow[mysql]==1.10.12  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-2.7.txt"
# airflow 升级 py27-airflow-1.10.12 不加constraint会报错
pip install -U  apache-airflow==1.10.12  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-2.7.txt"
# fbac前端创建用户
airflow create_user -r Admin -u admin -e qinyufeng@baidu.com -f qin -l yufeng -p admin
```

[> REF BLOG](https://zhuanlan.zhihu.com/p/90282578)