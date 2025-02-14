> Sequence: 根据指定的规范生成整数序列

## 

## 创建序列

```sql
CREATE [ TEMPORARY | TEMP ] SEQUENCE name [ INCREMENT [ BY ] increment ]
    [ MINVALUE minvalue | NO MINVALUE ] [ MAXVALUE maxvalue | NO MAXVALUE ]
    [ START [ WITH ] start ] [ CACHE cache ] [ [ NO ] CYCLE ]
    [ OWNED BY { table.column | NONE } ]
 
 /* 创建默认序列，从1开始，递增幅度为1，最大值为2^63-1*/
 create sequence 序列名称;
 /* 创建指定序列 */
create sequence 序列名称 increment by 递增幅度 minvalue 最小值  maxvalue 最大值  start with 开始值;

```

## 修改序列的值

### 方法 1

```
select setval('序列名称',修改后的值)；
```

### 方法 2

```sql
alter SEQUENCE 序列名称 RESTART WITH 修改后的值;
```

## 删除序列

```sql
drop sequence IF EXISTS 序列名称;
```

## 查看所有序列

```sql
SELECT c.relname FROM pg_class c WHERE c.relkind = 'S';
```

## 查看当前序列属性

```sql
select * from 序列名称;
```

## 给表的主键指定创建好的序列

```sql
alert table 表名 alert colum '主键id' set default nextval('要指定的序列名称');
```

## 序列自增

```sql
select nextval('序列名称');
```

## 序列函数

```
nextval: 递增序列对象到它的下一个数值并且返回该值
currval: 获取当前序列最后一次返回的值，如果该序列创建后未被调用，它可能会返回一个错误，可以用于判断该序列函数是否被其他会话调用
lastval: 和currval功能基本一直，它不需要序列名称作为参数，可以直接调用
setval: 
1. setval(regclass, bigint)：重置序列的计数器值，设置序列的计数器的值未指定值，将序列的is_calld字段设置未True，下一次nextval则会先递增序列，随后返回数值
2. setval(regclass, bigint, boolean)：与上面的功能基本一直，多了一个布尔参数，这个参数是指定is_calld的值，如果将is_calld参数的值设定为false，则下一次nextval返回该数值，下下一次nextval才会递增数列
```

