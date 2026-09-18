import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 결측치 처리 및 텍스트 정리
    df['genre'] = df['genre'].fillna('기타')
    df['nation'] = df['nation'].fillna('기타')
    
    # 판다스 내장 벡터화 메서드로 첫 번째 장르 추출
    df['main_genre'] = (
        df['genre']
        .astype(str)
        .str.split('|')
        .str[0]
        .str.strip()
    )
    df['main_genre'] = df['main_genre'].replace('', '기타')
    df['nation'] = df['nation'].astype(str).str.strip().replace('', '기타')
    
    return df

df = load_data()

# 타이틀 및 안내 문구
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("박스오피스 상위권 개봉 영화 216편의 장르 분포, 관객 수 규모 및 변수 간의 관계를 탐색합니다.")
st.divider()

# ==========================================
# 1. 장르별 영화 편수 (도넛 그래프)
# ==========================================
st.subheader("1. 장르별 영화 편수 분포 (도넛 그래프)")

# 장르별 편수 집계
genre_counts = df['main_genre'].value_counts().reset_index()
genre_counts.columns = ['main_genre', 'count']

# 도넛 그래프 생성
fig1 = px.pie(
    genre_counts,
    values='count',
    names='main_genre',
    hole=0.4,
    title="장르별 영화 편수 비율",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# 호버 서식 및 레이아웃 설정
fig1.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)
fig1.update_layout(
    margin=dict(t=40, b=20, l=20, r=20),
    legend_title_text="장르"
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ==========================================
# 2. 장르 및 영화별 총 관객 수 (트리맵)
# ==========================================
st.subheader("2. 장르 및 영화별 총 관객 수 (트리맵)")

# 트리맵 그래프 생성
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), 'main_genre', 'movieNm'],
    values='total_audi',
    color='main_genre',
    color_discrete_sequence=px.colors.qualitative.Set3,
    title="장르 및 영화별 총 관객 수 분포 (칸 크기: 총 관객 수)"
)

# 칸 마우스 호버 서식 설정
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,.0f}명<extra></extra>"
)
fig2.update_layout(
    margin=dict(t=40, b=20, l=20, r=20)
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ==========================================
# 3. 총 관객 수 분포 (히스토그램)
# ==========================================
st.subheader("3. 영화별 총 관객 수 분포 (히스토그램)")

# 히스토그램 그래프 생성
fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="영화별 총 관객 수 분포 (히스토그램)",
    labels={'total_audi': '총 관객 수 (명)', 'count': '영화 수'},
    color_discrete_sequence=['#4C78A8']
)

fig3.update_traces(
    hovertemplate="총 관객 수 구간: %{x}<br>영화 수: %{y}편<extra></extra>"
)
fig3.update_layout(
    xaxis_title="총 관객 수 (명)",
    yaxis_title="영화 수 (편)",
    bargap=0.1,
    margin=dict(t=40, b=20, l=20, r=20)
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ==========================================
# 4. 개봉일 스크린수와 총 관객 수의 관계 (산점도)
# ==========================================
st.subheader("4. 개봉일 스크린수와 총 관객 수의 관계 (산점도)")

# 산점도 그래프 생성
fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='main_genre',
    hover_name='movieNm',
    custom_data=['main_genre'],
    title="개봉일 스크린수 vs 총 관객 수",
    labels={'first_scrn': '개봉일 스크린 수 (개)', 'total_audi': '총 관객 수 (명)', 'main_genre': '장르'},
    color_discrete_sequence=px.colors.qualitative.Plotly
)

fig4.update_traces(
    marker=dict(size=9, opacity=0.8),
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>개봉일 스크린 수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

fig4.update_layout(
    xaxis_title="개봉일 스크린 수 (개)",
    yaxis_title="총 관객 수 (명)",
    margin=dict(t=40, b=20, l=20, r=20),
    legend_title_text="장르"
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ==========================================
# 5. 주요 장르별 총 관객 수 분포 (상자 그림)
# ==========================================
st.subheader("5. 주요 장르별 총 관객 수 분포 (상자 그림)")

# 영화가 10편 이상인 장르만 추출
genre_counts_series = df['main_genre'].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_major_genres = df[df['main_genre'].isin(major_genres)]

# 상자 그림 생성
fig5 = px.box(
    df_major_genres,
    x='main_genre',
    y='total_audi',
    color='main_genre',
    hover_name='movieNm',
    points='outliers',
    title="영화 10편 이상 주요 장르별 총 관객 수 분포 (상자 그림)",
    labels={'main_genre': '장르', 'total_audi': '총 관객 수 (명)'},
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

fig5.update_layout(
    xaxis_title="장르 (영화 10편 이상)",
    yaxis_title="총 관객 수 (명)",
    showlegend=False,
    margin=dict(t=40, b=20, l=20, r=20)
)

st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ==========================================
# 6. 개봉일 스크린수, 개봉 첫 주 관객, 총 관객 수의 관계 (버블 차트)
# ==========================================
st.subheader("6. 개봉일 스크린수, 개봉 첫 주 관객, 총 관객 수의 관계 (버블 차트)")

# 버블 차트 생성
fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='main_genre',
    hover_name='movieNm',
    custom_data=['main_genre', 'first_week_audi'],
    size_max=45,
    title="개봉일 스크린수 vs 총 관객 수 (버블 크기: 개봉 첫 주 관객 수)",
    labels={
        'first_scrn': '개봉일 스크린 수 (개)',
        'total_audi': '총 관객 수 (명)',
        'first_week_audi': '개봉 첫 주 관객 수 (명)',
        'main_genre': '장르'
    },
    color_discrete_sequence=px.colors.qualitative.Plotly
)

fig6.update_traces(
    marker=dict(opacity=0.7),
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>개봉일 스크린 수: %{x:,.0f}개<br>개봉 첫 주 관객 수: %{customdata[1]:,.0f}명<br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

fig6.update_layout(
    xaxis_title="개봉일 스크린 수 (개)",
    yaxis_title="총 관객 수 (명)",
    margin=dict(t=40, b=20, l=20, r=20),
    legend_title_text="장르"
)

st.plotly_chart(fig6, use_container_width=True)

st.divider()

# ==========================================
# 7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)
# ==========================================
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)")

# 제작 국가 및 장르별 영화 편수 사전 집계
df_sunburst = df.groupby(['nation', 'main_genre']).size().reset_index(name='movie_count')

# 선버스트 차트 생성
fig7 = px.sunburst(
    df_sunburst,
    path=['nation', 'main_genre'],
    values='movie_count',
    title="제작 국가 → 장르별 영화 편수 구조 (선버스트 차트)",
    color_discrete_sequence=px.colors.qualitative.Pastel1
)

fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percentParent:.1%}<extra></extra>"
)

fig7.update_layout(
    margin=dict(t=40, b=20, l=20, r=20)
)

st.plotly_chart(fig7, use_container_width=True)

st.divider()

# ==========================================
# 8. 10위권 머문 날수와 총 관객 수의 관계 (산점도)
# ==========================================
st.subheader("8. 10위권 머문 날수와 총 관객 수의 관계 (산점도)")

st.markdown("❓ **나만의 8번째 질문**: *10위권에 오래 머문 영화는 총 관객 수도 많은가?*")

# 산점도 그래프 생성
fig8 = px.scatter(
    df,
    x='days_in_top10',
    y='total_audi',
    color='main_genre',
    hover_name='movieNm',
    custom_data=['main_genre'],
    title="10위권에 머문 날수 vs 총 관객 수",
    labels={'days_in_top10': '10위권에 머문 날수 (일)', 'total_audi': '총 관객 수 (명)', 'main_genre': '장르'},
    color_discrete_sequence=px.colors.qualitative.Vivid
)

fig8.update_traces(
    marker=dict(size=9, opacity=0.8),
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>10위권 머문 날수: %{x}일<br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

fig8.update_layout(
    xaxis_title="10위권에 머문 날수 (일)",
    yaxis_title="총 관객 수 (명)",
    margin=dict(t=40, b=20, l=20, r=20),
    legend_title_text="장르"
)

st.plotly_chart(fig8, use_container_width=True)
