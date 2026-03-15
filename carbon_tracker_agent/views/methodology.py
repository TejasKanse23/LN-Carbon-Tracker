import streamlit as st
from utils.theme import inject_custom_css, page_header, section_header, insight_card

def show():
    inject_custom_css()
    page_header("📖", "Assessment Methodology",
                "Transparency on how carbon emissions are calculated within this prototype.")

    # ── Disclaimer ─────────────────────────────────────────────
    st.markdown("""
    <div style="background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.25);
                border-left:3px solid #3b82f6;border-radius:10px;
                padding:1rem 1.25rem;margin-bottom:1.75rem;">
        <div style="font-weight:700;color:#93c5fd;font-size:0.85rem;margin-bottom:0.35rem;">
            ℹ️ Prototype Disclaimer
        </div>
        <div style="color:#94a3b8;font-size:0.88rem;line-height:1.6;">
            The emission factors and formulas used here are simplified estimates designed for
            demonstration purposes. They do not replace certified carbon accounting frameworks
            such as <strong style="color:#f1f5f9;">GLEC</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Core Formula ────────────────────────────────────────────
    section_header("⚗️ Core Emission Formula")

    st.latex(r"E = D \times W \times EF \times UF \times FF")

    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:0.5rem;margin:1.25rem 0 1.75rem;">
    """ + "".join([
        f"""<div style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.15);
                       border-radius:10px;padding:0.85rem;text-align:center;">
                <div style="font-size:1.5rem;font-weight:800;color:#10b981;margin-bottom:0.25rem;">{sym}</div>
                <div style="font-size:0.72rem;font-weight:700;color:#94a3b8;text-transform:uppercase;
                            letter-spacing:0.05em;">{name}</div>
            </div>"""
        for sym, name in [
            ("E", "Emissions (kg CO₂e)"),
            ("D", "Distance (km)"),
            ("W", "Weight (t)"),
            ("EF", "Emission Factor"),
            ("UF · FF", "Penalty Factors"),
        ]
    ]) + """
    </div>
    """, unsafe_allow_html=True)

    # ── Factor Tables ───────────────────────────────────────────
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        section_header("🚛 Vehicle Base Factors (EF)")
        for truck, factor, note in [
            ("Heavy Truck",  "0.08 kg CO₂/t-km", "18t–20t payload"),
            ("Medium Truck", "0.12 kg CO₂/t-km", "15t–17t payload"),
            ("Light Truck",  "0.18 kg CO₂/t-km", "< 15t payload"),
        ]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.6rem 0.9rem;margin-bottom:0.45rem;
                        background:rgba(255,255,255,0.03);border-radius:8px;
                        border:1px solid rgba(255,255,255,0.06);">
                <div>
                    <div style="font-weight:600;font-size:0.85rem;color:#f1f5f9;">{truck}</div>
                    <div style="font-size:0.72rem;color:#64748b;">{note}</div>
                </div>
                <div style="font-weight:700;color:#10b981;font-size:0.9rem;">{factor}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        section_header("⛽ Fuel Adjustments (FF)")
        for fuel, factor, note in [
            ("Diesel", "1.0× (Base)",   "Standard reference"),
            ("CNG",    "0.85× (−15%)",  "Lower carbon content"),
            ("EV",     "0.10× (−90%)", "Tailpipe zero emission"),
        ]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.6rem 0.9rem;margin-bottom:0.45rem;
                        background:rgba(255,255,255,0.03);border-radius:8px;
                        border:1px solid rgba(255,255,255,0.06);">
                <div>
                    <div style="font-weight:600;font-size:0.85rem;color:#f1f5f9;">{fuel}</div>
                    <div style="font-size:0.72rem;color:#64748b;">{note}</div>
                </div>
                <div style="font-weight:700;color:#06d6a0;font-size:0.9rem;">{factor}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        section_header("📦 Utilization Penalties (UF)")
        st.markdown("""
        <div style="font-size:0.82rem;color:#94a3b8;margin-bottom:0.75rem;line-height:1.5;">
            Low utilization means burning fuel for empty space. We penalize shipments based on load fill rate:
        </div>
        """, unsafe_allow_html=True)
        for label, penalty, icon, color in [
            ("≥ 80% Utilization",   "1.0× — Optimal",      "✅", "#10b981"),
            ("50–79% Utilization",  "1.05× — Moderate",    "⚠️", "#f59e0b"),
            ("< 50% Utilization",   "1.2× — Inefficient",  "🚨", "#ef4444"),
        ]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.6rem 0.9rem;margin-bottom:0.45rem;
                        background:rgba(255,255,255,0.03);border-radius:8px;
                        border:1px solid rgba(255,255,255,0.06);">
                <div style="display:flex;align-items:center;gap:0.5rem;">
                    <span>{icon}</span>
                    <span style="font-weight:600;font-size:0.85rem;color:#f1f5f9;">{label}</span>
                </div>
                <div style="font-weight:700;color:{color};font-size:0.9rem;">{penalty}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── AI Section ──────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    section_header("🤖 Generative AI Assistant")

    st.markdown("""
    <div style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.18);
                border-radius:12px;padding:1.25rem 1.5rem;line-height:1.7;font-size:0.9rem;color:#94a3b8;">
        The AI assistant is powered by
        <strong style="color:#10b981;">Google Gemini 1.5 Flash</strong>.
        Every query builds a <strong style="color:#f1f5f9;">data context payload</strong> containing:
        <ol style="margin:0.75rem 0 0 1rem;padding:0;color:#94a3b8;">
            <li style="margin-bottom:0.35rem;">Overall KPIs and totals</li>
            <li style="margin-bottom:0.35rem;">Lane rankings and hotspot classifications</li>
            <li>The emission formula above</li>
        </ol>
        <div style="margin-top:0.9rem;color:#64748b;font-size:0.82rem;">
            Gemini uses this explicit context to deliver grounded, quantitative, and relevant answers
            rather than generic advice.
        </div>
    </div>
    """, unsafe_allow_html=True)
