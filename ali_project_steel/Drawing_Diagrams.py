from Pynite import FEModel3D

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumulative_trapezoid

import numpy as np

import numpy as np
import matplotlib.pyplot as plt



def find_extremes(x, y, x_start, x_end):
    # فیلتر کردن نقاط در بازه
    x_in = []
    y_in = []
    for xi, yi in zip(x, y):
        if x_start <= xi <= x_end:
            x_in.append(xi)
            y_in.append(yi)

    if not y_in:  # اگر توی بازه نقطه‌ای نبود
        return None

    # کمترین مقدار
    y_min = min(y_in)
    x_min = x_in[y_in.index(y_min)]
    return x_min, y_min


def calculate_and_plot_shear_integral(x_all, shear_all, spans):
    # لیست برای ذخیره انتگرال تجمعی
    cumulative_integral = []
    integrals = []
    current_index = 0

    # محاسبه انتگرال تجمعی برای کل سازه
    cumulative_sum = 0
    for i in range(len(x_all)):
        if i == 0:
            cumulative_integral.append(0)
        else:
            # استفاده از روش ذوزنقه‌ای برای هر بازه کوچک
            delta_integral = (shear_all[i - 1] + shear_all[i]) / 2 * (x_all[i] - x_all[i - 1])
            cumulative_sum += delta_integral
            cumulative_integral.append(cumulative_sum)

    # محاسبه انتگرال برای هر عضو
    for i in range(len(spans)):
        n_points = 200
        x_member = x_all[current_index:current_index + n_points]
        shear_member = shear_all[current_index:current_index + n_points]
        integral = np.trapz(shear_member, x_member)
        integrals.append(integral)
        current_index += n_points

    total_integral = sum(integrals)

    # رسم نمودار انتگرال تجمعی (دیاگرام گشتاور)
    plt.figure(figsize=(10, 6))
    plt.plot(x_all, cumulative_integral, color='#2196F3', linewidth=2, label="Moment Diagram")
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title("Moment Diagram")
    plt.xlabel("Length (m)")
    plt.ylabel("Moment (kN·m)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

    return integrals, total_integral



def plot_diagrams(model, spans):
    x_all = []
    shear_all = []
    moment_all = []
    deflection_all = []

    for i in range(len(spans)):
        member = model.members[f"M{i + 1}"]
        x = np.linspace(0, member.L(), 200)

        # محاسبه مقادیر
        V = [member.shear("Fz", xi, "Combo 1") for xi in x]
        M = [member.moment("My", xi, "Combo 1") for xi in x]
        d = [member.deflection("dz", xi, "Combo 1") for xi in x]


        # ذخیره مقادیر برای رسم کلی
        x_all.extend(x + sum(spans[:i]))
        shear_all.extend(V)
        moment_all.extend(M)
        deflection_all.extend(d)

    # # رسم دیاگرام برش
    plt.figure(figsize=(10, 6))
    plt.plot(x_all, shear_all, color='#4CAF50', linewidth=2, label="Shear Force")
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title("Shear Force Diagram")
    plt.xlabel("Length (m)")
    plt.ylabel("Shear Force (kN)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

    # # رسم دیاگرام لنگر
    # plt.figure(figsize=(10, 6))
    # plt.plot(x_all, moment_all, color='#FF5722', linewidth=2, label="Bending Moment")
    # plt.axhline(0, color='black', linewidth=0.8)
    # plt.title("Bending Moment Diagram")
    # plt.xlabel("Length (m)")
    # plt.ylabel("Bending Moment (kNm)")
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.legend()
    # plt.show()

    # محاسبه انتگرال دیاگرام برش
    # import numpy as np
    # print("Sum of shear forces:", np.trapezoid(shear_all, x_all))
    #
    # print(shear_all)
    # integral_shear = cumulative_trapezoid(shear_all, x_all, initial=0)
    integrals, total_integral = calculate_and_plot_shear_integral(x_all, shear_all, spans)

    # رسم دیاگرام انتگرال برش
    # plt.figure(figsize=(10, 6))
    # plt.plot(x_all, integral_shear, color='#2196F3', linewidth=2, label="Momment Diagram")
    # plt.axhline(0, color='black', linewidth=0.8)
    # plt.title("Momment Force Diagram")
    # plt.xlabel("Length (m)")
    # plt.ylabel("Momment Force (kN·m)")
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.legend()
    # plt.show()



    # رسم دیاگرام تغییرشکل
    plt.figure(figsize=(10, 6))
    plt.plot(x_all, deflection_all, color='#4CAF50', linewidth=2, label="Deflection")
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title("Deflection Diagram")
    plt.xlabel("Length (m)")
    plt.ylabel("Deflection (m)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

    return x_all,deflection_all
