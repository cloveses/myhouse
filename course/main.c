#include <stdio.h>
#include <stdlib.h>
#include "sqlite3.h"

	
//查询的回调函数声明及定义 

int select_callback(void * data, int col_count, char ** col_values, char ** col_Name)

{

  // 每条记录回调一次该函数,有多少条就回调多少次

  int i;

  for( i=0; i < col_count; i++){

    printf( "%s = %s\n", col_Name[i], col_values[i] == 0 ? "NULL" : col_values[i] );

  }



  return 0;

}	
	

int main(int argc, char * argv[])

{

  const char * sSQL1 = "create table users(userid varchar(20) PRIMARY KEY, age int, birthday datetime);";

  char * pErrMsg = 0;

  int result = 0;

  // 连接数据库

  sqlite3 * db = 0;

  int ret = sqlite3_open("./课程设计.db", &db);

  if( ret != SQLITE_OK ) {

    fprintf(stderr, "无法打开数据库: %s", sqlite3_errmsg(db));

    return(1);

  }

  printf("数据库连接成功!\n");
  getch(); 


  // 执行建表SQL

  sqlite3_exec( db, sSQL1, 0, 0, &pErrMsg );

  if( ret != SQLITE_OK ){

    fprintf(stderr, "SQL error: %s\n", pErrMsg);

    sqlite3_free(pErrMsg);

  }



  // 执行插入记录SQL

  result = sqlite3_exec( db, "insert into users values(111,18,'2000-03-11');", 0, 0, &pErrMsg);

  if(result == SQLITE_OK){

    printf("插入数据成功\n");

  }

  result = sqlite3_exec( db, "insert into users values(222,19,'1999-10-19');", 0, 0, &pErrMsg);

  if(result == SQLITE_OK){

    printf("插入数据成功\n");

  }
  


  // 查询数据表

  printf("查询数据库内容\n");

  sqlite3_exec( db, "select * from users;", select_callback, 0, &pErrMsg);
  
  
  //删除数据
  getch();
  
  
  ret = sqlite3_exec(db,"delete from users where userid=111",0,0,&pErrMsg);
  if(ret != SQLITE_OK){
  	sqlite3_close(db);
  	printf("删除失败\n");
  	return 1;
  } 
     printf("删除成功\n");
  
  
  getch(); 
  
   printf("查询数据库内容\n");

  sqlite3_exec( db, "select * from users;", select_callback, 0, &pErrMsg);
  
  // 关闭数据库
  getch();
 
  sqlite3_close(db);

  db = 0;

  printf("数据库关闭成功!\n");



  return 0;

}

//int main(){
//	const char *select_query="select * from users";
//	int ret = 0;
//	sqlite3 *db = 0;
//	char *s;
//	//打开数据库，不存在，创建数据库db
//	ret = sqlite3_open("./mydb",&db);
//	if(ret != SQLITE_OK)
//    {
//       printf("无法打开数据库\n");
//       return 1;
//    }
//    printf("数据库连接成功\n");
//    //创建表
//    ret = sqlite3_exec(db,"create table if not exists users(id int(10),name char(20))",0,0,&s);
//    if(ret !=   SQLITE_OK)
//    {
//        sqlite3_close(db);
//        printf("create error\n");
//        return 1;
//    }
//    printf("create success\n");
//    //插入数据
//    ret = sqlite3_exec(db,"insert into users values(1,'aass')",0,0,&s);
//    ret += sqlite3_exec(db,"insert into users values(2,'bbbb')",0,0,&s);
//    ret += sqlite3_exec(db,"insert into users values(3,'cccc')",0,0,&s);
//    if(ret != SQLITE_OK)
//    {
//    	     sqlite3_close(db);
//         printf("insert error\n");
//         return 1;
//    }
//    printf("insert success\n");
//    
//    //删除
//    ret = sqlite3_exec(db,"delete from users where id=1",0,0,&s);
//    if(ret != SQLITE_OK)
//    {
//         sqlite3_close(db);
//         printf("delete error\n");
//         return 1;
//    }
//    printf("delete success\n");
//    //更新
//    ret = sqlite3_exec(db,"update users set name='qqq' where id=3",0,0,&s);
//    if(ret != SQLITE_OK)
//    {
//    	sqlite3_close(db);
//         printf("update error\n");
//         return 1;
//    }
//    printf("update success\n");
//    
//    //查询
//    int nrow,ncolumn;
//    char ** db_result;
//    ret = sqlite3_get_table(db,select_query,&db_result,&nrow,&ncolumn,&s);
//     if(ret != SQLITE_OK)
//    {
//        printf("select error\n");
//        sqlite3_close(db);
//        return 1;
//    }
//    int i,j;
//    for(i=0;i<(nrow+1)*ncolumn;i+=ncolumn)
//    {
//        for(j=0;j<ncolumn;j++)
//        {
//             printf("%s  ",db_result[i+j]);
//    	}
//        printf("\n");
//    }
//    sqlite3_close(db);
//    db = 0;
//    return 0;
//}
