import pymysql


def insert_admin(username, password, mobile):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='aocc6530', charset='utf8', db='temp_admin')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = """
    insert into admin(username,password, mobile) 
    values (%s,%s,%s)
    """
    cursor.execute(sql, [username, password, mobile])
    conn.commit()

    cursor.close()
    conn.close()

def select_admin():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='aocc6530', charset='utf8', db='temp_admin')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from admin"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    insert_admin("泉奈","quannai","15515501555")
    # select_admin()

