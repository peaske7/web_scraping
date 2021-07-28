import json as _json
import math
import sys as _sys
from os import listdir as _listdir

from alive_progress import alive_bar as _alive_bar


def translate_state(postid: str) -> str:
    states = [
        {'value': "AK", 'text': "アラスカ"},
        {'value': "AL", 'text': "アラバマ"},
        {'value': "AR", 'text': "アーカンソー"},
        {'value': "AS", 'text': "アメリカン・サモア"},
        {'value': "AZ", 'text': "アリゾナ"},
        {'value': "CA", 'text': "カリフォルニア"},
        {'value': "CO", 'text': "コロラド"},
        {'value': "CT", 'text': "コネチケット"},
        {'value': "DC", 'text': "ワシントンD.C."},
        {'value': "DE", 'text': "デラウェア"},
        {'value': "FL", 'text': "フロリダ"},
        {'value': "GA", 'text': "ジョージア"},
        {'value': "GU", 'text': "グアム"},
        {'value': "HI", 'text': "ハワイ"},
        {'value': "IA", 'text': "アイオワ"},
        {'value': "ID", 'text': "アイダホ"},
        {'value': "IL", 'text': "イリノイ"},
        {'value': "IN", 'text': "インディアナ"},
        {'value': "KS", 'text': "カンザス"},
        {'value': "KY", 'text': "ケンタッキー"},
        {'value': "LA", 'text': "ルイジアナ"},
        {'value': "MA", 'text': "マサチューセッツ"},
        {'value': "MD", 'text': "メリーランド"},
        {'value': "ME", 'text': "メイン"},
        {'value': "MI", 'text': "ミシガン"},
        {'value': "MN", 'text': "ミネソタ"},
        {'value': "MO", 'text': "ミズーリ"},
        {'value': "MS", 'text': "ミシシッピ"},
        {'value': "MT", 'text': "モンタナ"},
        {'value': "NC", 'text': "ノースキャロライナ"},
        {'value': "ND", 'text': "ノースダコタ"},
        {'value': "NE", 'text': "ネブラスカ"},
        {'value': "NH", 'text': "ニューハンプシャー"},
        {'value': "NJ", 'text': "ニュージャージー"},
        {'value': "NM", 'text': "ニューメキシコ"},
        {'value': "NV", 'text': "ネバダ"},
        {'value': "NY", 'text': "ニューヨーク"},
        {'value': "OH", 'text': "オハイオ"},
        {'value': "OK", 'text': "オクラホマ"},
        {'value': "OR", 'text': "オレゴン"},
        {'value': "PA", 'text': "ペンシルベニア"},
        {'value': "PR", 'text': "プエルトリコ"},
        {'value': "RI", 'text': "ロードアイランド"},
        {'value': "SC", 'text': "サウスキャロライナ"},
        {'value': "SD", 'text': "サウスダコタ"},
        {'value': "TN", 'text': "テネシー"},
        {'value': "TX", 'text': "テキサス"},
        {'value': "UT", 'text': "ユタ"},
        {'value': "VA", 'text': "バージニア"},
        {'value': "VI", 'text': "バージン諸島"},
        {'value': "VT", 'text': "バーモント"},
        {'value': "WA", 'text': "ワシントン"},
        {'value': "WI", 'text': "ウィスコンシン"},
        {'value': "WV", 'text': "ウェストバージニア"},
        {'value': "WY", 'text': "ワイオミング"}
    ]
    for state in states:
        if state['value'] == postid:
            return state['text']
    return postid


def translate_control(control: str) -> str:
    if control == 'Public':
        return '公立'
    elif control == 'Private for-profit':
        return '私立営利'
    elif control == 'Private not-for-profit':
        return '私立非営利'
    else:
        return 'ー'


def mutate_regions(postid: str) -> str:
    west_mountain = ['MT', 'WY', 'CO', 'UT', 'NV', 'ID', 'AZ', 'NM']
    west_pacific = ['WA', 'OR', 'CA', 'AK', 'HI']
    midwest_westNorthCentral = ['ND', 'SD', 'MN', 'IA', 'NE', 'KS', 'mo']
    midwest_eastNorthCentral = ['WI', 'IL', 'MI', 'IN', 'OH']
    south_westSouthCentral = ['OK', 'AR', 'LA', 'TX']
    south_eastSouthCentral = ['KY', 'TN', 'AL', 'MS']
    south_southAtlantic = ['WV', 'VA', 'MD', 'DC', 'DE', 'NC', 'SC', 'GA', 'FL']
    northeast_middleAtlantic = ['NY', 'NJ', 'PA']
    northeast_newEngland = ['ME', 'MA', 'NH', 'CT', 'RI', 'VT']
    if postid in west_mountain:
        return 'アメリカ西部・ロッキー山脈地帯'
    if postid in west_pacific:
        return 'アメリカ西部・西海岸'
    if postid in midwest_westNorthCentral:
        return 'アメリカ中西部・西北中部'
    if postid in midwest_eastNorthCentral:
        return 'アメリカ中西部・東北中部'
    if postid in south_westSouthCentral:
        return 'アメリカ南部・西南中部'
    if postid in south_eastSouthCentral:
        return 'アメリカ南部・東南中部'
    if postid in south_southAtlantic:
        return 'アメリカ南部・大西洋側南部'
    if postid in northeast_newEngland:
        return 'アメリカ北東部・ニューイングランド'
    if postid in northeast_middleAtlantic:
        return 'アメリカ北東部・大西洋岸中部'
    return 'その他'


def translate_urb_lev(urb_lev: str) -> str:
    levels = [
        {'en': 'City: Large', 'ja': '都市：大規模'},
        {'en': 'City: Midsize', 'ja': '都市：中規模'},
        {'en': 'City: Small', 'ja': '都市：小規模'},
        {'en': 'Suburb: Large', 'ja': '郊外：大規模'},
        {'en': 'Suburb: Midsize', 'ja': '郊外：中規模'},
        {'en': 'Suburb: Small', 'ja': '郊外：小規模'},
        {'en': 'Town: Fringe', 'ja': '町：都市郊外の外辺'},
        {'en': 'Town: Distant', 'ja': '町：遠隔'},
        {'en': 'Town: Remote', 'ja': '町：遠隔'},
        {'en': 'Rural: Fringe', 'ja': '田舎：都市郊外の外辺'},
        {'en': 'Rural: Distant', 'ja': '田舎：遠隔'},
        {'en': 'Rural: Remote', 'ja': '田舎：遠隔'},
    ]
    for level in levels:
        if level['en'] == urb_lev:
            return level['ja']
    return urb_lev


# TODO: find translations to Carnegie classifications
def translate_carnegie_class(carnegie_class: str) -> str:
    classifications = [
        {'en': "Master's Colleges & Universities: Larger Programs", 'ja': 'M1・修士課程重点大学（大）'},
        {'en': "Master's Colleges & Universities: Medium Programs", 'ja': 'M2・修士課程重点大学（中）'},
        {'en': "Master's Colleges & Universities: Small Programs", 'ja': 'M3・修士課程重点大学（小）'},
        {'en': "Doctoral Universities: Very High Research Activity", 'ja': 'R1・博士課程重点総合大学'},
        {'en': "Doctoral Universities: High Research Activity", 'ja': 'R2・博士課程重点総合大学'},
        {'en': "Doctoral/Professional Universities", 'ja': 'D/PU・博士課程重点総合大学'},
        {'en': "Baccalaureate Colleges: Arts & Sciences Focus", 'ja': '学士重点単科大学・文理集中'},
        {'en': "Baccalaureate Colleges: Diverse Fields", 'ja': '学士重点単科大学・多種'},
        {'en': "Baccalaureate/Associate's Colleges: Associate's Dominant", 'ja': '準学士・学士課程混合単科大学・準学士課程主要'},
        {'en': "Baccalaureate/Associate's Colleges: Mixed Baccalaureate/Associate's", 'ja': '準学士・学士課程混合単科大学'},
        {'en': "Associate's Colleges: High Transfer-High Traditional", 'ja': '準学士重点単科大学・転学集中'},
        {'en': "Associate's Colleges: High Transfer-Mixed Traditional/Nontraditional", 'ja': '準学士重点単科大学・転学集中'},
        {'en': "Associate's Colleges: High Transfer-High Nontraditional", 'ja': '準学士重点単科大学・転学集中'},
        {'en': "Associate's Colleges: Mixed Transfer/Vocational & Technical-High Traditional",
         'ja': '準学士重点単科大学・転学就職混合'},
        {'en': "Associate's Colleges: Mixed Transfer/Vocational & Technical-Mixed Traditional/Nontraditional",
         'ja': '準学士重点単科大学・転学就職混合'},
        {'en': "Associate's Colleges: Mixed Transfer/Vocational & Technical-High Nontraditional",
         'ja': '準学士重点単科大学・転学就職混合'},
        {'en': "Associate's Colleges: High Vocational & Technical-High Traditional", 'ja': '準学士重点単科大学・就職集中'},
        {'en': "Associate's Colleges: High Vocational & Technical-Mixed Traditional/Nontraditional",
         'ja': '準学士重点単科大学・就職集中'},
        {'en': "Associate's Colleges: High Vocational & Technical-High Nontraditional", 'ja': '準学士重点単科大学・就職集中'},
        {'en': "Special Focus Two-Year: Health Professions", 'ja': '医療系特化・２年制大学'},
        {'en': "Special Focus Two-Year: Technical Professions", 'ja': '技術系特化・２年制大学'},
        {'en': "Special Focus Two-Year: Arts & Design", 'ja': '芸術・デザイン系特化・２年制大学'},
        {'en': "Special Focus Two-Year: Other Fields", 'ja': 'その他分野特化・２年制大学'},
        {'en': "Special Focus Four-Year: Faith-Related Institutions", 'ja': '信仰関係系特化・４年制大学'},
        {'en': "Special Focus Four-Year: Medical Schools & Centers", 'ja': '医学部・医療機関系特化・４年制大学'},
        {'en': "Special Focus Four-Year: Other Health Professions Schools", 'ja': 'その他医療系特化・４年制大学'},
        {'en': "Special Focus Four-Year: Engineering Schools", 'ja': '工学系特化・４年制大学'},
        {'en': "Special Focus Four-Year: Other Technology-Related Schools", 'ja': 'その他技術関係系特化・４年制大学'},
        {'en': "Special Focus Four-Year: Business & Management Schools", 'ja': 'ビジネス・マネジメント特化・４年制大学'},
        {'en': "Special Focus Four-Year: Arts, Music & Design Schools", 'ja': '芸術・音楽・デザイン特化・４年制大学'},
        {'en': "Special Focus Four-Year: Law Schools", 'ja': '法学特化・４年制大学'},
        {'en': "Special Focus Four-Year: Other Special Focus Institutions", 'ja': 'その他専門分野に特化した４年制大学'},
        {'en': "Tribal Colleges", 'ja': "部族大学"}
    ]
    for classification in classifications:
        if classification['en'] == carnegie_class:
            return classification['ja']
    return carnegie_class


# TODO: find translations for carnegie size & settings
def translate_carnegie_size_cat(carnegie_size_cat: str) -> str:
    if carnegie_size_cat != 'Exclusively graduate/professional':
        elems = carnegie_size_cat.split(', ')
        year_type = elems[0]
        size = elems[1]

        year_type_translation_lookup = [
            {'en': "Four-year", 'ja': '４年制大学・'},
            {'en': "Two-year", 'ja': '２年制大学・'},
        ]
        size_translation_lookup = [
            {'en': 'very small', 'ja': '最小規模'},
            {'en': 'small', 'ja': '小規模'},
            {'en': 'medium', 'ja': '中規模'},
            {'en': 'large', 'ja': '大規模'},
            {'en': 'very large', 'ja': '最大規模'},
        ]

        res_str = ''
        for year_type_translation in year_type_translation_lookup:
            if year_type_translation['en'] == year_type:
                res_str += year_type_translation['ja']
        for size_translation in size_translation_lookup:
            if size_translation['en'] == size:
                res_str += size_translation['ja']
        return res_str
    else:
        return '大学院'


def translate_cal_sys(cal_sys: str) -> str:
    if cal_sys == 'Differs by program':
        return 'プログラム別'
    elif cal_sys == 'Continuous':
        return '継続的'
    elif cal_sys == 'Semester':
        return 'セメスター制'
    elif cal_sys == 'Quarter':
        return 'クォーター制'
    elif cal_sys == 'Other academic year':
        return 'その他'
    else:
        return 'ー'


def translate_ps(program: str) -> str:
    programs = [
        {'cip': '01', 'ja': '農学', 'color': '#1b5e20'},
        {'cip': '03', 'ja': '天然資源とその保護', 'color': '#43a047'},
        {'cip': '04', 'ja': '建築学', 'color': '#00796b'},
        {'cip': '05', 'ja': '地域・民族・文化・ジェンダー研究', 'color': '#fff176'},
        {'cip': '09', 'ja': 'コミュニケーション、ジャーナリズム', 'color': '#004d40'},
        {'cip': '10', 'ja': '通信技術と関連サービス', 'color': '#26c6da'},
        {'cip': '11', 'ja': '情報科学', 'color': '#2196f3'},
        {'cip': '12', 'ja': 'パーソナルサービス・料理学', 'color': '#f06292'},
        {'cip': '13', 'ja': '教育学', 'color': '#ffee58'},
        {'cip': '14', 'ja': '工学', 'color': '#1565c0'},
        {'cip': '15', 'ja': '工学技術・技術者', 'color': '#2979ff'},
        {'cip': '16', 'ja': '外語学・文学・言語学', 'color': '#00c853'},
        {'cip': '19', 'ja': '家庭・消費者科学/人間科学', 'color': '#ffa726'},
        {'cip': '22', 'ja': '法学', 'color': '#64b5f6'},
        {'cip': '23', 'ja': '英語・英文学', 'color': '#ef5350'},
        {'cip': '24', 'ja': '一般教養・人文科学', 'color': '#795548'},
        {'cip': '25', 'ja': '図書館学', 'color': '#a1887f'},
        {'cip': '26', 'ja': '生物学・生物医学', 'color': '#558b2f'},
        {'cip': '27', 'ja': '数学・統計学', 'color': '#90a4ae'},
        {'cip': '28', 'ja': 'JROTC/ROTC', 'color': '#546e7a'},
        {'cip': '29', 'ja': '軍事技術', 'color': '#37474f'},
        {'cip': '30', 'ja': '集学', 'color': '#00e5ff'},
        {'cip': '31', 'ja': '公園・レクリエーション・レジャー・フィットネス研究', 'color': '#9fa8da'},
        {'cip': '32', 'ja': '基礎スキル', 'color': '#e1bee7'},
        {'cip': '33', 'ja': 'シチズンシップ活動', 'color': '#00e676'},
        {'cip': '34', 'ja': '健康関連の知識・技能', 'color': '#d81b60'},
        {'cip': '35', 'ja': '対人関係・社会的スキル', 'color': '#b2ff59'},
        {'cip': '36', 'ja': 'レジャー・娯楽活動', 'color': '#18ffff'},
        {'cip': '37', 'ja': '個人的認識・自己改善', 'color': '#c2185b'},
        {'cip': '38', 'ja': '哲学・宗教学', 'color': '#ff8a80'},
        {'cip': '39', 'ja': '進学・宗教活動', 'color': '#7b1fa2'},
        {'cip': '40', 'ja': '物理学', 'color': '#7c4dff'},
        {'cip': '41', 'ja': '科学技術/技術者', 'color': '#00b0ff'},
        {'cip': '42', 'ja': '心理学', 'color': '#ff1744'},
        {'cip': '43', 'ja': '保安・保護サービス', 'color': '#ec407a'},
        {'cip': '44', 'ja': '行政・社会福祉', 'color': '#ffab40'},
        {'cip': '45', 'ja': '社会科学', 'color': '#ffa000'},
        {'cip': '46', 'ja': '建設業の職業', 'color': '#d4e157'},
        {'cip': '47', 'ja': 'メカニック・修理技術/専門家', 'color': '#455a64'},
        {'cip': '48', 'ja': '精密生産学', 'color': "#607d8b"},
        {'cip': '49', 'ja': '輸送と材料の移動', 'color': '#76ff03'},
        {'cip': '50', 'ja': '芸術', 'color': '#c62828'},
        {'cip': '51', 'ja': '臨床科学', 'color': '#f50057'},
        {'cip': '52', 'ja': 'ビジネス・経営・マーケティング', 'color': '#d84315'},
        {'cip': '53', 'ja': '高校/中学の学位取得', 'color': '#ffc107'},
        {'cip': '54', 'ja': '歴史学', 'color': '#ad1457'},
        {'cip': '60', 'ja': 'レジデントプログラム', 'color': '#3949ab'},
    ]
    for el in programs:
        if el['cip'] == program:
            return el
    return program


def shallow_translate():
    dirname = '../../outputs/layer_5'
    fnames = _listdir(dirname)
    total = len(fnames)

    tracker = 0
    limit = total
    with _alive_bar(total) as bar:
        for fname in fnames:
            path = f"{dirname}/{fname}"

            try:
                file = open(path)
                school = _json.load(file)

                # ===== SHALLOW TRANSLATE =====
                # 1. campus
                # state, control, bea_regions (deleted and replaced), urbanization level,
                state_ja = translate_state(school['general']['campus']['state_postid'])
                school['general']['campus']['state_ja'] = state_ja

                control_ja = translate_control(school['general']['campus']['control'])
                school['general']['campus']['control_ja'] = control_ja

                regions_ja = mutate_regions(school['general']['campus']['state_postid'])
                school['general']['campus']['region_ja'] = regions_ja
                del school['general']['campus']['bea_regions']

                urbanization_level_ja = translate_urb_lev(school['general']['campus']['urbanization_level'])
                school['general']['campus']['urbanization_level_ja'] = urbanization_level_ja

                # 2. classifications
                # carnegie_classification, carnegie_size_category
                carnegie_class = school['general']['classifications']['carnegie_classification']
                if carnegie_class is not None:
                    classification_ja = translate_carnegie_class(carnegie_class)
                    school['general']['classifications']['carnegie_classification_ja'] = classification_ja
                else:
                    school['general']['classifications']['carnegie_classification_ja'] = 'ー'

                size_cat = school['general']['classifications']['carnegie_size_category']
                if size_cat is not None:
                    size_cat_ja = translate_carnegie_size_cat(size_cat)
                    school['general']['classifications']['carnegie_size_category_ja'] = size_cat_ja
                else:
                    school['general']['classifications']['carnegie_size_category_ja'] = 'ー'

                # 3. education
                # calendar system
                cal_sys_ja = translate_cal_sys(school['general']['education']['calendar_system'])
                school['general']['education']['calendar_system_ja'] = cal_sys_ja

                # program sizes
                program_sizes_ja = []

                program_sizes = school['general']['education'].get('program_sizes')
                if program_sizes is not None:
                    for program in program_sizes.items():
                        if not program[1] == 'NULL':
                            cip = program[0]
                            percent = program[1]
                            key_ja = translate_ps(cip)['ja']
                            color = translate_ps(cip)['color']
                            radius = math.sqrt(program[1] / 3.14)
                            program_sizes_ja.append(
                                {'cip': cip, 'program_ja': key_ja, 'percentage': percent, 'radius': radius, 'color': color})
                        else:
                            program_sizes_ja = []

                    if not len(program_sizes_ja):
                        school['general']['education']['program_sizes_ja'] = program_sizes_ja
                    else:
                        school['general']['education']['program_sizes_ja'] = sorted(program_sizes_ja,
                                                                                    key=lambda program: program[
                                                                                        'percentage'], reverse=True)
                else:
                    school['general']['education'] = {
                        'calendar_system': None,
                        'calendar_system_ja': None,
                        'program_sizes': [],
                        'program_sizes_ja': []
                    }

                # output altered data to new file
                new_path = f"../../outputs/layer_6/{fname}"
                with open(new_path, 'w+') as outfile:
                    outfile.write(_json.dumps(school))

            except AttributeError as e:
                print(f"AttributeError at {path}: {e}")
            except IndexError as e:
                print(f"IndexError at {path}: {e}")
            except KeyError as e:
                print(f"KeyError at {path}: {e}")
            except TypeError as e:
                print(f"TypeError at {path}: {e}")
            except:
                e = _sys.exc_info()[0]
                print(e)

            bar()
            tracker += 1
            if tracker == limit:
                break


def main():
    shallow_translate()


if __name__ == '__main__':
    main()
