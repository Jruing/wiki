# Neo4j 实现一个简单的CMDB管理平台

## 简介

> Neo4j是一个高性能的图形数据库管理系统，它使用图形模型来存储和查询数据。图形数据库与传统的关系型数据库不同，它们使用节点和边来表示数据实体和它们之间的关系，而不是使用表格和行,可以使用neo4j实现权限系统，知识图谱，cmdb等

## 部署

```
docker run -d --name=neo4j \
  --publish=7474:7474 --publish=7687:7687 \
  --volume=$HOME/neo4j/data:/data \
  --volume=$HOME/neo4j/logs:/logs \
  --volume=$HOME/neo4j/import:/var/lib/neo4j/import \
  --volume=$HOME/neo4j/plugins:/plugins \
  neo4j:latest
```

## neo4j密码
```
docker logs neo4j 2>&1 | grep 'Initial password'
```

访问地址：`http://ip:7474`

## 创建节点

```
# ()表示一个node节点，n是一个别名，tag是标签，{}是该节点的属性及该属性对应的值，可以有多个不同属性,属性和标签可以忽略
create (n:tag {"property":"属性值"})
```

## 创建节点与节点关联关系

```
# 先匹配要建立关联关系的两个节点,其次才创建关联关系
# 栗子
match (p1:instance {property:"192.168.1.1"}),(p2:env {property:"测试环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
# 先匹配出标签为`instance`，属性`property`的值为`192.168.1.1`以及标签为`env`，属性`property`的值为`测试环境`的两个节点，分别为p1和p2,创建p1指向p2的关联关系
`[r:envre {relation:''}]`:[]代表关联关系，r是一个别名，envre代表这个关联关系类型的标签。{}代表关联关系的属性，支持多个不同的属性
```

## 新增逻辑环境节点

```
Create (n:env {property:"生产环境"});
Create (n:env {property:"测试环境"});
```

## 新增主机实例节点
```
Create (n:instance {system:"Centos Linux",property:"192.168.1.1"});
Create (n:instance {system:"Centos Linux",property:"192.168.1.2"});
Create (n:instance {system:"Centos Linux",property:"192.168.1.3"});
Create (n:instance {system:"Centos Linux",property:"192.168.1.4"});
Create (n:instance {system:"Centos Linux",property:"192.168.1.5"});

Create (n:instance {system:"Centos Linux",property:"192.168.2.1"});
Create (n:instance {system:"Ubuntu Linux",property:"192.168.2.2"});
Create (n:instance {system:"Centos Linux",property:"192.168.2.3"});
Create (n:instance {system:"SUSE Linux",property:"192.168.2.4"});
Create (n:instance {system:"Centos Linux",property:"192.168.2.5"});
```
## 创建主机与逻辑环境关联关系

```
#192.168.1.x段的ip归属于测试环境
#192.168.2.x段的ip归属于生产环境
match (p1:instance {property:"192.168.1.1"}),(p2:env {property:"测试环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
match (p1:instance {property:"192.168.1.2"}),(p2:env {property:"测试环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
match (p1:instance {property:"192.168.1.3"}),(p2:env {property:"测试环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
match (p1:instance {property:"192.168.1.4"}),(p2:env {property:"测试环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
match (p1:instance {property:"192.168.1.5"}),(p2:env {property:"测试环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
match (p1:instance {property:"192.168.2.1"}),(p2:env {property:"生产环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
match (p1:instance {property:"192.168.2.2"}),(p2:env {property:"生产环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
match (p1:instance {property:"192.168.2.3"}),(p2:env {property:"生产环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
match (p1:instance {property:"192.168.2.4"}),(p2:env {property:"生产环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
match (p1:instance {property:"192.168.2.5"}),(p2:env {property:"生产环境"}) create (p1)-[r:envrel {relation:''}]->(p2);
```

## 新增应用服务节点
```
Create (n:service {servicetype:"application",property:"权限系统"});
Create (n:service {servicetype:"email",property:"邮件服务"});
Create (n:service {servicetype:"database",property:"Mysql"});
Create (n:service {servicetype:"application",property:"测试系统"});
Create (n:service {servicetype:"application",property:"oa系统"});
```


## 创建服务与主机关联关系
```
match (p1:service {property:"oa系统"}),(p2:instance {property:"192.168.2.1"}) create (p1)-[r:servicerel {relation:'隶属于'}]->(p2);
match (p1:service {property:"权限系统"}),(p2:instance {property:"192.168.2.2"}) create (p1)-[r:servicerel {relation:'隶属于'}]->(p2);
match (p1:service {property:"邮件服务"}),(p2:instance {property:"192.168.2.3"}) create (p1)-[r:servicerel {relation:'隶属于'}]->(p2);
match (p1:service {property:"Mysql"}),(p2:instance {property:"192.168.2.4"}) create (p1)-[r:servicerel {relation:'隶属于'}]->(p2);
match (p1:service {property:"测试系统"}),(p2:instance {property:"192.168.1.1"}) create (p1)-[r:servicerel {relation:'隶属于'}]->(p2);
match (p1:service {property:"oa系统"}),(p2:service {property:"Mysql"}) create (p1)-[r:depend {relation:'依赖于'}]->(p2);
```

## 匹配所有节点信息

> 列出所有节点及关联信息，这样可以很清晰的看出主机与服务及逻辑环境的关联关系

```
match (n)
return (n)
```

![image-20240808171246708](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20240808171246708.png)

## 匹配某个节点

```
match(n)
WHERE id(n) = <节点ID>
return n
```

## 匹配某个节点及与他关联的节点

```
match(n1)-[r]-(n2)
where id(n1)=15
return (n1),r,n2
```

![image-20240808172909552](https://jruing-blogs.oss-cn-beijing.aliyuncs.com/blogs/image-20240808172909552.png)

## 设置节点属性

```
# 为节点id为123的节点设置一个属性为name，值为John Doe
MATCH (n)
WHERE id(n) = 123
SET n.name = 'John Doe'
```

## 删除节点属性

```
# 移除节点id为123的name属性
MATCH (n)
WHERE id(n) = 123
REMOVE n.name
```

## 删除单个节点

> 注意：若该节点与其他节点有关联关系则会删除失败

```
MATCH (n)
WHERE id(n) = <节点ID>
DELETE n
```

## 删除节点及关联关系

```
MATCH (n)
WHERE id(n) = <节点ID>
DETACH DELETE n
```

