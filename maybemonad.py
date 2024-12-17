import traceback


class EmptyValue:
    def __init__(self, value):
        self.value = value

    def __rshift__(self, func):
        return EmptyValue(self.value)

    def get_value_or_crash(self):
        raise Exception(self.value)


class Value:
    def __init__(self, value):
        self.value = value

    def __rshift__(self, func):
        try:
            result = func(self.value)
            return Value(result)
        except Exception as e:
            return EmptyValue(traceback.format_exc())

    def get_value_or_crash(self):
        return self.value



class Vector:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self,other):
        return Vector(
            x=self.x + other.x,
            y=self.y + other.y
        )


Vector(3,5) + Vector(6,7)




def uppercase(value):
    return value.upper()

def lowercase(value):
    return value.lower()

data="Erdem"
data=Value("Erdem")

result =  (
    data 
    >> uppercase 
    >> lowercase
)



result=(
    2
    + 5
    + 7
    + 8
)





included=[]
excluded=[]

def managed(array):
    for item in array:
        if len(included):
            if item not in included:
                continue
        if len(excluded):
            if item in excluded:
                continue
        return item
    
for item in managed([3,5]):
    print(item)