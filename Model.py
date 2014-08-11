from uuid import uuid4

class Model:
    def __init__(self, children = []):
        self.id       = 'root'
        self.text     = 'Companies'
        self.state    = {'opened' : 1}
        self.children = children

    def type_name(self):
        return 'root'

    def child_types(self):
        return {'company'}

    def uuids(self, d = {}):
        if self.id in d:
            raise Exception('UUIDs not actually unique')
        d[self.id] = self
        for child in self.children: child.uuids(d)
        return d

    def to_json(self):
        json = {'type' : self.type_name()}
        for k, v in self.__dict__.items():
            if isinstance(v, list):
                json[k] = [child.to_json() for child in v]
            else:
                json[k] = v
        return json

    def count(self, types):
        count = 1 if self.type_name() in types else 0
        return count + sum(child.count(types) for child in self.children)

    def cut(self):
        employees = []
        for child in self.children:
            employees.extend(child.cut())
        return employees

    def depth(self, depth = 0):
        l = [child.depth(depth) for child in self.children]
        l.append(depth)
        return max(l)

    def median(self):
        n = self.count({'employee'})
        return float(self.total()) / n if n else 0

    def remove(self, obj):
        try:
            i = self.children.index(obj)
            del self.children[i]
            return i, self.children
        except ValueError:
            for child in self.children:
                i, l = child.remove(obj)
                if l: return i, l
        return None, None

    def total(self):
        return sum(child.total() for child in self.children)


class Company(Model):
    def __init__(self, text, children = [], id = None):
        self.text     = str(text)
        self.id       = id if id else str(uuid4())
        self.children = children

    def type_name(self):
        return 'company'

    def child_types(self):
        return {'department'}


class Department(Model):
    def __init__(self, text, children = [], id = None):
        self.text     = str(text)
        self.id       = id if id else str(uuid4())
        self.children = children

    def type_name(self):
        return 'department'

    def child_types(self):
        return {'department', 'employee'}

    def depth(self, depth = 0):
        depth += 1
        l = [child.depth(depth) for child in self.children]
        l.append(depth)
        return max(l)


class Employee(Model):
    def __init__(self, text, address, salary, id = None):
        self.text     = str(text)
        self.address  = address
        self.salary   = salary
        self.id       = id if id else str(uuid4())
        self.children = []

    def type_name(self):
        return 'employee'

    def child_types(self):
        return {}

    def cut(self):
        if self.salary:
            self.salary = float(self.salary) / 2
            return [self]
        return []

    def total(self):
        return self.salary


def sample():
    return Company('ACME Corporation', [
        Department('Research',    [
            Employee('Craig', 'Redmond', 123456),
            Employee('Erik',  'Utrecht', 12345 ),
            Employee('Ralf',  'Koblenz', 1234  ),
        ]),
        Department('Development', [
            Employee('Ray',   'Redmond', 234567),
            Department('Dev1', [
                Employee('Klaus', 'Boston', 23456),
                Department('Dev1.1', [
                    Employee('Karl', 'Riga',      2345),
                    Employee('Joe',  'Wifi City', 2344),
                ]),
            ]),
        ]),
    ])
