import psycopg2

try:
    connection = psycopg2.connect(
        host="43.143.223.4",
        port="5432",
        database="postgres",
        user="postgres",
        password="obe_group"
    )
    
    cursor = connection.cursor()
    print("成功连接到数据库")

    query = "select * from student;"
    cursor.execute(query)
    print(f"查询：{query}")

    print("查询结果:")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

except Exception as error:
    print("连接数据库时出错:", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("数据库连接已关闭")
