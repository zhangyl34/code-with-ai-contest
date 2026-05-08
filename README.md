# 5G 信号可视化看板

基于 **Streamlit** 构建的交互式 5G 路测数据可视化看板，支持信号覆盖地图和统计图表。

## 功能

- **信号覆盖地图** — 使用 pydeck 将 500 个采样点渲染在交互地图上，点颜色根据 RSRP 信号强度渐变（绿色 > -90dBm → 黄色 → 红色 < -110dBm）
- **频段分布饼图** — 统计 n28 / n41 / n78 各频段基站数量
- **终端类型饼图** — 统计 Smartphone / CPE / IoT 不同类型终端占比

## 数据

`data/signal_samples.csv` 包含 500 条 5G 模拟路测数据，字段：

| 字段 | 说明 |
|------|------|
| Latitude | 纬度 |
| Longitude | 经度 |
| CellID | 小区 ID |
| Band | 频段（n28 / n41 / n78） |
| RSRP_dBm | 信号强度（dBm） |
| SINR_dB | 信噪比（dB） |
| TerminalType | 终端类型（Smartphone / CPE / IoT） |
| Download_Mbps | 下载速率（Mbps） |

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
streamlit run app.py
```

在浏览器中打开 `http://localhost:8501` 即可查看看板。

## 依赖

- streamlit
- pandas
- pydeck
- numpy
- plotly

## 项目结构

```
contest/
├── app.py                    # 看板主程序
├── data/
│   └── signal_samples.csv    # 5G 模拟数据集
├── requirements.txt          # Python 依赖
└── README.md                 # 本文件
```
