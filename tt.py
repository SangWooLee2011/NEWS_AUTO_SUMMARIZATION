import math

v_list = [i for i in range(121, 131)]
th_list = [i for i in range(36, 46)]
h_list = [1.0, 1.1, 1.2, 1.3, 1.4 ,1.5, 1.6 ,1.7 ,1.8 ,1.9]

for v in v_list:
    for th in th_list:
        for h in h_list:
            temp = ((pow(v,2) * math.cos(th) * math.sin(th)) + (v * math.cos(th) * math.sqrt(pow(v,2)*pow(math.sin(th),2) + (2*9.8*h))))/9.8
            print("투사속도 = ", v, "투사각도 = ", th, "투사높이 = ",h, "최대수평변위 = ", temp)