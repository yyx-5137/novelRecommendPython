import pymysql
import random
import numpy
# 打开数据库连接
connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='12345678',
    db='novel',
    charset='utf8'
)
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = connect.cursor()
 
# 使用 execute()  方法执行 SQL 查询 
cursor.execute("select id,novel_name,tag from novel_info")
 
with open("ml-latest-small/movies.csv", encoding="utf-8",mode="w") as file:
	file.write("movieId,title,genres\n")
	# 使用 fetchone() 方法获取单条数据.
	for row in cursor.fetchall():
		file.write("{},{},{}\n".format(row[0],row[1],row[2]))
cursor.execute("select id,novel_name,tag from novel_info")
with open("ml-latest-small/ratings.csv", encoding="utf-8",mode="w") as file:
	file.write("userId,movieId,rating,timestamp\n")
	# 使用 fetchone() 方法获取单条数据.
	for row in cursor.fetchall():
		for i in range(1,101):
			if random.random()<0.1:
				file.write("{},{},{},{}\n".format(i,row[0],numpy.random.randint(1,5),12731238))
# 关闭数据库连接
connect.close()