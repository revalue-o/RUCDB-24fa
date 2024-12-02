import DatabaseManager
import os
os.chdir(os.path.dirname(__file__))
myDB = DatabaseManager.DatabaseManager()
myDB.connect()
'''
这是一个测试脚本，旨在对所有api进行全面测试
'''
'''
# def truncate_tables(self):
截断所有表

返回:
    0:  全部成功
    1:  失败
'''
def test_add_student():
    #生成的学生学号统一为202100xxxx的形式，密码为123456，姓名为test_studentx
    for i in range(10):
        myDB.add_student("202100"+str(i).zfill(4),"123456","test_student"+str(i))
    #测试重复添加
    result=myDB.add_student("2021000001","123456","test_student1")
    print("重复添加测试result:",result)
def test_inspect_stu_info():
    #测试查询学生信息
    for i in range(10):
        result=myDB.select_info_home("202100"+str(i).zfill(4))
        print("查询学生信息测试result:",result)
def test_add_teacher():
    for i in range(10):
        myDB.add_teacher("202200"+str(i).zfill(4),"123456","test_teacher"+str(i))

def test_student():
    test_add_student()
    test_inspect_stu_info()
    test_add_teacher()


# with open("./temp_store.txt", "r") as f:
#     course_start=int(f.readline())+15
#     cno_start=int(f.readline())+10
# course_start=185
# cno_start=50
# with open("./temp_store.txt", "w") as f:
#     f.writelines([str(course_start),'\n',str(cno_start)])
course_start=1
cno_start=1

def test_add_course():
    for i in range(15):
        myDB.add_course("test_course_"+str(i))
def test_add_class():
    for i in range(10):
        myDB.add_class("test_class_"+str(i),"2024"+str(i),i+course_start)
def test_add_student2class():
    for i in range(3):
        myDB.student_join_class("202100"+str(i).zfill(4),str(i//2+int(cno_start)))
        myDB.student_join_class("202100"+str(i+1).zfill(4),str(i//2+int(cno_start)))
def test_add_teacher2class():
    for i in range(3):
        myDB.teacher_join_class("202200"+str(i).zfill(4),str(i//2+int(cno_start)),0)
        myDB.teacher_join_class("202200"+str(i+1).zfill(4),str(i//2+int(cno_start)),0)
def test_addhandout2class():
    for i in range(5):
        myDB.add_handout("test_handout_"+str(i),"./"+str(i)+".txt")
    for i in range(2):
    
        myDB.post_handout(i+cno_start,i+1,"2022000001")#这里hno先设成i+1
        myDB.post_handout(i+cno_start,i+1,"2022000001")#这里hno先设成i+1
def test_addassignment2class():
    for i in range(5):
        myDB.add_assignment("test_assignment_"+str(i),114514,"测试中文profile","./"+str(i)+".txt")
    for i in range(2):
        myDB.post_assignment(i+1,i+1,"2022000001")#这里hno先设成i+1
        myDB.post_assignment(i+2,i+2,"2022000001")#这里hno先设成i+1
def test_select_info_home():
    for i in range(1):
        result=myDB.select_info_home("202100"+str(i).zfill(4))
        print("查询学生信息测试result:",result)
    for i in range(1):
        result=myDB.select_student_src("202200"+str(i).zfill(4),"test_course_"+str(i))
        result2=myDB.select_student_work("202100"+str(i).zfill(4),"test_course_"+str(i))
        print("查询教师信息测试result:",result)
        print("查询教师信息测试result2:",result2)
    
def collective_class_func_test():
    #数据库里保存的“文件”都只是文件路径
    test_add_course()
    test_add_class()
    test_add_student2class()
    test_add_teacher2class()

    print("test_addhandout2class")
    test_addhandout2class()
    print("test_addassignment2class")
    test_addassignment2class()

    test_select_info_home()
        
    
 
    
def add_course_test():
    result_1=myDB.add_course("test_course")
    result_2=myDB.add_course("test_course2")
    result_3=myDB.add_course("中文测试")
    result_4=myDB.add_course("超长中文课程名测试1145141919810---1145141919810；；；；；；；；；")
    print("result1,2,3,4:",result_1,result_2,result_3,result_4)
# def add_class_test():
#     #csemester 例子：20241
#     pass

# myDB.truncate_tables()
myDB.drop_tables()
myDB.create_tables()
test_student()


collective_class_func_test()

# def sql():
#     myDB.testSQL()
# sql()


