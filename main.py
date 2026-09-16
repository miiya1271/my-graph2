import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    "1년간 박스오피스 10위권에 든 주요 개봉 영화 216편의 데이터를 바탕으로 "
    "**장르별 분포**와 **주요 변수 간의 관계**를 시각화합니다."
)

# 데이터 로드 및 전처리
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    
    # 장르 전처리: 세로막대 기호(|)로 구분된 복수 장르는 첫 번째 장르만 추출
    df['genre'] = (
        df['genre']
        .fillna('기타')
        .astype(str)
        .apply(lambda x: x.split('|')[0].strip() if '|' in x else x.strip())
    )
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 사이드바 데이터 정보
with st.sidebar:
    st.header("📊 데이터 요약")
    st.metric("총 분석 영화 수", f"{len(df)} 편")
    st.metric("총 장르 수", f"{df['genre'].nunique()} 개")
    st.metric("평균 관객수", f"{int(df['total_audi'].mean()):,} 명")
    
    st.divider()
    if st.checkbox("원본 데이터 보기"):
        st.dataframe(df)

st.divider()

# =========================================================
# 그래프 1: 장르별 영화 편수 (도넛 그래프)
# =========================================================
st.subheader("1. 장르별 영화 편수 (분포)")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# 플롯리 도넛 차트 생성
fig1 = px.pie(
    genre_counts,
    values='count',
    names='genre',
    hole=0.4,
    title='장르별 영화 편수 비율',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# 호버 시 편수와 비율이 보이도록 설정
fig1.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

fig1.update_layout(
    height=500,
    margin=dict(t=50, b=20, l=20, r=20)
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("드라마, 액션, 애니메이션 장르가 전체 개봉 영화의 과반수를 차지하며 박스오피스 상위권 영화의 장르 집중도가 높음을 알 수 있습니다.")

st.divider()

# =========================================================
# 그래프 2: 개봉 첫 주 관객수와 총 관객수의 관계
# =========================================================
st.subheader("2. 개봉 첫 주 관객수와 총 관객수의 관계")

fig2 = px.scatter(
    df,
    x='first_week_audi',
    y='total_audi',
    color='genre',
    size='days_in_top10',
    hover_name='movieNm',
    hover_data={
        'first_week_audi': ':,',
        'total_audi': ':,',
        'days_in_top10': True,
        'genre': True
    },
    labels={
        'first_week_audi': '개봉 첫 주 관객수 (명)',
        'total_audi': '총 관객수 (명)',
        'genre': '장르',
        'days_in_top10': '10위권 유지 일수'
    },
    title='개봉 첫 주 관객수 vs 총 관객수 (점 크기: 10위권 유지 일수)'
)

fig2.update_layout(height=500)
st.plotly_chart(fig2, use_container_width=True)

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("개봉 첫 주 관객수가 높은 영화일수록 최종 총 관객수도 함께 증가하는 강한 양의 상관관계를 나타냅니다.")

st.divider()

# =========================================================
# 그래프 3: 장르별 개봉일 스크린수 분포
# =========================================================
st.subheader("3. 장르별 개봉일 스크린수 분포")

fig3 = px.box(
    df,
    x='genre',
    y='first_scrn',
    color='genre',
    points='all',
    hover_name='movieNm',
    labels={'genre': '장르', 'first_scrn': '개봉일 스크린수 (개)'},
    title='장르별 개봉일 스크린수 범위 및 이상치 분포'
)

fig3.update_layout(showlegend=False, height=500)
st.plotly_chart(fig3, use_container_width=True)

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("액션이나 범죄 장르는 개봉일 스크린수 중앙값이 높아 초기 상영관 확보 규모가 다른 장르에 비해 큼을 알 수 있습니다.")
