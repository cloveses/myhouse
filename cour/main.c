#include <stdio.h>
#include <stdlib.h>
#include "sqlite3.h"

/* run this program using the console pauser or add your own getch, system("pause") or input loop */

int main(int argc, char *argv[]) {
	const char *select_query="select * from users";
	int ret = 0;
	sqlite3 *db = 0;
	char *s;
	//打开数据库，不存在，创建数据库db
	ret = sqlite3_open("./mydb",&db);
	if(ret != SQLITE_OK)
    {
       printf("无法打开数据库\n");
       return 1;
    }
    printf("数据库连接成功\n");
    //创建表
    ret = sqlite3_exec(db,"create table if not exists users(id int(10),name char(20))",0,0,&s);
    if(ret !=   SQLITE_OK)
    {
        sqlite3_close(db);
        printf("create error\n");
        return 1;
    }
    printf("create success\n");
    //插入数据
    ret = sqlite3_exec(db,"insert into users values(1,'aass')",0,0,&s);
    ret += sqlite3_exec(db,"insert into users values(2,'bbbb')",0,0,&s);
    ret += sqlite3_exec(db,"insert into users values(3,'cccc')",0,0,&s);
    if(ret != SQLITE_OK)
    {
    	     sqlite3_close(db);
         printf("insert error\n");
         return 1;
    }
    printf("insert success\n");
    
    //删除
    ret = sqlite3_exec(db,"delete from users where id=1",0,0,&s);
    if(ret != SQLITE_OK)
    {
         sqlite3_close(db);
         printf("delete error\n");
         return 1;
    }
    printf("delete success\n");
    //更新
    ret = sqlite3_exec(db,"update users set name='qqq' where id=3",0,0,&s);
    if(ret != SQLITE_OK)
    {
    	sqlite3_close(db);
         printf("update error\n");
         return 1;
    }
    printf("update success\n");
    
    //查询
    int nrow,ncolumn;
    char ** db_result;
    ret = sqlite3_get_table(db,select_query,&db_result,&nrow,&ncolumn,&s);
     if(ret != SQLITE_OK)
    {
        printf("select error\n");
        sqlite3_close(db);
        return 1;
    }
    int i,j;
    for(i=0;i<(nrow+1)*ncolumn;i+=ncolumn)
    {
        for(j=0;j<ncolumn;j++)
        {
             printf("%s  ",db_result[i+j]);
    	}
        printf("\n");
    }
    sqlite3_close(db);
    db = 0;
    return 0;
}
