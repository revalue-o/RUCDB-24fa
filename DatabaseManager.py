import psycopg2
import bcrypt

class DatabaseManager:

    def __init__(
        self,
        debug=True,
        host="43.143.223.4",
        port="5432",
        database="postgres",
        user="postgres",
        password="obe_group"
    ):
        self._debug = debug

        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._password = password

        self._connection = None
        self._cursor = None

    def _print_debug(self, s: str):
        if self._debug:
            print("### DatabaseManager:", s)

    def connect(self):
        '''
        连接到Postgres

        返回:
            0:  连接成功
            1:  连接失败
        '''
        try:
            self._connection = psycopg2.connect(
                host="43.143.223.4",
                port="5432",
                database="postgres",
                user="postgres",
                password="obe_group"
            )
            self._cursor = self._connection.cursor()
            self._print_debug("成功连接到Postgres.")
            return 0

        except Exception as error:
            self._print_debug("连接到Postgres时出错:")
            print(error)
            return 1
    
    def disconnect(self):
        '''
        从Postgres断开连接

        返回:
            0:  断开连接成功
            1:  断开连接失败
        '''
        if self._connection:
            self._cursor.close()
            self._connection.close()
            self._print_debug("成功从Postgres断开连接.")
            return 0

        else:
            self._print_debug("先前未连接到Postgres,无法断开连接.")
            return 1
    
    def create_tables(self):
        '''
        创建所有表

        返回:
            0:  建表全部成功
            1:  建表失败
        '''
        with open("./sql/create.sql", 'r', encoding='utf-8') as file:
            sql_commands = file.read()

        sql_commands = sql_commands.split(';')

        for command in sql_commands:
            command = command.strip()

            if command:
                try:
                    self._cursor.execute(command)
                    self._print_debug("建表成功.")
                except Exception as error:
                    self._print_debug("建表失败:")
                    print(error)
                    self._connection.rollback()
                    return 1

        self._connection.commit()
        return 0

    def drop_tables(self):
        '''
        删除所有表

        返回:
            0:  删表全部成功
            1:  删表失败
        '''
        with open("./sql/drop.sql", 'r', encoding='utf-8') as file:
            sql_commands = file.read()

        sql_commands = sql_commands.split(';')

        for command in sql_commands:
            command = command.strip()

            if command:
                try:
                    self._cursor.execute(command)
                    self._print_debug("删表成功.")
                except Exception as error:
                    self._print_debug("删表失败:")
                    print(error)
                    self._connection.rollback()
                    return 1

        self._connection.commit()
        return 0
    
    def truncate_tables(self):
        '''
        截断所有表

        返回:
            0:  全部成功
            1:  失败
        '''
        with open("./sql/truncate.sql", 'r', encoding='utf-8') as file:
            sql_commands = file.read()

        sql_commands = sql_commands.split(';')

        for command in sql_commands:
            command = command.strip()

            if command:
                try:
                    self._cursor.execute(command)
                    self._print_debug("截断表成功.")
                except Exception as error:
                    self._print_debug("截断表失败:")
                    print(error)
                    self._connection.rollback()
                    return 1

        self._connection.commit()
        return 0

    def add_student(self,
                    sno: str,
                    spasswd: str,
                    sname: str  
                    ):
        '''
        添加一个学生用户

        参数:
            sno:        学工号,char(10)
            spasswd:    密码,不限长度
            sname:      学生姓名,varchar(16)

        返回:
            0:  添加学生用户成功
            1:  学工号格式不符合要求
            2:  学生姓名格式不符合要求
            3:  用户已存在
        '''

        if len(sno) != 10:
            self._print_debug("添加学生用户失败.")
            return 1

        if len(sname) > 16:
            self._print_debug("添加学生用户失败.")
            return 2

        query = f"select * from student where sno='{sno}';"
        self._cursor.execute(query)
        if self._cursor.fetchall() != []:
            self._print_debug("添加学生用户失败.")
            return 3

        shashedpasswd = bcrypt.hashpw(spasswd.encode('utf-8'), bcrypt.gensalt()).hex()
        query = f"insert into student values ('{sno}', '{shashedpasswd}', '{sname}')"

        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("添加学生用户成功.")
        return 0

    def add_teacher(self,
                    tno: str,
                    tpasswd: str,
                    tname: str  
                    ):
        '''
        添加一个教师用户

        参数:
            tno:        学工号,char(10)
            tpasswd:    密码,不限长度
            tname:      教师姓名,varchar(16)

        返回:
            0:  添加教师用户成功
            1:  学工号格式不符合要求
            2:  教师姓名格式不符合要求
            3:  用户已存在
        '''

        if len(tno) != 10:
            self._print_debug("添加教师用户失败.")
            return 1

        if len(tname) > 16:
            self._print_debug("添加教师用户失败.")
            return 2

        query = f"select * from teacher where tno='{tno}';"
        self._cursor.execute(query)
        if self._cursor.fetchall() != []:
            self._print_debug("添加教师用户失败.")
            return 3

        thashedpasswd = bcrypt.hashpw(tpasswd.encode('utf-8'), bcrypt.gensalt()).hex()
        query = f"insert into teacher values ('{tno}', '{thashedpasswd}', '{tname}')"

        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("添加教师用户成功.")
        return 0

    def delete_student(self,
                       sno: str
                       ):
        '''
        删除一个学生用户

        参数:
            sno:    学工号,char(10)
    
        返回:
            0:  删除学生用户成功
            1:  学工号格式不符合要求
            2:  不存在该用户
        '''

        if len(sno) != 10:
            self._print_debug("删除学生用户失败.")
            return 1
        
        query = f"select * from student where sno='{sno}'"
        self._cursor.execute(query)
        if self._cursor.fetchall() == []:
            self._print_debug("删除学生用户失败.")
            return 2

        query = f"delete from student where sno='{sno}'"

        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("删除学生用户成功.")
        return 0
        
    def delete_teacher(self,
                       tno: str
                       ):
        '''
        删除一个教师用户

        参数:
            tno:    学工号,char(10)
    
        返回:
            0:  删除教师用户成功
            1:  学工号格式不符合要求
            2:  不存在该用户
        '''

        if len(tno) != 10:
            self._print_debug("删除教师用户失败.")
            return 1
        
        query = f"select * from teacher where tno='{tno}'"
        self._cursor.execute(query)
        if self._cursor.fetchall() == []:
            self._print_debug("删除教师用户失败.")
            return 2

        query = f"delete from teacher where tno='{tno}'"
        
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("删除教师用户成功.")
        return 0

    def student_login_check(self,
                      sno: str,
                      spasswd: str
                      ):
        '''
        学生用户登录验证

        参数:
            sno:        学工号,char(10)
            spasswd:    密码,不限长度

        返回:
            0:  密码验证通过
            1:  密码验证不通过
            2:  用户不存在
        '''
        query = f"select shashedpasswd from student where sno='{sno}'"
        self._cursor.execute(query)
        result = self._cursor.fetchall()

        if result == []:
            self._print_debug("学生用户登录验证失败.")
            return 2
        
        shashedpasswd = result[0][0]
        if bcrypt.checkpw(spasswd.encode('utf-8'), bytes.fromhex(shashedpasswd)):
            self._print_debug("学生用户登录验证成功.")
            return 0
        else:
            self._print_debug("学生用户登录验证失败.")
            return 1

    def teacher_login_check(self,
                      tno: str,
                      tpasswd: str
                      ):
        '''
        教师用户登录验证

        参数:
            tno:        学工号,char(10)
            tpasswd:    密码,不限长度

        返回:
            0:  密码验证通过
            1:  密码验证不通过
            2:  用户不存在
        '''
        query = f"select thashedpasswd from teacher where tno='{tno}'"
        self._cursor.execute(query)
        result = self._cursor.fetchall()

        if result == []:
            self._print_debug("教师用户登录验证失败.")
            return 2
        
        thashedpasswd = result[0][0]
        if bcrypt.checkpw(tpasswd.encode('utf-8'), bytes.fromhex(thashedpasswd)):
            self._print_debug("教师用户登录验证成功.")
            return 0
        else:
            self._print_debug("教师用户登录验证失败.")
            return 1
