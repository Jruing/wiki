postgres安装

## 前置条件

```
yum install -y perl-ExtUtils-Embed readline-devel zlib-devel pam-devel libxml2-devel libxslt-devel openldap-devel python-devel gcc-c++ openssl-devel cmake
```

## 创建用户及用户组

```
groupadd postgres_group
useradd -d /home/postgres -g postgres_group postgres
```

## 编译安装

```
tar -zxvf postgres-16-1.tar.gz
./configure --prefix=/opt/pgsql/postgresql --without-icu
make && make install
```

## 启动数据库

```
# 创建数据存放目录
mkdir -p /home/postgres/pgdata
# 初始化数据库
cd /opt/pgsql/postgres/bin
./initdb -D /home/postgres/pgdata/
# 启动数据库
cd /opt/pgsql/postgres/bin
./pg_ctl -D /home/postgres/pgdata/ -l logfile start
# 停止数据库
# cd /opt/pgsql/postgres/bin
# ./pg_ctl -D /home/postgres/pgdata/ stop
# 登录数据库
cd /opt/pgsql/postgres/bin
./psql -h localhost -p 5432 postgres
```

## 开放远程访问

```
cd /home/postgres/pgdata
# 备份pg服务配置文件
cp postgresql.conf postgresql.conf_init
# 编辑pg服务配置文件
vi postgresql.conf #将该配置文件中的listen_address的值从localhost修改为*，并将开头的#删除 
# 备份pg远程访问配置文件
cp pg_hba.conf pg_hba.conf_init
# 编辑pg远程访问配置文件
vi pg_hba.conf
# IPv4 local connections:
host    all             all             0.0.0.0/0            trust #加入这一行
host    all             all             127.0.0.1/32            trust

# 停止pg服务
cd /opt/pgsql/postgres/bin
./pg_ctl -D /home/postgres/pgdata/ stop
./pg_ctl -D /home/postgres/pgdata/ -l logfile start
```

## 创建角色

```
# 先使用postgres用户登录数据库，创建一个可以登录及创建数据库的角色test001
create role test001 LOGIN CREATEDB;
# 修改角色test001的密码为test1234
alter user test001 password 'test1234';
# 创建一个名称为test_001数据库并设定归属者为test001
create database test_001 owner test001
# 使用test001登录test_001数据库
cd /opt/pgsql/postgres/bin
./psql -h192.168.198.129 -p5432 -U test001 -dtest_001
# 创建一个名称为monitor_schema的模式
create schema monitor_schema
```

## 创建用户

> 其实用户和角色都是角色，只是用户是具有登录权限的角色。

```
# 创建一个用户normal_user1
create user normal_user1;
# 为用户normal_user1设置密码
alter user normal_user1 password 'test1234';
# 创建一个具有创建数据库权限的角色
create role createdb_role CREATEDB;
# 将角色createdb_role的权限赋予用户normal_user1
grant createdb_role to normal_user1;
# 移除normal_user1创建库的权限
revoke createdb_role from normal_user1;
```

