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
    
def test_student():
    test_add_student()
    test_inspect_stu_info()
def test_add_teacher():
    for i in range(10):
        myDB.add_teacher("202200"+str(i).zfill(4),"123456","test_teacher"+str(i))
def test_inspect_tea_info():
    pass

    
def add_course_test():
    result_1=myDB.add_course("test_course")
    result_2=myDB.add_course("test_course2")
    result_3=myDB.add_course("中文测试")
    result_4=myDB.add_course("超长中文课程名测试1145141919810---1145141919810；；；；；；；；；")
    print("result1,2,3,4:",result_1,result_2,result_3,result_4)
def add_class_test():
    #csemester 例子：20241
    pass

myDB.truncate_tables()
test_student()

