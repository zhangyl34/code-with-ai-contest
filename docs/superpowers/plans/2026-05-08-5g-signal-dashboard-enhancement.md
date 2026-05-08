# 5G Signal Dashboard Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) for syntax tracking.

**Goal:** Add 3D column map, sidebar filters (band dropdown + RSRP slider), and real-time chart updates to the existing Streamlit dashboard.

**Architecture:** Single-file `app.py` modification. Replace `ScatterplotLayer` with `ColumnLayer` for 3D bars with normalized height. Add `st.sidebar` widgets whose values filter the DataFrame before all chart rendering. Streamlit's reactive execution model provides real-time updates automatically.

**Tech Stack:** Streamlit, pandas, pydeck (ColumnLayer), plotly

---

### Task 1: Add height normalization for 3D columns

**Files:**
- Modify: `E:\agent\besa_test\finalist\code-with-ai-contest\app.py`

- [ ] **Step 1: Read current app.py to understand structure**

Run: `Get-Content -LiteralPath "E:\agent\besa_test\finalist\code-with-ai-contest\app.py"`
Expected: 55 lines with imports, color function, map, pie charts

- [ ] **Step 2: Add height normalization after `df["color"]` line**

Insert after line 23 (`df["color"] = df["RSRP_dBm"].apply(rsrp_to_color)`):

```python
min_dl, max_dl = df["Download_Mbps"].min(), df["Download_Mbps"].max()
df["height"] = (df["Download_Mbps"] - min_dl) / (max_dl - min_dl) * 1300 + 200
```

This normalizes Download_Mbps to [200, 1500] range for visual height.

---

### Task 2: Replace ScatterplotLayer with ColumnLayer

**Files:**
- Modify: `E:\agent\besa_test\finalist\code-with-ai-contest\app.py:25-39`

- [ ] **Step 1: Replace layer definition**

Change from:
```python
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["Longitude", "Latitude"],
    get_fill_color="color",
    get_radius=100,
    pickable=True,
)
```

To:
```python
layer = pdk.Layer(
    "ColumnLayer",
    data=df,
    get_position=["Longitude", "Latitude"],
    get_elevation="height",
    elevation_scale=1,
    radius=50,
    get_fill_color="color",
    pickable=True,
    extruded=True,
)
```

Key changes: `"ColumnLayer"`, added `get_elevation`, `elevation_scale`, `extruded=True`, replaced `get_radius` with `radius=50`.

---

### Task 3: Add sidebar filters

**Files:**
- Modify: `E:\agent\besa_test\finalist\code-with-ai-contest\app.py`

- [ ] **Step 1: Add sidebar controls after color/height columns (after line 24, before chart heading)**

```python
st.sidebar.header("筛选条件")

bands = ["全部"] + sorted(df["Band"].unique().tolist())
selected_band = st.sidebar.selectbox("频段", bands)

rsrp_min = float(df["RSRP_dBm"].min())
rsrp_max = float(df["RSRP_dBm"].max())
rsrp_range = st.sidebar.slider(
    "RSRP 范围 (dBm)",
    min_value=rsrp_min,
    max_value=rsrp_max,
    value=(rsrp_min, rsrp_max),
)

filtered_df = df.copy()
if selected_band != "全部":
    filtered_df = filtered_df[filtered_df["Band"] == selected_band]
filtered_df = filtered_df[
    (filtered_df["RSRP_dBm"] >= rsrp_range[0]) &
    (filtered_df["RSRP_dBm"] <= rsrp_range[1])
]
```

---

### Task 4: Wire all charts to use filtered_df

**Files:**
- Modify: `E:\agent\besa_test\finalist\code-with-ai-contest\app.py`

- [ ] **Step 1: Change map data and charts to use `filtered_df`**

In the layer definition: change `data=df` to `data=filtered_df`
In the view state: change `df["Latitude"].mean()` to `filtered_df["Latitude"].mean()` and same for longitude
In both pie charts: change `df["Band"]` to `filtered_df["Band"]` and `df["TerminalType"]` to `filtered_df["TerminalType"]`

Resulting changes:
- Line ~35: `data=filtered_df`
- Lines ~38-39: `latitude=filtered_df["Latitude"].mean()` and `longitude=filtered_df["Longitude"].mean()`
- Line ~47: `band_counts = filtered_df["Band"].value_counts().reset_index()`
- Line ~53: `type_counts = filtered_df["TerminalType"].value_counts().reset_index()`

---

### Task 5: Verify app runs

- [ ] **Step 1: Run the app in headless mode to check for errors**

Run: `cd E:\agent\besa_test\finalist\code-with-ai-contest && streamlit run app.py 2>&1`
Expected: Streamlit starts successfully, no ImportError or runtime errors

- [ ] **Step 2: Verify complete final file**

Read the final app.py and confirm:
1. ColumnLayer with get_elevation="height" and extruded=True ✓
2. Sidebar with selectbox (bands) and slider (RSRP range) ✓
3. All charts use filtered_df ✓
4. Height normalization from Download_Mbps ✓
