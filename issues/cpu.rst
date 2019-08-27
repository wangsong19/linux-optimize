CPU
===

几个简单基本概念
----------------

负载
++++

平均负载:
    单位时间内系统处于可运行状态(Runnable/Running)和不可中断状态(Disable(I/O))的平均进程数(活跃进程)
    [实际是活跃进程数的指数衰减平均值，更快速的算法，也可简单理解为平均值]

  .. code:: shell
  $ uptime
    15:48  up 11 days, 53 mins, 7 users, load averages: 2.05 1.96 1.78
    ------------------------------------------------------------------
    时间   系统运行时间       在登录用户数  过去1分钟、5分钟、15分钟平均负载

  .. code:: shell
  $ cat /proc/cpuinfo | grep 'model name' | wc -l
    ---------------------------------------------
    这样可以查看到系统的cpu个数
 
    Q:> 设么时候负载最好?
    A:> 平均负载值 = cpu个数 [比如双核，最好负载为2.0左右]
    Q:> 达到什么值则为负载过高
    A:> cpus x 170% [其实正确来看待是超过cpus就应该引起注意了，特别是达到cpus x 1.5]
    Q:> cpu使用率和平均负载值一致吗？
    A:> 平均负载包含了正在使用cpu的进程，也就是一个 load_avg > use_avg 的关系
    
    tools
    ------------------------------------------------------------------------------------------------
    #stress#
    [linux 系统压力测试工具, 可以用来模拟负载高升的情况]

    #systat-mpstat#
    [linux 各个cpu性能分析工具, 实时查看每个cpu的性能指标]

    #systat-pidstat#
    [linux 进程分析工具，实时查看进程的cpu、I/O、内存还有上下文切换等情况]

    >>>
    CPU 密集型
    ``stress --cpu 1 --timeout 600``    >>  ``watch -d uptime`` [实时查看uptime的结果] >>  load 值在逐渐地攀升 \
    ``mpstat -P ALL 5 1`` [查看所有cpu 每5秒输出一次 输出1次] >>  %usr的cpu占用达到100 \
    ``pidstat -u 5 1`` [间隔5秒输出一组数据]    >>  可以明显看到CPU达到100%的PID和Command
    IO密集型
    ``stress -i 1 --timeout 600``   \
    ``watch -d uptime`` >>  load值确实也是在升高 \
    ``mpstat -P ALL 5`` >>  发现不是iowait升高，而是sys在升高
    ``pidstat -u 5 1``  >>  结果还是sys占用过高
    x> 原来是-i 写错了，-i表示fork进程，这样sys调用过高肯定的
    v> 正确测试语句：``stress -d 1 --hdd-bytes 1G`` [一个写进程逐渐写满1G的内存, 会清理]
    进程密集型
    ``stress -c 10 timeout 600``    >>  可以看到10个进程对cpu的占用情况 基本应该是接近10%的user每个进程[实际13-14, load 6.2左右]

上下文切换
++++++++++

    进程上下文切换 + 线程上下文切换 + 中断上下文切换
    过多的上下文切换会将资源浪费在寄存器、内核栈、虚拟内存等数据的保存与恢复中
    .. code:: shell
        $ vmstat 5
        procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
        r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
        2  0      0 1434044   2108 331844    0    0    95    24  192 4985  8  5 87  0  0
        --------------------------------------------------------------------------------
        cs[content-swicth]: 每秒上下文切换次数
        in[interrupt]: 每秒中断次数
        r[runnable]: 就绪队列长度
        b[blocked]: 不可中断睡眠进程数
    * 使用pidstat -w 也能看到上下文切换的情况
    .. code:: shell
        $ pidstat -uw 3
        平均时间:   UID       PID    %usr %system  %guest    %CPU   CPU  Command
        平均时间:     0     14152    0.00    0.05    0.00    0.05     -  kworker/0:0
        平均时间:     0     14168    0.10    0.24    0.00    0.33     -  pidstat
        
        平均时间:   UID       PID   cswch/s nvcswch/s  Command
        平均时间:     0         3      0.57      0.00  ksoftirqd/0
        平均时间:     0         9      1.24      0.00  rcu_sched
        平均时间:     0        11      0.24      0.00  watchdog/0
        --------------------------------------------------------------------------------
        cswch/s: 自愿每秒上下文切换次数 [一般是无法获取资源，比如IO，内存等资源时自愿切换]
        nvcswch/s: 非自愿每秒上下文切换次数 [cpu时间到或者被其他高优先级中断而被动切换]

    tools
    ------------------------------------------------------------------------------------------------
    #sysbench#
    [linux 多线程测试工具，一般测试不同系统参数下的数据库负载能力]

    >>>
    ``sysbench --threads=10 --max-time=300 threads run`` [给出10个线程强力运行30秒] \
    ``vmstat 2``    >>  可以发现上下文切换次数、中断次数、内存使用等骤升，等待队列增加
    ``pidstat -wt 2``   >>  去掉u 加上t只看cs情况并附上指标 发现此时的切换数[vmstat和pidstat]显示得才对的上,并且能看到子线程的切换数情况
    ``watch -d /proc/interrupts``   >>  除了上下文切换还可以通过系统给用户空间提供的只读中断记录虚拟文件 来查看中断的情况 >> 
    发现RES类型的中断贼多，也就是唤醒空闲CPU来执行新任务，那意思就是任务过多的调度问题了

CPU使用率
+++++++++

cpu在单位时间内的使用情况，用%表示。一般的指标有%sys，%user，%nice，%iowait，%steal等
一些概念：
    - 节拍率(Hz)：
        - 用以触发时间中断，全局变量Jiffies记录了开机以来记录的节拍数，每中断一次，自增1.
        - Hz是可配置的比如100，250，表示每秒时间中断100次，250次等等。该配置在/boot/config中 ``cat /boot/config-$(uname -r) | grep CONFIG_HZ``
        - 用户空间的节拍率总是固定的 USER_HZ=100
        - ``cat /proc/stat | grep ^cpu`` 记录了各个cpu在不同场景下cpu的使用时间（以USER_HZ为记录单位）
    - user[us]: 用户态使用时间
    - system[sys]: 内核态使用时间
    - idle[id]: 空闲时间[不包括IO等待时间]
    - nice[ni]: 低优先级用户态时间[1-19/-20-19, 值越低优先级越高, 0一般是区分用户与内核优先级别的分水岭]
    - iowait[wa]: IO等待时长
    - softirq[si]: 软中断处理时长
    - irq[hi]: 硬中断处理时长
    - steal[st]: 系统在虚拟机中运行时，被其他虚拟机占用（掠夺）的时长
    - guest[guest]: 虚拟机运行时长
    - guest_nice[gnice]: 虚拟机低优先级运行时长
    - CPU使用率
        1 - CPU空闲/CPU总运行时
    - 各个进程的cpu使用时间在/proc/[pid]/stat 中
    - 辅助工具是检测的一个时间段的值，也就是说在这段时间内的一个增量

    .. code:: shell
        $ perf top
        Samples: 208  of event 'cpu-clock', Event count (approx.): 38243368
        Overhead  Shared Object               Symbol
          16.02%  [kernel]                    [k] avtab_search_node
           7.23%  [kernel]                    [k] _raw_spin_unlock_irqrestore
        ---------------------------------------------------------------------
        Samples: 采样数
        event: 采样事件
        Event count: 事件总数
        Overhead: 基本比例
        Shared Object: 动态共享对象
        Symbol: 函数名
        [.]: 用户态
        [k]: 内核态
    * 可以使用perf-record 和 perf-report 来记录下和分析采样的数据
    .. code:: shell
        $ perf-record 
        # 等待一段时间 ctl-c
        $ perf-report

    tools
    ------------------------------------------------------------------------------------------------
    #ab#
    [apache bench, http压力测试工具]

    >>>
    $ ab -c 10 -n 50 http://xxx.xxx.xxx.xxx:8888/
    [并发10个请求，共50个请求]
    This is ApacheBench, Version 2.3 <$Revision: 1826891 $>
    ...
    Server Software:        BWS/1.1
    Server Hostname:        39.156.66.14
    Server Port:            80
    HTML transferred:       7689880 bytes
    ...
    Requests per second:    24.07 [#/sec] (mean)
    Time per request:       415.386 [ms] (mean)
    Time per request:       41.539 [ms] (mean, across all concurrent requests)
    ...
    
    #perf & perf-record & perf-report#
    [perf采样分析 根据top采样进程数据进行分析]
    
    >>>
    $ perf top -g -p 32122
    [直接开启采样而不做记录: 采样指令top -p指定进程号为32122， -g开启调用关系]
    
    Samples: 55  of event 'cpu-clock', Event count (approx.): 7950039
    Children      Self  Shared Object      Symbol
    -   36.79%    36.79%  [kernel]           [k] finish_task_switch
      26.58% 0x484d75c08548008b
      14.41% runtime.goexit
      ...
    

