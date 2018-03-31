#!/usr/bin/python
# -*- coding:utf-8 -*- 


import unittest
import HTMLTestRunnerCN
import HTMLTestRunner
import os
import sys
# from log import log
import logging
import datetime

# 将上一级目录路径加入系统路径
sys.path.append('../')
from database_control import DatabaseControl 



# 执行测试的类
class DatabaseControlTestCase(unittest.TestCase): 
    '''继承于Testcase, 是功能类 DatabaseControl 对应的测试类'''

    def setUp(self):
        '''
            是父类TestCase中定义的函数
            在setUp()方法中进行测试前的初始化工作
        '''
        # print "do something before test.Prepare environment."
        self.dbc = DatabaseControl(host='127.0.0.1', port=3306, user='root', passwd='admin', db_name='db_education', charset='utf8')
        self.course_dict={}
        self.course_dict['id']           =u'ST001'
        self.course_dict['name']         =u"Testing"
        self.course_dict['lesson_no']    =100L
        self.course_dict['stime']        =datetime.date(2018,1,1)
        self.course_dict['etime']        =datetime.date(2018,3,1)
        logging.basicConfig(filename='../log/DatabaseControlTestCase.log',format='[%(asctime)s-%(filename)s]\n-[%(levelname)s]:\t%(message)s', level = logging.DEBUG,filemode='a',datefmt='%Y-%m-%d %I:%M:%S %p')

        self.student_dict={}
        self.student_dict['id']= u"SS002"
        self.student_dict['name']= u"name"
        self.student_dict['gender']= u"男"
        self.student_dict['age']= 10
        self.student_dict['pname']= "pname"
        self.student_dict['phone']= "111222333"
        self.student_dict['lessonnum']= 20L 
        self.student_dict['accountnum']=20L
        self.student_dict['birthday']= datetime.date(2008,1,1)
        self.student_dict['note']=u"aa" 
    def tearDown(self):
        '''
            是父类TestCase中定义的函数
            在tearDown()方法中执行测试后的清除工作
        '''
        # print "do something after test.Clean up."
        self.dbc = None

    @classmethod
    def setUpClass(cls):
        '''
            如果想要在所有case执行之前准备一次环境，并在所有case执行结束之后再清理环境，我们可以用 setUpClass() 与 tearDownClass()
        '''
        # print "This setUpClass() method only called once."
        pass

    @classmethod
    def tearDownClass(cls):
        '''
            如果想要在所有case执行之前准备一次环境，并在所有case执行结束之后再清理环境，我们可以用 setUpClass() 与 tearDownClass()
        '''
        # print "This tearDownClass() method only called once too."
        pass

    def test_connect(self):
        '''
            测试数据库连通性
        '''
        print "测试数据连通性"
        # self.assertEqual(self.dbc.connect(), True)
        self.assertTrue(self.dbc.connect())
        logging.info(self.dbc.print_setting())
        # time.sleep(3)
        # self.assertIsNone(self.dbc.connect())

    def test_print_setting(self):
        print "测试打印数据库信息"
        print self.dbc.print_setting()


    def test_get_all_course(self):
        print "测试获取所有课程"
        res = self.dbc.get_all_course()
        print res
        self.assertIsNotNone(res)
        # self.res_dict = res

    # @unittest.skip("I don't want to run this case.")
    def test_edit_course_info(self):
        print "测试添加，刷新和删除课程"
        print "step1：检查是否存在%s，没有则pass"%self.course_dict['id']
        self.assertEqual(self.dbc.get_course_by_id(self.course_dict['id']), [])

        print "step2: 添加%s"%self.course_dict['id']
        self.dbc.edit_course_info(self.course_dict, 'add')
        res_dict = self.dbc.get_course_by_id(self.course_dict['id'])
        self.assertEqual(res_dict, self.course_dict)

        print "step3：更新%s"%self.course_dict['id']
        self.course_dict['name'] = u"testing22"
        self.dbc.edit_course_info(self.course_dict, 'update')
        res_dict = self.dbc.get_course_by_id(self.course_dict['id'])
        self.assertEqual(res_dict, self.course_dict)

        print "step4: 删除%s"%self.course_dict['id']
        res_dict = self.dbc.delete_course_by_id(self.course_dict['id'])
        self.assertEqual(self.dbc.get_course_by_id(self.course_dict['id']), [])


    def test_get_course_by_id(self):
        print "测试根据课程id获取课程信息"
        print "step1：使用正常的课程id"
        res = self.dbc.get_course_by_id("C0001")
        print res
        self.assertNotEqual(res, [])
        print "step1：使用错误的课程id"
        res = self.dbc.get_course_by_id("S0001")
        print res
        self.assertEqual(res, [])
        # raise RuntimeError("%s"%res['id'])

    def test_get_all_student(self):
        print "测试获取所有学生信息"
        print self.dbc.get_all_student()

    def test_get_student_by_id(self):
        print "测试根据学号获取学生信息"
        id = "S1111"
        print "学号错误时(id = %s)，获取id为空"%str(id)
        res = self.dbc.get_student_by_id(id)
        print res
        self.assertEqual(res, [])

        id = "S0002"
        print "学号正确时(id = %s)，正常获取学生信息"%str(id)
        res = self.dbc.get_student_by_id(id)
        print res
        self.assertNotEqual(res, [])

    def test_edit_student_info(self):
        print "测试添加，刷新和删除学生信息"
        print "step1：检查是否存在%s，没有则pass"%self.student_dict['id']
        self.assertEqual(self.dbc.get_student_by_id(self.student_dict['id']), [])

        print "step2: 添加%s"%self.student_dict['id']
        self.dbc.edit_student_info(self.student_dict, 'add')
        res_dict = self.dbc.get_student_by_id(self.student_dict['id'])
        self.assertEqual(res_dict, self.student_dict)

        print "step3：更新%s"%self.student_dict['id']
        self.student_dict['name'] = u"testing22"
        self.dbc.edit_student_info(self.student_dict, 'update')
        res_dict = self.dbc.get_student_by_id(self.student_dict['id'])
        self.assertEqual(res_dict, self.student_dict)

        print "step4: 删除%s"%self.student_dict['id']
        res_dict = self.dbc.delete_student_by_id(self.student_dict['id'])
        self.assertEqual(self.dbc.get_student_by_id(self.student_dict['id']), [])

# 构造测试集
# def gen_suite():
#     suite = unittest.TestSuite()
#     suite.addTest(DatabaseControlTestCase("testConnect"))
#     # suite.addTest(WidgetTestCase("testResize"))
#     # suite.addTest(WidgetTestCase("testDispose"))
#     # suite.addTest(WidgetTestCase("testResize"))
#     return suite

    def test_check_account(self):
        print "测试登录功能"

        user = "root"
        passwd = "admin"
        print "用户名密码正确时，正常登录（%s：%s）"%(user, passwd)
        res = self.dbc.check_account(user,passwd)
        print res
        self.assertTrue(res)

        user = "root2"
        passwd = "admin"
        print "用户名错误时，无法登录（%s：%s）"%(user, passwd)
        res = self.dbc.check_account(user,passwd)
        print res
        self.assertFalse(res)

        user = "root"
        passwd = "admin2"
        print "用户名正确，密码错误时，无法登录（%s：%s）"%(user, passwd)
        res = self.dbc.check_account(user,passwd)
        print res
        self.assertFalse(res)

        user = "root2"
        passwd = "admin2"
        print "用户名密码都错误时，无法登录（%s：%s）"%(user, passwd)
        res = self.dbc.check_account(user,passwd)
        print res
        self.assertFalse(res)

# 测试
if __name__ == "__main__":

    #==========================================================
    # 调用测试集的第一种方法
    # unittest.main(defaultTest = 'gen_suite')
    # unittest.main()


    #==========================================================
    # 调用测试集的另一种方法
    # 构造测试集
    # 执行测试
    # suite = gen_suite()
    # # runner = unittest.TextTestRunner()
    # runner = unittest.TextTestRunner(verbosity=2) # 参数用于指定输出测试函数名称
    # runner.run(suite)

    #==========================================================
    # 将结果用文件输出
    # suite = gen_suite()
    # with open('UnittestTextReport.txt', 'a') as f:
    #     runner = unittest.TextTestRunner(stream=f, verbosity=2)
    #     runner.run(suite)

    #===========================================================
    # 将结果用HTML报告的形式输出
    # 资料来源 :http://tungwaiyip.info/software/HTMLTestRunner.html
    # suite = gen_suite()
    # with open('res/HTMLReport.html', 'w') as f:
    #     runner = HTMLTestRunner(stream=f,
    #                             title='MathFunc Test Report',
    #                             description='generated by HTMLTestRunner.',
    #                             verbosity=2
    #                             )
    #     runner.run(suite)


    #===========================================================
    # 中文HTML结果的输出, 资料来源:https://github.com/findyou/HTMLTestRunnerCN

    with open('HTMLReportCN.html', 'w') as f:
        runner = HTMLTestRunnerCN.HTMLTestRunner(
            stream=f,
            title=u'单元测试报告',
            description='description',
            tester="corey",
            verbosity=2
            )
    # with open('HTMLReport.html', 'w') as f:
    #     runner = HTMLTestRunner.HTMLTestRunner(stream=f,
    #                             title='TestDatabase Test Report',
    #                             description='generated by HTMLTestRunner.',
    #                             verbosity=2
    #                             )

        unittest.main(testRunner=runner, verbosity=2)
        # runner.run(suite)
    # print os.path.abspath(__file__)