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

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("개봉일 스크린수가 많을수록 대체로 총 관객 수도 증가하는 양의 상관관계를 보이지만, 초기 스크린수가 적어도 입소문을 통해 대흥행을 기록하는 예외 사례도 존재합니다.")

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

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("장르별 중간값(중앙값)은 대개 수십만 명 수준에 형성되어 있으나, 일부 장르에서는 상자 밖의 극단적 흥행작(이상치)이 발생하여 동일 장르 내에서도 영화 간 관객 수 편차가 매우 큼을 알 수 있습니다.")

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

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("개봉일 스크린수가 많고 개봉 첫 주 관객 수(버블 크기)가 큰 영화일수록 최종 총 관객 수도 대폭 높게 형성되며, 초기 집객 성과가 최종 흥행 성공 여부에 강력한 영향을 미침을 알 수 있습니다.")

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

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("국가별로 제작되거나 개봉된 주요 영화 장르의 구조적 차이를 확인할 수 있으며, 특정 국가(예: 한국, 미국)에서 공급되는 장르의 다양성 및 집중도를 파악할 수 있습니다.")

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

# 그래프 해석 구역
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("10위권에 머문 날수가 길수록 총 관객 수가 증가하는 명확한 양의 상관관계를 보여줍니다. 초기 상영 스크린 수나 개봉 첫 주 흥행도 중요하지만, 10위권 내에서 오래 잔류하는 '장기 흥행(롱런)' 능력이 최종 천만 관객 등 대형 흥행을 만드는 데 핵심 요소임을 알 수 있습니다.")
