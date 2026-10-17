import psycopg2
from ConnectionToDb import get_connection
from psycopg2 import Error

def convert_IPE(data):
    converted_data = []
    factors = [
        1e-4,   # A (cm² → m²)
        1e-3,   # d (mm → m)
        1e-3,   # tw (mm → m)
        1e-3,   # bf (mm → m)
        1e-3,   # tf (mm → m)
        1,      # bf/(2*tf) (بدون واحد، نیازی به تبدیل ندارد)
        1e-8,   # Ix (cm⁴ → m⁴)
        1e-6,   # Sx (cm³ → m³)
        1e-2,   # rx (cm → m)
        1,      # G (kg/m) (بدون تغییر)
        1e-8,   # Iy (cm⁴ → m⁴)
        1e-6,   # Sy (cm³ → m³)
        1e-2,   # ry (cm → m)
        1e-3,   # r (mm → m)
        1e-3,   # K (mm → m)
        1e-3    # T (mm → m)
    ]
    # محاسبه از عنصر 1 تا 15 (data[1] تا data[15])
    for i in range(len(factors)):
        converted_data.append(float(data[i + 1]) * factors[i])
    return converted_data


def convert_INP_IPB(data):
    converted_data = []
    factors = [
        1e-4,  # A (cm² → m²)
        1e-3,  # d (mm → m)
        1e-3,  # tw (mm → m)
        1e-3,  # bf (mm → m)
        1e-3,  # tf (mm → m)
        1,  # bf/(2*tf) (بدون واحد)
        1e-8,  # Ix (cm⁴ → m⁴)
        1e-6,  # Sx (cm³ → m³)
        1e-2,  # rx (cm → m)
        1,  # G (kg/m) (بدون تغییر)
        1e-8,  # Iy (cm⁴ → m⁴)
        1e-6,  # Sy (cm³ → m³)
        1e-2,  # ry (cm → m)
        1,  # r (NULL - بدون تبدیل)
        1e-3,  # K (mm → m)
        1e-3  # T (mm → m)
    ]

    for i in range(len(factors)):
        value = data[i + 1]
        # اگر مقدار None یا NULL بود، بدون تغییر بذار
        if value is None or str(value).upper() == 'NULL':
            converted_data.append(value)
        else:
            # تبدیل به float و اعمال ضریب تبدیل
            converted_data.append(float(value) * factors[i])

    return converted_data


def convert_UNP_UPA(data):
    converted_data = []
    factors = [
        1e-6,   # mm² → m²
        1e-3,   # mm → m
        1e-3,   # mm → m
        1e-3,   # mm → m
        1e-3,   # mm → m
        1e-3,   # mm → m
        1e-3,   # mm → m
        1,      # kg/m (بدون تغییر)
        1e-8,   # cm⁴ → m⁴
        1e-6,   # cm³ → m³
        1e-2,   # cm → m
        1e-8,   # cm⁴ → m⁴
        1e-6,   # cm³ → m³
        1e-2,   # cm → m
        1e-2,   # cm → m
        1e-2,   # cm → m
        1e-2    # cm → m
    ]
    for i in range(len(factors)):
        if data[i + 1] is None:  # اگر مقدار None بود، از آن صرف‌نظر کن
            converted_data.append(None)
            continue
        converted_data.append(float(data[i + 1]) * factors[i])
    return converted_data




def convert_units(data):
    """
    تابع تبدیل واحد برای داده‌های ورودی
    - خانه 0: رشته (بدون تبدیل)
    - خانه 1 و 2 و 5: عدد (psi → kN/m²)
    - سایر خانه‌ها: بدون تبدیل
    """

    if not data:
        return []

    converted_data = list(data)  # کپی از داده اصلی
    psi_to_knm2 = 6.89476  # 1 psi = 6.89476 kN/m²

    # تبدیل خانه‌های عددی (1، 2 و 5)
    indices_to_convert = [1, 2, 5]
    for i in indices_to_convert:
        if i < len(data) and data[i] is not None:
            converted_data[i] = float(data[i]) * psi_to_knm2

    return converted_data


def get_section_data(profile_name):
    """
    تابع برای استخراج تمام اطلاعات یک پروفیل از پایگاه داده.
    :param profile_name: نام پروفیل (مثل IPE200، UNP120، INP160)
    :return: دیکشنری شامل اطلاعات پروفیل یا None در صورت خطا یا عدم وجود پروفیل
    """
    connection = get_connection()
    if connection is None:
        print("❌ Unable to connect to the database.")
        return None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        profile_type = profile_name[:3].upper()

        if profile_type in ['IPE', 'INP', 'IPB']:
            table_name = 'ipe_inp_ipb'
        elif profile_type in ['UNP', 'UPA']:
            table_name = 'upa_unp'
        else:
            print(f"⚠️ Profile type '{profile_type}' not supported.")
            return None

        query = f"SELECT * FROM {table_name} WHERE name = %s"
        cursor.execute(query, (profile_name,))
        result = cursor.fetchone()


        if result:
            if profile_type in ['IPE', 'INP', 'IPB']:

                if profile_type in ['IPE']:
                    result = convert_IPE(result)
                elif profile_type in ['INP', 'IPB']:
                    result = convert_INP_IPB(result)


            elif profile_type in ['UNP', 'UPA']:
                result = convert_UNP_UPA(result)

            return result
        else:
            print(f"⚠️ Profile {profile_name} not found in table {table_name}.")
            return None

    except Error as e:
        print(f"❌ Error executing query: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("✅ The connection to the database was closed.")


def get_steel_properties_by_name(steel_name):
    """
    دریافت خواص مکانیکی فولاد بر اساس نام آن از پایگاه داده
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT name, E_psi, G_psi, nu_ratio, rho_lb_ft3, fy_psi
            FROM steel_properties
            WHERE name = %s;
        """
        cursor.execute(query, (steel_name,))
        result = cursor.fetchone()

        if result:
            # keys = ['name', 'E_psi', 'G_psi', 'nu_ratio', 'rho_lb_ft3', 'fy_psi']
            result = convert_units(result)
            return result
        else:
            return f"Steel with name'{steel_name}'Not found."

    except Exception as e:
        return f"Error connecting or fetching data:{e}"

    finally:
        if conn:
            cursor.close()
            conn.close()



# تست تابع
# if __name__ == "__main__":
