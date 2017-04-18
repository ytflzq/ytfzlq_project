# -*-coding=UTF-8-*-
from django.db import connection
class Database:     
         
    def get_connection(self):     
        return connection     
         
    def get_cursor(self):     
        return self.get_connection().cursor()     
         
    # 根据SQL取一条指定数据     
    def select_fetchone(self,sql,params):     
        cursor = self.get_cursor()     
        cursor.execute(sql,params)     
        print "select_fetchone sql: %s" %(sql)     
        object = cursor.fetchone()     
        desc = cursor.description     
             
        if object:     
            print object     
            d = {}     
            i = 0     
            for item in desc:     
                d[item[0]] = object[i]     
                i=i+1     
            print "one %s" %(d)     
            return d     
        else:     
            return object     
     
     
    # 根据SQL取的数据列表     
    def select_fetchall(self,sql,params):     
        cursor = self.get_cursor()     
        cursor.execute(sql,params)     
             
        print "select_fetchall sql: %s" %(sql)     
             
        items = cursor.fetchall()     
             
        desc = cursor.description     
        li = []     
        if items:     
            for item in items:                     
                d = {}     
                i = 0     
                for de in desc:     
                    d[de[0]] = item[i]     
                    i=i+1     
                li.append(d);     
            return li     
        else:     
            return li     
         
             
    # 执行插入和更新     
    def execute(self,sql,params):     
        print "execute sql : %s" %(sql)     
        connection = self.get_connection()     
        cursor=connection.cursor()     
        cursor.execute(sql,params)     
        connection.commit() 
    #删除操作    
    def delOperation(self,tablename,id):
        sql = "delete from "+tablename+" where id =%s"
        print "execute sql : %s" %(sql)     
        params=[id]
        connection = self.get_connection()     
        cursor=connection.cursor()     
        cursor.execute(sql,params)
        connection.commit() 
        pass
import MySQLdb
if __name__ == '__main__':
    conn=MySQLdb.connect(host="localhost",user="yuantingfei",passwd="yuantingfei",db="ytf")
    cursor=conn.cursor()
    n=cursor.execute("SELECT DISTINCT name FROM user")
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    print row