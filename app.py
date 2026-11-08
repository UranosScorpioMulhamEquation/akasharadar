from datetime import date, datetime, timedelta
import math
import streamlit as st


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

    def __init__(self, first_name, birth_date_str):
        self.first_name = first_name.strip()
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

    def get_name_vibration(self):
        total_val = sum(ord(char.lower()) - 96 for char in self.first_name if char.isalpha())
        return (total_val % 22) or 22

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
                "akashic_lesson": "التخلي عن التعلق المادي الخانق والانفتاح على التطور الروحي (درس رااهو في العقرب)."
            }
        elif "الجوزاء" in ketu_sign_str:
            return {
                "title": "ناسخ مخطوطات ملكية، مترجم بلاطي، أو سفير تجاري وقاضي وثائق.",
                "wealth": "متوسط إلى جيد جداً؛ كسب وفير من العلوم، إدارة السجلات، والخدمات الكتابية والاستشارية.",
                "region": "طريق الحرير، بغداد العباسية، أو المراكز التجارية البيزنطية.",
                "death": "إرهاق ذهني حاد ونزيف في الدماغ أثناء إنجاز دراسة أو عمل كتابي مطول.",
                "akashic_lesson": "العمق الفلسفي بدلاً من تشتت الانتباه وسط كثرة المعلومات والكلمات (درس رااهو في القوس)."
            }
        elif "السرطان" in ketu_sign_str:
            return {
                "title": "كاهن معبد، حارس أسرار العشيرة، أو معالج تقليدي بالطب الشعبي والروحاني.",
                "wealth": "اعتماد أساسي على الهبات الدينية، العطايا، ووقف المعابد والأضرحة والموارد العائلية.",
                "region": "المعابد الهندية القديمة، التبت، جبال الأنديز، أو القرى العتيقة المعزولة.",
                "death": "في عزلة تامة داخل خلوة تأملية، أو غرق مفاجئ خلال طقس روحي قرب المياه.",
                "akashic_lesson": "التحرر من قيود الماضي العائلي والانطلاق نحو بناء الذات المستقلة (درس رااهو في الجدي)."
            }
        elif "الأسد" in ketu_sign_str:
            return {
                "title": "حاكم إقطاعي، أمير مقاطعة، أو فنان بلاط رفيع ومستشار سيادي.",
                "wealth": "واسع جداً وفخم؛ رافقته مظاهر البذخ الشديد، القصور، والمقتنيات الملكية.",
                "region": "أوروبا الوسطى، القصور الملكية في الصين الإمبراطورية، أو بلاد فارس.",
                "death": "انقلاب سياسي، تسمم متعمد في وليمة كبرى، أو اغتيال نتيجة مؤامرة بلاط.",
                "akashic_lesson": "خدمة الجماعة والمجتمع بدلاً من التمركز المطلق حول الأنا والذات (درس رااهو في الدلو)."
            }
        elif "العذراء" in ketu_sign_str:
            return {
                "title": "طبيب أعشاب ميداني، كيميائي مختبري، أو مراقب مالي وحسابات صارم.",
                "wealth": "مستقر، مرتب ومنظم بدقة بالغة؛ لا إسراف ولا فقر مدقع، ثروة مكتسبة بالكد والتدبير.",
                "region": "مكتبات الإسكندرية، بلاد الشام التاريخية، أو أثينا الكلاسيكية.",
                "death": "مرض عضال ومفاجئ ناجم عن عدوى مختبرية، أو تدهور صحي بسبب الوسواس القهري والعمل.",
                "akashic_lesson": "الإيمان بالحدس والكون بدلاً من البحث المستمر عن الكمال المادي (درس رااهو في الحوت)."
            }
        elif "الميزان" in ketu_sign_str:
            return {
                "title": "قاضٍ أعلى، مصلح اجتماعي، أو وسيط صلح بين القبائل والعروش.",
                "wealth": "متوازن ومنتظم؛ عوائد مالية ثابتة مقابل الأدوار التحكيمية وفض النزاعات القانونية.",
                "region": "شبه الجزيرة العربية، الأندلس المزدهرة، أو إيطاليا العصر الوسيط.",
                "death": "طبيعي أو نتيجة ضغوط نفسية وقانونية هائلة ومزمنة طوال سنوات العمل.",
                "akashic_lesson": "الاستقلالية في اتخاذ القرارات بدل الاعتماد الكلي على رضا الآخرين (درس رااهو في الحمل)."
            }
        elif "العقرب" in ketu_sign_str:
            return {
                "title": "عالم أسرار باطنية وكيمياء، جراح ميداني، أو محقق سري في أسرار الدولة.",
                "wealth": "ضخم ولكن غامض وسري؛ أموال طائلة نظير خدمات استخباراتية واكتشافات محظورة.",
                "region": "بابل القديمة، مصر الفرعونية، أو معاقل الكيمياء في أواسط أوروبا.",
                "death": "اغتيال سري، تسمم بغازات كيميائية، أو حادث غامض لم يتم كشف ملابساته.",
                "akashic_lesson": "الشفافية، تطهير الروح، والتخلي عن الرغبة في السيطرة الخفية (درس رااهو في الثور)."
            }
        elif "القوس" in ketu_sign_str:
            return {
                "title": "رئيس جامعة، فيلسوف كبير، قاضي تشريع ديني، أو مستكشف عظيم.",
                "wealth": "احترام مجتمعي هائل وموارد مالية وثقافية مستقرة تؤمن حياة فكرية رغيدة.",
                "region": "الهند الفيدية، مراكز فارس العلمية، أو الجامعات الأوروبية القديمة.",
                "death": "وفاة شيخوخة هادئة ومباركة، محاطاً بالكتب والمخطوطات وتلامذته.",
                "akashic_lesson": "التطبيق العملي للتجارب البسيطة بدلاً من التنظير الفلسفي المعقد (درس رااهو في الجوزاء)."
            }
        elif "الجدي" in ketu_sign_str:
            return {
                "title": "مهندس معماري مدبر، وزير مالية، أو مؤسس قلاع ومدن دفاعية.",
                "wealth": "ثراء ضخم ومترابط؛ جُمع عبر الانضباط الصارم، البناء طويل الأمد، والاستثمارات الحكيمة.",
                "region": "الإمبراطورية الرومانية، الصين القديمة، أو بريطانيا الصناعية.",
                "death": "إرهاق عمل مزمن، سقوط عرضي من مبنى مرتفع تحت الإنشاء، أو جلطة مفاجئة.",
                "akashic_lesson": "العناية بالجانب العاطفي والأسري بدل تكريس العمر للعمل والوصاية (درس رااهو في السرطان)."
            }
        elif "الدلو" in ketu_sign_str:
            return {
                "title": "عالم فلك، مخترع أنظمة طاقة، أو ثائر إصلاحي ضد الأنظمة الاستبدادية.",
                "wealth": "متقلب وغير مستقر؛ غالباً ما ضحى الشخص بالمال والثروة في سبيل أفكاره وإصلاحاته.",
                "region": "بغداد العباسية، أثينا، أو مراكز التنوير العلمي.",
                "death": "وفاة غامضة، في منفى اختياري، أو أثناء تجربة علمية غير محسوبة النتائج.",
                "akashic_lesson": "الارتباط الواقعي بالبشر على المستوى الفردي بدل المثالية الجماعية المجردة (درس رااهو في الأسد)."
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

        # استخراج معاني الأركانات والطاقات من القاموس
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
    <title>التقرير الشامل: الكارما وسجلات الأكاشا - {self.first_name}</title>
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
        @media print {{
            body {{ background: white; color: black; padding: 0; }}
            .container {{ box-shadow: none; border: none; background: white; }}
            .section, .maha-box, table {{ background: #f8fafc; border: 1px solid #cbd5e1; }}
            .meta-card {{ background: #f1f5f9; border-right-color: #0f172a; }}
            h1, .section h3 {{ color: #0f172a; }}
            .section p, td {{ color: #334155; }}
            .maha-header {{ background: #334155; color: white; }}
            th {{ background: #cbd5e1; color: black; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>تقرير الأكاشا ومصفوفة القدر المتقدم (مخصص لـ: {self.first_name})</h1>
        <div class="subtitle">تحليل زمني دقيق يربط مصفوفة القدر، التنجيم الهندي، وسجلات الأكاشا</div>
        
        <div class="grid-box">
            <div class="meta-card">اسم المستفيد: <span>{self.first_name}</span></div>
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


# --- واجهة Streamlit الرسومية ---
def main():
    st.set_page_config(page_title="محرك الأكاشا والكارما الفلكي", layout="centered")
    
    st.title("🌟 محرك التنجيم الهندي وسجلات الأكاشا الذكي")
    st.markdown("### الحياة السابقة، مصفوفة القدر، والفترات الزمنية الكارمية - استرو رادار")
    
    with st.form("karmic_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("الاسم الأول الحقيقي لحساب التردد:", "محمد")
        with col2:
            birth_date_input = st.date_input("تاريخ الميلاد:", value=date(2005, 4, 17), min_value=date(1960, 1, 1))
            
        submitted = st.form_submit_button("توليد التقرير الأكاشي الشامل")
        
    if submitted:
        if not first_name.strip():
            st.warning("يرجى إدخال الاسم الأول بشكل صحيح.")
            return
            
        engine = MasterKarmicEngineWithAntardasha(first_name, birth_date_input.strftime("%Y-%m-%d"))
        html_report = engine.export_complete_html()
        
        st.success("تم توليد التقرير الكارمي بنجاح!")
        
        # زر لتحميل التقرير كملف HTML للطباعة
        st.download_button(
            label="📥 تحميل التقرير بصيغة HTML (قابل للطباعة)",
            data=html_report,
            file_name=f"Karmic_Report_{first_name}.html",
            mime="text/html"
        )
        
        st.markdown("---")
        st.subheader("معاينة التقرير المباشرة:")
        st.iframe(html_report, height=950)

if __name__ == "__main__":
    main()