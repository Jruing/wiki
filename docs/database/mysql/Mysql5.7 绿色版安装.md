# Mysql5.7 绿色版安装

## 绿色版下载
[下载地址](https://dev.mysql.com/gt/Downloads/MySQL-5.7/mysql-5.7.18-winx64.zip)


## 安装步骤

1. 解压mysql-5.7.18-winx64.zip 到指定文件夹(根据自己情况确定)
2. 进入文件夹mysql-5.7.18-winx64
3. 创建名为 `data` 的文件夹(若文件夹已存在,则清空文件夹中的文件)

```

# 进入文件夹
cd mysql-5.7.18-winx64
# 查看目录信息
dir
# 判断有没有data,如果没有,则创建data文件夹
mkdir data
# 如果有,清空data文件夹
del data

```



## 启动及配置Mysql

1. 以管理员权限运行cmd,并进入 `mysql-5.7.18-winx64/bin`目录下

2. 安装Mysql服务: cmd中输入 `mysqld.exe –install`,安装成功会出现 `Service successfully installed` 的提示字样

   ```
   D:\tools\mysql-5.7.18-winx64\bin> mysqld.exe -install
   Service successfully installed.
   ```

   

3. 初始化数据库: cmd中输入 `mysqld --initialize-insecure --user=mysql --explicit_defaults_for_timestamp` (运行务必检测data文件夹中没有文件),这个没有任何返回值

4. 启动mysql: cmd中输入 `net start mysql`, 启动成功会出现 `mysql 服务已经启动成功` 的提示字样

   ```
   D:\tools\mysql-5.7.18-winx64\bin> net start mysql
   MySQL 服务正在启动 .
   MySQL 服务已经启动成功。
   ```

   

5. 测试mysql : cmd中输入 `mysql.exe -uroot -p`, 接下来会让你输入密码,没有密码直接回车就行,到这里就证明mysql安装是没有问题的

   ```
   D:\tools\mysql-5.7.18-winx64\bin>mysql.exe -uroot -p
   Enter password:
   Welcome to the MySQL monitor.  Commands end with ; or \g.
   Your MySQL connection id is 3
   Server version: 5.7.18 MySQL Community Server (GPL)
   
   Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.
   
   Oracle is a registered trademark of Oracle Corporation and/or its
   affiliates. Other names may be trademarks of their respective
   owners.
   
   Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
   
   mysql>
   ```

6. 我们需要配置mysql编码为UTF8,在`mysql-5.7.18-winx64` 目录下创建名为 `my.ini` 的文件,文件内容如下

   ```
   [mysqld]
   character-set-server=utf8
   [mysql]
   default-character-set=utf8
   ```

7. 查看mysql修改前编码

   ```
   mysql> show variables like 'character%';
   +--------------------------+----------------------------------------------+
   | Variable_name            | Value                                        |
   +--------------------------+----------------------------------------------+
   | character_set_client     | gbk                                          |
   | character_set_connection | gbk                                          |
   | character_set_database   | latin1                                       |
   | character_set_filesystem | binary                                       |
   | character_set_results    | gbk                                          |
   | character_set_server     | latin1                                       |
   | character_set_system     | utf8                                         |
   | character_sets_dir       | D:\tools\mysql-5.7.18-winx64\share\charsets\ |
   +--------------------------+----------------------------------------------+
   8 rows in set, 1 warning (0.00 sec)
   ```

8. 重启mysql服务

   ```
   # 进入bin目录
   cd bin/
   # 重启服务
   mysqld.exe restart
   ```
   
9. 查看mysql修改后编码

   ```
   mysql> show variables like 'character%';
   +--------------------------+----------------------------------------------+
   | Variable_name            | Value                                        |
   +--------------------------+----------------------------------------------+
   | character_set_client     | utf8                                         |
   | character_set_connection | utf8                                         |
   | character_set_database   | latin1                                       |
   | character_set_filesystem | binary                                       |
   | character_set_results    | utf8                                         |
   | character_set_server     | latin1                                       |
   | character_set_system     | utf8                                         |
   | character_sets_dir       | D:\tools\mysql-5.7.18-winx64\share\charsets\ |
   +--------------------------+----------------------------------------------+
   8 rows in set, 1 warning (0.00 sec)
   ```

10. 修改mysql密码

    ```
    # 进入名为mysql的数据库
    use mysql;
    
    # 修改mysql密码为 `123123`
    update user set authentication_string=PASSWORD("123123") where user="root";
    
    # 刷新权限
    flush privileges; 
    ```

    返回结果

    ```
    mysql> use;
    ERROR:
    USE must be followed by a database name
    mysql> use mysql;
    Database changed
    mysql> update user set authentication_string=PASSWORD("123123") where user="root";
    Query OK, 1 row affected, 1 warning (0.01 sec)
    Rows matched: 1  Changed: 1  Warnings: 1
    
    mysql> flush privileges;
    Query OK, 0 rows affected (0.03 sec)
    ```

11. 测试mysql密码

    ```
    # 退出mysql
    quit;
    
    # 进入mysql
    mysql.exe -uroot -p123123  // -u 指定登录用户  -p指定该用户密码
    
    ```

    返回结果

    ```
    D:\tools\mysql-5.7.18-winx64\bin>mysql.exe -uroot -p123123
    mysql: [Warning] Using a password on the command line interface can be insecure.
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 10
    Server version: 5.7.18 MySQL Community Server (GPL)
    
    Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.
    
    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.
    
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    
    mysql>
    ```

    

## 其他命令

1. 卸载mysql服务

   ```
   mysqld.exe –remove
   ```

2. 停止MySQL服务

   ```
   net stop mysql
   ```

3. 忘记root账户密码

   1. 在`my.ini` 中[mysqld]下添加一行`skip-grant-tables`
   2. 重启mysql服务,参考启动及配置mysql下第8点
   3. 在cmd中执行 `mysql -uroot -p` 进入mysql
   4. 修改root账户密码, 参考启动及配置mysql下第10点
   5. 退出mysql, 将`my.ini`文件中刚才加入的`skip-grant-tables` 删掉,保存文件重启mysql服务即可

4. 修改mysql访问权限,解决只允许localhost访问的问题

   1. 第一种解决方案: 改表法(不建议)

      ```
      Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
      
      mysql> use mysql;
      Database changed
      mysql> update user set host = '%' where user ='root';  // 修改root用户可以以任何地址访问mysql服务
      Query OK, 1 row affected (0.00 sec)
      Rows matched: 1  Changed: 1  Warnings: 0
      
      mysql> flush privileges; //刷新权限
      Query OK, 0 rows affected (0.02 sec)
      ```

   2. 第二种解决方案:授权法(建议)

      ```
      Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
      
      mysql> grant all privileges on *.* to 'root'@'%' identified by '123123'; //赋予root用户以密码为123123查看所有库
      Query OK, 0 rows affected, 1 warning (0.00 sec)
      
      mysql> flush privileges;  // 刷新权限
      Query OK, 0 rows affected (0.00 sec)
      ```

   3. 关闭授权

      ```
      Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
      
      mysql> revoke all on *.* from root@'%'; //撤销root用户的授权
      Query OK, 0 rows affected (0.00 sec)
      
      mysql> flush privileges;
      Query OK, 0 rows affected (0.00 sec)
      ```

