import pymysql
# 创建
spider = pymysql.Connect(
    host = '127.0.0.1',
    port=3306, # 主机端口号
    user='admin',
    password='qwe123',
    database='spider',
    charset='utf8' # 注意不能写出utf-8
)
# 创建‘游标对象’：
yb = spider.cursor()
# 写出sq;语句命令，再使用 游标对象名.execute(sql语句) 函数来执行命令：
c = 'create table if not exists s1(id int(11) primary key, name varchar(25))'
yb.execute(c)
# 插入数据：
s = 'insert into s1 values (1, "lucy"), (2, "tom")'
yb.execute(s)
# 查询数据：
ss = 'select * from s1'
yb.execute(ss)
print(yb.fetchall())
# 关闭事务：
'''
两种模式：
    1、关闭且保存修改==》数据库连接对象.commit()
    2、关闭且撤销修改==》数据库连接对象.rollback()
'''
yb.close()      # 关闭游标对象
spider.close()  # 关闭数据库连接对象
