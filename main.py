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
    
    # 여러 개로 나열된 장르 중 첫 번째 장르만 추출
    df['main_genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0].strip())
    
    return df

df = load_data()

# 타이틀 및 안내 문구
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("박스오피스 상위권 개봉 영화 216편의 장르 분포 및 흥행 관객 수 관계를 탐색합니다.")
st.divider()

# ==========================================
# 1. 장르별 영화 편수 (도넛 그래프)
# ==========================================
st.subheader("1. 장르별 영화 편수 분포")

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

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("특정 핵심 장르(드라마, 액션, 애니메이션 등)가 전체 개봉 영화 편수의 과반수 이상을 차지하며 높은 비중을 나타냅니다.")

st.divider()

# ==========================================
# 2. 장르 및 영화별 총 관객 수 (트리맵)
# ==========================================
st.subheader("2. 장르 및 영화별 총 관객 수 (트리맵)")

# 트리맵 그래프 생성 (계층 구조: 전체 -> main_genre -> movieNm, 크기: total_audi)
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), 'main_genre', 'movieNm'],
    values='total_audi',
    color='main_genre',
    color_discrete_sequence=px.colors.qualitative.Set3,
    title="장르 및 영화별 총 관객 수 분포 (칸 크기: 총 관객 수)"
)

# 칸 마우스 호버 서식 설정 (영화명, 총 관객 수)
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,.0f}명<extra></extra>"
)
fig2.update_layout(
    margin=dict(t=40, b=20, l=20, r=20)
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("영화 편수가 적은 장르라 하더라도 초대형 흥행작(천만 관객 영화 등)이 포함된 경우 해당 장르가 전체 총 관객 수에서 차지하는 비중이 매우 클 수 있습니다.")
