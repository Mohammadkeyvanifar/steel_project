import math

from GetDataFromDb import *


#ده گامی که در جزوه هستش

#گام اول و دوم
def step1_step2(beam_section, beam_section_data, material, material_data):
    print("beam section : ", beam_section)
    profile_type = beam_section[:3].upper()
    if profile_type in ['IPE', 'INP', 'IPB']:
        print(f"A (m2)= {beam_section_data[0]}")
        print(f"d (m)= {beam_section_data[1]}")
        print(f"tw (m)= {beam_section_data[2]}")
        print(f"bf (m)= {beam_section_data[3]}")
        print(f"tf (m)= {beam_section_data[4]}")
        print(f"bf/(2*tf) = {beam_section_data[5]}")
        print(f"Ix (m4)= {beam_section_data[6]}")
        print(f"Sx (m3)= {beam_section_data[7]}")
        print(f"rx (m)= {beam_section_data[8]}")
        print(f"G (kg/m)= {beam_section_data[9]}")
        print(f"Iy (m4)= {beam_section_data[10]}")
        print(f"Sy (m3)= {beam_section_data[11]}")
        print(f"ry (m)= {beam_section_data[12]}")
        print(f"r (m)= {beam_section_data[13]}")
        print(f"K (m)= {beam_section_data[14]}")
        print(f"T (m)= {beam_section_data[15]}")

    elif profile_type in ['UNP', 'UPA']:
        print(f"A (m2)= {beam_section_data[0]}")
        print(f"d (m)= {beam_section_data[1]}")
        print(f"tw (m)= {beam_section_data[2]}")
        print(f"bf (m)= {beam_section_data[3]}")
        print(f"tf (m)= {beam_section_data[4]}")
        print(f"k (m)= {beam_section_data[5]}")
        print(f"T (m)= {beam_section_data[6]}")
        print(f"G = {beam_section_data[7]}")
        print(f"Ix (m4)= {beam_section_data[8]}")
        print(f"Sx (m3)= {beam_section_data[9]}")
        print(f"rx (m)= {beam_section_data[10]}")
        print(f"Iy (m4)= {beam_section_data[11]}")
        print(f"Sy (m3)= {beam_section_data[12]}")
        print(f"ry (m)= {beam_section_data[13]}")
        print(f"eY (m)= {beam_section_data[14]}")
        print(f"xM (m)= {beam_section_data[15]}")
        print(f"a1 (m)= {beam_section_data[16]}")

    print(f"material name = {material_data[0]}")
    print(f"material e(kg/m2) = {material_data[1]}")
    print(f"material g(kg/m2) = {material_data[2]}")
    print(f"material nuratio = {material_data[3]}")
    print(f"material rho_ib_ft3 = {material_data[4]}")
    print(f"material fy(kg/m2) = {material_data[5]}")


global lcw,lpw,lw,lf,lpf,lcf,Mn1,Mn2,Mn,lp,lr,Rpc

def step3 (beam_section, beam_section_data, material_data):
    print("برسی وضعیت فشردگی بال و جان برای مقاطع ناودانی و i شکل")

    global lcw, lpw, lw, lf, lpf, lcf

    # برای جان
    lcw = 5.7 * pow(material_data[1] / material_data[5],0.5)
    lpw = 3.76 * pow(material_data[1] / material_data[5],0.5)
    lw = (beam_section_data[1] - (2 * beam_section_data[4])) / beam_section_data[2]

    if(lw <= lpw):
        print("جان فشرده است")
    elif (lpw <= lw <= lcw):
        print("جان غیر فشرده است")
    elif(lw > lcw):
        print("جان لاغر است")

    # برای بال
    profile_type = beam_section[:3].upper()
    lf = beam_section_data[3] / beam_section_data[4]
    lpf = 0.38 * pow(material_data[1] / material_data[5],0.5)
    lcf = pow(material_data[1] / material_data[5],0.5)

    if(profile_type in ['UNP', 'UPA']):
        if(lf <= lpf):
            print("بال فشرده")
        elif (lpf < lf < lcf):
            print("بال غیر فشرده")
        elif (lf > lcf):
            print("بال لاغر است")

    if(profile_type in ['IPE', 'INP', 'IPB']):
        lf = lf / 2
        if (lf <= lpf):
            print("بال فشرده")
        elif (lpf < lf <= lcf):
            print("بال غیر فشرده")
        elif (lf > lcf):
            print("بال لاغر است")

def step4(beam_section, beam_section_data, material_data):
    print("برسی وضعیت طول مهار جانبی بال برای ناودانی و i شکل")

    global lcw, lpw, lw, lf, lpf, lcf,lp,lr

    lp = 0
    profile_type = beam_section[:3].upper()

    if (profile_type in ['UNP', 'UPA']):
        if (lw <= lpw):
            # print("جان فشرده است")
            lp = 1.76 * beam_section_data[13] * pow(material_data[1] / material_data[5], 0.5)
            print("Lp (m)= ", lp)

    elif (profile_type in ['IPE', 'INP', 'IPB']):
        if (lw <= lpw):
            # print("جان فشرده است")
            lp = 1.76 * beam_section_data[12] * pow(material_data[1] / material_data[5], 0.5)
            print("Lp (m)= ", lp)
        elif (lpw <= lw <= lcw) | (lw > lcw):
            # print("جان غیر فشرده است")
            # print("جان لاغر است")
            Cw = beam_section_data[10] * pow(beam_section_data[1] - beam_section_data[4], 2) / 4
            rt = pow(pow(Cw * beam_section_data[10],0.5) / beam_section_data[7], 0.5)
            lp = 1.1 * rt * pow(material_data[1] / material_data[5],0.5)
            print("Lp (m)= " , lp)



    lr = 0
    if (profile_type in ['UNP', 'UPA']):
        if beam_section[:3] in ['UNP']:
            J = (pow(beam_section_data[2], 3) * (beam_section_data[15] - (2 * beam_section_data[4])) + (
                        2 * pow(beam_section_data[4], 3) * beam_section_data[3])) / 3
        elif beam_section[:3] in ['UPA']:
            J = (2 * (beam_section_data[3] * pow(beam_section_data[4], 3)) + (
                        beam_section_data[2] * pow(beam_section_data[1] - 2 * (beam_section_data[4]), 3))) / 3
        h0 = beam_section_data[1] - beam_section_data[4]
        Cb = beam_section_data[1] / 2
        Iyc = (beam_section_data[4] * pow(beam_section_data[3], 3) / 12)
        Sxt = Iyc / Cb
        Cw = beam_section_data[11] * pow(h0, 2) / 4
        C = ((beam_section_data[1] - beam_section_data[4]) / 2) * pow(beam_section_data[11] / Cw, 0.5)
        rt = pow(pow(Cw * beam_section_data[11], 0.5) / Sxt, 0.5)
        # J = (pow(beam_section_data[2], 3) * (beam_section_data[15] - (2 * beam_section_data[4])) + (2 * pow(beam_section_data[4], 3) * beam_section_data[3])) / 3
        lr = (1.95 * rt * (material_data[1] / (0.7 * material_data[5])) * pow(
            (J * C / Sxt * h0) + pow(    (pow(J * C / Sxt * h0, 2) + 6.67 * pow(material_data[5] * 0.7/ material_data[1], 2)     ), 0.5)
            , 0.5))
        print("Lr (m)= ", lr)

        # print("Lr = ", lr)

    elif (profile_type in ['IPE', 'INP', 'IPB']):
        if (lw <= lpw) | (lpw <= lw <= lcw):
            # print("جان فشرده است")
            #print("جان غیر فشرده")
            h0 = beam_section_data[1] - beam_section_data[4]
            Cb = beam_section_data[1] / 2
            Iyc = (beam_section_data[4] * pow(beam_section_data[3], 3) / 12)
            Sxt = Iyc / Cb
            Cw = beam_section_data[10] * pow(h0, 2) / 4
            rt = pow(pow(Cw * beam_section_data[10],0.5) / Sxt, 0.5)
            J = (pow(beam_section_data[2], 3) * (beam_section_data[15] - (2 * beam_section_data[4])) + (2 * pow(beam_section_data[4], 3) * beam_section_data[3])) / 3
            lr = 1.95 * rt * (material_data[1] / (0.7 * material_data[5])) * pow(   (J / Sxt * h0) + pow((pow(J / Sxt * h0 , 2) +   6.67*pow(material_data[5] * 0.7 / material_data[1] , 2)    ) , 0.5) , 0.5)
            print("Lr (m)= ", lr)
        elif (lw > lcw):
            # print("جان لاغر است")
            h0 = beam_section_data[1] - beam_section_data[4]
            Cw = beam_section_data[10] * pow(h0, 2) / 4
            rt = pow(pow(Cw * beam_section_data[10], 0.5) / Sxt, 0.5)
            lr = (math.pi * rt) * pow(beam_section_data[10] /Cw , 0.5)
            print("Lr (m)= ", lr)


def step5(beam_section, beam_section_data, material_data):
    print("محاسبه مقاومت اسمی خمشی با توجه معیار کمانش موضعی(Mn1)")

    global lcw, lpw, lw, lf, lpf, lcf, Mn1,Rpc

    profile_type = beam_section[:3].upper()

    if profile_type in ['IPE', 'INP', 'IPB']:
        # i شکل
        Zx = (beam_section_data[4] * beam_section_data[3]) * (beam_section_data[1] - beam_section_data[4])
        Mp = Zx * material_data[5]

        Cb = beam_section_data[1] / 2
        Iyc = (beam_section_data[4] * pow(beam_section_data[3], 3) / 12)
        Sxt = Iyc / Cb
        h = beam_section_data[1] - 2 * beam_section_data[4]
        My = Sxt * material_data[5]

        hc = h / 2
        aw = (hc * beam_section_data[2]) / (beam_section_data[3] * beam_section_data[4])

        Rpg = 1 - (aw / (1200 + (300 * aw))) * (
                    (h / beam_section_data[2]) - (5.7 * pow(material_data[1] / material_data[5], 0.5)))

        Kc = 0.555

        if (Iyc / beam_section_data[10] <= 0.23):
            Rpc = 1
        else:
            Rpc = (Mp / My) - ((Mp / My) - 1) * ((lw - lpw) / (lcw - lpw))

        if (lw <= lpw) & (lf <= lpf):
            # print("جان فشرده است")
            # print("بال فشرده")
            Zx = (beam_section_data[4] * beam_section_data[3]) * (beam_section_data[1] - beam_section_data[4])
            Mn1 = Zx * material_data[5]
        elif (lpf < lf <= lcf) & (lw <= lpw):
            # print("بال غیر فشرده")
            # print("جان فشرده است")
            Mn1 = Mp - (Mp - (0.7 * material_data[5] * beam_section_data[7])) * (lf - lpf) / (lcf - lpf)
        elif (lf <= lpf) & (lpw <= lw <= lcw):
            # print("بال فشرده")
            # print("جان غیر فشرده است")
            Mn1 = Rpc * My
        elif (lpw <= lw <= lcw) & (lpf < lf <= lcf):
            # print("جان غیر فشرده است")
            # print("بال غیر فشرده")
            Mn1 = (Rpc * My) - ((Rpc * My) - 0.7 * (material_data[5] * beam_section_data[7])) * (
                        (lf - lpf) / (lcf - lpf))
        elif (lw > lcw) & (lf <= lpf):
            # print("جان لاغر است")
            # print("بال فشرده")
            Mn1 = Rpg * material_data[5] * beam_section_data[7]
        elif (lw > lcw) & (lpf < lf <= lcf):
            # print("جان لاغر است")
            # print("بال غیر فشرده")
            Fcr = (material_data[5] - (0.3 * material_data[5])) * ((lf - lpf) / (lcf - lpf))
            Mn1 = Rpg * Fcr * beam_section_data[7]
        elif ((lw <= lpw) | (lpw <= lw <= lcw)) & (lf > lcf):
            # print("جان فشرده است")
            # print("جان غیر فشرده است")
            # print("بال لاغر است")
            Mn1 = (0.9 * material_data[1] * Kc * beam_section_data[7]) / pow(max(lcw, lf), 2)

        elif (lw > lcw) & (lf > lcf):
            # print("جان لاغر است")
            # print("بال لاغر است")
            Fcr = (0.9 * material_data[1] * Kc) / pow(max(lf, lw), 2)
            Mn1 = Rpg * Fcr * beam_section_data[7]



    elif profile_type in ['UNP', 'UPA']:
        # ناودانی
        if (lw <= lpw) & (lf <= lpf):
            # print("جان فشرده است")
            # print("بال فشرده")
            Zx = (beam_section_data[4] * beam_section_data[3]) * (beam_section_data[1] - beam_section_data[4])
            Mn1 = Zx * material_data[5]


    print("Mn1 (KN.m)=  ",  Mn1)



def step6(beam_section, beam_section_data, material_data, opening):
    # print("محاسبه مقاومت خمشی با توجه به معیار کمانش پیچشی جانبی(Mn2)")

    global lcw,lpw,lw,lf,lpf,lcf,Mn1,Mn2,lp,lr,Rpc

    Cb = 2.8
    Lb = opening
    Cw = beam_section_data[10] * pow(beam_section_data[1] - beam_section_data[4], 2) / 4
    rt = pow(pow(Cw * beam_section_data[10], 0.5) / beam_section_data[7], 0.5)
    h0 = beam_section_data[1] - beam_section_data[4]


    profile_type = beam_section[:3].upper()

    if profile_type in ['IPE', 'INP', 'IPB']:
        # i شکل


        if (lw <= lpw):
            # print("جان فشرده است")
            if(Lb <= lp):
                print("خمش پلاستیک (طول مهار جانبی)")
                Zx = (beam_section_data[4] * beam_section_data[3]) * (beam_section_data[1] - beam_section_data[4])
                Mn2 = Zx * material_data[5]
            elif(lp <= Lb <= lr):
                print("کمانش پیچشی_جانبی غیر الاستیک")
                Zx = (beam_section_data[4] * beam_section_data[3]) * (beam_section_data[1] - beam_section_data[4])
                Mp = Zx * material_data[5]
                Mn2 = Cb * ( Mp - (Mp - (0.7 * material_data[5] * beam_section_data[7])) * (Lb - lp) / (lr - lp))
                if(Mn2 > Mp):
                    Mn2 = Mp

            elif (Lb >= lr):
                print("کمانش پیچشی_جانبی الاستیک")
                J = (pow(beam_section_data[2], 3) * (beam_section_data[15] - (2 * beam_section_data[4])) + (2 * pow(beam_section_data[4], 3) * beam_section_data[3])) / 3
                Fcr = (  (Cb * pow(math.pi,2) *material_data[1]) / (pow(Lb/rt,2))  ) / pow(1 + 0.078 * (J / (beam_section_data[7] * h0)) * pow(Lb/rt,2)  ,0.5)
                Mn2 = Fcr * beam_section_data[7]
                Zx = (beam_section_data[4] * beam_section_data[3]) * (beam_section_data[1] - beam_section_data[4])
                Mp = Zx * material_data[5]
                if (Mn2 > Mp):
                    Mn2 = Mp

        elif(lpw <= lw <= lcw):
            # print("جان غیر فشرده است")
            if (Lb <= lp):
                print("خمش پلاستیک (طول مهار جانبی)")
                print("کاهش ظرفیت به علت کمانش پیچشی جانبی نخواهیم داشت")

            elif (lp <= Lb <= lr):
                print("کمانش پیچشی_جانبی غیر الاستیک")
                Iyc = (beam_section_data[4] * pow(beam_section_data[3], 3) / 12)
                Sxt = Iyc / Cb
                My = Sxt * material_data[5]
                Mn2 = Cb * ( Rpc * My - ((Rpc * My - 0.7 * material_data[5] * beam_section_data[7]) / ((Lb - lp) / (lr - lp)) ) )
                if (Mn2 > Rpc*My):
                    Mn2 = Rpc*My

            elif (Lb >= lr):
                print("کمانش پیچشی_جانبی الاستیک")
                J = (pow(beam_section_data[2], 3) * (beam_section_data[15] - (2 * beam_section_data[4])) + (
                            2 * pow(beam_section_data[4], 3) * beam_section_data[3])) / 3
                Fcr = ((Cb * pow(math.pi, 2) * material_data[1]) / (pow(Lb / rt, 2))) / pow(
                    1 + 0.078 * (J / (beam_section_data[7] * h0)) * pow(Lb / rt, 2), 0.5)
                Mn2 = Fcr * beam_section_data[7]
                Iyc = (beam_section_data[4] * pow(beam_section_data[3], 3) / 12)
                Sxt = Iyc / Cb
                My = Sxt * material_data[5]
                if(Mn2 > Rpc * My):
                    Mn2 = Rpc * My

        elif (lw > lcw):
            # print("جان لاغر است")
            if (Lb <= lp):
                print("خمش پلاستیک (طول مهار جانبی)")
                print("کاهش ظرفیت به علت کمانش پیچشی جانبی نخواهیم داشت")

            elif (lp <= Lb <= lr):
                print("کمانش پیچشی_جانبی غیر الاستیک")
                h = beam_section_data[1] - 2 * beam_section_data[4]
                hc = h / 2
                aw = (hc * beam_section_data[2]) / (beam_section_data[3] * beam_section_data[4])
                Rpg = 1 - (aw / (1200 + (300 * aw))) * (
                        (h / beam_section_data[2]) - (5.7 * pow(material_data[1] / material_data[5], 0.5)))

                Fcr = Cb((material_data[5] - (0.3*material_data[5]) ) ((Lb - lp) / (lr - lp)) )
                if(Fcr > material_data[5]):
                    Fcr = material_data[5]

                Mn2 = Rpg * Fcr * beam_section_data[7]

            elif (Lb >= lr):
                print("کمانش پیچشی_جانبی الاستیک")
                h = beam_section_data[1] - 2 * beam_section_data[4]
                hc = h / 2
                aw = (hc * beam_section_data[2]) / (beam_section_data[3] * beam_section_data[4])
                Rpg = 1 - (aw / (1200 + (300 * aw))) * (
                        (h / beam_section_data[2]) - (5.7 * pow(material_data[1] / material_data[5], 0.5)))


                Fcr = (Cb * pow(math.pi,2) * material_data[1]) / pow(Lb / rt,2)

                if (Fcr > material_data[5]):
                    Fcr = material_data[5]

                Mn2 = Rpg * Fcr * beam_section_data[7]


    elif profile_type in ['UNP', 'UPA']:
        # ناودانی
        if (Lb <= lp):
            print("خمش پلاستیک (طول مهار جانبی)")
            Zx = (beam_section_data[4] * beam_section_data[3]) * (beam_section_data[1] - beam_section_data[4])
            Mn2 = Zx * material_data[5]
        elif (lp <= Lb <= lr):
            print("کمانش پیچشی_جانبی غیر الاستیک")
            Zx = (beam_section_data[4] * beam_section_data[3]) * (beam_section_data[1] - beam_section_data[4])
            Mp = Zx * material_data[5]
            Mn2 = Cb * (Mp - (Mp - (0.7 * material_data[5] * beam_section_data[7])) * (Lb - lp) / (lr - lp))
            if (Mn2 > Mp):
                Mn2 = Mp


        elif (Lb >= lr):
            print("کمانش پیچشی_جانبی الاستیک")
            J = (pow(beam_section_data[2], 3) * (beam_section_data[15] - (2 * beam_section_data[4])) + (
                    2 * pow(beam_section_data[4], 3) * beam_section_data[3])) / 3
            Fcr = ((Cb * pow(math.pi, 2) * material_data[1]) / (pow(Lb / rt, 2))) / pow(1 + 0.078 * (J / (beam_section_data[7] * h0)) * pow(Lb / rt, 2) * ((h0 / 2) * pow(beam_section_data[11]) / Cw , 0.5), 0.5)
            Zx = (beam_section_data[4] * beam_section_data[3]) * (beam_section_data[1] - beam_section_data[4])
            Mp = Zx * material_data[5]
            Mn2 = Fcr * beam_section_data[9]

            if(Mn2 > Mp):
                Mn2 = Mp

    print("Mn2 (KN.m)= ", Mn2)
    return Mn2

def step7():
    print("محاسبه مقاوت خمشی با توجه به معیار تسلیم بال کششی(مقطع با یک محور تقارن)")
    print("کاربرد ندارد")


def step8(array_Mn2):
    print("محاسبه مقاومت خمشی نهایی")
    global Mn1, Mn
    Mn = min(Mn1,min(array_Mn2))
    Mu = 0.9 * Mn
    print("Mu (KN.m)= ", Mu)




def step9(beam_section, beam_section_data, material_data):
    print("کنترل مقاومت برشی(مطابق با فصل برش)")

    print("مقاومت برشی بدون توجه به عمل میدان کششی")
    print("1.rolled")
    print("2.non-rolled")
    choice = int(input("Enter option number (1, 2): "))
    if(choice == 1):
        Qv = 1
        Aw = beam_section_data[1] * beam_section_data[2]
        Cv1 = 1
        Vn = 0.6 * material_data[5] * Aw * Cv1
        Vu = Qv * Vn
        print("Vn (KN)= " ,Vn)
        print("Vu (KN)= ", Vu)

    elif (choice == 2):
        print("بدون وجود سخت کننده")
        Qv = 0.9
        Aw = beam_section_data[1] * beam_section_data[2]
        h = beam_section_data[1] - (2 * beam_section_data[4])
        Kv = 5.34
        if(1.1 * pow((Kv * material_data[1]) / material_data[5],0.5) < (h / beam_section_data[2])):
            Cv = (1.1 * pow((Kv * material_data[1])) / (h / beam_section_data[2]))
        else :
            Cv = 1

        Vn = 0.6 * material_data[5] * Aw * Cv
        Vu = Qv * Vn

        print("Vn (KN)= ", Vn)
        print("Vu (KN)= ", Vu)



def ste10(beam_section, beam_section_data, material_data, openning):
    print("کنترل معیار های بهره برداری")
    print("(معیار تغییر شکل)")
    Delta_Max = openning / 0.36
    print("Dealta_Max(m) = ", Delta_Max)
    return Delta_Max


# if __name__ == "__main__":
