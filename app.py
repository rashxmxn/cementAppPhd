import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time

st.set_page_config(
    page_title="Анализ состава бетона",
    layout="wide"
)

st.title("Анализ оптимального состава мелкозернистого бетона")

if 'analyze_clicked' not in st.session_state:
    st.session_state.analyze_clicked = False


data = {
    '№': [1, 2, 3, 4, 5, 6, 7, 8],
    'Cement_share (%)': [50, 60, 70, 80, 50, 60, 70, 80],
    'W_B': [0.429, 0.429, 0.358, 0.286, 0.429, 0.429, 0.322, 0.268],
    'Additive (%)': [0.09, 0.09, 0.10, 0.10, 0.09, 0.09, 0.10, 0.10],
    'Fiber (%)': [0.40, 0.40, 0.40, 0.40, 0.40, 0.40, 0.40, 0.40],
    'Rc28 (МПа)': [17.7, 18.1, 20.3, 22.9, 17.1, 18.3, 19.8, 22.6],
    'Rt (МПа)': [1.7, 1.9, 2.1, 3.2, 1.6, 2.0, 2.3, 3.4],
    'Rras (МПа)': [0.9, 1.0, 1.9, 2.5, 0.9, 1.1, 1.8, 2.9],
    'PGR (см)': [7.2, 7.2, 7.4, 7.3, 7.3, 7.1, 7.5, 7.4],
    'Experiment': ['Опыт 1', 'Опыт 1', 'Опыт 1', 'Опыт 1', 
                   'Опыт 2', 'Опыт 2', 'Опыт 2', 'Опыт 2']
}

df = pd.DataFrame(data)


df_avg = df.groupby('Cement_share (%)').agg({
    'Rc28 (МПа)': 'mean',
    'Rt (МПа)': 'mean',
    'Rras (МПа)': 'mean',
    'PGR (см)': 'mean',
    'W_B': 'mean'
}).reset_index()


st.subheader("Экспериментальные данные")

# Excel file uploader
uploaded_file = st.file_uploader(
    "Загрузите Excel файл с данными (опционально)",
    type=['xlsx', 'xls'],
    help="Файл должен содержать колонки: Cement_share (%), W_B, Additive (%), Fiber (%), Rc28 (МПа), Rt (МПа), Rras (МПа), PGR (см), Experiment"
)

if uploaded_file is not None:
    try:
        # Read Excel file
        df_uploaded = pd.read_excel(uploaded_file)
        
        # Check if required columns exist
        required_columns = ['Cement_share (%)', 'W_B', 'Additive (%)', 'Fiber (%)', 
                          'Rc28 (МПа)', 'Rt (МПа)', 'Rras (МПа)', 'PGR (см)', 'Experiment']
        
        if all(col in df_uploaded.columns for col in required_columns):
            # Remove № column from uploaded data if exists
            if '№' in df_uploaded.columns:
                df_uploaded = df_uploaded.drop(columns=['№'])
            # Add uploaded data to existing data
            df = pd.concat([df, df_uploaded], ignore_index=True)
            # Recalculate № column
            df['№'] = range(1, len(df) + 1)
            st.success(f"Добавлено {len(df_uploaded)} строк из Excel файла! Данные отображены в таблице ниже.")
        else:
            missing_cols = [col for col in required_columns if col not in df_uploaded.columns]
            st.error(f"В файле отсутствуют колонки: {', '.join(missing_cols)}")
            st.info("Используются данные по умолчанию. Проверьте формат Excel файла.")
    except Exception as e:
        st.error(f"Ошибка при чтении файла: {str(e)}")
        st.info("Используются данные по умолчанию.")

st.markdown("""
Ниже представлены результаты лабораторных испытаний образцов мелкозернистого бетона 
с различным содержанием цемента (50%, 60%, 70%, 80%).

**Инструкции:**
- **Импорт Excel:** загрузите файл выше - данные сразу появятся в таблице
- **Редактировать:** двойной клик по ячейке
- **Добавить строку:** кнопка + внизу таблицы
- **Удалить строку:** наведите на номер строки и кликните на значок корзины
""")

edited_df = st.data_editor(
    df,
    use_container_width=True,
    height=310,
    hide_index=True,
    num_rows="dynamic",
    column_config={
        '№': st.column_config.NumberColumn("№", min_value=1, max_value=100, step=1),
        'Cement_share (%)': st.column_config.NumberColumn("Cement_share (%)", min_value=0, max_value=100),
        'W_B': st.column_config.NumberColumn("W_B", format="%.3f"),
        'Additive (%)': st.column_config.NumberColumn("Additive (%)", format="%.2f"),
        'Fiber (%)': st.column_config.NumberColumn("Fiber (%)", format="%.2f"),
        'Rc28 (МПа)': st.column_config.NumberColumn("Rc28 (МПа)", format="%.1f"),
        'Rt (МПа)': st.column_config.NumberColumn("Rt (МПа)", format="%.1f"),
        'Rras (МПа)': st.column_config.NumberColumn("Rras (МПа)", format="%.1f"),
        'PGR (см)': st.column_config.NumberColumn("PGR (см)", format="%.1f"),
    }
)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("Анализировать данные", type="primary", use_container_width=True):
        st.session_state.analyze_clicked = True

if not st.session_state.analyze_clicked:
    st.stop()

analysis_container = st.empty()

with analysis_container:
    with st.spinner('Анализируем данные...'):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        time.sleep(0.2)

analysis_container.success('Анализ завершен!')
time.sleep(0.5)
analysis_container.empty()

df = edited_df.copy()

df_avg = df.groupby('Cement_share (%)').agg({
    'Rc28 (МПа)': 'mean',
    'Rt (МПа)': 'mean',
    'Rras (МПа)': 'mean',
    'PGR (см)': 'mean',
    'W_B': 'mean'
}).reset_index()

st.sidebar.header("Настройки визуализации")
show_individual = st.sidebar.checkbox("Показать отдельные эксперименты", value=False)
highlight_80 = st.sidebar.checkbox("Выделить 80% цемента", value=True)

col1, col2, col3, col4 = st.columns(4)

max_cement = df_avg.loc[df_avg['Rc28 (МПа)'].idxmax(), 'Cement_share (%)']
max_rc28 = df_avg['Rc28 (МПа)'].max()
max_rt = df_avg['Rt (МПа)'].max()
max_rras = df_avg['Rras (МПа)'].max()

with col1:
    st.metric(
        label="Оптимальная доля цемента",
        value=f"{int(max_cement)}%",
        delta="Рекомендуется"
    )

with col2:
    st.metric(
        label="Прочность на сжатие (Rc28)",
        value=f"{max_rc28:.1f} МПа",
        delta=f"+{max_rc28 - df_avg['Rc28 (МПа)'].min():.1f} МПа"
    )

with col3:
    st.metric(
        label="Прочность на растяжение (Rt)",
        value=f"{max_rt:.1f} МПа",
        delta=f"+{max_rt - df_avg['Rt (МПа)'].min():.1f} МПа"
    )

with col4:
    st.metric(
        label="Прочность на раскалывание (Rras)",
        value=f"{max_rras:.1f} МПа",
        delta=f"+{max_rras - df_avg['Rras (МПа)'].min():.1f} МПа"
    )


st.subheader("Зависимость прочностных характеристик от доли цемента")

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Прочность на сжатие после 28 суток (Rc28)',
        'Прочность на растяжение (Rt)',
        'Прочность на раскалывание (Rras)',
        'Подвижность смеси (PGR)'
    ),
    vertical_spacing=0.18,
    horizontal_spacing=0.15
)

colors = ['#3498db' if x != 80 else '#e74c3c' for x in df_avg['Cement_share (%)']]
if not highlight_80:
    colors = ['#3498db'] * len(df_avg)

fig.add_trace(
    go.Bar(
        x=df_avg['Cement_share (%)'],
        y=df_avg['Rc28 (МПа)'],
        name='Rc28',
        marker_color=colors,
        text=df_avg['Rc28 (МПа)'].round(1),
        textposition='outside',
        showlegend=False
    ),
    row=1, col=1
)

fig.add_trace(
    go.Bar(
        x=df_avg['Cement_share (%)'],
        y=df_avg['Rt (МПа)'],
        name='Rt',
        marker_color=colors,
        text=df_avg['Rt (МПа)'].round(1),
        textposition='outside',
        showlegend=False
    ),
    row=1, col=2
)

fig.add_trace(
    go.Bar(
        x=df_avg['Cement_share (%)'],
        y=df_avg['Rras (МПа)'],
        name='Rras',
        marker_color=colors,
        text=df_avg['Rras (МПа)'].round(1),
        textposition='outside',
        showlegend=False
    ),
    row=2, col=1
)

fig.add_trace(
    go.Bar(
        x=df_avg['Cement_share (%)'],
        y=df_avg['PGR (см)'],
        name='PGR',
        marker_color=colors,
        text=df_avg['PGR (см)'].round(1),
        textposition='outside',
        showlegend=False
    ),
    row=2, col=2
)

fig.update_xaxes(title_text="Доля цемента (%)", row=1, col=1)
fig.update_xaxes(title_text="Доля цемента (%)", row=1, col=2)
fig.update_xaxes(title_text="Доля цемента (%)", row=2, col=1)
fig.update_xaxes(title_text="Доля цемента (%)", row=2, col=2)

fig.update_yaxes(title_text="МПа", row=1, col=1)
fig.update_yaxes(title_text="МПа", row=1, col=2)
fig.update_yaxes(title_text="МПа", row=2, col=1)
fig.update_yaxes(title_text="см", row=2, col=2)

fig.update_layout(height=700, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Сравнительный анализ всех прочностных характеристик")

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=df_avg['Cement_share (%)'],
    y=df_avg['Rc28 (МПа)'],
    mode='lines+markers',
    name='Rc28 (сжатие)',
    line=dict(width=3),
    marker=dict(size=12)
))

fig2.add_trace(go.Scatter(
    x=df_avg['Cement_share (%)'],
    y=df_avg['Rt (МПа)'],
    mode='lines+markers',
    name='Rt (растяжение)',
    line=dict(width=3),
    marker=dict(size=12)
))

fig2.add_trace(go.Scatter(
    x=df_avg['Cement_share (%)'],
    y=df_avg['Rras (МПа)'],
    mode='lines+markers',
    name='Rras (раскалывание)',
    line=dict(width=3),
    marker=dict(size=12)
))

if highlight_80:
    fig2.add_vline(x=80, line_dash="dash", line_color="red", 
                   annotation_text="Оптимум: 80%", 
                   annotation_position="top")

fig2.update_layout(
    xaxis_title="Доля цемента (%)",
    yaxis_title="Прочность (МПа)",
    height=500,
    hovermode='x unified',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Зависимость водовяжущего отношения от доли цемента")

fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=df_avg['Cement_share (%)'],
    y=df_avg['W_B'],
    mode='lines+markers',
    name='W/B',
    line=dict(width=3, color='#9b59b6'),
    marker=dict(size=12),
    fill='tozeroy'
))

if highlight_80:
    fig3.add_vline(x=80, line_dash="dash", line_color="red",
                   annotation_text="Оптимальное значение",
                   annotation_position="top")

fig3.update_layout(
    xaxis_title="Доля цемента (%)",
    yaxis_title="Водовяжущее отношение (W/B)",
    height=400,
    showlegend=False
)

st.plotly_chart(fig3, use_container_width=True)


st.subheader("3D Визуализация")
st.markdown("""
Интерактивная 3D диаграмма показывает зависимость прочности на сжатие от доли цемента и водовяжущего отношения.  
*Используйте мышь для вращения графика*
""")

fig_3d = go.Figure(data=[go.Scatter3d(
    x=df['Cement_share (%)'],
    y=df['W_B'],
    z=df['Rc28 (МПа)'],
    mode='markers+text',
    marker=dict(
        size=df['Rt (МПа)'] * 3, 
        color=df['Cement_share (%)'], 
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Cement %"),
        line=dict(width=0.5, color='white')
    ),
    text=[f"Опыт {i+1}" for i in range(len(df))],
    textposition="top center",
    hovertemplate=
    '<b>Cement:</b> %{x}%<br>' +
    '<b>W/B:</b> %{y:.3f}<br>' +
    '<b>Rc28:</b> %{z:.1f} МПа<br>' +
    '<extra></extra>'
)])

fig_3d.update_layout(
    scene=dict(
        xaxis=dict(title='Доля цемента (%)', backgroundcolor="rgb(230, 230,230)"),
        yaxis=dict(title='Водовяжущее отношение (W/B)', backgroundcolor="rgb(230, 230,230)"),
        zaxis=dict(title='Прочность Rc28 (МПа)', backgroundcolor="rgb(230, 230,230)"),
    ),
    height=600,
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig_3d, use_container_width=True)


if show_individual:
    st.subheader("Сравнение отдельных экспериментов")
    
    fig4 = px.scatter(df, x='Cement_share (%)', y='Rc28 (МПа)', 
                      color='Experiment',
                      size='Rt (МПа)',
                      hover_data=['Rras (МПа)', 'W_B'],
                      title='Прочность на сжатие: Эксперимент 1 vs Эксперимент 2')
    
    fig4.update_layout(height=500)
    st.plotly_chart(fig4, use_container_width=True)


st.subheader("Исходные данные")

st.markdown("**Средние значения по долям цемента:**")
st.dataframe(df_avg.style.highlight_max(axis=0, subset=['Rc28 (МПа)', 'Rt (МПа)', 'Rras (МПа)']), 
             use_container_width=True, hide_index=True)

st.markdown("**Все экспериментальные данные:**")
st.dataframe(df, use_container_width=True, hide_index=True)


st.subheader("Выводы")

st.success(f"""
### Оптимальный состав: **{int(max_cement)}% цемента**

**Преимущества состава с 80% цемента:**
-   Максимальная прочность на сжатие: **{max_rc28:.1f} МПа** (+{((max_rc28/df_avg['Rc28 (МПа)'].min() - 1) * 100):.1f}% по сравнению с 50%)
-   Максимальная прочность на растяжение: **{max_rt:.1f} МПа** (+{((max_rt/df_avg['Rt (МПа)'].min() - 1) * 100):.1f}% по сравнению с 50%)
-   Максимальная прочность на раскалывание: **{max_rras:.1f} МПа** (+{((max_rras/df_avg['Rras (МПа)'].min() - 1) * 100):.1f}% по сравнению с 50%)
-   Оптимальное водовяжущее отношение: **{df_avg[df_avg['Cement_share (%)'] == 80]['W_B'].values[0]:.3f}**
-   Хорошая подвижность смеси: **{df_avg[df_avg['Cement_share (%)'] == 80]['PGR (см)'].values[0]:.1f} см**

""")

# Footer
st.markdown("""
<div style='text-align: center; color: gray;'>
     <p>Данные основаны на экспериментальных исследованиях</p>
</div>
""", unsafe_allow_html=True)
