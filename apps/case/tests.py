from django.test import TestCase

def test1(number):
    a = [i for i in range(number)]
    for i in a:
        print("%d "%i,end='')
test1(5)