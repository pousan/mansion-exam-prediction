#!/usr/bin/env python3
"""
マンション管理士2026 予想問題演習 Webアプリケーション生成スクリプト
UI/UX ProMax 基準のデザインシステム、論点可視化、誤りハイライト対比、
消去法モード、段階的解説開示を完全実装した単一ファイルWebアプリ。
"""

import json
import os

OUTPUT_HTML = "ui/index.html"

QUESTIONS_DATA = [
    {
        "id": "GM-001",
        "num": 1,
        "dept": "第5部 マンション管理適正化法",
        "ronten_id": "TH03",
        "ronten_name": "マンション管理士制度（資格・業務・義務）",
        "key_concept": "マンション管理士の「登録要件」「信用失墜行為の範囲」「秘密保持の存続期間」「定期講習受講義務」の4大基本規定",
        "rev_id": "",
        "rev_name": "",
        "question": "マンションの管理の適正化の推進に関する法律に規定するマンション管理士に関する次の記述のうち、同法の規定によれば、正しいものはどれか。",
        "answer": 4,
        "options": [
            {
                "num": 1,
                "text": "マンション管理士試験に合格した者は、国土交通大臣の登録を受けなくても、マンション管理士の名称を用いてその業務を行うことができる。",
                "status": "誤",
                "trap_phrase": "国土交通大臣の登録を受けなくても",
                "correct_phrase": "登録を受けなければ、名称を用いて業務を行うことはできない",
                "explanation": "登録を受けなければマンション管理士の名称を用いて業務を行うことはできず、マンション管理士でない者は名称使用制限（罰則あり）を受けます。",
                "statute": "マンション管理適正化法 第30条第1項、第43条",
                "quote": "「マンション管理士となる資格を有する者は、国土交通大臣の登録を受けることができる」「マンション管理士でない者は、マンション管理士又はこれに紛らわしい名称を使用してはならない」",
                "key_point": "試験合格＝資格取得ですが、業務を行うには「登録」が必須です（名称独占資格）。"
            },
            {
                "num": 2,
                "text": "マンション管理士は、マンション管理士の信用を傷つけるような行為をしてはならないが、その職責にふさわしくない非行については、業務外の行為であれば同法の規定に違反しない。",
                "status": "誤",
                "trap_phrase": "業務外の行為であれば同法の規定に違反しない",
                "correct_phrase": "業務の内外を問わず、信用を傷つける行為は一律に禁止される",
                "explanation": "信用失墜行為の禁止（適正化法第40条）は、業務上の行為に限らず、私生活上の重大な非行など「業務外」の行為であっても適用されます。",
                "statute": "マンション管理適正化法 第40条",
                "quote": "「マンション管理士は、マンション管理士の信用を傷つけるような行為をしてはならない」",
                "key_point": "他の士業（宅建士、弁護士等）と同様、私生活での非行も信用失墜行為として処分の対象となります。"
            },
            {
                "num": 3,
                "text": "マンション管理士は、正当な理由がなく、その業務に関して知り得た秘密を漏らしてはならないが、マンション管理士でなくなった後は、秘密保持義務を負わない。",
                "status": "誤",
                "trap_phrase": "マンション管理士でなくなった後は、秘密保持義務を負わない",
                "correct_phrase": "マンション管理士でなくなった後においても、同様に義務を負う",
                "explanation": "秘密保持義務は、マンション管理士の登録を消除された後や廃業した後においても存続します。",
                "statute": "マンション管理適正化法 第42条",
                "quote": "「マンション管理士は、正当な理由がなく、その業務に関して知り得た秘密を漏らしてはならない。マンション管理士でなくなった後においても、同様とする」",
                "key_point": "「でなくなった後においても同様とする」は本試験の超頻出ひっかけトラップです。"
            },
            {
                "num": 4,
                "text": "マンション管理士は、国土交通省令で定める期間ごとに、国土交通大臣の登録を受けた者が国土交通省令で定めるところにより行う講習を受けなければならない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。マンション管理士は、5年ごとに国土交通大臣の登録を受けた登録講習機関が行う講習（法定講習）を受講しなければなりません。",
                "statute": "マンション管理適正化法 第41条",
                "quote": "「マンション管理士は、国土交通省令で定める期間ごとに、次条から第四十一条の四までの規定により国土交通大臣の登録を受けた者が国土交通省令で定めるところにより行う講習を受けなければならない」",
                "key_point": "受講義務違反は登録取消し又は名称使用停止の対象となり得ます。"
            }
        ]
    },
    {
        "id": "GM-002",
        "num": 2,
        "dept": "第5部 マンション管理適正化法",
        "ronten_id": "TH03",
        "ronten_name": "マンション管理士の登録及び登録取消し",
        "key_concept": "必要的取消し（必ず取消す事由）と裁量的処分（取消し又は名称使用停止を選択できる事由）の明確な区別",
        "rev_id": "",
        "rev_name": "",
        "question": "マンションの管理の適正化の推進に関する法律に規定するマンション管理士の登録及び登録の取消し等に関する次の記述のうち、同法の規定によれば、誤っているものはどれか。",
        "answer": 1,
        "options": [
            {
                "num": 1,
                "text": "マンション管理士が、業務に関して知り得た秘密を正当な理由なく漏らしたときは、国土交通大臣は、直ちにその登録を取り消さなければならず、名称の使用停止を命ずることはできない。",
                "status": "誤",
                "trap_phrase": "直ちにその登録を取り消さなければならず、名称の使用停止を命ずることはできない",
                "correct_phrase": "登録を取り消し、又は期間を定めて名称の使用停止を命ずることができる（裁量的処分）",
                "explanation": "秘密保持義務違反（第42条）に対する処分は「必要的取消し」ではなく、「登録の取消し又は期間を定めた名称使用停止」のいずれかを行うことができる裁量的処分です。",
                "statute": "マンション管理適正化法 第33条第2項",
                "quote": "「国土交通大臣は、マンション管理士が第四十条、第四十一条又は第四十二条の規定に違反したときは、その登録を取り消し、又は期間を定めてマンション管理士の名称の使用の停止を命ずることができる」",
                "key_point": "「取り消さなければならない（必要的）」と「取り消すことができる（任意的/裁量的）」の引っかけは頻出です！"
            },
            {
                "num": 2,
                "text": "マンション管理士が、偽りその他不正の手段により登録を受けたときは、国土交通大臣は、その登録を取り消さなければならない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。不正の手段により登録を受けた場合は、情状酌量の余地がなく「必要的取消し」事由となります。",
                "statute": "マンション管理適正化法 第33条第1項第二号",
                "quote": "「国土交通大臣は、マンション管理士が次の各号のいずれかに該当するときは、その登録を取り消さなければならない」「二 偽りその他不正の手段により登録を受けたとき」",
                "key_point": "不正登録、欠格事由該当、精神機能障害該当は「必要的取消し」です。"
            },
            {
                "num": 3,
                "text": "マンション管理士は、氏名に変更があったときは、遅滞なくその旨を国土交通大臣に届け出るとともに、登録証を添えて提出し、その訂正を受けなければならない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。登録事項（氏名、生年月日等）に変更が生じたときは、遅滞なく届出を行い、登録証の訂正を受ける必要があります。",
                "statute": "マンション管理適正化法 第32条第1項・第2項",
                "quote": "「第三十条第二項に規定する事項に変更があったときは、遅滞なく、その旨を国土交通大臣に届け出なければならない」「当該届出に登録証を添えて提出し、その訂正を受けなければならない」",
                "key_point": "「遅滞なく届出」＋「登録証を添えて提出・訂正」の2ステップを正しく押さえましょう。"
            },
            {
                "num": 4,
                "text": "マンション管理士の登録がその効力を失ったときは、国土交通大臣は、その登録を消除しなければならない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。死亡や登録取消し、自発的消除申請等により登録が効力を失ったときは、国交大臣は名簿から消除しなければなりません。",
                "statute": "マンション管理適正化法 第34条",
                "quote": "「国土交通大臣は、マンション管理士の登録がその効力を失ったときは、その登録を消除しなければならない」",
                "key_point": "消除は国交大臣の職権・義務として行われます。"
            }
        ]
    },
    {
        "id": "GM-003",
        "num": 3,
        "dept": "第5部 マンション管理適正化法",
        "ronten_id": "TH05",
        "ronten_name": "管理受託契約等の重要事項説明と利益相反防止",
        "key_concept": "【令和8年4月1日施行・法改正A20】管理者受託型管理業者による自己取引・密接関係者取引の事前説明会開催義務",
        "rev_id": "A20",
        "rev_name": "管理業者管理者型における利益相反防止（適正化法第77条の2）",
        "question": "マンションの管理の適正化の推進に関する法律に規定する管理受託契約等の重要事項の説明等に関する次の記述のうち、同法の規定によれば、正しいものはどれか。",
        "answer": 3,
        "options": [
            {
                "num": 1,
                "text": "マンション管理業者は、従前の管理受託契約と同一の条件で管理受託契約を更新しようとするときであっても、あらかじめ説明会を開催し、区分所有者等及び管理者等に対し、管理業務主任者をして重要事項を説明させなければならない。",
                "status": "誤",
                "trap_phrase": "あらかじめ説明会を開催し、区分所有者等及び管理者等に対し…説明させなければならない",
                "correct_phrase": "同一条件更新時は説明会の開催は不要（全員への書面交付＋管理者等への説明・交付で足りる）",
                "explanation": "同一条件での更新時は、区分所有者等全員への説明会開催は不要です。区分所有者等全員への書面交付と、管理者等への書面交付・説明で足ります。",
                "statute": "マンション管理適正化法 第72条第2項・第3項",
                "quote": "「従前の管理受託契約又は管理者受託契約と同一の条件で…更新しようとするときは、あらかじめ、当該管理組合を構成するマンションの区分所有者等全員に対し、重要事項を記載した書面を交付しなければならない」",
                "key_point": "新規契約時は「説明会の開催」が必要ですが、更新（同一条件）時は「説明会の開催は不要」という大原則です。"
            },
            {
                "num": 2,
                "text": "マンション管理業者は、重要事項を記載した書面の交付に代えて、区分所有者等又は管理者等の承諾を得た場合であっても、電磁的方法により当該書面に記載すべき事項を提供することはできない。",
                "status": "誤",
                "trap_phrase": "電磁的方法により当該書面に記載すべき事項を提供することはできない",
                "correct_phrase": "あらかじめ相手方の承諾を得ることで、電磁的方法による提供が可能",
                "explanation": "相手方（区分所有者等又は管理者等）の承諾を得たときは、書面交付に代えて電磁的方法（電子メール、Web閲覧等）で提供することができます。",
                "statute": "マンション管理適正化法 第72条第6項",
                "quote": "「書面の交付に代えて、政令で定めるところにより…承諾を得て、当該書面に記載すべき事項を…情報通信の技術を利用する方法…により提供することができる」",
                "key_point": "デジタル社会形成整備法によるIT化推進規定です。"
            },
            {
                "num": 3,
                "text": "管理事務の委託を受けた管理組合の管理者等であるマンション管理業者は、自己又は密接な関係を有する者との間における取引を行うときは、原則として、あらかじめ説明会を開催し、区分所有者等に対し当該取引につき重要な事実として国土交通省令で定める事項を説明しなければならない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。【2026年4月1日施行の改正適正化法第77条の2新設】いわゆる「第三者管理方式（管理業者管理者型）」において、利益相反を防ぐため、自社やグループ会社との工事発注等の取引を行う前に、区分所有者等への事前説明会を開催することが義務付けられました。",
                "statute": "マンション管理適正化法 第77条の2（令和8年4月1日施行）",
                "quote": "「マンション管理業者（管理事務の委託を受けた管理組合の管理者等であるものに限る。）は、自己又は人的関係、資本関係その他の関係において当該マンション管理業者と密接な関係を有する者…との間における取引を行うときは…あらかじめ、国土交通省令で定めるところにより説明会を開催し…重要な事実として国土交通省令で定める事項を説明しなければならない」",
                "key_point": "令和8年度試験の目玉論点！第三者管理方式での利益相反取引に対する新設事前説明義務です。"
            },
            {
                "num": 4,
                "text": "管理業務主任者は、重要事項の説明をするときは、相手方から請求があったときに限り、管理業務主任者証を提示しなければならない。",
                "status": "誤",
                "trap_phrase": "相手方から請求があったときに限り、管理業務主任者証を提示しなければならない",
                "correct_phrase": "請求の有無にかかわらず、必ず提示しなければならない",
                "explanation": "重要事項説明を行うときは、請求がなくても必ず主任者証を提示しなければなりません（請求があったときの提示義務は、通常の業務遂行時です）。",
                "statute": "マンション管理適正化法 第72条第4項",
                "quote": "「管理業務主任者は、第一項又は前項の説明をするときは、説明の相手方に対し、管理業務主任者証を提示しなければならない」",
                "key_point": "重説時は無条件提示！一般業務時は請求時提示！宅建士と同様の超頻出ルールです。"
            }
        ]
    },
    {
        "id": "GM-004",
        "num": 4,
        "dept": "第5部 マンション管理適正化法",
        "ronten_id": "TH02",
        "ronten_name": "地方公共団体の関与（勧告・助言・指導・財産管理命令請求）",
        "key_concept": "【令和8年4月1日施行・法改正A21】知事等による立ち入り制限と、所有者不明専有部分管理命令の特例申立権",
        "rev_id": "A21",
        "rev_name": "地方公共団体による財産管理制度の申立て等（適正化法第5条の2の2）",
        "question": "マンションの管理の適正化の推進に関する法律に規定する助言、指導、勧告等に関する次の記述のうち、同法の規定によれば、誤っているものはどれか。",
        "answer": 1,
        "options": [
            {
                "num": 1,
                "text": "都道府県知事等の職員が立入検査を行う権限には、管理組合の管理者等に無断で、居住者の承諾なく人の居住の用に供する専有部分に立ち入って検査する権限も含まれる。",
                "status": "誤",
                "trap_phrase": "居住者の承諾なく人の居住の用に供する専有部分に立ち入って検査する権限も含まれる",
                "correct_phrase": "人の居住の用に供する専有部分に立ち入るには、あらかじめ居住者の承諾が絶対に必要",
                "explanation": "行政職員の立入検査権であっても、個人のプライバシー・居住権を保護するため、居住の用に供する専有部分に立ち入る際は居住者の承諾が不可欠です。",
                "statute": "マンション管理適正化法 第5条の2第6項",
                "quote": "「ただし、当該マンションの人の居住の用に供する専有部分に立ち入る場合においては、あらかじめ、当該専有部分に居住している者の承諾を得なければならない」",
                "key_point": "憲法35条（住居の不可侵）に基づく重要な制約です。承諾なしの立ち入りは認められません。"
            },
            {
                "num": 2,
                "text": "都道府県知事等は、管理組合の運営又はマンションの修繕の実施がマンション管理適正化指針に照らして著しく不適切であることを把握したときは、当該管理組合の管理者等に対し、指針に即したマンションの管理を行うよう勧告することができる。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。管理状況が著しく不適切である場合、知事等は管理者等に対して勧告を行うことができます。",
                "statute": "マンション管理適正化法 第5条の2第2項",
                "quote": "「都道府県知事等は…適正化指針に照らして著しく不適切であることを把握したときは、当該管理組合の管理者等に対し…適正化指針に即したマンションの管理を行うよう勧告することができる」",
                "key_point": "助言・指導（第1項）にとどまらず、「著しく不適切」な場合は「勧告（第2項）」が可能です。"
            },
            {
                "num": 3,
                "text": "都道府県等は、マンション管理適正化指針に即し、管理組合の管理者等に対し、マンションの管理の適正化を図るために必要な助言及び指導をすることができる。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。適正化指針に即し、地方公共団体は助言及び指導を行うことができます。",
                "statute": "マンション管理適正化法 第5条の2第1項",
                "quote": "「都道府県等は、マンション管理適正化指針に即し、管理組合の管理者等…に対し、マンションの管理の適正化を図るために必要な助言及び指導をすることができる」",
                "key_point": "地方公共団体の相談窓口や巡回指導の根拠規定です。"
            },
            {
                "num": 4,
                "text": "都道府県知事等は、マンション所有者不明専有部分につき、その適正な管理のため特に必要があると認めるときは、地方裁判所に対し、区分所有法の規定による所有者不明専有部分管理命令の請求をすることができる。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。【2026年4月1日施行の法改正】空き家・所有者不明住戸が放置され周囲に悪影響を及ぼすのを防ぐため、自治体（知事等）が自ら地裁に管理命令を請求できる特例が新設されました。",
                "statute": "マンション管理適正化法 第5条の2の2第1項（令和8年4月1日施行）",
                "quote": "「都道府県知事等は…所有者不明専有部分…につき、その適正な管理のため特に必要があると認めるときは、地方裁判所に対し、区分所有法第四十六条の二第一項の規定による命令の請求をすることができる」",
                "key_point": "区分所有法改正（財産管理制度）とリンクした、行政による画期的な新権限です！"
            }
        ]
    },
    {
        "id": "GM-005",
        "num": 5,
        "dept": "第2部 マンション標準管理規約(会計)",
        "ronten_id": "KZ01",
        "ronten_name": "管理組合の会計・収支・帳票類の保管閲覧",
        "key_concept": "「余剰金の充当先」「新年度開始後の経常経費支出」「帳簿閲覧請求の手続き」の基本ルール",
        "rev_id": "",
        "rev_name": "",
        "question": "マンション標準管理規約(単棟型)の会計に関する次の記述のうち、同規約の規定によれば、正しいものはどれか。",
        "answer": 4,
        "options": [
            {
                "num": 1,
                "text": "収支決算の結果、管理費に余剰を生じた場合には、その余剰はすべて修繕積立金に繰り入れなければならない。",
                "status": "誤",
                "trap_phrase": "すべて修繕積立金に繰り入れなければならない",
                "correct_phrase": "翌年度における管理費に充当する（修繕積立金への自動繰入れではない）",
                "explanation": "管理費の余剰金は、翌年度の管理費に充当するのが原則です。修繕積立金会計への繰入れには総会決議が必要です。",
                "statute": "標準管理規約(単棟型) 第61条第1項",
                "quote": "「収支決算の結果、管理費に余剰を生じた場合には、その余剰は翌年度における管理費に充当する」",
                "key_point": "管理費会計と修繕積立金会計の「区分経理の原則」により、勝手に繰り入れることはできません。"
            },
            {
                "num": 2,
                "text": "理事長は、新会計年度の開始後、通常総会で収支予算案の承認を得るまでの間に、通常の管理に要する経常的な経費の支出が必要となった場合であっても、総会の承認を得るまでは一切の支出を行うことができない。",
                "status": "誤",
                "trap_phrase": "総会の承認を得るまでは一切の支出を行うことができない",
                "correct_phrase": "理事会の承認を得て、経常的・やむを得ない経費の支出を行うことができる",
                "explanation": "年度開始から総会承認までのタイムラグにおける管理の中断を防ぐため、通常の管理に要する経常的経費は「理事会の承認」で支出が認められます。",
                "statute": "標準管理規約(単棟型) 第58条第3項第一号",
                "quote": "「理事長は…承認を得るまでの間に、以下の各号に掲げる経費の支出が必要となった場合には、理事会の承認を得てその支出を行うことができる」",
                "key_point": "電気代や清掃費などの経常経費が払えなくなるのを防ぐ実務上不可欠な規定です。"
            },
            {
                "num": 3,
                "text": "管理費等に不足を生じた場合には、管理組合は、各区分所有者の頭数で均等に除した金額を、組合員に対してその都度負担させなければならない。",
                "status": "誤",
                "trap_phrase": "各区分所有者の頭数で均等に除した金額を",
                "correct_phrase": "管理費等の負担割合（専有部分の床面積割合）により負担を求める",
                "explanation": "管理費等の負担割合は「共用部分の共有持分割合（原則として専有部分の床面積割合）」に従います。頭数割ではありません。",
                "statute": "標準管理規約(単棟型) 第61条第2項、第25条第2項",
                "quote": "「管理費等に不足を生じた場合には、管理組合は組合員に対して第25条第２項に定める管理費等の負担割合により、その都度必要な金額の負担を求めることができる」",
                "key_point": "マンションの費用負担は「頭数均等」ではなく「床面積割合」が鉄則です。"
            },
            {
                "num": 4,
                "text": "理事長は、会計帳簿、什器備品台帳その他の帳票類を作成して保管し、組合員又は利害関係人から理由を付した書面による請求があったときは、閲覧につき相当の日時、場所等を指定して、これらを閲覧させなければならない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。帳票類の閲覧請求には「理由を付した書面」が必要であり、理事長は濫用防止のため日時・場所等を指定して閲覧させます。",
                "statute": "標準管理規約(単棟型) 第64条第1項",
                "quote": "「理事長は、会計帳簿、什器備品台帳その他の帳票類を作成して保管し、組合員又は利害関係人の理由を付した書面による請求があったときは、これらを閲覧させなければならない。この場合において、閲覧につき、相当の日時、場所等を指定することができる」",
                "key_point": "「理由を付した書面による請求」と「日時・場所の指定権」がセットで頻出されます。"
            }
        ]
    },
    {
        "id": "GM-006",
        "num": 6,
        "dept": "第2部 マンション標準管理規約(会計)",
        "ronten_id": "KZ01",
        "ronten_name": "滞納管理費等の督促・法的措置・充当順序",
        "key_concept": "滞納者に対する訴訟提起の権限（理事会決議でOK）と弁済の充当順序",
        "rev_id": "",
        "rev_name": "",
        "question": "マンション標準管理規約(単棟型)に定める管理費等の徴収及び管理組合の会計等に関する次の記述のうち、同規約の規定によれば、誤っているものはどれか。",
        "answer": 2,
        "options": [
            {
                "num": 1,
                "text": "組合員が納入期日までに管理費等を納入しない場合には、管理組合は、未払金額について遅延損害金や違約金としての弁護士費用等を加算して請求することができる。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。滞納に対しては、遅延損害金や違約金としての弁護士費用、督促・徴収費用を加算して請求することができます。",
                "statute": "標準管理規約(単棟型) 第60条第2項",
                "quote": "「その未払金額について、年利○％の遅延損害金と、違約金としての弁護士費用等並びに督促及び徴収の諸費用を加算して、その組合員に対して請求することができる」",
                "key_point": "民法上の原則と異なり、規約の定めにより弁護士費用を違約金として請求可能としています。"
            },
            {
                "num": 2,
                "text": "理事長は、未納の管理費等及び使用料の請求に関して、訴訟その他法的措置を追行するには、常に総会の決議を経なければならない。",
                "status": "誤",
                "trap_phrase": "常に総会の決議を経なければならない",
                "correct_phrase": "総会決議ではなく、機動的な対応のため「理事会の決議」で追行可能",
                "explanation": "滞納督促の訴訟提起をいちいち年1回の総会待機にすると回収が遅れるため、標準管理規約では「理事会の決議」により理事長が管理組合を代表して訴訟追行できると定めています。",
                "statute": "標準管理規約(単棟型) 第60条第4項",
                "quote": "「理事長は、未納の管理費等及び使用料の請求に関して、理事会の決議により、管理組合を代表して、訴訟その他法的措置を追行することができる」",
                "key_point": "超重要論点！滞納管理費等の訴訟は「理事会決議」でOK（総会特別決議等は不要）。"
            },
            {
                "num": 3,
                "text": "滞納者からの収納金が全ての債務を消滅させるのに足りないときは、管理組合は、理事会の決議により定める弁済の充当の順序に従い、その弁済を充当することができる。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。一部入金があった場合、理事会決議で定める充当順序（例: 費用・遅延損害金→管理費元本）に従って充当できます。",
                "statute": "標準管理規約(単棟型) 第60条第5項",
                "quote": "「収納金が全ての債務を消滅させるのに足りないときは、管理組合は、理事会の決議により定める弁済の充当の順序に従い、その弁済を充当することができる」",
                "key_point": "民法上の指定充当・法定充当の特則を規約で定めたものです。"
            },
            {
                "num": 4,
                "text": "組合員は、すでに納入した管理費等及び使用料について、管理組合に対して返還請求又は分割請求をすることができない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。区分所有権を譲渡して退去する場合であっても、既納の管理費や修繕積立金の返還請求はできません。",
                "statute": "標準管理規約(単棟型) 第60条第7項",
                "quote": "「組合員は、納入した管理費等及び使用料について、その返還請求又は分割請求をすることができない」",
                "key_point": "「引っ越すから修繕積立金を返して」という請求は一切認められません。"
            }
        ]
    },
    {
        "id": "GM-007",
        "num": 7,
        "dept": "第4部 建築・設備",
        "ronten_id": "SB02",
        "ronten_name": "室内環境・換気・遮音等級（JIS/建築基準法）",
        "key_concept": "遮音性能を表すサッシのT等級の定義（数値大＝性能高）とシックハウス対策基準",
        "rev_id": "",
        "rev_name": "",
        "question": "マンションの室内環境及びシックハウス対策等に関する次の記述のうち、建築基準法及び関係基準によれば、誤っているものはどれか。",
        "answer": 1,
        "options": [
            {
                "num": 1,
                "text": "開口部に取り付けるサッシの遮音性能を示すT等級(JIS A 4706)においては、T値の等級数値が大きいものほど、遮音性能が低い。",
                "status": "誤",
                "trap_phrase": "T値の等級数値が大きいものほど、遮音性能が低い",
                "correct_phrase": "T値の等級数値（T-1〜T-4）が大きいものほど、遮音性能が高い",
                "explanation": "サッシのT等級（JIS A 4706）は、T-1（25dB低下）からT-4（40dB低下）まであり、数値が大きい等級ほど音響透過損失が大きく、遮音性能が高くなります。",
                "statute": "日本産業規格 JIS A 4706（サッシ）",
                "quote": "「サッシの遮音性能はT-1（25dB）、T-2（30dB）、T-3（35dB）、T-4（40dB）に区分され、等級数値が大きいほど遮音性能が高い」",
                "key_point": "床衝撃音のL等級（数値小＝性能高）と、サッシのT等級（数値大＝性能高）の「逆転関係」は頻出トラップ！"
            },
            {
                "num": 2,
                "text": "住宅の居室には、原則として、換気回数が1時間当たり0.5回以上となる機械換気設備の設置が義務付けられている。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。建築基準法施行令により、住宅の居室には原則として毎時0.5回以上の24時間機械換気設備の設置が義務付けられています。",
                "statute": "建築基準法施行令 第20条の8第1項第1号ホ",
                "quote": "「住宅等の居室にあつては、〇・五回以上」",
                "key_point": "「毎時0.5回」という数値要件は確実に暗記しておきましょう。"
            },
            {
                "num": 3,
                "text": "日本産業規格(JIS)等によるホルムアルデヒド等級の表示において、「F☆☆☆☆」と表示された建築材料は、ホルムアルデヒドの発散速度が極めて小さいため、居室の内装仕上げにおける使用面積の制限を受けない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。最高等級であるフォースター（F☆☆☆☆）建材は発散量が極めて少なく、内装仕上げの使用面積制限を受けません。",
                "statute": "建築基準法施行令 第20条の7第1項",
                "quote": "「第一種ホルムアルデヒド発散建築材料を使用しないことその他の国土交通大臣が定める基準に適合するもの」",
                "key_point": "F☆☆☆やF☆☆は使用面積が制限され、マークなしは使用禁止です。"
            },
            {
                "num": 4,
                "text": "子どもが飛び跳ねたり走り回ったりすることによって階下に伝わる衝撃音は「重量床衝撃音」と呼ばれ、床スラブの厚さや剛性を高めることが低減対策として有効である。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。子どもの跳びはね等の鈍い重低音は重量床衝撃音（LH）であり、スラブ厚や剛性を増すことが根本的な解決策となります。",
                "statute": "日本建築学会「建築物の遮音性能基準と設計指針」",
                "quote": "「重量床衝撃音は、床スラブの厚さや剛性を高めることが低減に有効である」",
                "key_point": "スプーン落下等の軽量床衝撃音（LL）はカーペット等の表面仕上げ材が有効ですが、重量床（LH）はスラブ剛性が決定打です。"
            }
        ]
    },
    {
        "id": "GM-008",
        "num": 8,
        "dept": "第4部 修繕・診断",
        "ronten_id": "SH03",
        "ronten_name": "コンクリート構造体の劣化現象と診断",
        "key_concept": "エフロレッセンス、中性化、ポップアウト、アルカリシリカ反応の定義の峻別",
        "rev_id": "",
        "rev_name": "",
        "question": "マンションの鉄筋コンクリート造建物の劣化現象に関する次の記述のうち、適切なものはどれか。",
        "answer": 4,
        "options": [
            {
                "num": 1,
                "text": "中性化とは、コンクリートが空気中の二酸化炭素等の作用によりアルカリ性を失っていく現象をいい、中性化が内部の鉄筋位置まで進行しても、鉄筋の防錆効果が損なわれることはない。",
                "status": "誤",
                "trap_phrase": "鉄筋位置まで進行しても、鉄筋の防錆効果が損なわれることはない",
                "correct_phrase": "鉄筋位置まで中性化が達すると、不働態被膜が破壊されて鉄筋に急速な錆が発生する",
                "explanation": "コンクリートの高アルカリ性（pH12〜13）により鉄筋表面に形成されている不働態被膜が、中性化（pH10以下）によって破壊され、鉄筋が腐食（発錆）します。",
                "statute": "日本建築学会「コンクリートの中性化の診断と対策」",
                "quote": "「中性化が鉄筋位置まで進行すると、不働態被膜が破壊されて鉄筋に発錆が生じやすくなる」",
                "key_point": "中性化自体はコンクリート強度を直接落としませんが、鉄筋を錆びさせ爆裂を引き起こします。"
            },
            {
                "num": 2,
                "text": "ポップアウトとは、硬化したコンクリートが乾燥する過程で水分が蒸発することにより、コンクリート全体が均一に収縮して亀裂が生じる現象をいう。",
                "status": "誤",
                "trap_phrase": "コンクリート全体が均一に収縮して亀裂が生じる現象",
                "correct_phrase": "内部の局部的な膨張圧により、表面の小部分が円錐状（お椀状）に剥脱・欠損する現象",
                "explanation": "全体が収縮するのは乾燥収縮です。ポップアウトは骨材中の微粉や凍害、反応等により表面が部分的にポンと弾け飛ぶ現象を指します。",
                "statute": "日本建築学会「コンクリートの劣化と診断」",
                "quote": "「ポップアウトとは、コンクリート内部の部分的な膨張圧により、コンクリート表面の小部分が円錐型のくぼみ状に破壊される現象をいう」",
                "key_point": "用語のすり替えひっかけ問題の典型例です。"
            },
            {
                "num": 3,
                "text": "アルカリシリカ反応とは、コンクリート中のセメントペーストと大気中の水分が反応して、コンクリート表面が酸性化し強度を増大させる現象をいう。",
                "status": "誤",
                "trap_phrase": "表面が酸性化し強度を増大させる現象",
                "correct_phrase": "アルカリ金属イオンと骨材中のシリカ鉱物が反応してゲルが生じ、吸水膨張して異常なひび割れを生じる劣化現象",
                "explanation": "アルカリシリカ反応（ASR）はコンクリートの「がん」とも呼ばれ、骨材とアルカリが反応してできたゲルが吸水膨張し、網目状のひび割れを起こす重大な劣化です。",
                "statute": "日本建築学会「アルカリ骨材反応の抑制対策」",
                "quote": "「アルカリシリカ反応とは、セメント中のアルカリ成分と骨材中の特定鉱物が反応して生成したゲルが吸水膨張し、異常なひび割れや変形を生じさせる現象をいう」",
                "key_point": "「強度を増大させる」という荒唐無稽な文言に惑わされないようにしましょう。"
            },
            {
                "num": 4,
                "text": "エフロレッセンス（白華）とは、コンクリート内部の水溶性成分（水酸化カルシウム等）が水分とともに表面に染み出し、空気中の二酸化炭素等と反応して白色の炭酸カルシウム等の結晶として析出する現象である。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "適切（正しい）。雨水などの浸入に伴って内部の水酸化カルシウムが溶出し、大気中の炭酸ガス（CO2）と化合して不溶性の白い炭酸カルシウム結晶となる現象です。",
                "statute": "日本建築学会「コンクリートの劣化と診断」",
                "quote": "「エフロレッセンスとは、コンクリート内部のアルカリ成分が水分とともに表面に溶出し、空気中の炭酸ガスと反応して白色の炭酸カルシウム等となる現象をいう」",
                "key_point": "白華が見られる箇所は「水が浸入・通過している証拠（漏水経路）」となります。"
            }
        ]
    },
    {
        "id": "GM-009",
        "num": 9,
        "dept": "第5部 マンション管理適正化法",
        "ronten_id": "TH05",
        "ronten_name": "管理事務の定期報告（自社管理者型と一般型の相違）",
        "key_concept": "業者が自ら管理者等である場合における「説明会開催義務」の厳格規定",
        "rev_id": "",
        "rev_name": "",
        "question": "マンションの管理の適正化の推進に関する法律に規定する管理事務の報告に関する次の記述のうち、同法の規定によれば、誤っているものはどれか。",
        "answer": 2,
        "options": [
            {
                "num": 1,
                "text": "マンション管理業者は、管理事務の委託を受けた管理組合に管理者等（マンション管理業者を除く。）が置かれているときは、定期に、当該管理者等に対し、管理業務主任者をして管理事務に関する報告をさせなければならない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。区分所有者から選任された外部管理者等がいる場合、その管理者等に対して主任者が定期報告を行います。",
                "statute": "マンション管理適正化法 第77条第1項",
                "quote": "「管理事務の委託を受けた管理組合に管理者等が置かれているときは…定期に、当該管理者等に対し、管理業務主任者をして、当該管理事務に関する報告をさせなければならない」",
                "key_point": "通常は管理者（理事長等）に対して報告すれば足ります。"
            },
            {
                "num": 2,
                "text": "マンション管理業者自身が当該管理組合の管理者等である場合であっても、管理業務主任者証を提示して自己の代表者に対して報告を行えば足り、区分所有者等に対する説明会を開催する必要はない。",
                "status": "誤",
                "trap_phrase": "自己の代表者に対して報告を行えば足り、区分所有者等に対する説明会を開催する必要はない",
                "correct_phrase": "業者が自ら管理者等であるときは、定期に説明会を開催し、区分所有者等全員に報告しなければならない",
                "explanation": "管理業者自身が管理者である場合、自分で自分に報告してもチェック機能が働かないため、法は「区分所有者等に対する説明会の開催」を義務付けています。",
                "statute": "マンション管理適正化法 第77条第2項",
                "quote": "「当該マンション管理業者が当該管理組合の管理者等であるときは…定期に、説明会を開催し、当該管理組合を構成するマンションの区分所有者等に対し、管理業務主任者をして、当該管理事務に関する報告をさせなければならない」",
                "key_point": "業者自身が管理者のときは「自分に報告で終わり」は絶対NG！説明会開催が必須です。"
            },
            {
                "num": 3,
                "text": "管理事務の委託を受けた管理組合に管理者等が置かれていないときは、マンション管理業者は、定期に説明会を開催し、区分所有者等に対し、管理業務主任者をして管理事務に関する報告をさせなければならない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。管理者不在の場合も、報告を受ける窓口がないため、区分所有者等に対する説明会を開催して報告します。",
                "statute": "マンション管理適正化法 第77条第2項",
                "quote": "「管理事務の委託を受けた管理組合に管理者等が置かれていないとき…は…定期に、説明会を開催し、当該管理組合を構成するマンションの区分所有者等に対し…報告をさせなければならない」",
                "key_point": "管理者なし or 管理者が業者自身 ➔ 説明会開催が必要！"
            },
            {
                "num": 4,
                "text": "管理業務主任者は、管理者等に対する管理事務の報告又は区分所有者等に対する説明会において報告をするときは、説明の相手方に対し、管理業務主任者証を提示しなければならない。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。重説時と同様、管理事務報告の際も相手方に対して主任者証を提示しなければなりません。",
                "statute": "マンション管理適正化法 第77条第3項",
                "quote": "「管理業務主任者は、前二項の説明をするときは、説明の相手方に対し、管理業務主任者証を提示しなければならない」",
                "key_point": "報告時も主任者証の提示が必須です。"
            }
        ]
    },
    {
        "id": "GM-010",
        "num": 10,
        "dept": "第5部 マンション管理適正化法",
        "ronten_id": "TH03",
        "ronten_name": "秘密保持義務違反・名称使用制限・罰則体系",
        "key_concept": "秘密保持義務違反の「刑罰（1年以下の拘禁刑・親告罪）」と、名称制限違反の罰金刑",
        "rev_id": "",
        "rev_name": "",
        "question": "マンションの管理の適正化の推進に関する法律に規定するマンション管理士の秘密保持義務及び罰則等に関する次の記述のうち、同法の規定によれば、正しいものはどれか。",
        "answer": 3,
        "options": [
            {
                "num": 1,
                "text": "マンション管理士が、正当な理由がなく、その業務に関して知り得た秘密を漏らしたときは、1年以下の拘禁刑又は30万円以下の罰金に処せられるが、この罪は告訴がなくても公訴を提起することができる。",
                "status": "誤",
                "trap_phrase": "告訴がなくても公訴を提起することができる",
                "correct_phrase": "被害者の「告訴がなければ公訴を提起することができない（親告罪）」",
                "explanation": "秘密保持義務違反の罪（1年以下の拘禁刑又は30万円以下の罰金）は、秘密を漏らされた被害者の意思を尊重するため「親告罪」とされています。",
                "statute": "マンション管理適正化法 第107条第2項",
                "quote": "「前項第二号の罪は、告訴がなければ公訴を提起することができない」",
                "key_point": "「親告罪」である点はマンション管理士試験の超有名テーマです！"
            },
            {
                "num": 2,
                "text": "マンション管理士が名称の使用停止を命ぜられた場合であっても、停止期間中にマンション管理士の名称を使用したことに対する罰則規定は設けられていない。",
                "status": "誤",
                "trap_phrase": "罰則規定は設けられていない",
                "correct_phrase": "停止期間中に名称を使用したときは「30万円以下の罰金」に処せられる",
                "explanation": "名称使用停止命令に違反して名称を使用した者は、適正化法第109条第二号により「30万円以下の罰金」に処せられます。",
                "statute": "マンション管理適正化法 第109条第二号",
                "quote": "「第三十三条第二項の規定によりマンション管理士の名称の使用の停止を命ぜられた者が、当該停止を命ぜられた期間中に、マンション管理士の名称を使用したとき」は30万円以下の罰金",
                "key_point": "命令無視にはしっかり刑事罰が用意されています。"
            },
            {
                "num": 3,
                "text": "マンション管理士でない者が「マンション管理士」又はこれに紛らわしい名称を使用したときは、30万円以下の罰金に処せられる。",
                "status": "正",
                "trap_phrase": "",
                "correct_phrase": "",
                "explanation": "正しい。無資格者・未登録者による「マンション管理士」の名称使用や紛らわしい名称の使用には、30万円以下の罰金刑が科されます。",
                "statute": "マンション管理適正化法 第43条、第109条第三号",
                "quote": "「マンション管理士でない者は、マンション管理士又はこれに紛らわしい名称を使用してはならない」「第四十三条の規定に違反した者は、三十万円以下の罰金に処する」",
                "key_point": "名称独占資格の実効性を担保するための罰則です。"
            },
            {
                "num": 4,
                "text": "マンション管理士が秘密保持義務に違反した場合であっても、刑罰が科されることはなく、行政処分として登録の取消し又は名称使用停止が命じられるにとどまる。",
                "status": "誤",
                "trap_phrase": "刑罰が科されることはなく、行政処分…にとどまる",
                "correct_phrase": "行政処分だけでなく「1年以下の拘禁刑又は30万円以下の罰金」という重い刑事罰が科される",
                "explanation": "秘密保持義務違反は、行政処分（登録取消し・名称使用停止）と刑事罰（1年以下の拘禁刑又は30万円以下の罰金）の双方の対象となります。",
                "statute": "マンション管理適正化法 第33条第2項、第107条第1項第二号",
                "quote": "「その登録を取り消し、又は期間を定めて…名称の使用の停止を命ずることができる」「一年以下の拘禁刑又は三十万円以下の罰金に処する」",
                "key_point": "秘密漏洩は刑事事件になり得ます。※懲役刑・禁錮刑は法改正により「拘禁刑」に統一されました。"
            }
        ]
    }
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026年度版 マンション管理士試験 予想問題演習 | Gemini Prediction Engine</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#eef2ff',
                            100: '#e0e7ff',
                            500: '#6366f1',
                            600: '#4f46e5',
                            700: '#4338ca',
                            900: '#312e81',
                        }
                    },
                    fontFamily: {
                        sans: ['"Hiragino Sans"', '"Hiragino Kaku Gothic ProN"', '"Noto Sans JP"', 'sans-serif'],
                        mono: ['"SF Mono"', 'Menlo', 'monospace']
                    }
                }
            }
        }
    </script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        /* Smooth transitions */
        .option-card {
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .option-card:hover {
            transform: translateY(-1px);
        }
        .eliminated {
            opacity: 0.45;
            text-decoration: line-through;
            background-color: rgba(241, 245, 249, 0.6);
        }
        .dark .eliminated {
            background-color: rgba(30, 41, 59, 0.6);
        }
    </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 min-h-screen font-sans flex flex-col antialiased selection:bg-indigo-500 selection:text-white transition-colors duration-200">

    <!-- Top App Bar -->
    <header class="sticky top-0 z-40 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-4 lg:px-8 py-3 transition-colors">
        <div class="max-w-5xl mx-auto flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-400 text-white flex items-center justify-center font-bold shadow-md shadow-indigo-500/20">
                    <i data-lucide="sparkles" class="w-5 h-5"></i>
                </div>
                <div>
                    <h1 class="text-sm lg:text-base font-extrabold tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
                        <span>マンション管理士 2026 予想問題演習</span>
                        <span class="text-xs bg-indigo-100 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-300 font-semibold px-2 py-0.5 rounded-full border border-indigo-200 dark:border-indigo-800">令和8年4月施行基準</span>
                    </h1>
                    <p class="text-xs text-slate-500 dark:text-slate-400 hidden sm:block">TAC過去8年問題集DB突合・最新法改正反映（GM-001〜GM-010）</p>
                </div>
            </div>

            <div class="flex items-center gap-2 sm:gap-4">
                <!-- Score summary -->
                <div class="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-semibold">
                    <span class="text-slate-500 dark:text-slate-400">進捗:</span>
                    <span id="answered-count" class="text-indigo-600 dark:text-indigo-400">0</span>/10問
                    <span class="text-slate-300 dark:text-slate-600">|</span>
                    <span class="text-emerald-600 dark:text-emerald-400">正解: <span id="correct-count">0</span></span>
                </div>

                <!-- Dark mode toggle -->
                <button id="theme-toggle" class="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition" title="テーマ切り替え">
                    <i id="theme-icon" data-lucide="moon" class="w-4 h-4"></i>
                </button>
            </div>
        </div>

        <!-- Question Navigation Chips -->
        <div class="max-w-5xl mx-auto pt-3 pb-1 overflow-x-auto no-scrollbar flex items-center gap-2">
            <span class="text-xs font-bold text-slate-400 shrink-0">問題切替:</span>
            <div id="nav-chips" class="flex items-center gap-1.5 shrink-0">
                <!-- Dynamically generated chips -->
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="flex-1 max-w-5xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">

        <!-- Question Meta Card (Focus on Topic & Clarity) -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 sm:p-6 shadow-sm space-y-4">
            <!-- Badges line -->
            <div class="flex flex-wrap items-center gap-2 text-xs">
                <span id="q-dept" class="px-2.5 py-1 rounded-md font-bold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700"></span>
                <span id="q-ronten" class="px-2.5 py-1 rounded-md font-bold bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 flex items-center gap-1.5">
                    <i data-lucide="tag" class="w-3.5 h-3.5"></i>
                    <span id="q-ronten-text"></span>
                </span>
                <span id="q-rev-badge" class="hidden px-2.5 py-1 rounded-md font-bold bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800 flex items-center gap-1.5 animate-pulse">
                    <i data-lucide="flame" class="w-3.5 h-3.5"></i>
                    <span id="q-rev-text"></span>
                </span>
            </div>

            <!-- Key Concept Banner (論点の急所) -->
            <div class="bg-gradient-to-r from-indigo-50 via-slate-50 to-white dark:from-indigo-950/40 dark:via-slate-900 dark:to-slate-900 border-l-4 border-indigo-500 rounded-r-xl p-3 sm:p-4">
                <div class="flex items-start gap-2.5">
                    <div class="p-1 rounded bg-indigo-500 text-white shrink-0 mt-0.5">
                        <i data-lucide="lightbulb" class="w-4 h-4"></i>
                    </div>
                    <div>
                        <div class="text-xs font-bold text-indigo-900 dark:text-indigo-200 tracking-wide uppercase">出題の急所（Key Concept）</div>
                        <p id="q-key-concept" class="text-xs sm:text-sm font-semibold text-slate-700 dark:text-slate-200 mt-0.5 leading-relaxed"></p>
                    </div>
                </div>
            </div>

            <!-- Question Text -->
            <div class="pt-2">
                <div class="text-xs font-bold text-indigo-600 dark:text-indigo-400 mb-1 flex items-center gap-1.5">
                    <span id="q-number-label">問 1</span>
                    <span class="text-slate-400">/ 10</span>
                    <span id="q-id-label" class="text-slate-400 font-mono text-[11px]">(GM-001)</span>
                </div>
                <p id="q-text" class="text-base sm:text-lg font-bold text-slate-900 dark:text-white leading-relaxed tracking-wide"></p>
            </div>
        </div>

        <!-- Options Card -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 sm:p-6 shadow-sm space-y-4">
            <div class="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 border-b border-slate-100 dark:border-slate-800 pb-3">
                <div class="flex items-center gap-2">
                    <i data-lucide="help-circle" class="w-4 h-4 text-indigo-500"></i>
                    <span>解答を選択してください（キーボード数字キー 1〜4 対応）</span>
                </div>
                <span class="text-[11px] bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded font-mono">消去法モード利用可能</span>
            </div>

            <!-- Options Container -->
            <div id="options-container" class="space-y-3">
                <!-- Dynamically populated options -->
            </div>

            <!-- Action Bar -->
            <div class="pt-4 flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-slate-100 dark:border-slate-800">
                <div class="text-xs text-slate-400 flex items-center gap-1.5">
                    <i data-lucide="info" class="w-3.5 h-3.5"></i>
                    <span>各肢右の「✕」ボタンで消去法マーカー、「？」で保留マークをつけられます</span>
                </div>
                <div class="flex items-center gap-3 w-full sm:w-auto">
                    <button id="submit-btn" disabled class="w-full sm:w-auto px-6 py-2.5 rounded-xl font-bold text-sm bg-indigo-600 hover:bg-indigo-700 active:scale-95 disabled:bg-slate-200 dark:disabled:bg-slate-800 disabled:text-slate-400 disabled:cursor-not-allowed disabled:transform-none text-white shadow-md shadow-indigo-600/20 transition flex items-center justify-center gap-2">
                        <span>この肢で回答する</span>
                        <i data-lucide="check-circle-2" class="w-4 h-4"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Feedback & Detailed Explanation Card (Reveals after submit) -->
        <div id="explanation-container" class="hidden space-y-6">
            
            <!-- Result Banner -->
            <div id="result-banner" class="rounded-2xl p-5 border flex items-center justify-between shadow-sm">
                <!-- Dynamically populated -->
            </div>

            <!-- Detailed Explanation Tabs / Accordion -->
            <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 sm:p-6 shadow-sm space-y-5">
                <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                    <h3 class="font-extrabold text-base sm:text-lg text-slate-900 dark:text-white flex items-center gap-2">
                        <i data-lucide="book-open-check" class="w-5 h-5 text-indigo-500"></i>
                        <span>肢別詳細解説 & 誤りハイライト対比</span>
                    </h3>
                    <span class="text-xs text-indigo-600 dark:text-indigo-400 font-semibold bg-indigo-50 dark:bg-indigo-950 px-2.5 py-1 rounded-full">
                        全4肢の急所を網羅
                    </span>
                </div>

                <!-- Explanation Cards Container -->
                <div id="explanation-cards" class="space-y-4">
                    <!-- Dynamically populated cards -->
                </div>
            </div>

            <!-- Bottom Navigation Bar -->
            <div class="flex items-center justify-between pt-2">
                <button id="prev-btn" class="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 font-semibold text-sm hover:bg-slate-50 dark:hover:bg-slate-800 transition flex items-center gap-2">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i>
                    <span>前の問題</span>
                </button>
                <button id="retry-btn" class="px-4 py-2 rounded-xl text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 text-xs font-semibold hover:bg-slate-100 dark:hover:bg-slate-800 transition flex items-center gap-1.5">
                    <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
                    <span>もう一度解く</span>
                </button>
                <button id="next-btn" class="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md shadow-indigo-600/20 transition flex items-center gap-2">
                    <span>次の問題へ</span>
                    <i data-lucide="arrow-right" class="w-4 h-4"></i>
                </button>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="mt-auto border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 py-6 text-center text-xs text-slate-500 dark:text-slate-400">
        <p>2026年マンション管理士試験 予想問題演習システム (Gemini Engine & UI/UX ProMax Edition)</p>
        <p class="mt-1 text-slate-400 dark:text-slate-600">法令基準日: 2026年4月1日施行 / 区分所有法・適正化法・標準管理規約完全準拠</p>
    </footer>

    <!-- App Logic Script -->
    <script>
        const QUESTIONS = %QUESTIONS_JSON%;

        // State Management
        let currentIdx = 0;
        let userAnswers = {}; // { qIdx: selectedOptNum }
        let eliminationState = {}; // { qIdx: { optNum: 'eliminated' | 'marked' | 'none' } }

        // DOM Elements
        const themeToggle = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');
        const navChips = document.getElementById('nav-chips');
        const answeredCountEl = document.getElementById('answered-count');
        const correctCountEl = document.getElementById('correct-count');

        const qDept = document.getElementById('q-dept');
        const qRonten = document.getElementById('q-ronten-text');
        const qRevBadge = document.getElementById('q-rev-badge');
        const qRevText = document.getElementById('q-rev-text');
        const qKeyConcept = document.getElementById('q-key-concept');
        const qNumberLabel = document.getElementById('q-number-label');
        const qIdLabel = document.getElementById('q-id-label');
        const qText = document.getElementById('q-text');

        const optionsContainer = document.getElementById('options-container');
        const submitBtn = document.getElementById('submit-btn');

        const explanationContainer = document.getElementById('explanation-container');
        const resultBanner = document.getElementById('result-banner');
        const explanationCards = document.getElementById('explanation-cards');

        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const retryBtn = document.getElementById('retry-btn');

        // Dark Mode Setup
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.classList.add('dark');
        }
        themeToggle.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            updateThemeIcon();
        });
        function updateThemeIcon() {
            const isDark = document.documentElement.classList.contains('dark');
            themeIcon.setAttribute('data-lucide', isDark ? 'sun' : 'moon');
            lucide.createIcons();
        }

        // Initialize UI
        function init() {
            renderNavChips();
            loadQuestion(0);
            updateThemeIcon();

            // Keyboard shortcut support
            window.addEventListener('keydown', (e) => {
                if (['1', '2', '3', '4'].includes(e.key)) {
                    const optNum = parseInt(e.key);
                    selectOption(optNum);
                } else if (e.key === 'Enter') {
                    if (!submitBtn.disabled && explanationContainer.classList.contains('hidden')) {
                        submitAnswer();
                    } else if (!explanationContainer.classList.contains('hidden') && currentIdx < QUESTIONS.length - 1) {
                        loadQuestion(currentIdx + 1);
                    }
                }
            });
        }

        // Render Top Navigation Chips
        function renderNavChips() {
            navChips.innerHTML = '';
            QUESTIONS.forEach((q, idx) => {
                const btn = document.createElement('button');
                btn.className = `w-7 h-7 rounded-lg text-xs font-bold transition flex items-center justify-center border `;
                
                const answered = userAnswers[idx] !== undefined;
                const isCorrect = answered && userAnswers[idx] === q.answer;
                const isCurrent = idx === currentIdx;

                if (isCurrent) {
                    btn.classList.add('ring-2', 'ring-indigo-500', 'ring-offset-1', 'dark:ring-offset-slate-900');
                }

                if (!answered) {
                    btn.classList.add('bg-white', 'dark:bg-slate-800', 'text-slate-600', 'dark:text-slate-300', 'border-slate-200', 'dark:border-slate-700', 'hover:border-indigo-400');
                } else if (isCorrect) {
                    btn.classList.add('bg-emerald-500', 'text-white', 'border-emerald-600');
                } else {
                    btn.classList.add('bg-rose-500', 'text-white', 'border-rose-600');
                }

                btn.innerText = idx + 1;
                btn.title = `問 ${idx + 1}: ${q.ronten_name}`;
                btn.addEventListener('click', () => loadQuestion(idx));
                navChips.appendChild(btn);
            });
        }

        // Load Question Details
        function loadQuestion(idx) {
            currentIdx = idx;
            const q = QUESTIONS[idx];

            // Update Metadata
            qDept.innerText = q.dept;
            qRonten.innerText = `${q.ronten_id} ${q.ronten_name}`;
            
            if (q.rev_id) {
                qRevBadge.classList.remove('hidden');
                qRevText.innerText = `🔥 2026年改正 (${q.rev_id}) ${q.rev_name}`;
            } else {
                qRevBadge.classList.add('hidden');
            }

            qKeyConcept.innerText = q.key_concept;
            qNumberLabel.innerText = `問 ${q.num}`;
            qIdLabel.innerText = `(${q.id})`;
            qText.innerText = q.question;

            // Render Options
            renderOptions();

            // Check if already answered
            if (userAnswers[idx] !== undefined) {
                showExplanation();
            } else {
                explanationContainer.classList.add('hidden');
                submitBtn.disabled = true;
            }

            // Update Nav State
            prevBtn.disabled = idx === 0;
            prevBtn.classList.toggle('opacity-50', idx === 0);
            prevBtn.classList.toggle('cursor-not-allowed', idx === 0);

            nextBtn.innerHTML = idx === QUESTIONS.length - 1 
                ? `<span>完了（結果確認）</span><i data-lucide="check" class="w-4 h-4"></i>`
                : `<span>次の問題へ</span><i data-lucide="arrow-right" class="w-4 h-4"></i>`;

            renderNavChips();
            updateStats();
            lucide.createIcons();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Render Options List
        function renderOptions() {
            optionsContainer.innerHTML = '';
            const q = QUESTIONS[currentIdx];
            const answered = userAnswers[currentIdx] !== undefined;
            const selectedOpt = userAnswers[currentIdx];

            if (!eliminationState[currentIdx]) {
                eliminationState[currentIdx] = {};
            }

            q.options.forEach((opt) => {
                const optState = eliminationState[currentIdx][opt.num] || 'none';
                const isSelected = selectedOpt === opt.num;
                const isCorrect = opt.num === q.answer;

                const card = document.createElement('div');
                card.className = `option-card relative rounded-xl border p-4 transition cursor-pointer select-none flex items-start justify-between gap-4 `;

                // Card Styling based on answer status
                if (!answered) {
                    if (isSelected) {
                        card.classList.add('border-indigo-600', 'bg-indigo-50/60', 'dark:bg-indigo-950/40', 'ring-2', 'ring-indigo-500/20');
                    } else if (optState === 'eliminated') {
                        card.classList.add('eliminated', 'border-slate-200', 'dark:border-slate-800');
                    } else {
                        card.classList.add('border-slate-200', 'dark:border-slate-800', 'bg-white', 'dark:bg-slate-900', 'hover:border-indigo-300', 'dark:hover:border-indigo-700');
                    }
                } else {
                    // Answered view
                    if (isCorrect) {
                        card.classList.add('border-emerald-500', 'bg-emerald-50/70', 'dark:bg-emerald-950/30', 'ring-2', 'ring-emerald-500/20');
                    } else if (isSelected && !isCorrect) {
                        card.classList.add('border-rose-500', 'bg-rose-50/70', 'dark:bg-rose-950/30', 'ring-2', 'ring-rose-500/20');
                    } else {
                        card.classList.add('border-slate-200', 'dark:border-slate-800', 'opacity-70');
                    }
                }

                // Left: Number Badge + Text
                const leftDiv = document.createElement('div');
                leftDiv.className = 'flex items-start gap-3 flex-1';

                const numBadge = document.createElement('span');
                numBadge.className = `w-6 h-6 rounded-lg text-xs font-bold shrink-0 flex items-center justify-center mt-0.5 `;
                if (answered) {
                    if (isCorrect) {
                        numBadge.classList.add('bg-emerald-600', 'text-white');
                    } else if (isSelected) {
                        numBadge.classList.add('bg-rose-600', 'text-white');
                    } else {
                        numBadge.classList.add('bg-slate-100', 'dark:bg-slate-800', 'text-slate-500');
                    }
                } else if (isSelected) {
                    numBadge.classList.add('bg-indigo-600', 'text-white');
                } else {
                    numBadge.classList.add('bg-slate-100', 'dark:bg-slate-800', 'text-slate-600', 'dark:text-slate-400');
                }
                numBadge.innerText = opt.num;

                const textSpan = document.createElement('span');
                textSpan.className = `text-sm sm:text-base leading-relaxed ${isSelected ? 'font-semibold text-indigo-950 dark:text-indigo-100' : 'text-slate-700 dark:text-slate-200'}`;
                textSpan.innerText = opt.text;

                leftDiv.appendChild(numBadge);
                leftDiv.appendChild(textSpan);
                card.appendChild(leftDiv);

                // Right: Elimination tools (only before answer)
                if (!answered) {
                    const toolDiv = document.createElement('div');
                    toolDiv.className = 'flex items-center gap-1 shrink-0';

                    // Eliminate toggle button (✕)
                    const elimBtn = document.createElement('button');
                    elimBtn.className = `p-1.5 rounded-lg border text-xs transition ${optState === 'eliminated' ? 'bg-rose-100 border-rose-300 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300' : 'border-slate-200 dark:border-slate-700 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200'}`;
                    elimBtn.innerHTML = `<i data-lucide="x" class="w-3.5 h-3.5"></i>`;
                    elimBtn.title = '消去線（✕）をつける';
                    elimBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        toggleElimination(opt.num);
                    });

                    toolDiv.appendChild(elimBtn);
                    card.appendChild(toolDiv);
                }

                // Click to Select
                if (!answered) {
                    card.addEventListener('click', () => selectOption(opt.num));
                }

                optionsContainer.appendChild(card);
            });

            lucide.createIcons();
        }

        // Toggle Option Selection
        function selectOption(num) {
            if (userAnswers[currentIdx] !== undefined) return;
            const q = QUESTIONS[currentIdx];
            userAnswers[currentIdx] = num;
            submitBtn.disabled = false;
            renderOptions();
        }

        // Toggle Elimination Mark
        function toggleElimination(num) {
            const current = eliminationState[currentIdx][num] || 'none';
            eliminationState[currentIdx][num] = current === 'eliminated' ? 'none' : 'eliminated';
            renderOptions();
        }

        // Submit Answer
        submitBtn.addEventListener('click', submitAnswer);
        function submitAnswer() {
            if (userAnswers[currentIdx] === undefined) return;
            showExplanation();
            renderNavChips();
            updateStats();
            lucide.createIcons();
        }

        // Show Explanation & Result
        function showExplanation() {
            const q = QUESTIONS[currentIdx];
            const selected = userAnswers[currentIdx];
            const isCorrect = selected === q.answer;

            explanationContainer.classList.remove('hidden');

            // Render Banner
            resultBanner.className = `rounded-2xl p-5 border flex items-center justify-between shadow-sm ${
                isCorrect 
                ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-800 text-emerald-900 dark:text-emerald-200' 
                : 'bg-rose-50 dark:bg-rose-950/40 border-rose-300 dark:border-rose-800 text-rose-900 dark:text-rose-200'
            }`;

            resultBanner.innerHTML = `
                <div class="flex items-center gap-3.5">
                    <div class="w-10 h-10 rounded-xl flex items-center justify-center text-white ${isCorrect ? 'bg-emerald-600' : 'bg-rose-600'}">
                        <i data-lucide="${isCorrect ? 'check-circle-2' : 'x-circle'}" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <div class="font-extrabold text-lg flex items-center gap-2">
                            <span>${isCorrect ? '正解です！お見事！' : '不正解…復習しましょう'}</span>
                            <span class="text-xs px-2 py-0.5 rounded-full font-bold ${isCorrect ? 'bg-emerald-200 dark:bg-emerald-800 text-emerald-800 dark:text-emerald-100' : 'bg-rose-200 dark:bg-rose-800 text-rose-800 dark:text-rose-100'}">
                                正解肢: [ 肢 ${q.answer} ]
                            </span>
                        </div>
                        <div class="text-xs opacity-80 mt-0.5">あなたの選択: 肢 ${selected}</div>
                    </div>
                </div>
            `;

            // Render 4 Detailed Explanation Cards
            explanationCards.innerHTML = '';
            q.options.forEach((opt) => {
                const card = document.createElement('div');
                const isThisOptionCorrect = opt.num === q.answer;
                card.className = `rounded-xl border p-4 sm:p-5 transition space-y-3.5 ${
                    isThisOptionCorrect 
                    ? 'border-emerald-300 dark:border-emerald-800 bg-emerald-50/30 dark:bg-emerald-950/20' 
                    : 'border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50'
                }`;

                // Header Line: Status + Option Text
                const headerLine = `
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded-md text-xs font-bold ${
                                opt.status === '正' 
                                ? 'bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200' 
                                : 'bg-rose-100 dark:bg-rose-900/60 text-rose-800 dark:text-rose-200'
                            }">
                                肢 ${opt.num} : 【${opt.status === '正' ? '⭕ 正しい' : '❌ 誤り'}】
                            </span>
                            ${isThisOptionCorrect ? '<span class="text-[11px] font-bold text-emerald-600 bg-emerald-100/70 px-2 py-0.5 rounded">正解肢</span>' : ''}
                        </div>
                        <div class="text-xs text-slate-400 font-mono">${opt.statute}</div>
                    </div>
                `;

                // Core Highlight & Contrast (誤り文章の可視化！)
                let highlightSection = '';
                if (opt.status === '誤' && opt.trap_phrase) {
                    // Generate highlighted text
                    const highlightedOptionText = opt.text.replace(
                        opt.trap_phrase, 
                        `<mark class="bg-rose-200 text-rose-900 dark:bg-rose-900/80 dark:text-rose-100 line-through decoration-rose-600 decoration-2 font-bold px-1.5 py-0.5 rounded">${opt.trap_phrase}</mark>`
                    );

                    highlightSection = `
                        <!-- Option Text with Inline Strikethrough Trap -->
                        <div class="p-3 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs sm:text-sm leading-relaxed">
                            <span class="text-slate-400 font-bold mr-1">設問の文:</span>
                            ${highlightedOptionText}
                        </div>

                        <!-- VS Card: Trap vs Correct rule -->
                        <div class="rounded-xl border border-rose-200 dark:border-rose-900/50 bg-rose-50/60 dark:bg-rose-950/20 p-3.5 space-y-2">
                            <div class="text-[11px] font-bold text-rose-800 dark:text-rose-300 uppercase tracking-wider flex items-center gap-1.5">
                                <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-rose-600"></i>
                                <span>誤りの急所（ここがトラップ！）</span>
                            </div>
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                                <div class="bg-white dark:bg-slate-900 p-2.5 rounded-lg border border-rose-100 dark:border-rose-900/30">
                                    <div class="font-bold text-rose-600 dark:text-rose-400 mb-0.5">❌ 問題の記述</div>
                                    <div class="text-slate-700 dark:text-slate-300 font-medium">${opt.trap_phrase}</div>
                                </div>
                                <div class="bg-white dark:bg-slate-900 p-2.5 rounded-lg border border-emerald-100 dark:border-emerald-900/30">
                                    <div class="font-bold text-emerald-600 dark:text-emerald-400 mb-0.5">⭕ 正しい規定</div>
                                    <div class="text-slate-800 dark:text-slate-200 font-bold">${opt.correct_phrase}</div>
                                </div>
                            </div>
                        </div>
                    `;
                }

                // General Explanation Text
                const explanationText = `
                    <div class="text-xs sm:text-sm text-slate-800 dark:text-slate-200 leading-relaxed font-medium">
                        ${opt.explanation}
                    </div>
                `;

                // Statute Quotation Box
                const statuteBox = `
                    <div class="bg-slate-100/80 dark:bg-slate-800/60 rounded-lg p-3 text-xs text-slate-600 dark:text-slate-300 space-y-1 border border-slate-200 dark:border-slate-700">
                        <div class="font-bold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                            <i data-lucide="scroll" class="w-3.5 h-3.5 text-indigo-500"></i>
                            <span>条文根拠: ${opt.statute}</span>
                        </div>
                        <div class="italic text-[11px] leading-relaxed pl-4 border-l-2 border-indigo-400 text-slate-700 dark:text-slate-300">${opt.quote}</div>
                    </div>
                `;

                // Examiner's Key Point
                const pointBox = `
                    <div class="text-[11px] text-indigo-700 dark:text-indigo-300 bg-indigo-50 dark:bg-indigo-950/40 px-3 py-1.5 rounded-lg flex items-center gap-1.5 border border-indigo-100 dark:border-indigo-900">
                        <i data-lucide="check" class="w-3.5 h-3.5 text-indigo-500 shrink-0"></i>
                        <span><strong>合格のツボ:</strong> ${opt.key_point}</span>
                    </div>
                `;

                card.innerHTML = headerLine + highlightSection + explanationText + statuteBox + pointBox;
                explanationCards.appendChild(card);
            });

            // Re-render options to show checkmarks
            renderOptions();
        }

        // Retry Question
        retryBtn.addEventListener('click', () => {
            delete userAnswers[currentIdx];
            loadQuestion(currentIdx);
        });

        // Navigation
        prevBtn.addEventListener('click', () => {
            if (currentIdx > 0) loadQuestion(currentIdx - 1);
        });
        nextBtn.addEventListener('click', () => {
            if (currentIdx < QUESTIONS.length - 1) {
                loadQuestion(currentIdx + 1);
            } else {
                alert(`全10問の演習が完了しました！\\n正解数: ${getCorrectCount()} / 10問 (正解率 ${getCorrectCount() * 10}%)`);
            }
        });

        // Stats calculation
        function getCorrectCount() {
            let correct = 0;
            QUESTIONS.forEach((q, idx) => {
                if (userAnswers[idx] === q.answer) correct++;
            });
            return correct;
        }

        function updateStats() {
            const answered = Object.keys(userAnswers).length;
            const correct = getCorrectCount();
            answeredCountEl.innerText = answered;
            correctCountEl.innerText = correct;
        }

        // Run
        init();
    </script>
</body>
</html>
"""

def main():
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    questions_json_str = json.dumps(QUESTIONS_DATA, ensure_ascii=False, indent=2)
    html_content = HTML_TEMPLATE.replace("%QUESTIONS_JSON%", questions_json_str)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Successfully generated UI prototype app at: {OUTPUT_HTML}")
    print(f"File size: {os.path.getsize(OUTPUT_HTML)} bytes")

if __name__ == "__main__":
    main()
