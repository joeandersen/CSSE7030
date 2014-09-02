class Employee(object):
   def __init__(self, name, salary):
       self._name = name
       self._salary = salary

   def my_name(self):
       return self._name

   def wage(self):
       return self._salary/26   # fortnight pay
        

class Worker(Employee):
     def __init__(self,name,salary,boss):
         Employee.__init__(self,name,salary)
         self._boss = boss

     def get_manager(self):
        return self._boss

class Executive(Employee):
    def __init__(self, name, salary,bonus):
        Employee.__init__(self,name,salary)
        self._bonus = bonus

    def wage(self):
        return Employee.wage(self) + self._bonus/26 
