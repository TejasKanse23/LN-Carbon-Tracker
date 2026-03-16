import streamlit as st
import os
import pandas as pd
from io import BytesIO

import matplotlib
matplotlib.use("Agg")   # headless — no GUI window
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image as RLImage,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ── colour palette (module-level constants) ────────────────────────────────
C_GREEN  = colors.HexColor("#10b981")
C_BLUE   = colors.HexColor("#1e40af")
C_PURPLE = colors.HexColor("#6d28d9")
C_RED    = colors.HexColor("#dc2626")
C_AMBER  = colors.HexColor("#d97706")
C_SLATE  = colors.HexColor("#0f172a")
C_LIGHT  = colors.HexColor("#f1f5f9")
C_MUTED  = colors.HexColor("#64748b")
WHITE    = colors.white
BLACK    = colors.HexColor("#1e293b")

# ── module-level paragraph styles (created once, never recreated) ──────────
def _ps(name, **kw):
    from reportlab.lib.styles import getSampleStyleSheet
    base = getSampleStyleSheet()["Normal"]
    d = dict(parent=base, fontName="Helvetica", fontSize=10,
             textColor=BLACK, leading=14)
    d.update(kw)
    return ParagraphStyle(name, **d)

_PDF_STYLES = {
    "TITLE":   _ps("rg_TITLE",   fontSize=22, fontName="Helvetica-Bold",
                   textColor=WHITE,  alignment=TA_CENTER, spaceAfter=2, leading=28),
    "SUBT":    _ps("rg_SUBT",    fontSize=12, fontName="Helvetica",
                   textColor=colors.HexColor("#a7f3d0"), alignment=TA_CENTER,
                   spaceAfter=0, leading=16),
    "SUBT2":   _ps("rg_SUBT2",   fontSize=9,
                   textColor=colors.HexColor("#94a3b8"), alignment=TA_CENTER,
                   spaceAfter=0),
    "SEC_H":   _ps("rg_SEC_H",   fontSize=11, fontName="Helvetica-Bold",
                   textColor=WHITE, spaceBefore=0, spaceAfter=0, leading=14),
    "BULLET":  _ps("rg_BULLET",  fontSize=9, spaceAfter=5, leading=14,
                   leftIndent=14),
    "INFO_BG": _ps("rg_INFO_BG", fontSize=9,
                   textColor=colors.HexColor("#065f46"),
                   backColor=colors.HexColor("#d1fae5"),
                   borderPad=8, leading=14, spaceAfter=0),
    "FOOT":    _ps("rg_FOOT",    fontSize=7.5, textColor=C_MUTED,
                   alignment=TA_CENTER, spaceBefore=6),
}


# ── data analysis ──────────────────────────────────────────────────────────
def analyze_lane(origin: str, dest: str, data_path: str):
    df = pd.read_csv(data_path)
    lane_df = df[
        (df["origin"].str.lower() == origin.lower()) &
        (df["destination"].str.lower() == dest.lower())
    ]
    if lane_df.empty:
        return None

    network_avg = float(df["estimated_emissions_kg_co2e"].mean())
    n     = int(len(lane_df))
    dist  = float(lane_df["distance_km"].sum())
    freq  = float(lane_df["weight_ton"].sum())
    util  = float(lane_df["utilization_percent"].mean())
    age   = float(lane_df["Age of vehicle"].mean()) if "Age of vehicle" in lane_df.columns else 0.0
    vehs  = lane_df["vehicle_type"].value_counts().head(3).index.tolist()

    total_em = float(lane_df["estimated_emissions_kg_co2e"].sum())
    avg_em   = total_em / n if n > 0 else 0.0
    intensity = total_em / (dist * freq / n) if freq > 0 else 0.0

    congestion_frac = float(
        (lane_df.get("traffic congestion", pd.Series(["Low"])).str.lower() == "high").mean()
    )
    diesel_pct = float((lane_df["fuel_type"].str.lower() == "diesel").mean() * 100)

    drivers = []
    if congestion_frac > 0.3:
        drivers.append(
            f"High traffic congestion on {congestion_frac*100:.0f}% of shipments "
            "significantly reduces fuel efficiency on this lane."
        )
    if age > 6.0:
        drivers.append(
            f"Older vehicle fleet (average age {age:.1f} years) uses more fuel "
            "and generates higher carbon emissions per trip."
        )
    if util < 70.0:
        drivers.append(
            f"Low average load utilisation ({util:.1f}%) means trucks are running "
            "partially empty, driving up carbon per tonne moved."
        )
    if diesel_pct > 50:
        drivers.append(
            f"Heavy dependence on Diesel-powered vehicles ({diesel_pct:.1f}% of "
            "shipments) contributes substantially to carbon output."
        )
    if not drivers:
        drivers.append(
            "Operations on this lane are relatively efficient. "
            "Incremental gains are still achievable through fleet upgrades."
        )

    p80  = float(lane_df["estimated_emissions_kg_co2e"].quantile(0.8))
    high = lane_df[lane_df["estimated_emissions_kg_co2e"] > p80]
    hotspots = []
    if len(high) > 0:
        ineff = high[high["utilization_percent"] < 60]
        if len(ineff) > 0:
            hotspots.append(
                f"{len(ineff)} shipments have both high carbon output and poor "
                "utilisation (below 60%) -- these are the priority targets."
            )
        hotspots.append(
            "The top 20% of shipments by carbon output account for a "
            "disproportionately large share of total lane emissions."
        )
    hotspots.append(
        "Peak congestion windows directly correlate with emission spikes; "
        "scheduling off-peak dispatches would reduce carbon significantly."
    )

    recs = []
    if util < 85:
        recs.append(
            "Consolidate loads to push average utilisation above 85%; "
            "this is the single highest-impact action for this lane."
        )
    if diesel_pct > 30:
        recs.append(
            "Progressively replace Diesel trucks with CNG or EV alternatives "
            "on this lane, starting with the highest-frequency routes."
        )
    if age > 5.0:
        recs.append(
            "Phase out vehicles older than 7 years. Newer-generation engines "
            "emit 15-30% less carbon per km."
        )
    if congestion_frac > 0.2:
        recs.append(
            "Shift departure windows to off-peak hours (before 7am or after 9pm) "
            "to avoid congestion-related idling emissions."
        )
    if not recs:
        recs.append("Maintain current practices. Small gains are addressable via EV transition.")

    potential   = (avg_em - network_avg) * n if avg_em > network_avg else total_em * 0.10
    potential   = max(potential, 0)
    red_pct     = potential / total_em * 100 if total_em > 0 else 0
    impact_msg  = (
        f"Implementing the above recommendations could reduce total lane carbon output by "
        f"approximately {red_pct:.1f}%, saving {potential:,.0f} kg of carbon per cycle."
    )

    return {
        "overview": {
            "lane_name":            f"{origin} to {dest}",
            "total_shipments":      n,
            "total_distance_km":    round(dist, 1),
            "total_freight_tons":   round(freq, 1),
            "avg_utilization":      round(util, 1),
            "avg_vehicle_age":      round(age, 1),
            "common_vehicle_types": vehs,
        },
        "emissions": {
            "total_carbon_kg":          round(total_em, 1),
            "avg_carbon_per_shipment":  round(avg_em, 1),
            "emission_intensity":       round(intensity, 4),
            "network_avg_carbon":       round(network_avg, 1),
            "status_vs_network":        "Above Network Average" if avg_em > network_avg else "Below Network Average",
        },
        "drivers":         drivers,
        "hotspots":        hotspots,
        "recommendations": recs,
        "reduction": {
            "potential_reduction_kg": round(potential, 1),
            "impact_summary":         impact_msg,
        },
        # raw series for charts
        "_raw": {
            "lane_df":       lane_df,
            "network_avg":   network_avg,
            "avg_em":        avg_em,
            "diesel_pct":    diesel_pct,
        },
    }


# ── chart generators (return PNG bytes) ────────────────────────────────────
DARK_BG  = "#0f172a"
MID_BG   = "#1e293b"
GRID_COL = "#334155"
TEXT_COL = "#e2e8f0"

def _chart_carbon_comparison(avg_em: float, network_avg: float) -> BytesIO:
    """Horizontal bar: lane avg vs network avg carbon."""
    fig, ax = plt.subplots(figsize=(7, 2.2), facecolor=DARK_BG)
    ax.set_facecolor(MID_BG)

    labels  = ["Network Average", "This Lane"]
    values  = [network_avg, avg_em]
    colours = ["#3b82f6", "#10b981" if avg_em <= network_avg else "#ef4444"]
    bars    = ax.barh(labels, values, color=colours, height=0.45, edgecolor="none")

    for bar, val in zip(bars, values):
        ax.text(val + max(values)*0.01, bar.get_y() + bar.get_height()/2,
                f"{val:,.0f} kg", va="center", color=TEXT_COL, fontsize=9)

    ax.set_xlabel("Avg Carbon per Shipment (kg)", color=TEXT_COL, fontsize=8)
    ax.tick_params(colors=TEXT_COL, labelsize=8)
    ax.spines[:].set_visible(False)
    ax.xaxis.grid(True, color=GRID_COL, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_title("Lane Carbon vs Network Average", color=TEXT_COL, fontsize=10, pad=8)

    fig.tight_layout(pad=0.8)
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, facecolor=DARK_BG)
    plt.close(fig)
    buf.seek(0)
    return buf


def _chart_fuel_mix(lane_df) -> BytesIO:
    """Donut chart: fuel type breakdown."""
    counts = lane_df["fuel_type"].str.title().value_counts()
    labels = counts.index.tolist()
    sizes  = counts.values.tolist()
    pal    = ["#ef4444","#3b82f6","#10b981","#f59e0b","#8b5cf6","#06b6d4"]
    palette = pal[:len(labels)]

    fig, ax = plt.subplots(figsize=(4.5, 3.2), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, colors=palette,
        autopct="%1.0f%%", startangle=90,
        pctdistance=0.78,
        wedgeprops=dict(width=0.55, edgecolor=DARK_BG, linewidth=1.5),
    )
    for at in autotexts:
        at.set_color(TEXT_COL); at.set_fontsize(8)
    ax.legend(labels, loc="lower center", bbox_to_anchor=(0.5, -0.18),
              ncol=3, fontsize=7.5, frameon=False,
              labelcolor=TEXT_COL, facecolor=DARK_BG)
    ax.set_title("Fuel Type Mix", color=TEXT_COL, fontsize=10, pad=8)

    fig.tight_layout(pad=0.6)
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, facecolor=DARK_BG)
    plt.close(fig)
    buf.seek(0)
    return buf


def _chart_utilisation_dist(lane_df) -> BytesIO:
    """Bar chart: utilisation buckets."""
    bins   = [0, 50, 60, 70, 80, 90, 100]
    labels = ["<50%", "50-60%", "60-70%", "70-80%", "80-90%", "90-100%"]
    counts = pd.cut(lane_df["utilization_percent"], bins=bins, labels=labels,
                    include_lowest=True).value_counts().reindex(labels).fillna(0)

    fig, ax = plt.subplots(figsize=(7, 2.5), facecolor=DARK_BG)
    ax.set_facecolor(MID_BG)

    bar_colours = ["#ef4444","#f59e0b","#f59e0b","#3b82f6","#10b981","#10b981"]
    bars = ax.bar(labels, counts.values, color=bar_colours, edgecolor="none", width=0.6)

    for bar, val in zip(bars, counts.values):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(int(val)), ha="center", color=TEXT_COL, fontsize=8)

    ax.set_ylabel("Shipments", color=TEXT_COL, fontsize=8)
    ax.set_xlabel("Load Utilisation Bucket", color=TEXT_COL, fontsize=8)
    ax.tick_params(colors=TEXT_COL, labelsize=8)
    ax.spines[:].set_visible(False)
    ax.yaxis.grid(True, color=GRID_COL, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_title("Load Utilisation Distribution", color=TEXT_COL, fontsize=10, pad=8)

    patches = [
        mpatches.Patch(color="#ef4444", label="Poor (<60%)"),
        mpatches.Patch(color="#f59e0b", label="Moderate"),
        mpatches.Patch(color="#10b981", label="Good (>80%)"),
    ]
    ax.legend(handles=patches, fontsize=7.5, frameon=False,
              labelcolor=TEXT_COL, facecolor=DARK_BG, loc="upper right")

    fig.tight_layout(pad=0.8)
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, facecolor=DARK_BG)
    plt.close(fig)
    buf.seek(0)
    return buf




# ── table helper ───────────────────────────────────────────────────────────
def _data_table(rows, col_widths, hdr_bg=C_BLUE):
    t = Table(rows, colWidths=col_widths)
    style_cmds = [
        ("BACKGROUND",    (0, 0), (-1, 0), hdr_bg),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 9),
        ("TOPPADDING",    (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("FONTSIZE",      (0, 1), (-1, -1), 9),
        ("TOPPADDING",    (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("GRID",          (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(rows)):
        bg = C_LIGHT if i % 2 == 1 else WHITE
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t


def _section_banner(text, bg, col_total, style):
    t = Table([[Paragraph(text, style)]], colWidths=[col_total])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), bg),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))
    return t


# ── PDF builder ────────────────────────────────────────────────────────────
def build_pdf(data: dict) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=2*cm,
    )

    COL1      = 7.5 * cm
    COL2      = 9.3 * cm
    COL_TOTAL = COL1 + COL2

    st = _PDF_STYLES   # shorthand

    ov    = data["overview"]
    em    = data["emissions"]
    red   = data["reduction"]
    above = "Above" in em["status_vs_network"]

    story = []

    # ── Cover banner ──────────────────────────────────────────────────────
    banner = Table(
        [
            [Paragraph("Carbon Intelligence Report", st["TITLE"])],
            [Paragraph(f"Lane: {ov['lane_name']}", st["SUBT"])],
            [Paragraph("Sustainability & Decarbonization Analysis", st["SUBT2"])],
        ],
        colWidths=[COL_TOTAL],
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), C_SLATE),
        ("TOPPADDING",    (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
    ]))
    story.append(banner)
    story.append(Spacer(1, 14))

    # ── 1. Lane Overview ──────────────────────────────────────────────────
    story.append(_section_banner("1.  Lane Overview", C_BLUE, COL_TOTAL, st["SEC_H"]))
    story.append(Spacer(1, 5))
    story.append(_data_table(
        [
            ["Metric",               "Value"],
            ["Total Shipments",      f"{ov['total_shipments']:,}"],
            ["Total Distance",       f"{ov['total_distance_km']:,} km"],
            ["Total Freight",        f"{ov['total_freight_tons']:,} tonnes"],
            ["Avg Utilisation",      f"{ov['avg_utilization']}%"],
            ["Avg Vehicle Age",      f"{ov['avg_vehicle_age']} years"],
            ["Common Vehicle Types", ", ".join(ov['common_vehicle_types'])],
        ],
        [COL1, COL2], hdr_bg=C_BLUE,
    ))
    story.append(Spacer(1, 14))

    # ── 2. Carbon Emission Analysis ───────────────────────────────────────
    story.append(_section_banner("2.  Carbon Emission Analysis", C_GREEN, COL_TOTAL, st["SEC_H"]))
    story.append(Spacer(1, 5))
    em_rows = [
        ["Metric",                       "Value"],
        ["Total Carbon Emissions",        f"{em['total_carbon_kg']:,} kg"],
        ["Avg Carbon per Shipment",       f"{em['avg_carbon_per_shipment']:,} kg"],
        ["Carbon Intensity",              f"{em['emission_intensity']:.4f} kg / tonne-km"],
        ["Network Average per Shipment",  f"{em['network_avg_carbon']:,} kg"],
        ["Status vs Network",             em["status_vs_network"]],
    ]
    em_t = _data_table(em_rows, [COL1, COL2], hdr_bg=C_GREEN)
    # colour status cell
    last = len(em_rows) - 1
    em_t.setStyle(TableStyle([
        ("TEXTCOLOR", (1, last), (1, last), C_RED if above else C_GREEN),
        ("FONTNAME",  (1, last), (1, last), "Helvetica-Bold"),
    ]))
    story.append(em_t)
    story.append(Spacer(1, 14))

    # ── Charts Section ─────────────────────────────────────────────────────
    raw = data["_raw"]
    story.append(_section_banner("Carbon Analytics Charts", C_BLUE, COL_TOTAL, st["SEC_H"]))
    story.append(Spacer(1, 8))

    # Chart 1: Lane vs Network bar
    c1_buf = _chart_carbon_comparison(raw["avg_em"], raw["network_avg"])
    c1_img = RLImage(c1_buf, width=COL_TOTAL, height=COL_TOTAL * (2.2/7.0))
    story.append(c1_img)
    story.append(Spacer(1, 10))

    # Charts 2 & 3 side-by-side
    c2_buf = _chart_fuel_mix(raw["lane_df"])
    c3_buf = _chart_utilisation_dist(raw["lane_df"])
    c2_img = RLImage(c2_buf, width=COL_TOTAL * 0.44, height=COL_TOTAL * 0.44 * (3.2/4.5))
    c3_img = RLImage(c3_buf, width=COL_TOTAL * 0.54, height=COL_TOTAL * 0.54 * (2.5/7.0))
    side_t = Table([[c2_img, c3_img]], colWidths=[COL_TOTAL*0.46, COL_TOTAL*0.54])
    side_t.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(side_t)
    story.append(Spacer(1, 14))

    # ── 3. Emission Drivers ───────────────────────────────────────────────
    story.append(_section_banner("3.  Emission Drivers", C_AMBER, COL_TOTAL, st["SEC_H"]))
    story.append(Spacer(1, 6))
    for item in data["drivers"]:
        story.append(Paragraph(f"   - {item}", st["BULLET"]))
    story.append(Spacer(1, 12))


    # ── 4. Carbon Hotspot Detection ───────────────────────────────────────
    story.append(_section_banner("4.  Carbon Hotspot Detection", C_RED, COL_TOTAL, st["SEC_H"]))
    story.append(Spacer(1, 6))
    for item in data["hotspots"]:
        story.append(Paragraph(f"   - {item}", st["BULLET"]))
    story.append(Spacer(1, 12))

    # ── 5. Sustainability Recommendations ─────────────────────────────────
    story.append(_section_banner("5.  Sustainability Recommendations", C_PURPLE, COL_TOTAL, st["SEC_H"]))
    story.append(Spacer(1, 6))
    for i, item in enumerate(data["recommendations"], 1):
        story.append(Paragraph(f"   {i}.  {item}", st["BULLET"]))
    story.append(Spacer(1, 12))

    # ── 6. Reduction Opportunity Summary ──────────────────────────────────
    story.append(_section_banner("6.  Reduction Opportunity Summary", C_SLATE, COL_TOTAL, st["SEC_H"]))
    story.append(Spacer(1, 6))
    story.append(_data_table(
        [
            ["Metric",                    "Estimate"],
            ["Potential Carbon Reduction", f"{red['potential_reduction_kg']:,} kg"],
        ],
        [COL1, COL2], hdr_bg=C_SLATE,
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(red["impact_summary"], st["INFO_BG"]))

    # ── Footer ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 22))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_MUTED, spaceAfter=6))
    story.append(Paragraph(
        "Generated by LN Carbon Intelligence Platform  |  Confidential  |  For Internal Use Only",
        st["FOOT"],
    ))

    doc.build(story)
    buf.seek(0)
    return buf.read()


# ── Streamlit page ──────────────────────────────────────────────────────────
@st.cache_data
def _load_lane_options():
    """Load and cache the unique origin→destination pairs from the dataset."""
    data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "carbon_tracker_shipments.csv")
    )
    df = pd.read_csv(data_path, usecols=["origin", "destination"])
    df["origin"]      = df["origin"].str.strip().str.title()
    df["destination"] = df["destination"].str.strip().str.title()
    # Build dict: origin -> sorted list of valid destinations
    pairs = df.groupby("origin")["destination"].unique().apply(sorted).to_dict()
    origins = sorted(pairs.keys())
    return origins, pairs


def show():
    st_lib = st   # avoid name clash with local `st` dict
    st_lib.markdown(
        "<h2 style='color:#10b981;margin-bottom:0.2rem;'>📄 Lane Carbon Intelligence Report</h2>",
        unsafe_allow_html=True,
    )
    st_lib.markdown(
        "<p style='color:#94a3b8;margin-top:0;'>"
        "Select a freight lane from the dataset to generate a professional sustainability report.</p>",
        unsafe_allow_html=True,
    )

    # Load pairs from CSV (cached)
    origins, pairs = _load_lane_options()

    c1, c2 = st_lib.columns(2)
    with c1:
        origin = st_lib.selectbox(
            "Origin City",
            options=["-- Select Origin --"] + origins,
            index=0,
            key="report_origin",
        )

    # Cascade: show only destinations valid for chosen origin
    if origin == "-- Select Origin --":
        valid_dests = []
    else:
        valid_dests = pairs.get(origin, [])

    with c2:
        dest = st_lib.selectbox(
            "Destination City",
            options=["-- Select Destination --"] + list(valid_dests),
            index=0,
            key="report_dest",
            disabled=(origin == "-- Select Origin --"),
        )

    ready = origin != "-- Select Origin --" and dest != "-- Select Destination --"

    if st_lib.button("Generate Report", type="primary", use_container_width=True, disabled=not ready):
        with st_lib.spinner("Analysing lane data..."):
            data_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "data", "carbon_tracker_shipments.csv")
            )
            data = analyze_lane(origin, dest, data_path)

        if data is None:
            st_lib.error(
                f"No shipments found for **{origin} to {dest}**. "
                "This lane may have been filtered out. Try another combination."
            )
            return

        st_lib.success(f"Report generated for **{origin} to {dest}**!")

        # KPI strip
        k1, k2, k3, k4 = st_lib.columns(4)
        k1.metric("Total Shipments",   f"{data['overview']['total_shipments']:,}")
        k2.metric("Total Carbon (kg)", f"{data['emissions']['total_carbon_kg']:,}")
        k3.metric("Avg Utilisation",   f"{data['overview']['avg_utilization']}%")
        above = "Above" in data["emissions"]["status_vs_network"]
        k4.metric(
            "vs Network Avg",
            "Above Average" if above else "Below Average",
            delta=f"{data['emissions']['avg_carbon_per_shipment'] - data['emissions']['network_avg_carbon']:+.1f} kg",
            delta_color="inverse",
        )

        with st_lib.expander("Emission Drivers", expanded=True):
            for d in data["drivers"]:
                st_lib.markdown(f"- {d}")

        with st_lib.expander("Carbon Hotspot Detection"):
            for h in data["hotspots"]:
                st_lib.markdown(f"- {h}")

        with st_lib.expander("Sustainability Recommendations", expanded=True):
            for r in data["recommendations"]:
                st_lib.markdown(f"- {r}")

        st_lib.info(f"**Reduction Opportunity:** {data['reduction']['impact_summary']}")

        # PDF download — built fresh each click
        pdf_bytes = build_pdf(data)
        st_lib.download_button(
            label="Download Full Report (PDF)",
            data=pdf_bytes,
            file_name=f"CarbonReport_{origin}_{dest}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

