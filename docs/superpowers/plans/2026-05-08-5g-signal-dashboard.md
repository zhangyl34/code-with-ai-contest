# 5G Signal Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Streamlit web dashboard that displays 5G signal data on an interactive map with RSRP-based coloring and two pie charts.

**Architecture:** Single-file Streamlit app (`app.py`) that reads CSV with pandas, renders a pydeck scatterplot map with RSRP color mapping, and shows plotly pie charts for band/terminal distribution.

**Tech Stack:** Streamlit, pandas, pydeck (deck.gl), plotly

---

### Task 1: Implement data loading and RSRP color mapping

**Files:**
- Modify: `E:\agent\besa_test\contest\app.py` (full rewrite)

- [ ] **Step 1: Replace app.py with full implementation**

Write the complete Streamlit app:

```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk

st.set_page_config(page_title="5G 信号可视化看板", layout="wide")
st.title("5G 信号可视化看板")

# Load data
df = pd.read_csv("data/signal_samples.csv")

# Color mapping function: RSRP -> [R, G, B]
def rsrp_to_color(rsrp):
    if rsrp > -90:
        return [0, 255, 0]       # green
    elif rsrp < -110:
        return [255, 0, 0]       # red
    else:
        # gradient: red(-110) -> yellow(-100) -> green(-90)
        ratio = (rsrp + 110) / 20  # 0 at -110, 1 at -90
        r = int(255 * (1 - ratio))
        g = int(255 * ratio)
        return [r, g, 0]

df["color"] = df["RSRP_dBm"].apply(rsrp_to_color)

# Map
st.subheader("信号覆盖地图")
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["Longitude", "Latitude"],
    get_fill_color="color",
    get_radius=100,
    pickable=True,
)
view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=11,
)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# Pie charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("各频段基站数量")
    band_counts = df["Band"].value_counts().reset_index()
    band_counts.columns = ["Band", "count"]
    fig1 = px.pie(band_counts, values="count", names="Band", title="频段分布")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("不同类型终端占比")
    type_counts = df["TerminalType"].value_counts().reset_index()
    type_counts.columns = ["TerminalType", "count"]
    fig2 = px.pie(type_counts, values="count", names="TerminalType", title="终端类型分布")
    st.plotly_chart(fig2, use_container_width=True)
```

- [ ] **Step 2: Verify app runs without errors**

Run: `cd E:\agent\besa_test\contest && streamlit run app.py --server.headless=true 2>&1`
Expected: Streamlit starts successfully (may need to Ctrl+C after verification)

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: implement 5G signal dashboard with map and pie charts"
```
