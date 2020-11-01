def my_align(string, length=0, align_type='<'):
    """
    :param string: 中英文混排时待列对齐的原字符串
    :param length: 待预留列宽,折合的半角字符总数,默认0
    :param align_type: 对齐类型,默认左对齐.左对齐<,右对齐>,居中对齐-
    :return: 补充空格后的字符串
    """
    if length <= len(string.encode('GBK')):
        return string
    len_ch = (len(string.encode('GBK')) - len(string)) * 2  # 中文折合的半角字符总数
    len_en = len(string) * 2 - len(string.encode('GBK'))    # 英文折合的半角字符总数
    len_sp = length - len_ch - len_en                       # 补充空格总数
    if align_type == '>':    # 右对齐
        return ' ' * len_sp + string
    elif align_type == '-':  # 居中对齐
        return ' ' * int(len_sp / 2) + string + ' ' * (len_sp - int(len_sp / 2))
    return string + ' ' * len_sp  # 左对齐


class Course:
    __l = []
    __CourseNum = []

    def __init__(self, num, name, stu_num, teacher, max_num):
        self.num = num
        self.name = name
        self.stu_num = stu_num
        self.teacher = teacher
        self.max_num = max_num
        Course.__l.append(self)
        Course.__CourseNum.append(self.num)

    def printnum(self):
        print(my_align("课程序号", 10)+my_align("当前人数", 10))
        print(my_align(str(self.num), 10)+my_align(str(self.stu_num), 10))

    def printmax_num(self):
        print(my_align("课程序号", 10)+my_align("最大选课人数", 10))
        print(my_align(str(self.num), 10)+my_align(str(self.max_num), 10))

    def printteac(self):
        print(my_align("课程序号", 10)+my_align("开课老师", 10))
        print(my_align(str(self.num), 10)+my_align(str(self.teacher), 10))

    @classmethod
    def addCourse(cls, num, name, teac, max_num):
        Course.__CourseNum.append(num)
        Course.__l.append(Course(num, name, 0, teac, max_num))

    # @classmethod
    # def add(cls, course):
    #     Course.__CourseNum.append(course.num)
    #     Course.__l.append(course)

    @classmethod
    def dropCourse(cls, num):
        Course.__CourseNum.remove(num)
        for c in Course.__l:
            if c.num == num:
                Course.__l.remove(c)

    @classmethod
    def get(cls, i):
        return Course.__l[i-1]

    @classmethod
    def IsCourse(cls, num):
        if num in Course.__CourseNum:
            return True
        return False

    @classmethod
    def lookup(cls, num):
        for c in Course.__l:
            if num == c.num:
                return c


class Student:
    def __init__(self, num, name, c_list):
        self.num = num
        self.name = name
        self.c_list = c_list

    def showcourses(self):
        print(my_align("序号", 7)+my_align("课程序号", 10) + my_align("课程名", 15) +
              my_align("开课教师", 10)+my_align("当前人数", 10)+my_align("最大选课人数", 10))
        i = 1
        delete_list = []
        for num in self.c_list:
            if Course.IsCourse(num):
                c = Course.lookup(num)
                print(my_align(str(i), 7) + my_align(str(c.num), 10) + my_align(
                    c.name, 15) + my_align(c.teacher, 10) + my_align(str(c.stu_num), 10) + my_align(str(c.max_num), 10))
                i += 1
            else:
                delete_list.append(num)

        for num in delete_list:
            self.c_list.remove(num)

    def select(self, num):
        if not Course.IsCourse(num):
            print("该课程序号不存在！")
            return
        c = Course.lookup(num)
        if c.stu_num >= c.max_num:
            print("该课程人数已满！")
            return
        if num in self.c_list:
            print("已选过该课程，无法重复选择！")
            return
        self.c_list.append(num)
        c.stu_num += 1
        print("选课成功！")

    def withdraw(self, num):
        if not Course.IsCourse(num):
            print("该课程序号不存在！")
            return
        if num not in self.c_list:
            print("未选过该课程！")
            return
        self.c_list.remove(num)
        c = Course.lookup(num)
        c.stu_num -= 1
        print("退课成功！")


class Teacher:
    def __init__(self, num, name, c_list):
        self.num = num
        self.name = name
        self.c_list = c_list

    def showcourses(self):
        print(my_align("序号", 7)+my_align("课程序号", 10) + my_align("课程名", 15) +
              my_align("开课教师", 10)+my_align("当前人数", 10)+my_align("最大选课人数", 10))
        i = 1
        for num in self.c_list:
            c = Course.lookup(num)
            print(my_align(str(i), 7) + my_align(str(c.num), 10) + my_align(
                c.name, 15) + my_align(c.teacher, 10) + my_align(str(c.stu_num), 10) + my_align(str(c.max_num), 10))
            i += 1

    def OpenCourse(self, num, name, max_num):
        if Course.IsCourse(num):
            print("该课程序号已存在！")
            return
        Course.addCourse(num, name, self.name, max_num)
        self.c_list.append(num)
        print("开课成功!")

    def CloseCourse(self, num):
        if not Course.IsCourse(num):
            print("该课程不存在！")
            return
        if num not in self.c_list:
            print("该课程为其他老师开设，您无权关闭！")
            return
        Course.dropCourse(num)
        self.c_list.remove(num)
        print("成功关闭课程!")


def printMenu():
    print("##############################################################################")
    print('                          南开大学选课系统v0.01a')
    print('')
    print('                             学生界面请按[s]')
    print('                             老师界面请按[t]')
    print('                             查看课程请按[c]')
    print('')
    print("##############################################################################")
    print('请输入相应的命令（退出请按[q]）：')


def printMenuStu():
    print("##############################################################################")
    print('                                 学生界面')
    print('')
    print('                             查看选课内容请按[c]')
    print('                                选课请按[a]')
    print('                                退课请按[d]')
    print('                              查看课程请按[l]')
    print('                              返回菜单请按[b]')
    print('')
    print("##############################################################################")
    print('请输入相应的命令（返回菜单请按[b]）：')


def printMenuTeac():
    print("##############################################################################")
    print('                                 教师界面')
    print('')
    print('                                开课请按[c]')
    print('                              关闭课程请按[a]')
    print('                              查看课程请按[l]')
    print('                              返回菜单请按[b]')
    print('')
    print("##############################################################################")
    print('请输入相应的命令（返回菜单请按[b]）：')


# 1. 从文件中读取信息到学生和老师列表中
student_list = []
s_list = []
teacher_list = []
t_list = []
with open('./data.txt', 'r', encoding='UTF-8') as lines:
    array = lines.readlines()  # 该列表每一个元素是txt文件的每一行
    for a in array:
        a = a.strip('\n')  # 去掉换行符\n
        items = a.split()  # 空格切分
        if items[0] == 's':
            student_list.append(items)
        elif items[0] == 't':
            teacher_list.append(items)
        elif items[0] == 'c':
            course = Course(items[1], items[2], items[3], items[5], items[4])

# 2. 添加学生课程关系
for s in student_list:
    ids = s[3].split(',')  # 所选课程
    student = Student(s[1], s[2], ids)
    s_list.append(student)

# 3. 添加老师课程关系
for t in teacher_list:
    ids = t[3].split(',')  # 所教课程
    teacher = Teacher(t[1], t[2], ids)
    t_list.append(teacher)
