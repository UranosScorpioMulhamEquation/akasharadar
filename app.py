from datetime import date, datetime, timedelta
import math
import streamlit as st
import os
import uuid
# ==================== 1. Security (Fixed) ====================
KEY_FILE = "license.key"

def get_machine_id():
    return hex(uuid.getnode())

def generate_password(mid):
    # مطابقة تامة لمنطق أداة فك الحماية الثابتة
    digits = ''.join(filter(str.isdigit, mid))
    if not digits: 
        try:
            digits = str(int(mid, 16))
        except:
            return "Error"
    num = int(digits)
    result = round(abs(num / 2 * 3.14))
    return str(result)[:6]

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = os.path.exists(KEY_FILE)

if not st.session_state['authenticated']:
    st.set_page_config(page_title="Security", layout="centered")
    st.title("Security Activation - Ask the programmer for your password")
    st.warning("Send your Machine ID to programmer email : mulham81ahmed@gmail.com ")

    mid = get_machine_id()
    st.info(f"Machine ID: {mid}")
    pwd = st.text_input("Enter Activation Key:", type="password")
    
    if st.button("Activate"):
        if pwd == generate_password(mid):
            with open(KEY_FILE, "w") as f: 
                f.write(pwd)
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Invalid Activation Key.")
            
    st.stop()

# ==========================================
# جدول الحروف الأبجدية الكامل (الجمل الكبير)
# ==========================================
ABJAD_DICT = {
    'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1, 'ء': 1,
    'ب': 2,
    'ج': 3,
    'د': 4,
    'ه': 5, 'ة': 5,
    'و': 6,
    'ز': 7,
    'ح': 8,
    'ط': 9,
    'ي': 10, 'ى': 10,
    'ك': 20,
    'ل': 30,
    'م': 40,
    'ن': 50,
    'س': 60,
    'ع': 70,
    'ف': 80,
    'ص': 90,
    'ق': 100,
    'ر': 200,
    'ش': 300,
    'ت': 400,
    'ث': 500,
    'خ': 600,
    'ذ': 700,
    'ض': 800,
    'ظ': 900,
    'غ': 1000
}

ZODIAC_MAP = {
    1: 'الحمل',
    2: 'الثور',
    3: 'الجوزاء',
    4: 'السرطان',
    5: 'الأسد',
    6: 'العذراء',
    7: 'الميزان',
    8: 'العقرب',
    9: 'القوس',
    10: 'الجدي',
    11: 'الدلو',
    12: 'الحوت'
}

# قائمة المنازل القمرية الـ 28 التقليدية
LUNAR_MANSIONS = {
    1: "الشرطان", 2: "البطين", 3: "الثريا", 4: "الدبران", 5: "الهقعة", 6: "الهنعة", 7: "ذراع",
    8: "النثرة", 9: "الطرفة", 10: "الجبهة", 11: "الزبرة", 12: "الصرفة", 13: "العواء", 14: "السماك",
    15: "الغفر", 16: "زبانا", 17: "الإكليل", 18: "القلب", 19: "الشولة", 20: "النعائم", 21: "البلدة",
    22: "ذبح", 23: "سعد السعود", 24: "سعد الأخبية", 25: "سعد البلع", 26: "سعد الذابح", 27: "الفرغ المقدم", 28: "الفرغ المؤخر"
}


class MasterKarmicEngineWithAntardasha:

    # قاموس شرح معاني الطاقة المهيمنة (الـ 22 طاقة الكبرى لمصفوفة القدر)
    ENERGY_MEANINGS = {
        1: "الساحر: طاقة البدايات، الإرادة الصلبة، القدرة على الابتكار وتسيير الأمور بمهارة وقيادة ذاتية.",
        2: "الكاهنة: طاقة الحدس العميق، الأسرار، الحكمة الصامتة، والتأمل الباطني وقراءة ما بين السطور.",
        3: "الإمبراطورة: طاقة الخصوبة، الوفرة المادية، النمو، الرعاية، والاهتمام بالتفاصيل الأسرية والمهنية.",
        4: "الإمبراطور: طاقة السلطة، النظام، الاستقرار الهيكلي، البناء المؤسسي، والمسؤولية القيادية.",
        5: "الكاهن الأكبر: طاقة العلم، التقاليد، الإرشاد الروحي، التعليم، والالتزام بالمنظومة الأخلاقية.",
        6: "العاشقان: طاقة الاختيارات العاطفية، الشراكات، الانسجام، التناغم، وبحث القلب عن الجمال.",
        7: "العربة: طاقة الحركة، السفر، الإصرار، الانتصار على التحديات، والانتقال لمحطة حياتية أوسع.",
        8: "العدالة: طاقة التوازن، الكارما، الحقيقة المطلقة، والوضوح القانوني والإداري.",
        9: "الناسك: طاقة الحكمة العميقة، العزلة الاختيارية للنضج، البحث المعرفي، والاستنارة الداخلية.",
        10: "عجلة الحظ: طاقة التحولات القدرية، الفرص المفاجئة، وانفتاح أبواب الرزق وتغير الدورات للأفضل.",
        11: "القوة: طاقة الحيوية الجسدية العالية، الشجاعة، السيطرة على النفس، والقدرة الفائقة على التحمل.",
        12: "المصلوب: طاقة التضحية الواعية، رؤية الأمور من منظور معكوس، وتجاوز الابتلاءات بالصبر الروحي.",
        13: "الموت: طاقة التحول الجذري، التجدد الشامل، وإغلاق صفحات القديم لفتح آفاق متجددة.",
        14: "الاعتدال: طاقة التناغم، الصبر، الشفاء الذاتي، والامتزاج الهادئ والمتوازن للعناصر.",
        15: "الشيطان: طاقة مواجهة الإغراءات، كشف التعلقات المادية الخفية، والتحرر من القيود النفسية.",
        16: "البرج: طاقة الصدمات المفاجئة، هدم الهياكل غير الصالحة، وإعادة التأسيس على قواعد صحيحة.",
        17: "النجمة: طاقة الأمل، الإلهام المضيء، الشهرة، والتألق المستقبلي الواعد في الأفق.",
        18: "القمر: طاقة الخيال، الأوهام، الغموض، وتفعيل مواجهة المخاوف الكامنة في العقل الباطن.",
        19: "الشمس: طاقة السعادة المطلقة، الوضوح الإشعاعي، النجاح الجماهيري، والحيوية الكبرى.",
        20: "الحكم: طاقة البعث العائلي أو الشخصي، التحرر من قيود الماضي، واليقظة الكبرى.",
        21: "العالم: طاقة التوسع العالمي، الانفتاح على الثقافات والآفاق الكبرى، والكمال وتحقيق الغايات.",
        22: "الأحمق: طاقة الحرية المطلقة، البدايات العفوية النصف واعية، والمغامرة الجريئة بلا قيود.",
    }

    def __init__(self, first_name_part1, first_name_part2, mother_name_part1, mother_name_part2, is_first_composite, is_mother_composite, birth_date_str):
        self.p1 = first_name_part1.strip()
        self.p2 = first_name_part2.strip() if is_first_composite else ""
        self.m1 = mother_name_part1.strip()
        self.m2 = mother_name_part2.strip() if is_mother_composite else ""
        
        self.is_first_composite = is_first_composite
        self.is_mother_composite = is_mother_composite
        
        full_first = f"{self.p1} {self.p2}".strip()
        full_mother = f"{self.m1} {self.m2}".strip()
        self.full_display_name = f"{full_first} بن/بنت {full_mother}"
        self.first_name = self.p1  # للتوافق مع التقرير الشامل القديم
        
        self.birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        self.day = self.birth_date.day
        self.month = self.birth_date.month
        self.year = self.birth_date.year

        # ثوابت الكواكب وتسلسلها الفيدي (Vimshottari Dasha Lords)
        self.dasha_lords = [
            "كيتو (Ketu - الجذور والكارما)",
            "الزهرة (Venus - العلاقات والرخاء)",
            "الشمس (Sun - الروح والقيادة)",
            "القمر (Moon - العقل والمشاعر)",
            "المريخ (Mars - الطاقة والصراع)",
            "راهو (Rahu - الشغف والتطور)",
            "المشترى (Jupiter - الحكمة والثروة)",
            "زحل (Saturn - العدالة والكارما الثقيلة)",
            "عطارد (Mercury - الفكر والاتصال)",
        ]
        self.dasha_years = [7, 20, 6, 10, 7, 18, 16, 19, 17]

    def _reduce_to_22(self, num):
        while num > 22:
            num = sum(int(digit) for digit in str(num))
        return 22 if num == 0 else num

    def calculate_matrix_of_destiny(self):
        p1 = self._reduce_to_22(self.day)  # زاوية اليوم (الشخصية)
        p2 = self._reduce_to_22(self.month)  # زاوية الشهر (الروحانيات)
        year_sum = sum(int(d) for d in str(self.year))
        p3 = self._reduce_to_22(year_sum)  # زاوية السنة (القدر)

        p4 = self._reduce_to_22(p1 + p2 + p3)  # الأرضية / الزاوية الرابعة
        center = self._reduce_to_22(p1 + p2 + p3 + p4)  # المركز (طاقة الروح الأساسية)

        money_line = self._reduce_to_22(p1 + p4 + center)
        love_line = self._reduce_to_22(p2 + p3 + center)
        health_line = self._reduce_to_22(p1 + p2 + center)

        return {
            "p1": p1,
            "p2": p2,
            "p3": p3,
            "p4": p4,
            "center": center,
            "money_line": money_line,
            "love_line": love_line,
            "health_line": health_line,
        }

    def calculate_name_value(self, name_part, is_composite_first_box=False):
        total = 0
        name_part = name_part.strip()
        if not name_part:
            return 0
        for i, char in enumerate(name_part):
            if char == 'ة' or char == 'ه':
                if is_composite_first_box and i == len(name_part) - 1:
                    total += 400
                else:
                    total += 5
            elif char in ABJAD_DICT:
                total += ABJAD_DICT[char]
        return total

    def reduce_to_12(self, number):
        while number > 12:
            number -= 12
        if number <= 0:
            number = ((number - 1) % 12) + 1
        return number

    def get_name_vibration(self):
        total_val = sum(ord(char.lower()) - 96 for char in self.first_name if char.isalpha())
        return (total_val % 22) or 22

    def calculate_jafr_esoteric_profile(self):
        val_part1 = self.calculate_name_value(self.p1, is_composite_first_box=self.is_first_composite)
        val_part2 = self.calculate_name_value(self.p2, is_composite_first_box=False) if self.is_first_composite else 0
        
        val_mother1 = self.calculate_name_value(self.m1, is_composite_first_box=self.is_mother_composite)
        val_mother2 = self.calculate_name_value(self.m2, is_composite_first_box=False) if self.is_mother_composite else 0
        
        val_first = val_part1 + val_part2
        val_mother = val_mother1 + val_mother2
        
        total_name_val = val_first + val_mother
        if total_name_val == 0:
            total_name_val = 45

        zodiac_index = self.reduce_to_12(total_name_val)
        zodiac_name = ZODIAC_MAP.get(zodiac_index, 'الحمل')
        
        deg_30 = (total_name_val % 30) or 30
        manzila_28 = (total_name_val % 28) or 28
        manzila_name = LUNAR_MANSIONS.get(manzila_28, "غير متوفرة")
        
        mod_4 = (total_name_val % 4) or 4

        elements = {1: "ناري (حار يابس)", 2: "ترابي (بارد يابس)", 3: "هوائي (حار رطب)", 4: "مائي (بارد رطب)"}
        dominant_element = elements[mod_4]
        
        missing_elements = {
            1: "مائي (تحتاج للهدوء والتأمل والابتعاد عن العصبية)",
            2: "هوائي (تحتاج لتنشيط التواصل الفكري والمرونة)",
            3: "ترابي (تحتاج للواقعية والاستقرار المادي)",
            4: "ناري (تحتاج لتحفيز الشجاعة والمبادرة والحماس)"
        }
        missing_element = missing_elements[mod_4]

        metals = {1: "الذهب والحديد", 2: "الفضة والبلاتين", 3: "النحاس الأصفر", 4: "الألماس والفضة الخالصة"}
        stones = {1: "الياقوت الأحمر والعقيق", 2: "الزمرد والزبرجد", 3: "الجمشت والتوْرمالين", 4: "اللؤلؤ والمرجان"}

        diseases = {
            1: "التهابات الدم، ارتفاع ضغط الدم، والصداع العصبي.",
            2: "مشاكل الجهاز الهضمي، القولون العصبي، وآلام المفاصل.",
            3: "اضطرابات الجهاز التنفسي، الحساسية، والأرق الذهني.",
            4: "الرطوبة في الجسم، ضعف المناعة، والتقلبات الهرمونية والنفسية."
        }
        
        foods = {
            1: "الخضار الورقية، الفواكه الطازجة، والتقليل من البهارات الحارة.",
            2: "الحبوب الكاملة، اللحوم المشوية، والتوابل الدافئة والعسل.",
            3: "السوائل الطبيعية، الأسماك، والأطعمة الغنية بالأوميغا 3.",
            4: "المكسرات، الزنجبيل، التمور، والقرفة."
        }

        return {
            "zodiac": zodiac_name,
            "degree": f"الدرجة {deg_30} من برج {zodiac_name}",
            "lunar_mansion": f"المنزلة رقم {manzila_28} ({manzila_name})",
            "element": dominant_element,
            "missing_element": missing_element,
            "total_val": total_name_val,
            "psychology": "طاقة نفسية عميقة، حدس قوي، قدرة عالية على قراءة النوايا، وتحليل الأمور بدقة.",
            "diseases": diseases[mod_4],
            "foods": foods[mod_4],
            "weather_effect": "يتأثر جسدياً بتغيرات الطقس والحرارة؛ الطقس المعتدل ينشط حيويته بينما الطقس الرطب البارد يسبب له الخمول.",
            "lucky_days": ["الأحد والخميس (طاقة للرزق)", "الإثنين والجمعة (للعلاقات والسلام)"],
            "metal_stone": f"المعدن: {metals[mod_4]} | الحجر الكريم: {stones[mod_4]}",
            "personality_type": "قيادي وإبداعي بطبعه، يفضل استقلالية القرار.",
            "social_relations": "علاقات اجتماعية منتقاة؛ يفضل القلة الصادقة على الكثرة.",
            "offspring": "طاقة إنجاب جيدة ومستقرة وفق الموازين العددية.",
            "business_fields": "التجارة الحرة، الإدارة، الاستشارات، التقنية، أو المشاريع الخاصة.",
            "money_flow": "تدفق مالي نشط يحتاج لضبط المصاريف والابتعاد عن الاستثمار العشوائي.",
            "evil_eye": "هالته عرضة أحياناً للعين والحسد لنجاحه وبروزه، وتحتاج لتحصين دوري.",
            "karmic_inheritance": "كارما موروثة تتعلق بالصبر والتضحية لأجل العائلة.",
            "spiritual_cure": "سورة البقرة، آية الكرسي، المعوذتان، وأسماء (يا حفيظ، يا سلام).",
            "locations": "المدن الساحلية المعتدلة والمدن الكبرى.",
            "wealth_period": "نعم، سيصبح ثرياً (وتبرز ثروته بوضوح في منتصف العمر وبعد الأربعينات).",
            "fame": "حضور كارزمي ملحوظ؛ قد يبلغ مرتبة الشهرة والتأثير الجماهيري.",
            "prison": "طاقة الحروف لا توحي بوجود أحكام قضائية سالبة للحرية.",
            "surgery": "احتمال خفيف لتدخل جراحي عارض، ولا توجد عمليات كبرى خطيرة.",
            "marriage": "زواج متوازن ومستقر في سن النضج (بين 25 و 30 عاماً)."
        }

    def calculate_vedic_nodes_and_moon(self):
        y, m, d = self.year, self.month, self.day
        if m <= 2:
            y -= 1
            m += 12
        A = y // 100
        B = 2 - A + (A // 4)
        jd = (
            int(365.25 * (y + 4716))
            + int(30.6001 * (m + 1))
            + d
            + B
            - 1524.5
        )

        T = (jd - 2451545.0) / 36525.0
        rahu_trop = (125.04452 - 1934.136261 * T + 0.0020708 * (T**2)) % 360
        ayanamsa = 23.85 + (self.year - 2000 + self.month / 12.0) * (50.27 / 3600.0)

        rahu_sidereal = (rahu_trop - ayanamsa) % 360
        ketu_sidereal = (rahu_sidereal + 180) % 360

        moon_approx = (218.316 + 13.176396 * (jd - 2451545.0)) % 360
        moon_sidereal = (moon_approx - ayanamsa) % 360

        vedic_signs = [
            "الحمل (Mesha)",
            "الثور (Vrishabha)",
            "الجوزاء (Mithuna)",
            "السرطان (Karka)",
            "الأسد (Simha)",
            "العذراء (Kanya)",
            "الميزان (Tula)",
            "العقرب (Vrischika)",
            "القوس (Dhanu)",
            "الجدي (Makara)",
            "الدلو (Kumbha)",
            "الحوت (Meena)",
        ]

        ketu_sign_idx = int(ketu_sidereal // 30)
        rahu_sign_idx = int(rahu_sidereal // 30)

        nakshatra_span = 360.0 / 27.0
        nakshatra_idx = int(moon_sidereal // nakshatra_span)
        ruler_idx = nakshatra_idx % 9

        return {
            "ketu_sign": vedic_signs[ketu_sign_idx],
            "rahu_sign": vedic_signs[rahu_sign_idx],
            "ruler_index": ruler_idx,
            "init_ruler": self.dasha_lords[ruler_idx],
        }

    def generate_detailed_timeline_with_antardasha(self):
        vedic = self.calculate_vedic_nodes_and_moon()
        r_idx = vedic["ruler_index"]

        timeline = []
        current_maha_date = self.birth_date

        for i in range(9):
            maha_idx = (r_idx + i) % 9
            maha_planet = self.dasha_lords[maha_idx]
            maha_years = self.dasha_years[maha_idx]
            maha_end_date = current_maha_date + timedelta(
                days=maha_years * 365.25
            )

            antardashas = []
            curr_antar_date = current_maha_date

            for j in range(9):
                antar_idx = (maha_idx + j) % 9
                antar_planet = self.dasha_lords[antar_idx]
                antar_years_val = (maha_years * self.dasha_years[antar_idx]) / 120.0
                antar_end_date = curr_antar_date + timedelta(
                    days=antar_years_val * 365.25
                )

                antardashas.append({
                    "planet": antar_planet,
                    "start": curr_antar_date.strftime("%Y-%m-%d"),
                    "end": antar_end_date.strftime("%Y-%m-%d"),
                })
                curr_antar_date = antar_end_date

            timeline.append({
                "maha_planet": maha_planet,
                "start": current_maha_date.strftime("%Y-%m-%d"),
                "end": maha_end_date.strftime("%Y-%m-%d"),
                "duration": f"{maha_years} سنة",
                "antardashas": antardashas,
            })
            current_maha_date = maha_end_date

        return timeline

    def get_ketu_past_life_profile(self, ketu_sign_str):
        if "الحمل" in ketu_sign_str:
            return {
                "title": "قائد عسكري ميداني، محارب قبلي، أو رائد هجرات بشرية كبرى عبر الحدود.",
                "wealth": "ثروات متقلبة وموسمية؛ مستمدة من الغنائم، الخراج العسكري، والممتلكات المنتزعة بالقوة.",
                "region": "السهوب الآسيوية، السفوح الجبلية لآسيا الوسطى، أو شمال أوروبا القديمة.",
                "death": "مفاجئ وعنيف في ساحة المعركة، متأثراً بإصابة مباشرة من سلاح حاد أو نزيف.",
                "akashic_lesson": "التحول من العدوان الفردي إلى الدبلوماسية وبناء السلام (درس رااهو في الميزان)."
            }
        elif "الثور" in ketu_sign_str:
            return {
                "title": "مالك أراضي إقطاعي، مرابي ملكي، أو تاجر مجوهرات وأحجار كريمة نادرة.",
                "wealth": "ثراء فاحش، مستقر وطويل الأمد؛ عقارات، أصول ملموسة، ومقتنيات ذهبية ضخمة.",
                "region": "وادي النيل، الهلال الخصيب، فارس القديمة، أو جزر المتوسط الغنية.",
                "death": "هادئ وبطيء في الشيخوخة نتيجة التخمة، السمنة المفرطة، أو أزمة قلبية مرتبطة بالرفاهية.",
                "akashic_lesson": "الالتزام بالتخلي عن التعلق المادي الخانق والانفتاح على التطور الروحي (درس رااهو في العقرب)."
            }
        else:
            return {
                "title": "متصوف، ناسخ كتب مقدسة، شاعر روحي زاهد، أو رحالة جوال.",
                "wealth": "زهيد ماديًا وغني روحيًا؛ عاش على الكفاف والهبات البسيطة متجردًا من كل ملذات الدنيا.",
                "region": "قمم الهيمالايا، أديرة أيرلندا النائية، أو السواحل الشرقية.",
                "death": "غرق في عرض البحر، اختفاء طوعي في البرية، أو مرض روحي غامض.",
                "akashic_lesson": "الاندماج الإيجابي في العالم المادي بدل الهروب التام إلى العزلة الروحية (درس رااهو في العذراء)."
            }

    def export_complete_html(self):
        matrix = self.calculate_matrix_of_destiny()
        vedic = self.calculate_vedic_nodes_and_moon()
        karmic_info = self.get_ketu_past_life_profile(vedic["ketu_sign"])
        name_vib = self.get_name_vibration()
        timeline = self.generate_detailed_timeline_with_antardasha()

        center_desc = self.ENERGY_MEANINGS.get(matrix["center"], "طاقة فريدة من الأركانا الكبرى.")
        name_vib_desc = self.ENERGY_MEANINGS.get(name_vib, "طاقة اسمية أكاشية فريدة.")
        p1_desc = self.ENERGY_MEANINGS.get(matrix["p1"], "طاقة الشخصية.")
        p2_desc = self.ENERGY_MEANINGS.get(matrix["p2"], "طاقة الروحانيات.")
        p3_desc = self.ENERGY_MEANINGS.get(matrix["p3"], "طاقة القدر.")
        p4_desc = self.ENERGY_MEANINGS.get(matrix["p4"], "طاقة الأرضية.")

        money_desc = self.ENERGY_MEANINGS.get(matrix["money_line"], "طاقة مالية وموارد.")
        love_desc = self.ENERGY_MEANINGS.get(matrix["love_line"], "طاقة علاقات وتناغم.")
        health_desc = self.ENERGY_MEANINGS.get(matrix["health_line"], "طاقة حيوية وصحة جسدية.")

        timeline_html = ""
        for t in timeline:
            antar_rows = ""
            for ant in t["antardashas"]:
                antar_rows += f"<tr><td>{ant['planet']}</td><td>{ant['start']}</td><td>{ant['end']}</td></tr>"

            timeline_html += f"""
            <div class="maha-box">
                <div class="maha-header">
                    <span>الفترة الكبرى (Mahadasha): <strong>{t['maha_planet']}</strong> ({t['duration']})</span>
                    <span>{t['start']} إلى {t['end']}</span>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>الفترة الفرعية (Antardasha)</th>
                            <th>تاريخ البداية</th>
                            <th>تاريخ النهاية</th>
                        </tr>
                    </thead>
                    <tbody>
                        {antar_rows}
                    </tbody>
                </table>
            </div>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>التقرير الشامل: الكارما وسجلات الأكاشا - {self.full_display_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Cairo', sans-serif;
            background-color: #030712;
            color: #f3f4f6;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 950px;
            margin: auto;
            background: #0f172a;
            border-radius: 16px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.8);
            padding: 40px;
            border: 1px solid #1e293b;
        }}
        h1 {{
            text-align: center;
            color: #f59e0b;
            font-size: 28px;
            margin-bottom: 5px;
        }}
        .subtitle {{
            text-align: center;
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 30px;
        }}
        .grid-box {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 25px;
        }}
        .meta-card {{
            background: #1e293b;
            border-radius: 8px;
            padding: 15px;
            border-right: 4px solid #f59e0b;
        }}
        .meta-card span {{
            color: #fbbf24;
            font-weight: bold;
        }}
        .section {{
            margin-bottom: 25px;
            padding: 18px 22px;
            background: #172033;
            border-radius: 10px;
            border-left: 4px solid #38bdf8;
        }}
        .section h3 {{
            margin: 0 0 8px 0;
            color: #38bdf8;
            font-size: 18px;
        }}
        .section p {{
            margin: 0;
            color: #cbd5e1;
            font-size: 16px;
            line-height: 1.6;
        }}
        .maha-box {{
            background: #1e293b;
            border-radius: 10px;
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #334155;
        }}
        .maha-header {{
            display: flex;
            justify-content: space-between;
            background: #0284c7;
            color: white;
            padding: 12px 15px;
            border-radius: 6px;
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #0f172a;
            border-radius: 6px;
            overflow: hidden;
        }}
        th, td {{
            padding: 10px 12px;
            text-align: right;
            border-bottom: 1px solid #1e293b;
            font-size: 13px;
        }}
        th {{
            background: #334155;
            color: #e2e8f0;
            font-weight: 600;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            font-size: 12px;
            color: #64748b;
            border-top: 1px solid #334155;
            padding-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>تقرير الأكاشا ومصفوفة القدر المتقدم (مخصص لـ: {self.full_display_name})</h1>
        <div class="subtitle">تحليل زمني دقيق يربط مصفوفة القدر، التنجيم الهندي، وسجلات الأكاشا</div>
        
        <div class="grid-box">
            <div class="meta-card">اسم المستفيد: <span>{self.full_display_name}</span></div>
            <div class="meta-card">تاريخ الميلاد: <span>{self.birth_date.strftime('%Y-%m-%d')}</span></div>
            <div class="meta-card">طاقة المركز (الروح): <span>الأركانا #{matrix['center']}</span></div>
            <div class="meta-card">تردد الاسم الأكاشي: <span>الرقم {name_vib}</span></div>
            <div class="meta-card">زاوية الشخصية (P1): <span>الأركانا #{matrix['p1']}</span></div>
            <div class="meta-card">زاوية الروحانيات (P2): <span>الأركانا #{matrix['p2']}</span></div>
            <div class="meta-card">زاوية القدر (P3): <span>الأركانا #{matrix['p3']}</span></div>
            <div class="meta-card">الأرضية الرابعة (P4): <span>الأركانا #{matrix['p4']}</span></div>
            <div class="meta-card">موقع كيتو (الجذور الكارمية): <span>{vedic['ketu_sign']}</span></div>
            <div class="meta-card">موقع رااهو (مسار التطور): <span>{vedic['rahu_sign']}</span></div>
        </div>

        <div class="section">
            <h3>🌟 التحليل العميق لطاقة المركز (طاقة الروح الأساسية)</h3>
            <p><strong>الأركانا #{matrix['center']}:</strong> {center_desc}</p>
        </div>

        <div class="section">
            <h3>🔤 التحليل العميق لتردد الاسم الأكاشي</h3>
            <p><strong>الرقم {name_vib}:</strong> {name_vib_desc}</p>
        </div>

        <div class="section">
            <h3>📐 معاني أركانات الزوايا الأساسية في مصفوفة القدر</h3>
            <p>👤 <strong>زاوية الشخصية (P1 - الأركانا #{matrix['p1']}):</strong> {p1_desc}</p>
            <p style="margin-top: 10px;">🕊️ <strong>زاوية الروحانيات (P2 - الأركانا #{matrix['p2']}):</strong> {p2_desc}</p>
            <p style="margin-top: 10px;">⏳ <strong>زاوية القدر (P3 - الأركانا #{matrix['p3']}):</strong> {p3_desc}</p>
            <p style="margin-top: 10px;">🏛️ <strong>الأرضية الرابعة (P4 - الأركانا #{matrix['p4']}):</strong> {p4_desc}</p>
        </div>

        <div class="section">
            <h3>📊 خطوط الطاقة في المصفوفة (المال، العلاقات، الصحة)</h3>
            <p>💰 <strong>خط المال (Money Line - الأركانا #{matrix['money_line']}):</strong> {money_desc}</p>
            <p style="margin-top: 10px;">❤️ <strong>خط العلاقات (Love Line - الأركانا #{matrix['love_line']}):</strong> {love_desc}</p>
            <p style="margin-top: 10px;">🛡️ <strong>خط الصحة (Health Line - الأركانا #{matrix['health_line']}):</strong> {health_desc}</p>
        </div>

        <div class="section">
            <h3>🏛️ المهنة والمنصب في الحياة السابقة</h3>
            <p>{karmic_info['title']}</p>
        </div>

        <div class="section">
            <h3>💰 مستوى الثراء والموارد المالية السابقة</h3>
            <p>{karmic_info['wealth']}</p>
        </div>

        <div class="section">
            <h3>🌍 الجغرافيا الثقافية والبلدان</h3>
            <p>{karmic_info['region']}</p>
        </div>

        <div class="section">
            <h3>⏳ طبيعة ونهاية الانتقال (الموت الكارمي)</h3>
            <p>{karmic_info['death']}</p>
        </div>

        <div class="section">
            <h3>✨ الدرس الأكاشي والكارمي الحالي</h3>
            <p>{karmic_info['akashic_lesson']}</p>
        </div>

        <div class="section">
            <h3>🌀 الجدول الزمني الكامل للفترات الكبرى والفرعية (Mahadasha & Antardasha)</h3>
            <p>يتيح لك هذا التسلسل الهرمي تتبع تأثير الكواكب بدقة فائقة على مدار سنين العمر:</p>
            {timeline_html}
        </div>

        <div class="footer">
            جميع الحقوق محفوظة - الفلكي استرو رادار
        </div>
    </div>
</body>
</html>
"""
        return html_content

    def export_jafr_esoteric_html(self):
        jafr = self.calculate_jafr_esoteric_profile()
        
        return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>التقرير الطاقي الباطني حسب علم الجفر - {self.full_display_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Cairo', sans-serif; background-color: #050515; color: #f3f4f6; margin: 0; padding: 20px; }}
        .container {{ max-width: 950px; margin: auto; background: #0f172a; border-radius: 16px; box-shadow: 0 25px 50px rgba(0,0,0,0.8); padding: 40px; border: 1px solid #3b82f6; }}
        h1 {{ text-align: center; color: #38bdf8; font-size: 28px; margin-bottom: 5px; }}
        .subtitle {{ text-align: center; color: #94a3b8; font-size: 14px; margin-bottom: 30px; }}
        .grid-box {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 25px; }}
        .meta-card {{ background: #1e293b; border-radius: 8px; padding: 15px; border-right: 4px solid #38bdf8; }}
        .meta-card span {{ color: #38bdf8; font-weight: bold; }}
        .section {{ margin-bottom: 25px; padding: 18px 22px; background: #1e293b; border-radius: 10px; border-left: 4px solid #f59e0b; }}
        .section h3 {{ margin: 0 0 8px 0; color: #f59e0b; font-size: 18px; }}
        .section p {{ margin: 0; color: #cbd5e1; font-size: 16px; line-height: 1.6; }}
        .footer {{ text-align: center; margin-top: 40px; font-size: 12px; color: #64748b; border-top: 1px solid #334155; padding-top: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔮 التقرير الطاقي الباطني حسب علم الجفر وحساب الجمل الكبير</h1>
        <div class="subtitle">المستفيد: {self.full_display_name} | المجموع الحرفي: {jafr['total_val']}</div>
        
        <div class="grid-box">
            <div class="meta-card">الاسم واسم الأم: <span>{self.full_display_name}</span></div>
            <div class="meta-card">البرج الباطني (الطالع): <span>{jafr['zodiac']}</span></div>
            <div class="meta-card">درجة البرج: <span>{jafr['degree']}</span></div>
            <div class="meta-card">المنزلة الرقمية (القمرية): <span>{jafr['lunar_mansion']}</span></div>
            <div class="meta-card">الطبع الغالب: <span>{jafr['element']}</span></div>
            <div class="meta-card">الطبع المفقود (للتوازن): <span>{jafr['missing_element']}</span></div>
        </div>

        <div class="section">
            <h3>🧠 التوازن الطاقي والنفسي</h3>
            <p>{jafr['psychology']}</p>
        </div>

        <div class="section">
            <h3>🩺 الاستعدادات للأمراض المستقبلية والصحية</h3>
            <p>{jafr['diseases']}</p>
        </div>

        <div class="section">
            <h3>🥗 الأغذية والأعشاب المناسبة لطبعك</h3>
            <p>{jafr['foods']}</p>
        </div>

        <div class="section">
            <h3>⚡ تأثير الطقس على الطاقة الجنسية والجسدية</h3>
            <p>{jafr['weather_effect']}</p>
        </div>

        <div class="section">
            <h3>📅 الأيام والتواريخ المحظوظة والمحسوسة</h3>
            <p>{' | '.join(jafr['lucky_days'])}</p>
        </div>

        <div class="section">
            <h3>💍 المعدن والأحجار الكريمة المناسبة</h3>
            <p>{jafr['metal_stone']}</p>
        </div>

        <div class="section">
            <h3>👤 نوع الطاقة الشخصية وطبيعة العلاقات الاجتماعية</h3>
            <p><strong>نوع الطاقة:</strong> {jafr['personality_type']}<br><br><strong>طبيعة العلاقات:</strong> {jafr['social_relations']}</p>
        </div>

        <div class="section">
            <h3>👶 عقدة النكاح والذرية والانجاب</h3>
            <p>{jafr['offspring']}</p>
        </div>

        <div class="section">
            <h3>💼 المجالات المهنية والتجارية الأنسب ونمط تدفق الأموال</h3>
            <p><strong>المجالات المهنية:</strong> {jafr['business_fields']}<br><br><strong>تدفق الأموال:</strong> {jafr['money_flow']}</p>
        </div>

        <div class="section">
            <h3>🧿 القابليات الطاقية (الحسد والعين) والكارما الموروثة</h3>
            <p><strong>العين والحسد:</strong> {jafr['evil_eye']}<br><br><strong>كارما الرحم:</strong> {jafr['karmic_inheritance']}</p>
        </div>

        <div class="section">
            <h3>📜 الأسماء والآيات والأسماء الحسنى للتحصين والعلاج</h3>
            <p>{jafr['spiritual_cure']}</p>
        </div>

        <div class="section">
            <h3>🌍 المدن والدول المناسبة للسكن أو السفر</h3>
            <p>{jafr['locations']}</p>
        </div>

        <div class="section">
            <h3>⏳ التوقعات الكبرى (الثروة، الشهرة، السجن، العمليات، وزواجك)</h3>
            <p>
                <strong>💰 الثروة ومرحلة العمر:</strong> {jafr['wealth_period']}<br><br>
                <strong>🌟 الشهرة:</strong> {jafr['fame']}<br><br>
                <strong>⚖️ خطر السجن:</strong> {jafr['prison']}<br><br>
                <strong>🏥 العمليات الجراحية الكبرى:</strong> {jafr['surgery']}<br><br>
                <strong>💍 وقت زواجك المتوقع:</strong> {jafr['marriage']}
            </p>
        </div>

        <div class="footer">تم إصدار هذا التقرير الباطني عبر محرك علم الحرف والجفر الفلكي - استرو رادار</div>
    </div>
</body>
</html>
"""


# --- واجهة Streamlit الرسومية ---
def main():
    st.set_page_config(page_title="محرك الأكاشا وعلم الجفر الفلكي", layout="centered")
    
    st.title("🌟 محرك التنجيم الهندي / الأكاشا و علم الجفر")
    st.markdown("### استخراج مصفوفة القدر والتقارير الطاقية الباطنية - استرو رادار")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("إعدادات الاسم الأول")
        first_name_type = st.selectbox("نوع الاسم الأول:", ["مفرد", "مركب"], key="f_type")
        if first_name_type == "مفرد":
            first_name_part1 = st.text_input("أدخل الاسم الأول المفرد:", value="فاطمة", key="fn1")
            first_name_part2 = ""
        else:
            first_name_part1 = st.text_input("الشطر الأول من الاسم الأول:", value="فاطمة", key="fn1_comp")
            first_name_part2 = st.text_input("الشطر الثاني من الاسم الأول:", value="الزهراء", key="fn2_comp")
            
    with col2:
        st.subheader("إعدادات اسم الأم و تاريخ الميلاد")
        mother_name_type = st.selectbox("نوع اسم الأم:", ["مفرد", "مركب"], key="m_type")
        if mother_name_type == "مفرد":
            mother_name_part1 = st.text_input("أدخل اسم الأم المفرد:", value="رجاء", key="mn1")
            mother_name_part2 = ""
        else:
            mother_name_part1 = st.text_input("الشطر الأول من اسم الأم:", value="", key="mn1_comp")
            mother_name_part2 = st.text_input("الشطر الثاني من اسم الأم:", value="", key="mn2_comp")
            
    birth_date_input = st.date_input("تاريخ الميلاد:", value=date(2005, 4, 17), min_value=date(1960, 1, 1))
        
    submitted = st.button("توليد التقرير الكارمي الشامل")
    jafr_submitted = st.button("🔮 التقرير الطاقي لك حسب علم الجفر")
        
    is_first_comp = (first_name_type == "مركب")
    is_mother_comp = (mother_name_type == "مركب")
    
    if submitted:
        if not first_name_part1.strip() or not mother_name_part1.strip():
            st.warning("يرجى إدخال الحقول المطلوبة بشكل صحيح.")
            return
            
        engine = MasterKarmicEngineWithAntardasha(
            first_name_part1, first_name_part2, mother_name_part1, mother_name_part2, 
            is_first_comp, is_mother_comp, birth_date_input.strftime("%Y-%m-%d")
        )
        html_report = engine.export_complete_html()
        
        st.success("تم توليد التقرير الكارمي الشامل بنجاح!")
        st.download_button(
            label="📥 تحميل التقرير الشامل بصيغة HTML",
            data=html_report,
            file_name=f"Karmic_Report_{first_name_part1}.html",
            mime="text/html"
        )
        st.iframe(html_report, height=950)

    if jafr_submitted:
        if not first_name_part1.strip() or not mother_name_part1.strip():
            st.warning("يرجى إدخال الحقول المطلوبة بشكل صحيح.")
            return
            
        engine = MasterKarmicEngineWithAntardasha(
            first_name_part1, first_name_part2, mother_name_part1, mother_name_part2, 
            is_first_comp, is_mother_comp, birth_date_input.strftime("%Y-%m-%d")
        )
        jafr_report = engine.export_jafr_esoteric_html()
        
        st.success("تم توليد التقرير الطاقي حسب علم الجفر بنجاح!")
        st.download_button(
            label="📥 تحميل تقرير علم الجفر بصيغة HTML (قابل للطباعة)",
            data=jafr_report,
            file_name=f"Jafr_Report_{first_name_part1}.html",
            mime="text/html"
        )
        st.iframe(jafr_report, height=950)

if __name__ == "__main__":
    main()
