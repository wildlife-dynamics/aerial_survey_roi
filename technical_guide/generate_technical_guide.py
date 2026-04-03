"""
Generate the Aerial Survey ROI Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output:   aerial_survey_roi_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "aerial_survey_roi_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK = colors.HexColor("#115631")
GREEN_MID  = colors.HexColor("#2d6a4f")
AMBER      = colors.HexColor("#e7a553")
SLATE      = colors.HexColor("#3d3d3d")
LIGHT_GREY = colors.HexColor("#f5f5f5")
MID_GREY   = colors.HexColor("#cccccc")
WHITE      = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body",       fontSize=9,  leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9,  leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8,  leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note",       fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)

# ── Helpers ────────────────────────────────────────────────────────────────────
def hr():             return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, s=BODY): return Paragraph(text, s)
def h1(t):            return Paragraph(t, H1)
def h2(t):            return Paragraph(t, H2)
def h3(t):            return Paragraph(t, H3)
def sp(n=6):          return Spacer(1, n)
def b(text):          return Paragraph(f"• {text}", BULLET)
def note(text):       return Paragraph(f"<b>Note:</b> {text}", NOTE)
def code(text):       return Paragraph(text, CODE)

def tbl(data, col_widths, header_row=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


# ── Page template ──────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5 * cm, 7, "Aerial Survey ROI — Technical Guide")
    canvas.drawRightString(w - 1.5 * cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build ──────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="Aerial Survey ROI — Technical Guide",
        author="Ecoscope",
    )
    story = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("Aerial Survey ROI", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8), hr(),
        p("Transect Planning Workflow — Configuration &amp; Reference", META),
        p(f"Version 1.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(), PageBreak(),
    ]

    # ── 1. Overview ────────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"), hr(),
        p(
            "The <b>Aerial Survey ROI</b> workflow generates parallel transect lines "
            "across a user-defined polygon boundary at a configurable compass bearing "
            "and spacing. Outputs are exported as geospatial files and rendered as an "
            "interactive map widget in the Ecoscope dashboard."
        ),
        sp(4),
        b("<b>aerial_survey.gpkg</b> — transect lines as a GeoPackage"),
        b("<b>aerial_survey.geoparquet</b> — transect lines in GeoParquet format"),
        b("<b>aerial_survey.html</b> — interactive HTML ecomap"),
        b("<b>Dashboard widget</b> — map titled <i>Aerial Survey Lines</i>"),
    ]

    # ── 2. Prerequisites ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Prerequisites"), hr(),

        h2("2.1 Packages"),
        tbl(
            [
                ["Package",                             "Version",   "Channel"],
                ["ecoscope-workflows-core",             "0.22.17.*", "https://repo.prefix.dev/ecoscope-workflows/"],
                ["ecoscope-workflows-ext-ecoscope",     "0.22.17.*", "https://repo.prefix.dev/ecoscope-workflows/"],
                ["ecoscope-workflows-ext-custom",       "0.0.39.*",  "https://repo.prefix.dev/ecoscope-workflows-custom/"],
                ["ecoscope-workflows-ext-ste",          "0.0.18.*",  "https://repo.prefix.dev/ecoscope-workflows-custom/"],
            ],
            [6*cm, 3*cm, 7.5*cm],
        ),

        sp(4), h2("2.2 Environment"),
        tbl(
            [
                ["Variable",                     "Required", "Description"],
                ["ECOSCOPE_WORKFLOWS_RESULTS",   "Yes",      "Writable directory for all output files."],
            ],
            [5.5*cm, 2*cm, 9*cm],
        ),

        sp(4), h2("2.3 Input File"),
        tbl(
            [
                ["Format",                                                      "Geometry",             "CRS"],
                ["GeoPackage (.gpkg), GeoJSON (.geojson), GeoParquet (.geoparquet)",
                 "Polygon or MultiPolygon",
                 "Any EPSG — reprojected to EPSG:4326 automatically."],
            ],
            [6*cm, 4*cm, 6.5*cm],
        ),
        note("Files with no CRS assigned will raise a projection error. Set an EPSG code before uploading."),
    ]

    # ── 3. Configurable Parameters ─────────────────────────────────────────────
    story += [
        sp(4), h1("3. Configurable Parameters"), hr(),
        p("Four task groups are user-configurable. All remaining tasks run with fixed defaults."),
    ]

    # 3.1 Set Workflow Details
    story += [
        sp(4), h2("3.1 Set Workflow Details"),
        p("<b>Task ID:</b> <code>workflow_details</code>  ·  <b>Function:</b> <code>set_workflow_details</code>"),
        p("Name and description for this run. Appears in the dashboard header."),
        tbl(
            [
                ["Field",       "Type",   "Example"],
                ["Name",        "string", "Mara North Conservancy Aerial Survey"],
                ["Description", "string", "Pre-season transect planning, April 2026"],
            ],
            [3.5*cm, 2.5*cm, 10.5*cm],
        ),
    ]

    # 3.2 Time Range
    story += [
        sp(4), h2("3.2 Time Range  (optional)"),
        p("<b>Task ID:</b> <code>time_range</code>  ·  <b>Function:</b> <code>set_time_range</code>"),
        p(
            "Does <b>not</b> filter the ROI or transect geometry. "
            "Recorded in the dashboard for traceability against a specific survey window."
        ),
        tbl(
            [
                ["Field",       "Format",         "Example"],
                ["Since",       "ISO 8601",        "2026-02-03T10:14:00.000Z"],
                ["Until",       "ISO 8601",        "2026-03-03T10:14:00.000Z"],
                ["Timezone",    "IANA label",      "UTC"],
                ["Time format", "strftime string", "%d %b %Y %H:%M:%S"],
            ],
            [3*cm, 3.5*cm, 10*cm],
        ),
    ]

    # 3.3 Define Region of Interest
    story += [
        sp(4), h2("3.3 Define Region of Interest"),
        p(
            "<b>Task group</b>  ·  "
            "<b>Task ID:</b> <code>retrieve_file_params</code>  ·  "
            "<b>Function:</b> <code>get_file_path</code>"
        ),
        p("Provide the boundary file as a URL or local path. The file is loaded into a GeoDataFrame and styled as a map layer."),
        tbl(
            [
                ["Input method", "Example"],
                ["URL",          "https://example.com/my_conservancy.gpkg"],
                ["Local path",   "/data/inputs/my_conservancy.gpkg"],
            ],
            [4*cm, 12.5*cm],
        ),
        sp(4),
        h3("Automatic tasks after load"),
        tbl(
            [
                ["Task ID",             "Function",                    "Action"],
                ["load_gdf",            "load_df",                     "Load file into GeoDataFrame."],
                ["assign_geom_type",    "get_gdf_geom_type",           "Tag geometry type for downstream rendering."],
                ["generate_layers_map", "create_deckgl_layer_from_gdf","Create ROI boundary layer — olive green (#556b2f), 15 % opacity."],
            ],
            [4*cm, 4.5*cm, 8*cm],
        ),
    ]

    # 3.4 Draw Aerial Survey Lines
    story += [
        sp(4), h2("3.4 Draw Aerial Survey Lines"),
        p(
            "<b>Task group</b>  ·  "
            "<b>Task ID:</b> <code>survey_lines</code>  ·  "
            "<b>Function:</b> <code>draw_survey_lines</code>"
        ),
        p(
            "Generates parallel transect lines tiled across the ROI bounding box at the "
            "given bearing, then clips them to the ROI polygon. Lines outside the boundary "
            "are discarded."
        ),
        tbl(
            [
                ["Parameter", "UI Label",                  "Type",   "Description",                                          "Example"],
                ["direction", "Survey Direction (degrees)", "number", "Compass bearing (0–360°). 0° = N–S, 90° = E–W.",       "0"],
                ["spacing",   "Line Spacing (m)",           "number", "Distance in metres between adjacent transect lines.",   "1500"],
            ],
            [2.5*cm, 4.5*cm, 2*cm, 6*cm, 1.5*cm],
        ),
        sp(4),
        h3("Spacing guidance"),
        tbl(
            [
                ["ROI size",              "Suggested spacing"],
                ["Small  (< 100 km²)",    "500 – 1 000 m"],
                ["Medium (100–1 000 km²)","1 000 – 2 500 m"],
                ["Large  (> 1 000 km²)",  "2 500 – 5 000 m"],
            ],
            [6*cm, 10.5*cm],
        ),
        note(
            "If spacing exceeds the cross-track ROI extent, draw_survey_lines returns an "
            "empty GeoDataFrame and all downstream tasks are skipped. Reduce spacing and re-run."
        ),
        sp(4),
        h3("Line style"),
        tbl(
            [
                ["Property",        "Value"],
                ["Colour",          "Yellow  #FFFF00  RGB(255, 255, 0)"],
                ["Opacity",         "55 %"],
                ["Width",           "1–5 px (pixel-scaled)"],
                ["Display CRS",     "EPSG:4326"],
            ],
            [5*cm, 11.5*cm],
        ),
    ]

    # ── 4. Workflow DAG ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Workflow DAG"), hr(),
        p(
            "Tasks are chained via <code>${{ workflow.&lt;id&gt;.return }}</code> references. "
            "The table lists every node, its upstream dependencies, and its role."
        ),
        sp(4),
        tbl(
            [
                ["Task ID",                         "Depends on",                                                   "Role"],
                ["workflow_details",                "—",                                                            "Run name / description"],
                ["time_range",                      "—",                                                            "Reporting time window"],
                ["groupers",                        "—",                                                            "Attribute groupers (default: empty)"],
                ["configure_base_maps",             "—",                                                            "ArcGIS tile layer configuration"],
                ["retrieve_file_params",            "—",                                                            "Resolve ROI file URL or path"],
                ["load_gdf",                        "retrieve_file_params",                                         "Load ROI into GeoDataFrame"],
                ["assign_geom_type",                "load_gdf",                                                     "Tag geometry type"],
                ["generate_layers_map",             "assign_geom_type",                                             "ROI boundary DeckGL layer (olive green)"],
                ["survey_lines",                    "load_gdf",                                                     "Generate transect lines"],
                ["persist_aerial_gdf",              "survey_lines",                                                 "Write aerial_survey.gpkg"],
                ["persist_aerial_gpq",              "survey_lines",                                                 "Write aerial_survey.geoparquet"],
                ["transform_gdf",                   "survey_lines",                                                 "Reproject lines to EPSG:4326"],
                ["aerial_survey_polylines",         "transform_gdf",                                                "Survey lines DeckGL layer (yellow)"],
                ["zoom_gdf_extent",                 "load_gdf",                                                     "Fit viewport to ROI extent"],
                ["combine_map_layers",              "generate_layers_map, aerial_survey_polylines",                 "Merge ROI + survey line layers"],
                ["draw_aerial_survey_lines_ecomap", "configure_base_maps, combine_map_layers, zoom_gdf_extent",     "Render HTML ecomap"],
                ["persist_ecomaps",                 "draw_aerial_survey_lines_ecomap",                              "Write aerial_survey.html"],
                ["create_aerial_widgets",           "persist_ecomaps",                                              "Wrap map in dashboard widget"],
                ["patrol_dashboard",                "workflow_details, create_aerial_widgets, time_range, groupers","Assemble dashboard"],
            ],
            [4*cm, 5.5*cm, 7*cm],
        ),
    ]

    # ── 5. Outputs ─────────────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Outputs"), hr(),
        p("All files are written to <code>$ECOSCOPE_WORKFLOWS_RESULTS</code>."),
        tbl(
            [
                ["File",                   "Format",     "Use"],
                ["aerial_survey.gpkg",     "GeoPackage", "QGIS, ArcGIS, GPS flight-planning"],
                ["aerial_survey.geoparquet","GeoParquet", "Python / GeoPandas, cloud storage"],
                ["aerial_survey.html",     "HTML",       "Browser — interactive PyDeck ecomap"],
                ["Dashboard widget",       "Ecoscope",   "In-app reporting"],
            ],
            [4.5*cm, 3*cm, 9*cm],
        ),
        sp(4), h2("Map layer styles"),
        tbl(
            [
                ["Layer",            "Colour",                             "Opacity",  "Width"],
                ["ROI boundary",     "Olive green  #556b2f",               "15 % fill","1.25 px"],
                ["Survey transects", "Yellow  #FFFF00",                    "55 %",     "1–5 px"],
                ["World Hillshade",  "ArcGIS tile",                        "100 %",    "—"],
                ["World Street Map", "ArcGIS tile",                        "15 %",     "—"],
            ],
            [3.5*cm, 4.5*cm, 3*cm, 5.5*cm],
        ),
    ]

    # ── 6. Skip Logic ──────────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Skip Logic"), hr(),
        p(
            "All tasks share a global <code>skipif</code> policy "
            "(<code>task-instance-defaults</code> in <code>spec.yaml</code>):"
        ),
        code(
            "skipif:<br/>"
            "&nbsp;&nbsp;conditions:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- any_is_empty_df<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;- any_dependency_skipped"
        ),
        sp(4),
        tbl(
            [
                ["Condition",              "Trigger",                              "Effect"],
                ["any_is_empty_df",        "Any upstream GeoDataFrame is empty.",  "Task and all dependants are skipped, not crashed."],
                ["any_dependency_skipped", "Any upstream task was skipped.",        "Skip propagates transitively through the DAG."],
            ],
            [4*cm, 5.5*cm, 7*cm],
        ),
        note(
            "Skipped tasks show in the runner UI with a skipped status — not an error. "
            "Confirm all tasks completed to verify a full successful run."
        ),
    ]

    # ── 7. Troubleshooting ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Troubleshooting"), hr(),
        tbl(
            [
                ["Symptom",                              "Cause",                                    "Fix"],
                ["Tasks skipped downstream",
                 "Empty GeoDataFrame from ROI load or draw_survey_lines.",
                 "Check file path/URL; verify polygon features in QGIS; reduce spacing."],
                ["No lines on map",
                 "Spacing too large for the ROI extent.",
                 "Halve the spacing value and re-run."],
                ["CRS error",
                 "Source file has no CRS.",
                 "QGIS: Layer Properties → Set CRS. Python: gdf.set_crs('EPSG:4326')."],
                ["File not found",
                 "URL inaccessible or requires authentication.",
                 "Use a direct download link (e.g. Dropbox ?dl=1)."],
                ["Missing output files",
                 "ECOSCOPE_WORKFLOWS_RESULTS unset or not writable.",
                 "Export the variable; confirm directory write permissions."],
                ["Blank HTML map",
                 "Browser CORS block on local tile requests.",
                 "Serve with: python -m http.server 8080"],
            ],
            [4*cm, 5*cm, 7.5*cm],
        ),
    ]

    # ── 8. Example ─────────────────────────────────────────────────────────────
    story += [
        sp(4), h1("8. Example Configuration"), hr(),
        p("From <code>test-cases.yaml</code> — scenario: <i>all-grouper</i> (Mara North Conservancy):"),
        code(
            "workflow_details:<br/>"
            "&nbsp;&nbsp;name: Custom<br/>"
            "<br/>"
            "time_range:<br/>"
            "&nbsp;&nbsp;timezone: { label: UTC, tzCode: UTC, utc: '+00:00' }<br/>"
            "&nbsp;&nbsp;time_format: '%d %b %Y %H:%M:%S'<br/>"
            "&nbsp;&nbsp;since: '2026-02-03T10:14:00.000Z'<br/>"
            "&nbsp;&nbsp;until: '2026-02-03T10:14:00.000Z'<br/>"
            "<br/>"
            "retrieve_file_params:<br/>"
            "&nbsp;&nbsp;input_method:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;url: 'https://www.dropbox.com/.../mnc_conservancy.gpkg'<br/>"
            "<br/>"
            "survey_lines:<br/>"
            "&nbsp;&nbsp;direction: 'North South'<br/>"
            "&nbsp;&nbsp;spacing: 1500"
        ),
        sp(6),
        b("N–S transect lines, 1 500 m apart, clipped to the MNC boundary."),
        b("Outputs: <code>aerial_survey.gpkg</code>, <code>aerial_survey.geoparquet</code>, <code>aerial_survey.html</code>."),
        b("Dashboard widget titled <i>Aerial Survey Lines</i>."),
    ]

    # ── 9. Software Versions ───────────────────────────────────────────────────
    story += [
        sp(4), h1("9. Software Versions"), hr(),
        tbl(
            [
                ["Package",                         "Version",   "Role"],
                ["ecoscope-workflows-core",         "0.22.17.*", "Workflow engine and core task library"],
                ["ecoscope-workflows-ext-ecoscope", "0.22.17.*", "Ecoscope spatial analysis tasks"],
                ["ecoscope-workflows-ext-custom",   "0.0.39.*",  "Custom tasks including draw_survey_lines"],
                ["ecoscope-workflows-ext-ste",      "0.0.18.*",  "STE-specific extension tasks"],
            ],
            [5.5*cm, 3*cm, 8*cm],
        ),
        p("Packages are pinned to patch-compatible versions (<code>.*</code>) and managed by <b>pixi</b>."),
    ]

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
