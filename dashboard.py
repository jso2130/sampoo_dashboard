import streamlit as st
import pandas as pd

st.set_page_config(page_title="샴푸 대시보드", layout="wide")

st.markdown("""
<style>
[data-baseweb="tag"] { background-color: #888888 !important; }
[data-baseweb="tag"] span { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ─── 사이드바 메뉴 ────────────────────────────────────────────────────────────
page = st.sidebar.radio("메뉴", ["🧴  Dashboard", "📋  Guidelines"], label_visibility="collapsed")

# ════════════════════════════════════════════════════════════════════════════════
# 공통 데이터
# ════════════════════════════════════════════════════════════════════════════════
SURFACTANTS = [
    'Dehyton ML', 'Dehyton MC', 'Dehyton PK 45', 'Dehyton AB 30',
    'Texapon SB 3 KC', 'Plantapon ACG 50', 'Plantapon LC 7',
    'Plantapon Amino SCG-L', 'Plantapon Amino KG-L',
    'Plantacare 818', 'Plantacare 2000', 'Dehyquart A-CA',
]
POLYMERS   = ['Salcare Super 7', 'Dehyquart CC6', 'Dehyquart CC7 Benz', 'Luviquat Excellence']
THICKENERS = ['Arlypon TT', 'Arlypon F']

SURF_CHEM = {
    'Dehyton ML':            {'quat': 0.000, 'sulfo': 0.000, 'carb': 0.030, 'acetal': 0.000, 'c0': 0.80, 'cneg': 0.15, 'cpos': 0.05},
    'Dehyton MC':            {'quat': 0.000, 'sulfo': 0.000, 'carb': 0.010, 'acetal': 0.000, 'c0': 0.82, 'cneg': 0.12, 'cpos': 0.06},
    'Dehyton PK 45':         {'quat': 0.000, 'sulfo': 0.020, 'carb': 0.000, 'acetal': 0.000, 'c0': 0.75, 'cneg': 0.15, 'cpos': 0.10},
    'Dehyton AB 30':         {'quat': 0.000, 'sulfo': 0.000, 'carb': 0.020, 'acetal': 0.000, 'c0': 0.78, 'cneg': 0.13, 'cpos': 0.09},
    'Texapon SB 3 KC':       {'quat': 0.000, 'sulfo': 0.050, 'carb': 0.000, 'acetal': 0.000, 'c0': 0.65, 'cneg': 0.30, 'cpos': 0.05},
    'Plantapon ACG 50':      {'quat': 0.000, 'sulfo': 0.000, 'carb': 0.040, 'acetal': 0.000, 'c0': 0.60, 'cneg': 0.35, 'cpos': 0.05},
    'Plantapon LC 7':        {'quat': 0.000, 'sulfo': 0.000, 'carb': 0.000, 'acetal': 0.080, 'c0': 0.90, 'cneg': 0.05, 'cpos': 0.05},
    'Plantapon Amino SCG-L': {'quat': 0.000, 'sulfo': 0.000, 'carb': 0.060, 'acetal': 0.000, 'c0': 0.55, 'cneg': 0.40, 'cpos': 0.05},
    'Plantapon Amino KG-L':  {'quat': 0.000, 'sulfo': 0.000, 'carb': 0.060, 'acetal': 0.000, 'c0': 0.55, 'cneg': 0.40, 'cpos': 0.05},
    'Plantacare 818':        {'quat': 0.000, 'sulfo': 0.000, 'carb': 0.000, 'acetal': 0.100, 'c0': 0.92, 'cneg': 0.04, 'cpos': 0.04},
    'Plantacare 2000':       {'quat': 0.000, 'sulfo': 0.000, 'carb': 0.000, 'acetal': 0.100, 'c0': 0.92, 'cneg': 0.04, 'cpos': 0.04},
    'Dehyquart A-CA':        {'quat': 0.080, 'sulfo': 0.000, 'carb': 0.000, 'acetal': 0.000, 'c0': 0.40, 'cneg': 0.05, 'cpos': 0.55},
}

RECS = {
    'Dehyton ML': [
        {'combo': ('Dehyton ML', 'Texapon SB 3 KC'),
         'surf':  {'Dehyton ML': (3.0, 12.0), 'Texapon SB 3 KC': (5.0, 18.0)},
         'poly':  {'Salcare Super 7': (0.5, 1.5), 'Dehyquart CC6': (1.0, 2.5)},
         'thick': {'Arlypon TT': (1.0, 2.5), 'Arlypon F': (0.5, 2.0)}},
        {'combo': ('Dehyton ML', 'Plantacare 2000'),
         'surf':  {'Dehyton ML': (5.0, 15.0), 'Plantacare 2000': (3.0, 10.0)},
         'poly':  {'Salcare Super 7': (0.5, 1.5)},
         'thick': {'Arlypon TT': (1.0, 3.0)}},
        {'combo': ('Plantapon Amino SCG-L', 'Dehyton ML'),
         'surf':  {'Plantapon Amino SCG-L': (5.0, 15.0), 'Dehyton ML': (3.0, 10.0)},
         'poly':  {'Salcare Super 7': (0.5, 1.5)},
         'thick': {'Arlypon TT': (1.0, 2.5)}},
    ],
    'Dehyton MC': [
        {'combo': ('Dehyton MC', 'Texapon SB 3 KC'),
         'surf':  {'Dehyton MC': (2.0, 8.0), 'Texapon SB 3 KC': (8.0, 20.0)},
         'poly':  {'Dehyquart CC6': (0.5, 2.0)},
         'thick': {'Arlypon TT': (1.0, 2.5)}},
    ],
    'Dehyton PK 45': [
        {'combo': ('Dehyton PK 45', 'Plantapon LC 7'),
         'surf':  {'Dehyton PK 45': (3.0, 10.0), 'Plantapon LC 7': (5.0, 15.0)},
         'poly':  {'Luviquat Excellence': (0.5, 1.5)},
         'thick': {'Arlypon TT': (0.5, 2.0)}},
    ],
    'Dehyton AB 30': [
        {'combo': ('Dehyton AB 30', 'Texapon SB 3 KC'),
         'surf':  {'Dehyton AB 30': (3.0, 10.0), 'Texapon SB 3 KC': (5.0, 18.0)},
         'poly':  {'Salcare Super 7': (0.5, 1.5)},
         'thick': {'Arlypon F': (0.5, 2.0)}},
    ],
    'Texapon SB 3 KC': [
        {'combo': ('Dehyton ML', 'Texapon SB 3 KC'),
         'surf':  {'Dehyton ML': (3.0, 12.0), 'Texapon SB 3 KC': (5.0, 18.0)},
         'poly':  {'Salcare Super 7': (0.5, 1.5), 'Dehyquart CC6': (1.0, 2.5)},
         'thick': {'Arlypon TT': (1.0, 2.5), 'Arlypon F': (0.5, 2.0)}},
        {'combo': ('Dehyton MC', 'Texapon SB 3 KC'),
         'surf':  {'Dehyton MC': (2.0, 8.0), 'Texapon SB 3 KC': (8.0, 20.0)},
         'poly':  {'Dehyquart CC6': (0.5, 2.0)},
         'thick': {'Arlypon TT': (1.0, 2.5)}},
        {'combo': ('Dehyton AB 30', 'Texapon SB 3 KC'),
         'surf':  {'Dehyton AB 30': (3.0, 10.0), 'Texapon SB 3 KC': (5.0, 18.0)},
         'poly':  {'Salcare Super 7': (0.5, 1.5)},
         'thick': {'Arlypon F': (0.5, 2.0)}},
        {'combo': ('Dehyquart A-CA', 'Texapon SB 3 KC'),
         'surf':  {'Dehyquart A-CA': (1.0, 5.0), 'Texapon SB 3 KC': (5.0, 18.0)},
         'poly':  {'Dehyquart CC6': (0.5, 2.0), 'Luviquat Excellence': (0.5, 1.5)},
         'thick': {'Arlypon TT': (1.0, 2.5)}},
    ],
    'Plantapon ACG 50': [
        {'combo': ('Plantapon ACG 50', 'Plantacare 818'),
         'surf':  {'Plantapon ACG 50': (5.0, 15.0), 'Plantacare 818': (3.0, 10.0)},
         'poly':  {'Salcare Super 7': (0.5, 1.0)},
         'thick': {'Arlypon TT': (1.0, 2.0)}},
    ],
    'Plantapon LC 7': [
        {'combo': ('Dehyton PK 45', 'Plantapon LC 7'),
         'surf':  {'Dehyton PK 45': (3.0, 10.0), 'Plantapon LC 7': (5.0, 15.0)},
         'poly':  {'Luviquat Excellence': (0.5, 1.5)},
         'thick': {'Arlypon TT': (0.5, 2.0)}},
        {'combo': ('Plantapon LC 7', 'Plantacare 2000'),
         'surf':  {'Plantapon LC 7': (5.0, 15.0), 'Plantacare 2000': (3.0, 10.0)},
         'poly':  {'Dehyquart CC7 Benz': (0.5, 1.5)},
         'thick': {'Arlypon F': (0.5, 1.5)}},
    ],
    'Plantapon Amino SCG-L': [
        {'combo': ('Plantapon Amino SCG-L', 'Dehyton ML'),
         'surf':  {'Plantapon Amino SCG-L': (5.0, 15.0), 'Dehyton ML': (3.0, 10.0)},
         'poly':  {'Salcare Super 7': (0.5, 1.5)},
         'thick': {'Arlypon TT': (1.0, 2.5)}},
    ],
    'Plantapon Amino KG-L': [
        {'combo': ('Plantapon Amino KG-L', 'Plantacare 818'),
         'surf':  {'Plantapon Amino KG-L': (5.0, 15.0), 'Plantacare 818': (3.0, 10.0)},
         'poly':  {'Dehyquart CC6': (0.5, 2.0)},
         'thick': {'Arlypon TT': (0.5, 2.0)}},
    ],
    'Plantacare 818': [
        {'combo': ('Plantapon ACG 50', 'Plantacare 818'),
         'surf':  {'Plantapon ACG 50': (5.0, 15.0), 'Plantacare 818': (3.0, 10.0)},
         'poly':  {'Salcare Super 7': (0.5, 1.0)},
         'thick': {'Arlypon TT': (1.0, 2.0)}},
        {'combo': ('Plantapon Amino KG-L', 'Plantacare 818'),
         'surf':  {'Plantapon Amino KG-L': (5.0, 15.0), 'Plantacare 818': (3.0, 10.0)},
         'poly':  {'Dehyquart CC6': (0.5, 2.0)},
         'thick': {'Arlypon TT': (0.5, 2.0)}},
    ],
    'Plantacare 2000': [
        {'combo': ('Dehyton ML', 'Plantacare 2000'),
         'surf':  {'Dehyton ML': (5.0, 15.0), 'Plantacare 2000': (3.0, 10.0)},
         'poly':  {'Salcare Super 7': (0.5, 1.5)},
         'thick': {'Arlypon TT': (1.0, 3.0)}},
        {'combo': ('Plantapon LC 7', 'Plantacare 2000'),
         'surf':  {'Plantapon LC 7': (5.0, 15.0), 'Plantacare 2000': (3.0, 10.0)},
         'poly':  {'Dehyquart CC7 Benz': (0.5, 1.5)},
         'thick': {'Arlypon F': (0.5, 1.5)}},
    ],
    'Dehyquart A-CA': [
        {'combo': ('Dehyquart A-CA', 'Texapon SB 3 KC'),
         'surf':  {'Dehyquart A-CA': (1.0, 5.0), 'Texapon SB 3 KC': (5.0, 18.0)},
         'poly':  {'Dehyquart CC6': (0.5, 2.0), 'Luviquat Excellence': (0.5, 1.5)},
         'thick': {'Arlypon TT': (1.0, 2.5)}},
    ],
}

# ════════════════════════════════════════════════════════════════════════════════
# Dashboard 페이지
# ════════════════════════════════════════════════════════════════════════════════
if "Dashboard" in page:

    def get_recs_for(surf):
        seen, result = set(), []
        for recs in RECS.values():
            for rec in recs:
                key = rec['combo']
                if surf in rec['surf'] and key not in seen:
                    seen.add(key)
                    result.append(rec)
        return result

    def show_rec(rec, idx, selected_surf):
        other_surfs = {k: v for k, v in rec['surf'].items() if k != selected_surf}
        lines = [f"**추천 조합 {idx}**"]
        lines.append(f"{selected_surf} = {rec['surf'][selected_surf][0]}-{rec['surf'][selected_surf][1]}%")
        for k, v in other_surfs.items():
            lines.append(f"{k} = {v[0]}-{v[1]}%")
        for k, v in rec['poly'].items():
            lines.append(f"{k} = {v[0]}-{v[1]}%")
        for k, v in rec['thick'].items():
            lines.append(f"{k} = {v[0]}-{v[1]}%")
        st.markdown("  \n".join(lines))

    def build_features(s1, v1, s2, v2, poly, poly_v, thick, thick_v):
        arlypon_tt = thick_v if thick == 'Arlypon TT' else 0.0
        arlypon_f  = thick_v if thick == 'Arlypon F'  else 0.0
        luviquat   = poly_v  if poly  == 'Luviquat Excellence' else 0.0
        cc6        = poly_v  if poly  == 'Dehyquart CC6'       else 0.0
        cc7        = poly_v  if poly  == 'Dehyquart CC7 Benz'  else 0.0
        salcare    = poly_v  if poly  == 'Salcare Super 7'     else 0.0
        quat_d = sulfo_d = carb_d = acetal_d = 0.0
        c0_sum = cneg_sum = cpos_sum = 0.0
        for surf, conc in [(s1, v1), (s2, v2)]:
            if surf and conc > 0:
                f = SURF_CHEM.get(surf, {})
                quat_d   += f.get('quat',  0) * conc
                sulfo_d  += f.get('sulfo', 0) * conc
                carb_d   += f.get('carb',  0) * conc
                acetal_d += f.get('acetal',0) * conc
                c0_sum   += f.get('c0',  0.8) * conc
                cneg_sum += f.get('cneg',0.1) * conc
                cpos_sum += f.get('cpos',0.1) * conc
        total_c = c0_sum + cneg_sum + cpos_sum + 1e-5
        return {
            'Arlypon TT': arlypon_tt, 'Arlypon F': arlypon_f,
            'Luviquat Excellence': luviquat, 'Dehyquart CC6': cc6,
            'Dehyquart CC7 Benz': cc7, 'Salcare Super 7': salcare,
            'quat_d': quat_d, 'sulfo_d': sulfo_d, 'carb_d': carb_d, 'acetal_d': acetal_d,
            'C_0_Ratio': c0_sum / total_c,
            'C_neg_Total_Ratio': cneg_sum / total_c,
            'C_pos_Total_Ratio': cpos_sum / total_c,
        }

    def predict_viscosity(f):
        score = (f['Arlypon TT'] * 1.20 + f['Arlypon F'] * 1.00 +
                 f['Salcare Super 7'] * 0.60 + f['Luviquat Excellence'] * 0.45 +
                 f['Dehyquart CC6'] * 0.40 + f['Dehyquart CC7 Benz'] * 0.40 +
                 f['carb_d'] * 0.50)
        return '높음 / 보통' if score >= 1.5 else '매우 낮음'

    def predict_turbidity(f):
        clarity = (f['acetal_d'] * 2.50 + f['Salcare Super 7'] * 0.80 +
                   f['quat_d'] * 1.20 - f['carb_d'] * 1.80 -
                   f['C_neg_Total_Ratio'] * 1.50 + f['C_pos_Total_Ratio'] * 0.80)
        return '맑음' if clarity >= 0.15 else '탁함'

    if 'visc_pred' not in st.session_state:
        st.session_state['visc_pred'] = None
        st.session_state['turb_pred'] = None

    st.markdown(
        "<h1 style='text-align: center;'>🫧 배합비 기반 샴푸 물성 예측 대시보드</h1>",
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown(
        "<p style='font-size: 16px; font-weight: 600; margin-bottom: 4px;'>성분별 배합비를 입력해주세요</p>"
        "<p style='color: #888888; font-size: 13px; margin-bottom: 20px;'>계면활성제 (8~13 W/W%) → 폴리머 (1~3 W/W%) → 증점제 (1~5 W/W%)</p>",
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        sel1 = st.multiselect("계면활성제 1", SURFACTANTS, max_selections=1)
        val1 = st.number_input("배합비 (%)", min_value=0.0, max_value=100.0, step=0.1,
                               disabled=not sel1, key="v1", label_visibility="collapsed")
    with c2:
        exclude1 = sel1 if sel1 else []
        sel2 = st.multiselect("계면활성제 2", [s for s in SURFACTANTS if s not in exclude1], max_selections=1)
        val2 = st.number_input("배합비 (%)", min_value=0.0, max_value=100.0, step=0.1,
                               disabled=not sel2, key="v2", label_visibility="collapsed")
    with c3:
        sel3 = st.multiselect("폴리머", POLYMERS, max_selections=1)
        val3 = st.number_input("배합비 (%)", min_value=0.0, max_value=100.0, step=0.1,
                               disabled=not sel3, key="v3", label_visibility="collapsed")
    with c4:
        sel4 = st.multiselect("증점제", THICKENERS, max_selections=1)
        val4 = st.number_input("배합비 (%)", min_value=0.0, max_value=100.0, step=0.1,
                               disabled=not sel4, key="v4", label_visibility="collapsed")

    if sel1:
        recs = get_recs_for(sel1[0])
        if recs:
            rec_cols = st.columns(len(recs))
            for col, (i, rec) in zip(rec_cols, enumerate(recs, 1)):
                with col:
                    show_rec(rec, i, sel1[0])

    can_predict = bool(sel1 and val1 > 0 and sel4 and val4 > 0)
    _, btn_col = st.columns([5, 1])
    with btn_col:
        if st.button("예측하기", disabled=not can_predict, use_container_width=True,
                     help="성분 선택 후 배합비를 입력하면 활성화됩니다."):
            f = build_features(
                sel1[0] if sel1 else None, val1,
                sel2[0] if sel2 else None, val2,
                sel3[0] if sel3 else None, val3,
                sel4[0] if sel4 else None, val4,
            )
            st.session_state['visc_pred'] = predict_viscosity(f)
            st.session_state['turb_pred'] = predict_turbidity(f)

    st.divider()

    visc_label = st.session_state['visc_pred'] or "-"
    turb_label = st.session_state['turb_pred'] or "-"
    left, right = st.columns(2)
    with left:
        st.markdown(
            f"<div style='border:2px solid #ccc;border-radius:12px;padding:32px;text-align:center;'>"
            f"<p style='font-size:20px;font-weight:600;margin-bottom:12px;'>점도 등급</p>"
            f"<p style='font-size:60px;font-weight:bold;margin:0;'>{visc_label}</p></div>",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"<div style='border:2px solid #ccc;border-radius:12px;padding:32px;text-align:center;'>"
            f"<p style='font-size:20px;font-weight:600;margin-bottom:12px;'>탁도 등급</p>"
            f"<p style='font-size:60px;font-weight:bold;margin:0;'>{turb_label}</p></div>",
            unsafe_allow_html=True,
        )

# ════════════════════════════════════════════════════════════════════════════════
# Guidelines 페이지
# ════════════════════════════════════════════════════════════════════════════════
else:
    st.markdown(
        "<h1 style='text-align:center;margin-bottom:48px;'>🫧 배합비 가이드라인</h1>"
        "<p style='margin-bottom:4px;'>데이터 검증으로 완성된 제형: 안정성과 목표 물성을 모두 잡은 성분별 최적 범위</p>"
        "<p style='color:#888888;font-size:13px;margin-bottom:16px;'>• 목표 물성 : 점도 중간/높음 등급 (100~5000cP), 탁도 맑음 등급 (100NTU 이하)</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    seen = set()
    surf_rows, poly_rows, thick_rows = [], [], []
    for recs in RECS.values():
        for rec in recs:
            key = rec['combo']
            if key in seen:
                continue
            seen.add(key)
            s1, s2 = key
            combo_str = f"{s1} + {s2}"
            surf_rows.append({
                '계면활성제 1': s1,
                '배합비 1 (W/W%)': f"{rec['surf'][s1][0]} ~ {rec['surf'][s1][1]}",
                '계면활성제 2': s2,
                '배합비 2 (W/W%)': f"{rec['surf'][s2][0]} ~ {rec['surf'][s2][1]}",
            })
            for poly, (lo, hi) in rec['poly'].items():
                poly_rows.append({'계면활성제 조합': combo_str, '폴리머': poly, '배합비 (W/W%)': f"{lo} ~ {hi}"})
            for thick, (lo, hi) in rec['thick'].items():
                thick_rows.append({'계면활성제 조합': combo_str, '증점제': thick, '배합비 (W/W%)': f"{lo} ~ {hi}"})

    st.subheader("계면활성제 조합 및 배합비")
    st.dataframe(pd.DataFrame(surf_rows), use_container_width=True, hide_index=True)
    st.divider()
    st.subheader("폴리머 종류 및 배합비")
    st.dataframe(pd.DataFrame(poly_rows), use_container_width=True, hide_index=True)
    st.divider()
    st.subheader("증점제 종류 및 배합비")
    st.dataframe(pd.DataFrame(thick_rows), use_container_width=True, hide_index=True)
