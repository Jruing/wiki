## 简介

```
UPX，即"Ultimate Packer for eXecutables"，是一款广受推崇的免费开源可执行文件压缩工具。它以其简洁的编写方式和强大的扩展性，为用户提供了一个高效的解决方案，专门用于压缩可执行的二进制程序、动态链接库以及其他类型的二进制文件，显著缩减它们的体积。UPX的核心优势在于其惊人的压缩能力，能够将文件大小减少50%至70%，有效节省磁盘空间，降低网络传输带宽需求，以及减少分发成本。自1996年问世以来，UPX在存储资源稀缺的年代，尤其是软盘盛行时期，其对可执行文件的压缩技术显得尤为关键。

除了基本的压缩功能，UPX还具备以下显著优势：

- 可靠性：UPX内置了一套严密的校验机制，确保压缩前后的文件保持完整性，保障程序的可靠性。
- 安全性：作为一个长期开源的项目，UPX的压缩逻辑对所有开发者和防病毒软件厂商开放，便于验证其安全性。
- 解压速度：在现代硬件上，UPX的解压速度超过500MB/秒，确保了快速的运行体验。
- 无内存开销：运行解压后的程序不会增加额外的内存负担，保持系统的流畅运行。
- 卓越的压缩比：与传统的Zip压缩算法相比，UPX提供了更优的压缩效果，进一步减少了分发文件的体积，节省了网络传输和存储资源。
- 通用性：UPX支持多种可执行文件格式的打包，包括Windows应用程序和DLL、macOS应用程序以及Linux可执行文件。
- 可扩展性：得益于其优秀的代码架构，UPX能够轻松添加对新的可执行文件格式和压缩算法的支持。

UPX以其卓越的性能和多功能性，成为了开发者和系统管理员在文件压缩领域的首选工具。

```

## 使用说明

用法： `upx [option] 文件名`

压缩相关参数

```
-9 或 –best: 使用最高的压缩比，这通常会产生最小的文件大小，但压缩速度较慢。
-6 或 –ultra: 使用较高的压缩比，压缩速度较快于 -9。
-5 或 –super: 使用较好的压缩比，压缩速度更快。
-4 或 –fast: 使用较快的压缩比，适合快速压缩。
-3 或 –veryfast: 使用最快的压缩比，适合快速处理大量文件。
```

输出控制参数

```
-o 或 –output <file>: 指定压缩后输出文件的路径和名称。
-d 或 --decompress: 解压已压缩的文件。
-t 或 –test: 测试压缩后的文件是否仍可正常运行。
-v 或 –verbose: 输出详细的压缩信息。
-qq 或 –quiet: 静默模式，不输出任何信息。
```

其他常用参数

```
-s 或 –strip: 移除调试信息。
-a 或 –add <file>: 向压缩后的可执行文件添加一个或多个文件。
-r 或 –replace: 替换压缩文件中的某个资源。
-m 或 –move: 移动指定的资源。
-l 或 –list: 列出压缩文件中的所有资源。
-i 或 –info: 显示压缩文件的信息。
-h 或 –help: 显示帮助信息。
-V 或 –version: 显示 UPX 的版本信息。
```



## 测试验证

```
# 采用使用最高的压缩比进行压缩
C:\Users\Lenovo\Desktop>upx.exe -9 caddy.exe
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2024
UPX 4.2.4       Markus Oberhumer, Laszlo Molnar & John Reiser    May 9th 2024

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
  41527296 ->  12843520   30.93%    win64/pe     caddy.exe                                                                                                                                                                                      Packed 1 file.
# 压缩前：39.6 MB (41,527,296 字节)  压缩后：12.2MB (12,843,520 字节)
# 测试压缩后是否可以正常执行
C:\Users\Lenovo\Desktop>upx.exe -t caddy.exe
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2024
UPX 4.2.4       Markus Oberhumer, Laszlo Molnar & John Reiser    May 9th 2024

testing caddy.exe [OK]

Tested 1 file.
```

