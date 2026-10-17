from My_Inputs import *
from GetDataFromDb import *
from Drawing_Diagrams import plot_diagrams, find_extremes
from Design_Steps import *

import matplotlib.pyplot as plt
import numpy as np
from Pynite import FEModel3D
from scipy.integrate import cumulative_trapezoid


if __name__ == "__main__":
    # دریافت ورودی‌ها
    spans = openings_input()
    num_supports = len(spans) + 1
    supports = get_support_types(num_supports)
    beam_section = beam_section_input()
    material = material_input()
    loads = beam_loading(sum(spans))

    # ساخت مدل PyNite
    model = FEModel3D()

    # تعریف گره‌ها
    node_positions = [0]
    for length in spans:
        node_positions.append(node_positions[-1] + length)


    for i, pos in enumerate(node_positions):
        model.add_node(f"N{i+1}", pos, 0, 0)

    #تعریف تکیه گاه ها
    for i, support in enumerate(supports):
        if support == "fixed":
            model.def_support(
                f"N{i + 1}",
                support_DX=True,  # قید افقی
                support_DY=True,  # قید خارج از صفحه
                support_DZ=True,  # قید عمودی
                support_RX=True,  # قید چرخش حول X
                support_RY=True,  # قید چرخش حول Y
                support_RZ=True  # قید چرخش حول Z
            )
        elif support == "pinned":
            model.def_support(
                f"N{i + 1}",
                support_DX=True,  # قید افقی
                support_DY=True,  # قید خارج از صفحه
                support_DZ=True,  # قید عمودی
                support_RX=True,  # قید پیچش
                support_RY=True,  # قید چرخش حول Y
                support_RZ=False  # آزاد برای چرخش در صفحه تیر
            )
        elif support == "roller":
            model.def_support(
                f"N{i + 1}",
                support_DX=False,  # آزاد افقی
                support_DY=True,  # قید خارج از صفحه
                support_DZ=True,  # قید عمودی
                support_RX=True,  # قید پیچش
                support_RY=True,  # قید چرخش حول Y
                support_RZ=False  # آزاد برای چرخش در صفحه تیر
            )

    # تعریف ماده (Material)
    # مقادیر نمونه - باید با ورودی کاربر تطبیق داده شود
    material_data = get_steel_properties_by_name(material)  #['name', 'E_psi', 'G_psi', 'nu_ratio', 'rho_lb_ft3', 'fy_psi']
    # print(material_data,"\n")
    # E = 29e6  # مدول الاستیسیته (psi)
    # G = 81e9  # مدول برشی (psi)
    # nu = 0.3  # نسبت پواسون
    # rho = 490  # چگالی (lb/ft³)
    # fy = 36000  # تنش تسلیم (psi)
    model.add_material(material_data[0], float(material_data[1]), float(material_data[2]), material_data[3], material_data[4], float(material_data[5]))

    # تعریف مقطع (Section)
    beam_section_data = get_section_data(beam_section)
    if beam_section[:3] in ['IPE', 'INP', 'IPB']:
        A = beam_section_data[0]
        Ixx = beam_section_data[6]
        Iy = beam_section_data[10]
        J = (pow(beam_section_data[2],3) * (beam_section_data[15] - (2 * beam_section_data[4])) + (2 * pow(beam_section_data[4],3) *beam_section_data[3])) / 3
        Zy = 1e-4
        Zz = 1e-4
        model.add_steel_section(beam_section, A, Iy, Ixx, J, Zy, Zz, material_data[0])
    elif beam_section[:3] in ['UNP']:
        A = beam_section_data[0]
        Ixx = beam_section_data[8]
        Iy = beam_section_data[11]
        J = (pow(beam_section_data[2], 3) * (beam_section_data[15] - (2 * beam_section_data[4])) + (2 * pow(beam_section_data[4], 3) * beam_section_data[3])) / 3
        Zy = 1e-4
        Zz = 1e-4
        model.add_steel_section(beam_section, A, Iy, Ixx, J, Zy, Zz, material_data[0])
    elif beam_section[:3] in ['UPA']:
        A = beam_section_data[0]
        Ixx = beam_section_data[8]
        Iy = beam_section_data[11]
        J = (2 * (beam_section_data[3] * pow(beam_section_data[4],3)) + (beam_section_data[2] * pow(beam_section_data[1] - 2 * (beam_section_data[4]),3)))/3
        Zy = 1e-4
        Zz = 1e-4
        model.add_steel_section(beam_section, A, Iy, Ixx, J, Zy, Zz, material_data[0])

    # print(J,"\n")
    # # محاسبه مقادیر مقطع از ورودی کاربر
    # A = beam_section_data[0]  # مساحت مقطع (m²)
    # Ixx = float(get_moment_of_inertia(beam_properties)) * 1e-8  # ممان اینرسی حول محور x
    # Iy = Ixx  # ممان اینرسی حول محور y
    # J = 1e-6  # ثابت پیچش
    #
    # # برای مقطع فولادی (اگر نیاز باشد)
    # Zy = 1e-4  # مدول قطعه حول محور y
    # Zz = 1e-4  # مدول قطعه حول محور z
    # model.add_steel_section("BeamSection", A, Iy, Ixx, J, Zy, Zz, "Steel")


    # تعریف عضو (Member) بین گره‌ها

    # E = 29e6  # یا محاسبه از material
    # Ixx = float(get_moment_of_inertia(beam_section)) * 1e-8
    # A = 0.003  # مساحت مقطع (فعلاً ثابت فرض شده)
    # G = 81e9
    # Iy = Ixx
    # J = 1e-6

    # for i in range(len(spans)):
        # model.add_member(f"M{i+1}", f"N{i+1}", f"N{i+2}", material_data[1], material_data[2], Iy, Ixx, J, A, 0, False, False)
        # تعریف عضو (Member) بین گره‌ها
    # تعریف عضو (Member) بین گره‌ها
    for i in range(len(spans)):
        model.add_member(
            f"M{i + 1}",  # نام عضو
            f"N{i + 1}",  # گره شروع
            f"N{i + 2}",  # گره پایان
            material_data[0],  # نام ماده
            beam_section,  # نام مقطع
            0.0,  # چرخش
            False,  # tension_only
            False  # comp_only
        )

    # اضافه کردن بارهای متمرکز

    for pos, mag in loads[0]:
        # پیدا کردن عضوی که بار در آن قرار دارد
        for i in range(len(spans)):
            start_x = node_positions[i]
            end_x = node_positions[i+1]
            if start_x <= pos <= end_x:
                a = pos - start_x  # فاصله از ابتدای عضو
                model.add_member_pt_load(f"M{i+1}", "FZ", mag, a)
                break

    # اضافه کردن بارهای گسترده
    for load in loads[1]:  # loads[1] حاوی بارهای گسترده است
        load_type = load[0]

        if load_type == 'rectangular':
            # بار یکنواخت
            _, start, end, magnitude = load
            for i in range(len(spans)):
                span_start = node_positions[i]
                span_end = node_positions[i + 1]

                # بررسی آیا بار در این عضو قرار دارد
                if not (end < span_start or start > span_end):
                    # محاسبه محدوده بار در این عضو
                    member_start = max(start, span_start) - span_start
                    member_end = min(end, span_end) - span_start

                    # اضافه کردن بار یکنواخت
                    model.add_member_dist_load(
                        f"M{i + 1}",
                        "FZ",  # جهت بار (عمودی)
                        magnitude,  # مقدار در ابتدا
                        magnitude,  # مقدار در انتها (یکنواخت)
                        member_start,  # شروع بار نسبت به عضو
                        member_end  # پایان بار نسبت به عضو
                    )

        elif load_type == 'triangular':
            _, start, end, peak_mag, peak_pos = load
            for i in range(len(spans)):
                span_start = node_positions[i]
                span_end = node_positions[i + 1]

                if not (end < span_start or start > span_end):
                    member_start = max(start, span_start) - span_start
                    member_end = min(end, span_end) - span_start

                    if peak_pos == 'start':
                        model.add_member_dist_load(f"M{i + 1}", "FZ", peak_mag, 0, member_start, member_end)
                    elif peak_pos == 'end':
                        model.add_member_dist_load(f"M{i + 1}", "FZ", 0, peak_mag, member_start, member_end)
                    else:  # قله وسط
                        peak_rel = (start + end) / 2 - span_start
                        model.add_member_dist_load(f"M{i + 1}", "FZ", 0, peak_mag, member_start, peak_rel)
                        model.add_member_dist_load(f"M{i + 1}", "FZ", peak_mag, 0, peak_rel, member_end)

    # تحلیل مدل
    model.analyze()
    # نمایش نتایج واکنش‌ها
    for i in range(len(node_positions)):
        # node = model.GetNode(f"N{i+1}")
        node = model.nodes[f"N{i + 1}"]
        print(f"Node {i + 1} Reaction (KN): {node.RxnFZ}")


    model.analyze()

    x_all, deflection_all = plot_diagrams(model, spans)


    print(" -------- ")
    print("| Design |")
    print(" -------- ")

    step1_step2(beam_section, beam_section_data, material, material_data)

    step3(beam_section, beam_section_data, material_data)

    step4(beam_section, beam_section_data, material_data)

    step5(beam_section, beam_section_data, material_data)

    Mn2_array = []
    print("محاسبه مقاومت خمشی با توجه به معیار کمانش پیچشی جانبی(Mn2)")
    print("برای دهانه های")
    for i in range(len(spans)):
        print(i + 1)
        Mn2_array.append(step6(beam_section, beam_section_data, material_data, spans[i]))

    step7()
    step8(Mn2_array)
    step9(beam_section, beam_section_data, material_data)

    Delta_Max_array = []
    for i in range(len(spans)):
        print("openning ->",i + 1)
        Delta_Max_array.append(ste10(beam_section, beam_section_data, material_data, spans[i]))

    y_extremes = []
    x_start = 0
    for i in range(len(spans)):
        x_end = x_start + spans[i]
        xmin, ymin = find_extremes(x_all, deflection_all, x_start, x_end)
        x_start = x_start + spans[i]
        y_extremes.append(ymin)



    for i in range(len(spans)):
        print("openning ->",i + 1)
        if (Delta_Max_array[i] > y_extremes[i]):
            print("(Delta_Max > y_extremes) -> so its ok ")
        else:
            print("(Delta_Max <= y_extremes) -> so its not ok ")
