#just get inputs


def openings_input():
    # دریافت تعداد دهانه‌ها
    num_spans = int(input("Number of openings?"))
    # لیست برای ذخیره طول دهانه‌ها
    spans = []
    # دریافت طول هر دهانه به تعداد مشخص شده
    for i in range(num_spans):
        length = float(input(f"enter the span length {i + 1} Span length(m) "))
        spans.append(length)
    return spans
#
#
def beam_section_input():
    # Display beam section options
    print("Select the beam section type:")
    print("1. I-shaped with equal flanges")
    # print("2. I-shaped with unequal flanges")
    print("2. Channel")

    while True:
        # Get user choice
        choice = int(input("Enter option number (1, 2): "))
        # Process choice and get relevant inputs
        if choice == 1 or choice == 2:
            # For I-shaped with equal flanges or channel, only section name is required
            section_name = input("Enter section name: ")
            return section_name  # {"section_type": "I_equal" if choice == 1 else "Channel", "name":section_name}
        else:
            print("Invalid option! Please select 1, 2.")



def material_input():
    # دریافت نوع مصالح از کاربر
    material = input("Enter the material type (e.g., ST37): ")
    return material

def beam_loading(beam_length: float):
    """
    تابع دریافت بارهای متمرکز و گسترده روی تیر با اعتبارسنجی.

    پارامترها:
        beam_length (float): طول تیر

    خروجی:
        tuple: (بارهای متمرکز, بارهای گسترده)
    """
    concentrated_loads = []
    num_concentrated = int(input("Enter number of concentrated loads: "))
    for i in range(num_concentrated):
        print(f"\nConcentrated load #{i + 1}:")
        position = float(input("Enter position of load (from start of beam)(m): "))
        if position >= beam_length:
            raise ValueError(f"Load position {position} must be less than beam length {beam_length}")
        magnitude = float(input("Enter magnitude of load(KN): "))
        concentrated_loads.append((position, -abs(magnitude)))  # ← منفی کردن

    distributed_loads = []
    num_distributed = int(input("\nEnter number of distributed loads: "))
    for i in range(num_distributed):
        print(f"\nDistributed load #{i + 1}:")
        print("Select load type:")
        print("1. Rectangular (uniform)")
        print("2. Triangular (variable)")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            load_type = 'rectangular'
        elif choice == '2':
            load_type = 'triangular'
        else:
            raise ValueError("Invalid choice! Only 1 or 2 accepted.")

        start = float(input("Enter start position of load(m): "))
        end = float(input("Enter end position of load(m): "))

        if start >= beam_length or end > beam_length:
            raise ValueError(f"Load range ({start}-{end}) must be within beam length {beam_length}")
        if start > end:
            raise ValueError(f"Start position {start} must be less than or equal to end position {end}")

        if load_type == 'rectangular':
            magnitude = float(input("Enter uniform magnitude (height) of load(KN/m): "))
            distributed_loads.append(('rectangular', start, end, -abs(magnitude)))  # ← منفی کردن
        else:  # مثلثی
            peak_magnitude = float(input("Enter peak magnitude of load: "))
            print("Select peak location:")
            print("1. At start position")
            print("2. At end position")
            peak_choice = input("Enter your choice (1 or 2): ")

            if peak_choice == '1':
                peak_location = 'start'
            elif peak_choice == '2':
                peak_location = 'end'
            else:
                raise ValueError("Invalid choice! Only 1 or 2 accepted for peak location.")

            distributed_loads.append(('triangular', start, end, -abs(peak_magnitude), peak_location))  # ← منفی کردن

    return concentrated_loads, distributed_loads




#
def get_support_types(num_supports):
    """
    Get support types from user

    Parameters:
        num_supports (int): Number of supports

    Returns:
        list: Support types
    """
    print("\nEnter support types for each support (starting from left):")
    print("Options: 'fixed', 'pinned', 'roller'")
    supports = []
    for i in range(num_supports):
        while True:
            support = input(f"Support {i + 1} type: ").lower()
            if support in ['fixed', 'pinned', 'roller']:
                supports.append(support)
                break
            else:
                print("Invalid support type. Choose 'fixed', 'pinned', or 'roller'")
    return supports


# if __name__ == "__main__":
#     material = material_input()
#     print(material)
#     print(openings_input())
