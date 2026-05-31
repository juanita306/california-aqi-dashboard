import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="California Air Quality Intelligence",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS (MODERN PROFESSIONAL UI)
# =========================================================

st.markdown("""
<style>

/* ===== TERMA UTAMA & LATAR BELAKANG GLOBAL (NAVY GELAP) ===== */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #111844 !important;
    color: #EAE0CF !important;
}

/* Memaksa kawasan kandungan tengah juga berwarna Navy */
[data-testid="stHeader"], [data-testid="stMainSpace"] {
    background-color: #111844 !important;
}

/* ===== REMOVE STREAMLIT DEFAULT ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ===== SIDEBAR (GRADASI DEEP BLUE TO BLUE SLATE) ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111844, #4B5694) !important;
    border-right: 1px solid #7288AE !important;
}

section[data-testid="stSidebar"] * {
    color: #EAE0CF !important;
}

/* ===== HERO SECTION ===== */
.hero-box {
    padding: 30px;
    border-radius: 25px;
    background: linear-gradient(135deg, #4B5694, #111844) !important;
    border: 1px solid #7288AE !important;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #EAE0CF !important;
}

.hero-subtitle {
    font-size: 18px;
    color: #7288AE !important;
    margin-top: -10px;
}

/* ===== KPI CARD (BEKAS WARNA DENIM DUST) ===== */
.metric-card {
    background-color: #4B5694 !important; /* Memaksa bekas bertukar warna */
    padding: 22px;
    border-radius: 22px;
    border: 1px solid #7288AE !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.metric-title {
    color: #EAE0CF !important;
    opacity: 0.8;
    font-size: 15px;
}

.metric-value {
    font-size: 40px;
    font-weight: 700;
    color: #EAE0CF !important;
}

.metric-desc {
    color: #7288AE !important;
    font-size: 14px;
}

/* ===== CHART CONTAINER ===== */
.chart-container {
    background-color: #4B5694 !important;
    padding: 25px;
    border-radius: 24px;
    border: 1px solid #7288AE !important;
    margin-bottom: 20px;
}

/* ===== INSIGHT BOX ===== */
.insight-box {
    background-color: rgba(75, 86, 148, 0.2) !important; /* Kaca lutsinar */
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 20px;
    border-left: 5px solid #7288AE !important;
    height: 100%;
}

.insight-title {
    font-size: 24px;
    font-weight: 700;
    color: #EAE0CF !important;
    margin-bottom: 15px;
}

/* ===== SECTION TITLE ===== */
.section-title {
    font-size: 28px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 15px;
    color: #EAE0CF !important;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

/* ===== FIX WARNA TEKS SEARCH BOX SIDEBAR ===== */
div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
    color: #111844 !important;
}
div[data-baseweb="popover"] * {
    color: #111844 !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    try:
        df = pd.read_csv("california_aqi_2021.csv")
    except:
        df = pd.read_csv("california_aqi_2021.csv.csv")

    df['tanggal'] = pd.to_datetime(df['tanggal'])

    df['bulan_num'] = df['tanggal'].dt.month
    df['nama_bulan'] = df['tanggal'].dt.strftime('%B')

    def kategori(aqi):
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive"
        else:
            return "Unhealthy"

    df['Kategori'] = df['indeks_kualitas_udara'].apply(kategori)

    return df

df = load_data()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# Air Quality Control Panel")

st.sidebar.markdown(
    "Gunakan filter untuk melakukan eksplorasi data kualitas udara California."
)

daftar_kota = sorted(df['kota'].unique())

kota = st.sidebar.selectbox(
    "📍 Pilih Kota",
    daftar_kota
)

df_filtered = df[df['kota'] == kota]

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
    <div style="
        background-color: #4B5694; 
        padding: 20px 25px; 
        border-radius: 12px; 
        border: 1px solid rgba(234, 224, 207, 0.2);
        margin-bottom: 25px;
    ">
        <h1 style="color: #EAE0CF; margin: 0; font-size: 30px; font-weight: bold;">
            California Air Quality Intelligence Dashboard
        </h1>
        <p style="color: #EAE0CF; margin: 5px 0 0 0; font-size: 14px; opacity: 0.8;">
            Advanced Environmental Monitoring • Deep Analytics • Streamlit Intelligence System
        </p>
    </div>
""", unsafe_allow_html=True)

# =========================================================
# KPI SECTION
# =========================================================

st.markdown('<div class="section-title">📊 Executive Summary</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

avg_aqi = round(df_filtered['indeks_kualitas_udara'].mean(),1)
max_aqi = int(df_filtered['indeks_kualitas_udara'].max())
good_days = int((df_filtered['Kategori'] == "Good").sum())
total_data = len(df_filtered)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average AQI</div>
        <div class="metric-value">{avg_aqi}</div>
        <div class="metric-desc">Air Quality Index</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Peak Pollution</div>
        <div class="metric-value">{max_aqi}</div>
        <div class="metric-desc">Maximum AQI</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Healthy Days</div>
        <div class="metric-value">{good_days}</div>
        <div class="metric-desc">Good Air Category</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Records</div>
        <div class="metric-value">{total_data}</div>
        <div class="metric-desc">Observation Samples</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# MONTHLY TREND + INSIGHT (VERSI RESET TOTAL - FIX DATA & STRUKTUR)
# ==============================================================================

# LANGKAH 1: Ambil data tren bulanan
df_trend = (
    df_filtered
    .groupby(['bulan_num', 'nama_bulan'])['indeks_kualitas_udara']
    .mean()
    .reset_index()
    .sort_values('bulan_num')
)

# AMAN & PASTI: Hitung langsung dari df_filtered kota terpilih
total_data = len(df_filtered)
good_days = int((df_filtered['Kategori'] == "Good").sum())

# LANGKAH 2: Hitung variabel untuk template AI Insight
bulan_terparah = df_trend.loc[df_trend['indeks_kualitas_udara'].idxmax()]['nama_bulan']
aqi_terparah = round(df_trend['indeks_kualitas_udara'].max(), 1)

bulan_terbersih = df_trend.loc[df_trend['indeks_kualitas_udara'].idxmin()]['nama_bulan']
aqi_terbersih = round(df_trend['indeks_kualitas_udara'].min(), 1)

# Hitung persentase hari sehat
persen_sehat = round((good_days / total_data) * 100, 1) if total_data > 0 else 0.0

# Logika penentuan level risiko dan warna tema dinamis
if avg_aqi <= 50:
    risk_label = "Low / Healthy"
    risk_color = "#22c55e"  # Hijau Cerah
    risk_msg = "Air quality is satisfactory. No health risks for the general public."
elif avg_aqi <= 100:
    risk_label = "Moderate / Warning"
    risk_color = "#f59e0b"  # Oranye/Kuning
    risk_msg = "Acceptable air quality. Sensitive individuals should reduce prolonged outdoor exertion."
elif avg_aqi <= 150:
    risk_label = "Unhealthy for Sensitive"
    risk_color = "#F5824A"  # Merah
    risk_msg = "Sensitive groups (children, elderly) may experience health effects. Limit outdoor activities."
else:
    risk_label = "High / Critical Danger"
    risk_color = "#7f1d1d"  # Merah Gelap
    risk_msg = "HEALTH WARNING: Everyone may experience serious health effects. Stay indoors."


# LANGKAH 3: Gambar Wadah Kolom Berdampingan
col_chart, col_insight = st.columns([2, 1])

# --- BAGIAN KIRI: GRAFIK TREN BULANAN ---
with col_chart:
    # Menggunakan container bawaan Streamlit, otomatis bikin kotak lonjong rapi!
    with st.container(border=True):
        st.markdown(f"### 📈 Monthly Air Quality Trend")
        
        fig_line = px.line(
            df_trend,
            x='nama_bulan',             
            y='indeks_kualitas_udara',  
            markers=True,
            labels={
                'nama_bulan': 'Month', 
                'indeks_kualitas_udara': 'Air Quality Index'
            }
        )

        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', # Transparan agar mengikuti warna tema kontainer
            plot_bgcolor='rgba(0,0,0,0)',   
            font_color='#EAE0CF',           
            height=340,
            margin=dict(l=20, r=20, t=15, b=20)
        )
        st.plotly_chart(fig_line, use_container_width=True)

   


# --- BAGIAN KANAN: KOTAK AI INSIGHT OTOMATIS ---
with col_insight:
    # Kita pisah teks HTML dan CSS-nya menggunakan teknik penambahan (+) agar kurung kurawal CSS tidak merusak Python
    html_insight = (
        '<div class="insight-box" style="border-left: 5px solid ' + str(risk_color) + '; background-color: #4B5694 !important; height: 100%;">'
        '    <div class="insight-title">🧠 AI Insight: ' + str(kota) + '</div>'
        '    <ul>'
        '        <li>Pollution peak in <b>' + str(kota) + '</b> detected in <b>' + str(bulan_terparah) + '</b> reaching <b>' + str(aqi_terparah) + ' AQI</b>.</li>'
        '        <li>Worthy air condition observed in <b>' + str(bulan_terbersih) + '</b> dropping down to <b>' + str(aqi_terbersih) + ' AQI</b>.</li>'
        '        <li>Average AQI for this city is currently <b>' + str(avg_aqi) + '</b>.</li>'
        '        <li>About <b>' + str(persen_sehat) + '%</b> of observation days classified as an absolute healthy climate.</li>'
        '    </ul>'
        '    <br>'
        '    <p style="margin-bottom: 5px; color: #EAE0CF; font-size: 14px; opacity: 0.8;"><b>Environmental Risk Level:</b></p>'
        '    <div style="background-color: ' + str(risk_color) + '22; color: ' + str(risk_color) + '; padding: 8px 15px; border-radius: 12px; font-weight: bold; border: 1px solid ' + str(risk_color) + '44; display: inline-block; font-size: 16px; margin-bottom: 15px;">'
        '        ' + str(risk_label) + ''
        '    </div>'
        '    <p style="color: #EAE0CF; font-size: 14px; line-height: 1.4; opacity: 0.9;">'
        '        <b>Policy Recommendation:</b><br>' + str(risk_msg) + ''
        '    </p>'
        '</div>'
    )

    # Kirim ke Streamlit
    st.markdown(html_insight, unsafe_allow_html=True)


# =========================================================
# DONUT + BAR CHART
# =========================================================

st.markdown('<div class="section-title">🎯 Air Quality Distribution</div>', unsafe_allow_html=True)

col_pie, col_bar = st.columns(2)

with col_pie:

    fig_pie = px.pie(
        df_filtered,
        names='Kategori',
        hole=0.55,
        color='Kategori',
        color_discrete_map={
            'Good':'#254F22',
            'Moderate':'#EDE4C2',
            'Unhealthy for Sensitive':'#F5824A',
            'Unhealthy':'#A03A13'
        }
    )

    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', # Transparan mengikuti container
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#EAE0CF',
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(
        font=dict(
            color='#EAE0CF'        # Teks 'Good', 'Moderate' dll. jadi terang dan jelas
        )
     )
    )

    st.plotly_chart(fig_pie, use_container_width=True)

with col_bar:
    # 🎯 FIX JUDUL: Tulis judul langsung secara manual di dalam container agar pasti muncul
    with st.container(border=True):
        st.markdown("### 🍃 Top 10 Cleanest Cities (Lowest AQI)")
        
        # Hitung ulang data 10 kota terbersih
        df_bar = (
            df.groupby('kota')['indeks_kualitas_udara']
            .mean()
            .reset_index()
            .sort_values('indeks_kualitas_udara', ascending=True)
            .head(10)
        )
        
        fig_bar = px.bar(
            df_bar,                      
            x='kota',
            y='indeks_kualitas_udara',
            color='indeks_kualitas_udara',
            # Menggunakan warna gradasi hijau-biru yang adem
            color_continuous_scale=['#4BB8FA', '#2C5EAD'], 
            labels={'kota': 'City', 'indeks_kualitas_udara': 'Avg AQI'}
        )

        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#EAE0CF',
            coloraxis_showscale=False, 
            margin=dict(l=20, r=20, t=10, b=20),
            height=340, # Disamakan tingginya dengan donut chart di kiri
            
            # 🎯 FIX GRAFIK PENDEK: Memaksa sumbu Y dan X melakukan auto-scale secara proporsional
            yaxis=dict(
                autorange=True,
                fixedrange=False,
                showgrid=True,
                gridcolor='rgba(234, 224, 207, 0.1)' # Garis panduan tipis transparan
            ),
            xaxis=dict(
                type='category' # Memastikan nama kota diurutkan sebagai teks kategori, bukan acak
            )
        )
        
        # Tampilkan grafik ke dashboard
        st.plotly_chart(fig_bar, use_container_width=True)

# =========================================================
# GAUGE CHART
# =========================================================

st.markdown('<div class="section-title">🌡️ Environmental Risk Gauge</div>', unsafe_allow_html=True)

fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = avg_aqi,
    title = {'text': "Average AQI"},
    gauge = {
        'axis': {'range': [0, 200]},
        'bar': {'color': "#38bdf8"},
        'steps': [
            {'range': [0, 50], 'color': "#254F22"},
            {'range': [50, 100], 'color': "#EDE4C2"},
            {'range': [100, 150], 'color': "#F5824A"},
            {'range': [150, 200], 'color': "#A03A13"}
        ]
    }
))

fig_gauge.update_layout(
    paper_bgcolor='#111844',
    font_color='white',
    height=400
)

st.plotly_chart(fig_gauge, use_container_width=True)

# =========================================================
# DATA TABLE
# =========================================================

st.markdown('<div class="section-title">📋 Air Quality Dataset Preview</div>', unsafe_allow_html=True)

st.dataframe(
    df_filtered.head(20),
    use_container_width=True
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<hr style="border:1px solid #1e293b">

<center>

### 🌍 Environmental Intelligence System

Developed using Streamlit • Plotly • Python Analytics

</center>
""", unsafe_allow_html=True)