class Student(object):
    def __init__(self,name,snum):
        self._name = name
        self._snum = snum
        self._courses = []
        self._srec = {
            }
    def get_name (self):
        return self._name

    def get_snum(self):
        return self._snum

    def enrol(self,courses):
        self._courses.extend(courses)

    def get_courses(self):
        return self._courses

    def get_srec(self):
        return self._srec

    def update_srec(self,rec):
        """update student reocrd with results in rec"""
        self._srec.update(rec)
        self._courses = []
              

    def __repr__(self):
        return "Student('{0}', '{1}')".format(self._name,self._snum)

    def __str__(self):
        return "Student: name = {0}, snum = {1}, courses = {2}".format(self._name,self._snum,self._courses)


peter = Student('Peter', 's1234567')
peter.enrol(['CSSE1001','MATH1061'])
print peter
trish = Student('Trish','s2345678')

peter.update_srec({'CSSE1001':5,'MATH1061':4})
