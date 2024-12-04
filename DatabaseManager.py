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

    # def delete_student(self,
    #                    sno: str
    #                    ):
    #     '''
    #     删除一个学生用户

    #     参数:
    #         sno:    学工号,char(10)
    
    #     返回:
    #         0:  删除学生用户成功
    #         1:  学工号格式不符合要求
    #         2:  不存在该用户
    #     '''

    #     if len(sno) != 10:
    #         self._print_debug("删除学生用户失败.")
    #         return 1
        
    #     query = f"select * from student where sno='{sno}'"
    #     self._cursor.execute(query)
    #     if self._cursor.fetchall() == []:
    #         self._print_debug("删除学生用户失败.")
    #         return 2

    #     query = f"delete from student where sno='{sno}'"

    #     self._cursor.execute(query)
    #     self._connection.commit()
    #     self._print_debug("删除学生用户成功.")
    #     return 0
        
    # def delete_teacher(self,
    #                    tno: str
    #                    ):
    #     '''
    #     删除一个教师用户

    #     参数:
    #         tno:    学工号,char(10)
    
    #     返回:
    #         0:  删除教师用户成功
    #         1:  学工号格式不符合要求
    #         2:  不存在该用户
    #     '''

    #     if len(tno) != 10:
    #         self._print_debug("删除教师用户失败.")
    #         return 1
        
    #     query = f"select * from teacher where tno='{tno}'"
    #     self._cursor.execute(query)
    #     if self._cursor.fetchall() == []:
    #         self._print_debug("删除教师用户失败.")
    #         return 2

    #     query = f"delete from teacher where tno='{tno}'"
        
    #     self._cursor.execute(query)
    #     self._connection.commit()
    #     self._print_debug("删除教师用户成功.")
    #     return 0

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

    def add_course(self,
                   coursename: str
                   ):
        '''
        添加一门课程

        参数:
            coursename:     课程名称,varchar(32)

        返回:
            0:  添加成功
            1:  课程名称格式不符合要求

        注意:
            暂定可以存在多门名称相同的课程(比如数院开的高代和统院开的高代)
            添加课程成功之后,数据库会自动生成courseid,可以用其它接口(后续实现)查询
        '''

        if len(coursename) > 32:
            self._print_debug("添加课程失败.")
            return 1

        query = f"insert into course (coursename) values ('{coursename}');"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("添加课程成功.")
        return 0

    def add_class(self,
                  cname: str,
                  csemester: str,
                  courseno: int
                  ):
        '''
        添加一个教学班

        参数:
            cname:      教学班名,varchar(32)
            csemester:  开课学期,char(5)
            courseno:   对应课程ID,serial

        返回:
            0:  添加成功
            1:  教学班名不符合要求
        
        注意:
            这里假定csemester和courseno不是由文本框输入的,
            而是通过下拉框等形式转化成的,不会出错

            csemester的格式参照课本,如20241, 20242

            添加教学班成功之后,数据库会自动生成cno,可以用其它接口(后续实现)查询
        '''
        if len(cname) > 32:
            self._print_debug("添加教学班失败.")
            return 1
    
        query = f"insert into class (cname, csemester, courseno) values ('{cname}', '{csemester}', '{courseno}')"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("添加教学班成功.")
        return 0

    def student_join_class(self,
                           sno: str,
                           cno: int
                           ):
        '''
        把一个学生添加进一个教学班

        参数:
            sno:    学工号,char(10)
            cno:    教学班ID,serial

        返回:
            0:  添加成功
            1:  该学生已经在该班级当中

        注意:
            这里假定sno和cno不是由文本框输入的,
            而是通过下拉框等形式转化成的,不会出错
        '''
        query = f"select * from attend_class where sno='{sno}' and cno='{cno}';"
        self._cursor.execute(query)
        if self._cursor.fetchall() != []:
            self._print_debug("添加学生进入班级失败.")
            return 1
        
        query = f"insert into attend_class values ('{sno}', '{cno}');"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("添加学生进入班级成功.")
        return 0

    def teacher_join_class(self,
                           tno: str,
                           cno: int,
                           is_ta: bool
                           ):
        '''
        把一个教师添加进一个教学班

        参数:
            tno:    学工号,char(10)
            cno:    教学班ID,serial
            is_ta:  是否为助教,boolean

        返回:
            0:  添加成功
            1:  该教师已经在该班级当中

        注意:
            这里假定tno, cno, is_ta不是由文本框输入的,
            而是通过下拉框等形式转化成的,不会出错
        '''
        query = f"select * from teach_class where tno='{tno}' and cno='{cno}';"
        self._cursor.execute(query)
        if self._cursor.fetchall() != []:
            self._print_debug("添加教师进入班级失败.")
            return 1
        
        query = f"insert into teach_class values ('{tno}', '{cno}', {is_ta==True});"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("添加教师进入班级成功.")
        return 0

    def add_handout(self,
                    hname: str,
                    hfilepath: str
                    ):
        '''
        添加一个课件

        参数:
            hname:      课件名称,varchar(64)
            hfilepath:  文件路径,varchar(128)

        返回:
            0:  添加课件成功
            1:  课件名称格式不符合要求

        注意：
            1. 应该在已经上传文件并得到文件路径之后,再执行这个类方法.
            2. 这个类方法只是在课件表当中添加一条记录,后续还应该执行post_handout()
            3. 这里假定hfilepath不是由用户输入,而是后端自动生成的,因此不会超长
            4. 允许同名课件,会自动生成不同的课件ID
        '''
        if len(hname) > 64:
            self._print_debug("添加课件失败.")
            return 1

        query = f"insert into handout (hname, hfilepath) values ('{hname}', '{hfilepath}');"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("添加课件成功.")
        return 0

    def post_handout(self,
                     cno: int,
                     hno: int,
                     tno: str
                     ):
        '''
        一个教师把一个课件发布到一个教学班

        参数:
            cno:    教学班ID,int
            hno:    课件ID,int
            tno:    教师的学工号,char(10)

        返回:
            0:  成功发布
            1:  该课件先前已经被发布到该教学班中

        注意:
            这里假定cno, hno, tno都是后端代码给出,
            而非用户在文本框当中输入的,不会出错;

            同一个课件可以发布到不同的教学班,这里是对obe的一点改进

            发布时间会自动存入数据库
        '''

        query = f"select * from post_handout where cno='{cno}' and hno='{hno}';"
        self._cursor.execute(query)
        if self._cursor.fetchall() != []:
            self._print_debug("发布课件失败.")
            return 1
        
        query = f"insert into post_handout values ({cno}, {hno}, '{tno}', now());"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("发布课件成功.")
        return 0

    def add_assignment(self,
                       aname: str,
                       adeadline: int,
                       aprofile: str,
                       afilepath: str
                       ):
        '''
        添加一个作业
        参数:
            aname:      作业名称,varchar(64)
            adeadline:  截止时间,Unix时间戳(距离1970年的秒数)
            aprofile:   作业简介,varchar(1024)
            afilepath:  文件路径,varchar(128)

        返回:
            0:  添加作业成功
            1:  作业名称格式不符合要求
            2:  作业简介格式不符合要求

        注意：
            1. 应该在已经上传文件并得到文件路径之后,再执行这个类方法.
            2. 这个类方法只是在作业表当中添加一条记录,后续还应该执行post_assignment()
            3. 这里假定afilepath不是由用户输入,而是后端自动生成的,因此不会超长
            4. 允许同名作业,会自动生成不同的作业ID
        '''
        if len(aname) > 64:
            self._print_debug("添加作业失败.")
            return 1
        
        if len(aprofile) > 1024:
            self._print_debug("添加作业失败.")
            return 2

        query = f"insert into assignment (aname, adeadline, aprofile, afilepath) values ('{aname}', to_timestamp({adeadline}), '{aprofile}', '{afilepath}')"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("添加作业成功.")
        return 0

    def post_assignment(self,
                     cno: int,
                     ano: int,
                     tno: str
                     ):
        '''
        一个教师把一个作业布置到一个教学班

        参数:
            cno:    教学班ID,int
            ano:    作业ID,int
            tno:    教师的学工号,char(10)

        返回:
            0:  成功发布
            1:  该作业先前已经被布置到该教学班中

        注意:
            这里假定cno, ano, tno都是后端代码给出,
            而非用户在文本框当中输入的,不会出错;

            同一个作业可以布置到不同的教学班,这里是对obe的一点改进

            布置时间会自动存入数据库
        '''

        query = f"select * from post_assignment where cno='{cno}' and ano='{ano}';"
        self._cursor.execute(query)
        if self._cursor.fetchall() != []:
            self._print_debug("布置作业失败.")
            return 1
        
        query = f"insert into post_assignment values ({cno}, {ano}, '{tno}', now());"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("布置作业成功.")
        return 0
    
    def submit_assignment(self,
                          sno: str,
                          ano: int,
                          submit_filepath: str
                          ):
        '''
        一个学生提交一次作业

        参数:
            sno:                学工号,char(10)
            ano:                作业ID,int
            submit_filepath:    文件路径,varchar(128)

        返回:
            0:  提交成功

        注意：
            自动覆盖之前的提交,提交时间、是否超时等信息自动保存到数据库当中
        '''
        query = f"select * from submit_assignment where sno='{sno}' and ano='{ano}';"
        self._cursor.execute(query)
        if self._cursor.fetchall() != []:
            query = f"update submit_assignment set submit_time = now(), is_over_time = (now() > (select adeadline from assignment a where a.ano = {ano})), submit_filepath = '{submit_filepath}' where sno = '{sno}', ano = {ano};"
        else:
            query = f"insert into submit_assignment values ('{sno}', {ano}, now(), (now() > (select adeadline from assignment a where a.ano = {ano})), '{submit_filepath}');"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("提交作业成功.")
        return 0
    
    def select_info_home(self,sno):
        #测试人员认为这里可能出现sql注入---sno  sno=' or 1=1;--
        
        '''
        :param sno:
        :return:courses upload
        查询学生姓名：根据学号从 student 表中查询学生姓名。
        查询课程名称：根据学号从 attend_class 表中获取教学班ID，再从 class 表中获取课程ID，最后从 course 表中获取课程名称。
        查询上传资料：根据学号从多个表中联查教师上传的资料信息。
        查询上传作业：根据学号从多个表中联查教师上传的作业信息。
        返回结果：将查询到的学生姓名、课程名称和上传信息返回。
        '''
        query_student_name=f"select s1.sname from student s1 where s1.sno='{sno}'; "
        try:
            self._cursor.execute(query_student_name)
            student_name=self._cursor.fetchall()
        except Exception as e:
            print(f"There is an error:{e}")
            return None
        student_name=student_name[0][0]
        query_course=f"select cor1.coursename from course cor1,class cla1,attend_class at1 where at1.sno='{sno}' and at1.cno=cla1.cno and cla1.courseno=cor1.courseno;"
        try:
            self._cursor.execute(query_course)
            course_name=self._cursor.fetchall()
        except Exception as e:
            print(f"There is an error:{e}")
            return None
        query_course=[i[0] for i in course_name]
        query_src = (
            f"SELECT t1.tname, cour1.coursename, hand1.hname "
            f"FROM attend_class at1, teach_class tc1, teacher t1, course cour1, class cla1, post_handout ph1, handout hand1 "
            f"WHERE at1.sno = '{sno}' "
            f"AND tc1.cno = at1.cno "
            f"AND tc1.tno = t1.tno "
            f"AND cla1.cno = at1.cno "
            f"AND cour1.courseno = cla1.courseno "
            f"AND ph1.cno = tc1.cno "
            f"AND ph1.hno = hand1.hno;"
        )
        try:
            self._cursor.execute(query_src)
            src=self._cursor.fetchall()
        except Exception as e:
            print(f"There is an error:{e}")
            return None
        upload_info=[]
        for i in src:
            upload_info.append({"name":i[0],"course":i[1],"src":i[2]})
        query_work = (
            f"SELECT t1.tname, cour1.coursename, ass1.aname "
            f"FROM attend_class at1, teach_class tc1, teacher t1, course cour1, class cla1, post_assignment pa1, assignment ass1 "
            f"WHERE at1.sno = '{sno}' "
            f"AND tc1.cno = at1.cno "
            f"AND tc1.tno = t1.tno "
            f"AND cla1.cno = at1.cno "
            f"AND cour1.courseno = cla1.courseno "
            f"AND pa1.cno = tc1.cno "
            f"AND pa1.ano = ass1.ano;"
        )
        try:
            self._cursor.execute(query_work)
            work=self._cursor.fetchall()
        except Exception as e:
            print(f"There is an error:{e}")
            return None
        for i in work:
            upload_info.append({"name":i[0],"course":i[1],"work":i[2]})
        return student_name,query_course,upload_info


    def select_info_course(self,sno,course_name):
        pass
    def select_student_src(self,sno,course_name):
        '''
        :param sno:
        :param course_name:
        :return:
        这段代码定义了一个名为 select_student_src 的方法，用于从数据库中查询特定学生在特定课程中的课件信息。具体功能如下：
        构建 SQL 查询：根据传入的学生编号 sno 和课程名称 course_name，构建一个 SQL 查询语句，从多个表中获取相关数据。
        执行查询：使用 _cursor 对象执行 SQL 查询，并捕获可能的异常。
        处理结果：将查询结果转换为一个包含课程名、课件名、发布时间和文件路径的字典列表。
        返回结果：返回包含上述信息的字典列表。
        '''
        query_src = (
            f"SELECT cour1.coursename, hand1.hname,ph1.post_handout_time,hand1.hfilepath "
            f"FROM attend_class at1, course cour1, class cla1, post_handout ph1, handout hand1 "
            f"WHERE at1.sno = '{sno}' "
            f"AND cla1.cno = at1.cno "
            f"AND cour1.courseno = cla1.courseno "
            f"AND ph1.cno = at1.cno "
            f"AND ph1.hno = hand1.hno "
            f"AND cour1.coursename LIKE '{course_name}'"
        )
        try:
            self._cursor.execute(query_src)
            src=self._cursor.fetchall()
        except Exception as e:
            print(f"There is an error:{e}")
            return None
        files=[]
        for i in src:
            files.append({"course":i[0],"name":i[1],"date":i[2],"path":i[3]})
        return files
    def select_student_work(self,sno,course_name):
        query_work = (
            f"SELECT  cour1.coursename, ass1.aname ,ass1.adeadline,ass1.aprofile,ass1.afilepath "
            f"FROM attend_class at1, course cour1, class cla1, post_assignment pa1, teach_class tc1,assignment ass1 "
            f"WHERE at1.sno = '{sno}' "
            f"AND cla1.cno = at1.cno "
            f"AND cour1.courseno = cla1.courseno "
            f"AND pa1.cno = tc1.cno "
            f"AND pa1.ano = ass1.ano "
            f"AND cour1.coursename LIKE '{course_name}';"
        )
        try:
            self._cursor.execute(query_work)
            work = self._cursor.fetchall()
        except Exception as e:
            print(f"There is an error:{e}")
            return None
        work_load=[]
        for i in work:
            work_load.append({"course":i[0],"name":i[1],"deadline":i[2],"profile":i[3],"path":i[4]})
        return work_load
    
#下面这个函数是dhl写的，用于执行sql语句来测试
    def testSQL(self):
        # query = f"select * from course,class where class.courseno=course.courseno;"
        query = f"select * from class;"
        self._cursor.execute(query)
        src=self._cursor.fetchall()
        print(src)
        self._connection.commit()
    
    '''
    TODO:
    1.select_info_home函数仅考虑了学生的情况，应该增加对教师的查询
    2.负责对接的后端需要过滤特殊字符，防止SQL注入
    3.需要增加获取课程信息的接口，便于前端做出教师用户添加教学班的下拉菜单（总不能遍历所有学生来找出所有课程吧）
    4.对于handout同3，感觉应该写一个针对教师用户的hangout查询接口
    '''

    def add_student_to_class(self,cname,cteacher,sno):
        query=f"select cno from class where cname='{cname}';"
        self._cursor.execute(query)
        src=self._cursor.fetchall()
        # print("src:  ",src)
        cno=int(src[0][0])
        # print(type(cno))
        self.student_join_class(sno,cno)
        self._connection.commit()
    
    '''
    接受cname（教学班名），cteacher（教学的老师），sno（学生学号）功能为添加该学生到该教学班
    '''
    #还有一个任务是修改add_course的前端使得加课程的时候顺便加教学班
    def add_course_and_class(self,coursename):
        '''
        添加一门课程，同时添加对应的教学班，教学班名称=课程名+yyyy+学期
        '''
        if len(coursename) > 32:
            self._print_debug("添加课程失败.")
            return 1

        query = f"insert into course (coursename) values ('{coursename}');"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("添加课程成功.")
        
        query = f"select courseno from course where coursename='{coursename}';"
        self._cursor.execute(query)
        src=self._cursor.fetchall()
        courseno=int(src[0][0])
        cname=coursename+"20241"#暂定这样的一一对应关系
        csemester="20241"
        query = f"insert into class (cname, csemester, courseno) values ('{cname}', '{csemester}', '{courseno}')"
        self._cursor.execute(query)
        self._connection.commit()
        self._print_debug("添加教学班成功.")
        return 0

        