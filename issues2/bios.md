
# BIOS

+ ROM
> Read Only Memory(只读存储器)，与可读可写的RAM(Random Access Memory)可读可写不同，它焊在主板上且只读。
	电脑主板刚启动的时会将有限的空间划分为 ROM(0xFFFFF-0xF0000)、存储器扩充区RAM(0xF0000-0xC0000)、视频显示区RAM(0xC0000-0xA0000)、普通内存区RAM(0xA0000-0x00000)、BIOS数据区及终端服务(0xA0000-0x00000)、BIOS中断向量表(0xA0000-0x00000)。ROM用于加载第一条指令。

+ Grub2
> 系统启动工具。Grub2将启动盘的前512字节(以0xAA55结束)写入启动逻辑。
	- 检查硬件
	- 基本的中断能力
	- 视频显示能力
	- 内存能力(用于输入输出数据暂存)及内存映射能力
> BIOS完成后会加载1个镜像到内存中运行,由这个镜像继续加载后面的镜像:
	BIOS -> boot.img:		加载Grub2的另一个镜像core.img
		boot.img是引导扇区
	boot.img -> core.img:	包含了解压缩、硬盘启动、内核、及其他模块
		硬盘启动[diskboot.img]
		解压缩	[lzma_decompress.img]
		内核	[kernel]
		模块及其他[modules & others]
	lzma_decompress.img -> 从实模式切换到保护模式以获得更多内存
		* 调用real_to_prot
		* 打开1M以外的地址线控制线第21根(扩大寻址范围)
		* 建立分段分页用于区分进程
		* 解压缩kernel.img, 运行kernel
	kernel.img -> 进入交互
		* 调用grub_normal_execute()选择操作系统
		* 根据linux指定命令(linux16)找到内核文件并加载
		* grub_command_execute("boot",0,0)启动内核
	

+ 0号进程
> 唯一一个没有通过fork或kernel_thread产生的进程
	- 中断处理: trap_init()
	- 内存处理: mm_init()
	- 内核调度: sched_init()
	- 基于内存的文件系统rootfs: vfs_caches_init()
	- 其他内容初始化: rest_init()
	[当然还有其他的一些初始化没有列举完]

+ 1号进程
> rest_init() 用 kernel_thread创建1号进程。
	为了更好地管理资源，x86提供了分层权限(内核态和用户态)分为4层:
	+ Ring0: 内核
	+ Ring1: 设备驱动
	+ Ring2: 设备驱动
	+ Ring3: 应用
	一个完整的保护模式下的系统调用如下:
		用户态-系统调用-保存寄存器-内核执行系统调用-恢复寄存器-返回到用户态
	初始化一系列的系统服务，控制台，这样用户就能登录了
	
+ 2号进程
> 继续kernel_thread()
