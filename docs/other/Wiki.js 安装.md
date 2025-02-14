
[toc]

## 安装NodeJS

### 下载

```
# 官网地址
http://nodejs.cn/download/
# 选择Linux二进制文件
wget https://npmmirror.com/mirrors/node/v16.19.1/node-v16.19.1-linux-x64.tar.xz
```

### 解压

```
// 将 tar.xz 压缩文件转成 node-v16.19.1-linux-x64.tar
xz -d node-v16.19.1-linux-x64.tar.xz

// 再用 tar xvf node-v10.15.0-linux-arm64.tar  解压缩文件
tar -xvf node-v16.19.1-linux-x64.tar
```

### 测试

```
# 进入安装目录
cd ./node-v16.19.1-linux-x64/bin
# 查看版本
./node -v
```

### 配置软连接

```
ln -s /usr/local/src/node-v16.19.1-linux-x64/bin/node /usr/local/bin/node
ln -s /usr/local/src/node-v16.19.1-linux-x64/bin/npm /usr/local/bin/npm
```

## 升级sqlite(可忽略)

> 如果wikijs需要使用sqlite3作为数据库则需要使用此步骤, wiki.js需要sqlite3.9+以上的版本

### 卸载旧的sqlite

```
yum remove sqlite
```

### 下载

```
# 官网地址 https://www.sqlite.org/download.html
wget -O sqlite-3350500.tar.gz   https://www.sqlite.org/2021/sqlite-autoconf-3350500.tar.gz
```

### 解压安装

```
# 解压
tar -zxvf sqlite-3350500.tgz.gz
# 进入目录
cd sqlite-3350500
# 编译安装
./configure --prefix=/usr/local/sqlite3
make && make install
```

### 测试是否安装成功

```
ls -l /usr/local/sqlite3/lib/*sqlite*
ls -l /usr/local/sqlite3/include/*sqlite*
**执行上述命令查看是否有输出
```

### 替换旧sqlite

```
# 替换旧的软连接
mv /usr/bin/sqlite3  /usr/bin/sqlite3_old
# 设置新的软连接
ln -s /usr/local/sqlite3/bin/sqlite3   /usr/bin/sqlite3
echo "/usr/local/sqlite3/lib" > /etc/ld.so.conf.d/sqlite3.conf
ldconfig
```

### 检查版本

```
[root@localhost ~]# sqlite3
SQLite version 3.35.5 2021-04-19 18:32:05
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite>
```



## 安装wiki.js
> 官网：https://docs.requarks.io/install/requirements
### 下载

```
wget https://github.com/Requarks/wiki/releases/latest/download/wiki-js.tar.gz
```

### 解压

```
mkdir wiki
tar xzf wiki-js.tar.gz -C ./wiki
cd ./wiki
# 重命名配置文件
mv config.sample.yml config.yml
```

### 配置文件修改

```
# 端口
port: 3000 # 修改端口

# MySql/ PostgreSQL / MSSQL Server
db:
  type: mysql
  host: localhost
  port: 3306
  user: wikijs
  pass: wikijsrocks
  db: wiki
  
# sqlite
db:
  type: sqlite
  storage: db.sqlite

```

### 启动
```
node server
```

