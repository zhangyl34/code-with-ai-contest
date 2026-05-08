import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk

st.set_page_config(page_title="5G 信号可视化看板", layout="wide")
st.title("5G 信号可视化看板")

df = pd.read_csv("data/signal_samples.csv")

def rsrp_to_color(rsrp):
    if rsrp > -90:
        return [0, 255, 0]
    elif rsrp < -110:
        return [255, 0, 0]
    else:
        ratio = (rsrp + 110) / 20
        r = int(255 * (1 - ratio))
        g = int(255 * ratio)
        return [r, g, 0]

df["color"] = df["RSRP_dBm"].apply(rsrp_to_color)

min_dl, max_dl = df["Download_Mbps"].min(), df["Download_Mbps"].max()
df["height"] = (df["Download_Mbps"] - min_dl) / (max_dl - min_dl) * 1300 + 200

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

st.subheader("信号覆盖地图")
layer = pdk.Layer(
    "ColumnLayer",
    data=filtered_df,
    get_position=["Longitude", "Latitude"],
    get_elevation="height",
    elevation_scale=1,
    radius=50,
    get_fill_color="color",
    pickable=True,
    extruded=True,
)
view_state = pdk.ViewState(
    latitude=filtered_df["Latitude"].mean(),
    longitude=filtered_df["Longitude"].mean(),
    zoom=11,
)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

col1, col2 = st.columns(2)

with col1:
    st.subheader("各频段基站数量")
    band_counts = filtered_df["Band"].value_counts().reset_index()
    band_counts.columns = ["Band", "count"]
    fig1 = px.pie(band_counts, values="count", names="Band", title="频段分布")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("不同类型终端占比")
    type_counts = filtered_df["TerminalType"].value_counts().reset_index()
    type_counts.columns = ["TerminalType", "count"]
    fig2 = px.pie(type_counts, values="count", names="TerminalType", title="终端类型分布")
    st.plotly_chart(fig2, use_container_width=True)
