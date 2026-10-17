import numpy as np
from My_Inputs import beam_section_input, material_input
# فرض بر وجود DB یا steelpy برای خواص؛ بدون اتصال

PHI_B = 0.9
PHI_V = 0.9
L_DEF_LIMIT = 360
FREQ_MIN = 3.0

def step1_select_initial_section(section_name, material):
    print("گام 1: انتخاب مقطع اولیه")
    # فرض خواص از DB یا steelpy
    sec_props = {'Ix': 1e-4, 'Sx': 1e-3, 'h': 0.2, 'bf': 0.1, 'tf': 0.01, 'tw': 0.005, 'ry': 0.05, 'G': 10}  # فرضی
    Fy = 240e6 if material == "ST37" else 340e6
    E = 200e9
    return sec_props, Fy, E

def step2_calculate_geometric_props(sec_props):
    print("گام 2: محاسبه مشخصات هندسی")
    return sec_props  # قبلاً گرفته شده

def step3_check_compactness(sec_props, Fy, E):
    print("گام 3: بررسی فشردگی")
    h, bf, tf, tw = sec_props['h'], sec_props['bf'], sec_props['tf'], sec_props['tw']
    lambda_p_flange = 0.38 * np.sqrt(E / Fy)
    flange_ratio = bf / (2 * tf)
    web_ratio = h / tw
    lambda_p_web = 3.76 * np.sqrt(E / Fy)
    if flange_ratio <= lambda_p_flange and web_ratio <= lambda_p_web:
        compactness = "فشرده"
    else:
        compactness = "غیرفشرده"  # ساده‌شده
    return compactness

def step4_check_lateral_bracing(sec_props, Fy, E, Lb):
    print("گام 4: بررسی مهار جانبی")
    ry = sec_props['ry']
    Lp = 1.76 * ry * np.sqrt(E / Fy)
    Lr = np.pi * ry * np.sqrt(E / (0.7 * Fy))
    if Lb <= Lp:
        lateral_bracing = "فشرده"
    elif Lb <= Lr:
        lateral_bracing = "غیرفشرده"
    else:
        lateral_bracing = "لاغر"
    return lateral_bracing

def step5_nominal_bending_strength_local(compactness, sec_props, Fy):
    print("گام 5: مقاومت اسمی خمشی (کمانش موضعی)")
    Sx = sec_props['Sx']
    if compactness == "فشرده":
        Mn_local = Fy * Sx
    else:
        Mn_local = 0.7 * Fy * Sx  # ساده
    return Mn_local

def step6_bending_strength_ltb(Mn_local, lateral_bracing, sec_props, Fy, E, Lb):
    print("گام 6: مقاومت خمشی (کمانش پیچشی)")
    ry = sec_props['ry']
    Lp = 1.76 * ry * np.sqrt(E / Fy)
    Lr = np.pi * ry * np.sqrt(E / (0.7 * Fy))
    if lateral_bracing == "فشرده":
        Mn_ltb = Mn_local
    elif lateral_bracing == "غیرفشرده":
        Cb = 1.0
        Mn_ltb = Cb * (Mn_local - (Mn_local - 0.7 * Fy * sec_props['Sx']) * ((Lb - Lp) / (Lr - Lp)))
    else:
        Mn_ltb = (np.pi**2 * E * sec_props['Iy']) / Lb**2
    return Mn_ltb

def step7_bending_strength_tension_flange(Mn_ltb, section_name):
    print("گام 7: مقاومت خمشی (تسلیم بال کششی)")
    if 'unequal' in section_name.lower():
        Mn_tension = Mn_ltb * 0.95
    else:
        Mn_tension = Mn_ltb
    return Mn_tension

def step8_final_bending_strength(Mn_local, Mn_ltb, Mn_tension, M_max):
    print("گام 8: مقاومت خمشی نهایی")
    Mn = min(Mn_local, Mn_ltb, Mn_tension)
    phi_Mn = PHI_B * Mn
    if M_max > phi_Mn:
        print("خمش: شکست")
    else:
        print("خمش: OK")
    return phi_Mn

def step9_shear_strength(sec_props, Fy, V_max):
    print("گام 9: کنترل برشی")
    h, tw = sec_props['h'], sec_props['tw']
    Vn = 0.6 * Fy * h * tw  # Cv=1 فرض
    phi_Vn = PHI_V * Vn
    if V_max > phi_Vn:
        print("برش: شکست")
    else:
        print("برش: OK")
    return phi_Vn

def step10_serviceability_checks(beam_length, delta_max, E, Ixx, mass_per_length):
    print("گام 10: کنترل بهره‌برداری")
    delta_limit = beam_length / L_DEF_LIMIT
    if delta_max > delta_limit:
        print("تغییرشکل: شکست")
    else:
        print("تغییرشکل: OK")

    freq = (np.pi / (2 * beam_length**2)) * np.sqrt(E * Ixx / mass_per_length)
    if freq < FREQ_MIN:
        print("ارتعاش: شکست")
    else:
        print("ارتعاش: OK")

def main_design():
    section_name = beam_section_input()
    material = material_input()

    #دلیل گرفتن این ورودی ها در grok هست
    Lb = float(input("Lb (m): "))
    M_max = float(input("M_max (N.m): "))
    V_max = float(input("V_max (N): "))
    delta_max = float(input("delta_max (m): "))
    beam_length = float(input("beam_length (m): "))

    sec_props, Fy, E = step1_select_initial_section(section_name, material)
    sec_props = step2_calculate_geometric_props(sec_props)
    compactness = step3_check_compactness(sec_props, Fy, E)
    lateral_bracing = step4_check_lateral_bracing(sec_props, Fy, E, Lb)
    Mn_local = step5_nominal_bending_strength_local(compactness, sec_props, Fy)
    Mn_ltb = step6_bending_strength_ltb(Mn_local, lateral_bracing, sec_props, Fy, E, Lb)
    Mn_tension = step7_bending_strength_tension_flange(Mn_ltb, section_name)
    phi_Mn = step8_final_bending_strength(Mn_local, Mn_ltb, Mn_tension, M_max)
    phi_Vn = step9_shear_strength(sec_props, Fy, V_max)
    step10_serviceability_checks(beam_length, delta_max, E, sec_props['Ix'], sec_props['G'])

if __name__ == "__main__":
    main_design()