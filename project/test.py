class Test:

    def __init__(self, value: int) -> None:
        self.value = value

    def __eq__(self, other):
        return self.value == other.value
    
    def __hash__(self) -> int:
        return self.value.__hash__()


test = Test(1)
dico = {test: 1}
test2 = Test(1)
print(test2 in dico)