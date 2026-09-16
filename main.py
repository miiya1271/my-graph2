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

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("특정 핵심 장르(드라마, 액션, 애니메이션 등)가 전체 개봉 영화 편수의 과반수 이상을 차지하며 높은 비중을 나타냅니다.")

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

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("영화 편수가 적은 장르라 하더라도 초대형 흥행작이 포함된 경우 해당 장르가 전체 총 관객 수에서 차지하는 비중이 매우 클 수 있습니다.")

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

# 통계 데이터 계산
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

under_1m_count = len(df[df['total_audi'] < 1000000])
under_1m_ratio = (under_1m_count / len(df)) * 100

# 주요 통계 요약 카드 및 문구
col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="📌 밀집 구간 (관객 수 100만 명 미만)",
        value=f"{under_1m_count}편 ({under_1m_ratio:.1f}%)"
    )
with col2:
    st.metric(
        label="🏆 최다 관객 동원 영화",
        value=f"{top_movie_name}",
        delta=f"{top_movie_audi:,.0f} 명",
        delta_color="normal"
    )

st.markdown(
    f"📌 **분석 결과**: 대부분의 영화(**{under_1m_ratio:.1f}%**, {under_1m_count}편)가 **관객 수 100만 명 미만 구간**에 집중되어 있으며, "
    f"가장 많은 관객 수를 기록한 영화는 **'{top_movie_name}'**(총 **{top_movie_audi:,.0f}명**)입니다."
)

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("영화 시장의 흥행은 전형적인 롱테일(Long Tail) 구조를 띠어 대다수의 영화는 소규모 관객 구간에 몰려 있고 소수의 극단적 대형 흥행작이 우측 끝에 위치합니다.")

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
    hover_data={'first_scrn': True, 'total_audi': True, 'main_genre': True},
    title="개봉일 스크린수 vs 총 관객 수",
    labels={'first_scrn': '개봉일 스크린 수 (개)', 'total_audi': '총 관객 수 (명)', 'main_genre': '장르'},
    color_discrete_sequence=px.colors.qualitative.Plotly
)

fig4.update_traces(
    marker=dict(size=9, opacity=0.8),
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[2]}<br>개봉일 스크린 수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

fig4.update_layout(
    xaxis_title="개봉일 스크린 수 (개)",
    yaxis_title="총 관객 수 (명)",
    margin=dict(t=40, b=20, l=20, r=20),
    legend_title_text="장르"
)

st.plotly_chart(fig4, use_container_width=True)

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("개봉일 스크린수가 많을수록 대체로 총 관객 수도 증가하는 양의 상관관계를 보이지만, 초기 스크린수가 적어도 입소문을 통해 대흥행을 기록하는 예외 사례도 존재합니다.")
