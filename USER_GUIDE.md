# User Guide: Aerial Survey ROI Workflow

## Overview

This workflow generates aerial survey transect lines over a user-defined Region of Interest (ROI). It takes a geospatial boundary file as input and outputs:

- An interactive HTML ecomap showing the survey lines overlaid on the ROI
- The survey lines exported as a GeoPackage (`.gpkg`)
- The survey lines exported as a GeoParquet (`.geoparquet`)
- A dashboard widget displaying the map

---

## Prerequisites

- Access to an Ecoscope Workflows deployment (the workflow runner UI or API)
- A geospatial file defining your Region of Interest — supported formats include GeoPackage (`.gpkg`), Shapefile, or GeoJSON. The file should contain polygon geometry.
- The `ECOSCOPE_WORKFLOWS_RESULTS` environment variable must be set to a writable output directory on your deployment.

---

## Step-by-Step Instructions

### Step 1 — Set Workflow Details

Provide a name/description for this workflow run. This label will appear in the output dashboard.

- **Name**: e.g., `Mara North Conservancy Aerial Survey`

---

### Step 2 — Set Time Range

Define the time range for the workflow. While the aerial line generation itself is not time-filtered, the time range is recorded in the dashboard for reference and reporting.

| Field | Description | Example |
|---|---|---|
| Since | Start date/time (ISO 8601) | `2026-02-03T10:14:00.000Z` |
| Until | End date/time (ISO 8601) | `2026-03-03T10:14:00.000Z` |
| Timezone | Timezone label | `UTC` |
| Time format | Display format for dates | `%d %b %Y %H:%M:%S` |

---

### Step 3 — Set Groupers *(optional)*

Groupers allow you to split outputs by a categorical attribute. Leave this empty (default) if you do not need grouped outputs.

---

### Step 4 — Configure Base Map Layers *(optional)*

The workflow comes pre-configured with two ArcGIS base layers:

1. **World Hillshade** — terrain shading at full opacity
2. **World Street Map** — street/label overlay at 15% opacity

You can replace or adjust these if your deployment supports custom tile URLs.

---

### Step 5 — Define Region of Interest (ROI file)

This is the primary required input. Provide the path or URL to your ROI boundary file.

| Input method | Example |
|---|---|
| File URL | `https://www.dropbox.com/scl/fi/14rcy4lkwp7xgewj3xf7k/mnc_conservancy.gpkg?...&dl=0` |
| Local path | `/data/inputs/my_conservancy.gpkg` |

**Requirements:**
- The file must contain polygon geometry.
- GeoPackage (`.gpkg`) is the recommended format.
- The coordinate reference system (CRS) can be any EPSG — the workflow reprojects to EPSG:4326 automatically.

---

### Step 6 — Draw Aerial Survey Lines

Configure how the transect lines are drawn across your ROI.

| Parameter | Description | Example |
|---|---|---|
| `direction` | Orientation of survey transects | `North South` or `East West` |
| `spacing` | Distance between transect lines in meters | `1500` |

The lines will be clipped to the ROI boundary.

---

## Outputs

Once the workflow completes successfully, the following files are written to `$ECOSCOPE_WORKFLOWS_RESULTS`:

| File | Format | Description |
|---|---|---|
| `aerial_survey.gpkg` | GeoPackage | Survey transect lines, ready for use in QGIS or ArcGIS |
| `aerial_survey.geoparquet` | GeoParquet | Survey transect lines in cloud-native format |
| `aerial_survey.html` | HTML | Interactive ecomap with ROI boundary and survey lines |

The dashboard will display a single map widget titled **"Aerial Survey Lines"** showing:
- The ROI boundary (olive green fill, 15% opacity)
- The generated survey transects (yellow lines)

---

## Troubleshooting

| Problem | Likely cause | Resolution |
|---|---|---|
| Workflow step is skipped | Input GeoDataFrame is empty | Verify your ROI file contains valid polygon features |
| Map shows no lines | ROI geometry is invalid or very small relative to spacing | Reduce the `spacing` value or check your ROI file |
| File not found error | URL or path to ROI file is incorrect | Confirm the file is accessible from the workflow runner |
| CRS errors | Source file has no CRS defined | Assign a CRS to your file before uploading (e.g., EPSG:4326) |

---
