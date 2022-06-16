from django.test import TestCase
for i in range(10):
    def fak():
        from faker import Faker #  引用faker包
        fa = Faker(locale='zh-CN')
        for y in range(1):
                t = fa.ssn()
                return t


    fak()
    ID=fak()

    if len(ID)==18:
        print('生成的⾝份证号码是：'+ID)
    else:
        print('生成的⾝份证号码错误，请重新输⼊：')
        ID=input('请输⼊18位⾝份证号码：')
    ID_add=ID[0:2]     #省份，截出前两位 2个数
    ID_birth=ID[6:14]  #8个数
    ID_sex=ID[16:17]   #1个数
    #print(ID_add,ID_birth,ID_sex)
    pro={'11':'北京','12':'天津','13':'河北','14':'⼭西','15':'内蒙',
         '21':'辽宁','22':'吉林','23':'⿊龙江','31':'上海','32':'江苏',
         '33':'浙江','34':'安徽','35':'福建','36':'江西','37':'⼭东',
         '41':'河北','42':'湖北','43':'湖南','44':'⼴东','45':'⼴西',
         '46':'海南','50':'重庆','51':'四川','52':'贵州','53':'云南',
         '54':'西藏','61':'陕西','62':'⽢肃','63':'青海','64':'宁夏',
         '65':'新疆','71':'台湾','81':'⾹港'
        }
    sx='猴鸡狗猪⿏⽜虎兔龙蛇马⽺'
    def getbirth(a):  #读取⽣⽇，⽣肖函数
        year=a[0:4]
        moon=a[4:6]
        day=a[6:]
        y=int(year)%12
        print('您的⽣⽇为：'+year+'年'+moon+'⽉'+day+'⽇')
        print('您的⽣肖为：',sx[y])
    getbirth(ID_birth)
    def getsex(a):    #读取性别函数
        if int(a) % 2 == 0:
            print('您的性别为：⼥')
        else:
            print('您的性别为：男')
    getsex(ID_birth)
