import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Glossário Jurídico - Descomplicando o Direito",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1f3a60;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .term-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #1f3a60;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .news-card {
        background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 12px;
        border-left: 4px solid #17a2b8;
    }
    .definition-card {
        background: linear-gradient(135deg, #f0f7ff 0%, #e3f2fd 100%);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        border: 2px solid #1f3a60;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 15px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do estado
if 'termo_selecionado' not in st.session_state:
    st.session_state.termo_selecionado = None

# Dados completos do glossário
@st.cache_data
def carregar_dados_juridicos():
    termos = [
        {
            "termo": "Habeas Corpus", "definicao": "Remédio constitucional que visa proteger o direito de locomoção do indivíduo, evitando ou cessando violência ou coação em sua liberdade de ir e vir.", "area": "Direito Constitucional", "fonte": "STF", "data": "2024-01-15", "exemplo": "O Habeas Corpus foi concedido para um preso que estava encarcerado sem mandado judicial válido.", "sinonimos": ["HC", "Remédio Constitucional"], "relacionados": ["Mandado de Segurança", "Mandado de Injunção", "Habeas Data"], "detalhes": "Previsto no art. 5º, LXVIII da Constituição Federal"
        },
        {
            "termo": "Ação Rescisória", "definicao": "Ação judicial que tem por objeto desconstituir sentença transitada em julgado, por vícios que a tornam nula ou inexistente.", "area": "Direito Processual Civil", "fonte": "STJ", "data": "2024-01-12", "exemplo": "A parte ajuizou ação rescisória para anular sentença proferida com base em documento falso.", "sinonimos": ["Rescisão da Sentença"], "relacionados": ["Coisa Julgada", "Recurso", "Sentença"], "detalhes": "Disciplinada nos arts. 966 a 976 do CPC"
        },
        {
            "termo": "Usucapião", "definicao": "Modo de aquisição da propriedade móvel ou imóvel pela posse prolongada, contínua e incontestada, atendidos os requisitos legais.", "area": "Direito Civil", "fonte": "Câmara dos Deputados", "data": "2024-01-10", "exemplo": "O proprietário adquiriu o imóvel por usucapião após 15 anos de posse mansa e pacífica.", "sinonimos": ["Prescrição Aquisitiva"], "relacionados": ["Propriedade", "Posse", "Direitos Reais"], "detalhes": "Regulada pelos arts. 1.238 a 1.244 do Código Civil"
        },
        {
            "termo": "Crime Culposo", "definicao": "Conduta voluntária que produz resultado ilícito não desejado, decorrente de imprudência, negligência ou imperícia.", "area": "Direito Penal", "fonte": "Planalto", "data": "2024-01-08", "exemplo": "O motorista foi condenado por crime culposo de homicídio após causar acidente por excesso de velocidade.", "sinonimos": ["Culpa", "Delito Culposo"], "relacionados": ["Crime Doloso", "Culpa", "Dolo"], "detalhes": "Definido no art. 18, II do Código Penal"
        },
        {
            "termo": "Princípio da Isonomia", "definicao": "Princípio constitucional que estabelece a igualdade de todos perante a lei, sem distinção de qualquer natureza.", "area": "Direito Constitucional", "fonte": "STF", "data": "2024-01-05", "exemplo": "O princípio da isonomia foi invocado para garantir tratamento igualitário a homens e mulheres em concurso público.", "sinonimos": ["Igualdade", "Isonomia"], "relacionados": ["Princípios Constitucionais", "Direitos Fundamentais"], "detalhes": "Previsto no caput do art. 5º da Constituição Federal"
        },
        {
            "termo": "Desconsideração da Personalidade Jurídica", "definicao": "Instrumento que permite ultrapassar a autonomia patrimonial da pessoa jurídica para atingir bens particulares de seus sócios.", "area": "Direito Empresarial", "fonte": "STJ", "data": "2024-01-03", "exemplo": "A desconsideração foi aplicada para cobrar dívidas da empresa diretamente dos sócios.", "sinonimos": ["Desconsideração", "Disregard Doctrine"], "relacionados": ["Pessoa Jurídica", "Responsabilidade"], "detalhes": "Prevista no art. 50 do Código Civil e art. 28 do CDC"
        },
        {
            "termo": "Mandado de Segurança", "definicao": "Remédio constitucional para proteger direito líquido e certo não amparado por habeas corpus ou habeas data.", "area": "Direito Constitucional", "fonte": "STF", "data": "2023-12-28", "exemplo": "Concedido mandado de segurança para assegurar vaga em concurso público.", "sinonimos": ["MS"], "relacionados": ["Habeas Corpus", "Direito Líquido e Certo"], "detalhes": "Previsto no art. 5º, LXIX da CF"
        },
        {
            "termo": "Coisa Julgada", "definicao": "Qualidade da sentença que não mais admite recurso, tornando-se imutável.", "area": "Direito Processual Civil", "fonte": "STJ", "data": "2023-12-25", "exemplo": "A sentença transitou em julgado após esgotados todos os recursos.", "sinonimos": ["Res Judicata"], "relacionados": ["Sentença", "Recurso"], "detalhes": "Disciplinada no art. 502 do CPC"
        },
        {
            "termo": "Agravo de Instrumento", "definicao": "Recurso cabível contra decisão interlocutória que causa lesão grave e de difícil reparação.", "area": "Direito Processual Civil", "fonte": "STJ", "data": "2023-12-20", "exemplo": "O agravo foi interposto contra decisão que indeferiu prova pericial.", "sinonimos": ["Agravo"], "relacionados": ["Recurso", "Decisão Interlocutória"], "detalhes": "Disciplinado nos arts. 1.015 a 1.020 do CPC"
        },
        {
            "termo": "Jus Postulandi", "definicao": "Capacidade de postular em juízo, ou seja, de propor ações e defender-se perante o Poder Judiciário.", "area": "Direito Processual", "fonte": "STJ", "data": "2023-12-15", "exemplo": "A defensoria pública exerce o jus postulandi em favor dos necessitados.", "sinonimos": ["Capacidade Postulatória"], "relacionados": ["Legitimidade", "Capacidade Processual"], "detalhes": "Em regra, exercido por advogados (art. 1º da Lei 8.906/94)"
        }
    ]
    return pd.DataFrame(termos)

# Funções para APIs (simuladas)
class APIServicosJuridicos:
    @staticmethod
    def buscar_stf(termo):
        stf_data = {
            "Habeas Corpus": {
                "definicao": "Remédio constitucional que visa proteger o direito de locomoção do indivíduo, conforme art. 5º, LXVIII da CF.",
                "jurisprudencia": "STF - HC 123.456/DF: Concedido habeas corpus para trancamento de ação penal.",
                "fonte": "STF - Supremo Tribunal Federal"
            },
            "Mandado de Segurança": {
                "definicao": "Remédio constitucional para proteger direito líquido e certo não amparado por habeas corpus.",
                "jurisprudencia": "STF - MS 34.567/RJ: Concedido mandado de segurança para direito público.",
                "fonte": "STF - Supremo Tribunal Federal"
            }
        }
        return stf_data.get(termo, {})

    @staticmethod
    def buscar_stj(termo):
        stj_data = {
            "Ação Rescisória": {
                "definicao": "Ação para desconstituir sentença transitada em julgado por vícios.",
                "exemplo": "STJ - REsp 1.234.567/SP: Admitida ação rescisória por documento novo.",
                "fonte": "STJ - Superior Tribunal de Justiça"
            },
            "Usucapião": {
                "definicao": "Modo de aquisição da propriedade pela posse prolongada.",
                "exemplo": "STJ - REsp 987.654/RS: Reconhecida usucapião extraordinária.",
                "fonte": "STJ - Superior Tribunal de Justiça"
            }
        }
        return stj_data.get(termo, {})

# Funções de visualização
def criar_grafico_areas(df):
    contagem_areas = df['area'].value_counts().reset_index()
    contagem_areas.columns = ['Área', 'Quantidade']
    fig = px.pie(contagem_areas, values='Quantidade', names='Área', 
                 title='📊 Distribuição por Área do Direito',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=450)
    return fig

def buscar_noticias(termo):
    noticias_base = {
        "Habeas Corpus": [
            {"titulo": "STF concede habeas corpus e solta réu", "fonte": "Consultor Jurídico", "data": "2024-01-15", "resumo": "Decisão do Supremo por falta de provas consistentes."},
            {"titulo": "Novo entendimento sobre habeas corpus", "fonte": "Jornal do Direito", "data": "2024-01-10", "resumo": "Tribunais discutem aplicação em prisão cautelar."}
        ],
        "Ação Rescisória": [
            {"titulo": "STJ admite ação rescisória por documento novo", "fonte": "Migalhas", "data": "2024-01-12", "resumo": "Reconhecida possibilidade de rescisão de sentença."}
        ]
    }
    return noticias_base.get(termo, [{"titulo": f"Notícias sobre {termo}", "fonte": "Glossário Jurídico", "data": "2024-01-01", "resumo": "Em breve mais notícias sobre este termo."}])

# Páginas do aplicativo
def exibir_pagina_inicial(df):
    st.markdown("### 🎯 Bem-vindo ao Glossário Jurídico Digital")
    st.write("Site desenvolvido para **descomplicar o Direito** com definições claras e acessíveis.")
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Termos", len(df))
    with col2: st.metric("Áreas", df['area'].nunique())
    with col3: st.metric("Fontes", df['fonte'].nunique())
    with col4: st.metric("Atualização", df['data'].max())
    
    # Gráficos
    col1, col2 = st.columns(2)
    with col1: st.plotly_chart(criar_grafico_areas(df), use_container_width=True)
    
    # Termos recentes
    st.markdown("### 🔄 Termos Recentes")
    termos_recentes = df.sort_values('data', ascending=False).head(4)
    for _, termo in termos_recentes.iterrows():
        with st.container():
            st.markdown(f'<div class="term-card">', unsafe_allow_html=True)
            st.markdown(f"#### {termo['termo']}")
            st.write(termo['definicao'][:120] + "...")
            st.caption(f"**Área:** {termo['area']} | **Fonte:** {termo['fonte']}")
            if st.button("Ver detalhes", key=f"home_{termo['termo']}"):
                st.session_state.termo_selecionado = termo['termo']
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

def exibir_explorar_termos(df, area_selecionada, fonte_selecionada, termo_busca):
    st.markdown("### 📚 Explorar Termos Jurídicos")
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if area_selecionada != "Todas": df_filtrado = df_filtrado[df_filtrado['area'] == area_selecionada]
    if fonte_selecionada != "Todas": df_filtrado = df_filtrado[df_filtrado['fonte'] == fonte_selecionada]
    if termo_busca: df_filtrado = df_filtrado[df_filtrado['termo'].str.contains(termo_busca, case=False)]
    
    # Resultados
    if len(df_filtrado) > 0:
        st.success(f"**{len(df_filtrado)}** termo(s) encontrado(s)")
        for _, termo in df_filtrado.iterrows():
            with st.container():
                st.markdown(f'<div class="term-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"#### {termo['termo']}")
                    st.write(termo['definicao'])
                    st.caption(f"**Área:** {termo['area']} | **Fonte:** {termo['fonte']}")
                with col2:
                    if st.button("🔍 Detalhes", key=f"exp_{termo['termo']}"):
                        st.session_state.termo_selecionado = termo['termo']
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Nenhum termo encontrado. Tente outros filtros.")

def exibir_pagina_termo(df, termo_nome):
    termo_data = df[df['termo'] == termo_nome].iloc[0]
    
    st.markdown(f'<div class="definition-card">', unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"# {termo_data['termo']}")
        st.markdown(f"**Área:** {termo_data['area']} | **Fonte:** {termo_data['fonte']} | **Data:** {termo_data['data']}")
    with col2:
        if st.button("← Voltar"): st.session_state.termo_selecionado = None; st.rerun()
    
    st.markdown("---")
    
    # Conteúdo
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📖 Definição")
        st.info(termo_data['definicao'])
        
        st.markdown("### 💼 Exemplo Prático")
        st.write(termo_data['exemplo'])
        
        if termo_data['detalhes']:
            st.markdown("### 📋 Detalhes Legais")
            st.write(termo_data['detalhes'])
        
        # APIs
        st.markdown("### ⚖️ Consulta aos Tribunais")
        col_api1, col_api2 = st.columns(2)
        with col_api1:
            with st.expander("🔍 STF - Supremo Tribunal Federal"):
                dados_stf = APIServicosJuridicos.buscar_stf(termo_nome)
                if dados_stf: st.write(dados_stf.get('definicao', 'Consulta simulada'))
        with col_api2:
            with st.expander("🔍 STJ - Superior Tribunal de Justiça"):
                dados_stj = APIServicosJuridicos.buscar_stj(termo_nome)
                if dados_stj: st.write(dados_stj.get('definicao', 'Consulta simulada'))
    
    with col2:
        st.markdown("### 🏷️ Informações")
        if termo_data['sinonimos']:
            st.markdown("**Sinônimos:**")
            for s in termo_data['sinonimos']: st.write(f"• {s}")
        
        st.markdown("**Relacionados:**")
        for r in termo_data['relacionados']: st.write(f"• {r}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Notícias
    st.markdown("### 📰 Notícias Recentes")
    noticias = buscar_noticias(termo_nome)
    for noticia in noticias:
        with st.container():
            st.markdown(f'<div class="news-card">', unsafe_allow_html=True)
            st.markdown(f"#### {noticia['titulo']}")
            st.write(noticia['resumo'])
            st.caption(f"Fonte: {noticia['fonte']} | Data: {noticia['data']}")
            st.markdown('</div>', unsafe_allow_html=True)

def exibir_pagina_noticias(df):
    st.markdown("### 📰 Últimas Notícias Jurídicas")
    st.info("Em desenvolvimento: integração com Google News API")
    
    termos_com_noticias = ["Habeas Corpus", "Ação Rescisória", "Usucapião"]
    for termo in termos_com_noticias:
        with st.expander(f"📢 {termo}"):
            noticias = buscar_noticias(termo)
            for noticia in noticias:
                st.write(f"**{noticia['titulo']}**")
                st.caption(f"{noticia['fonte']} - {noticia['data']}")
                st.write(noticia['resumo'])
                st.markdown("---")

def exibir_pagina_sobre():
    st.markdown("### ℹ️ Sobre o Projeto")
    st.write("""
    **Glossário Jurídico: Descomplicando o Direito**
    
    **Desenvolvido por:** Carolina Souza, Lara Carneiro e Mayra Rizkalla
    **Turma A** - Projeto P2 Programação 2
    
    **🎯 Objetivos:**
    - Fornecer definições claras de termos jurídicos
    - Contextualizar conceitos com exemplos práticos
    - Integrar notícias relacionadas aos termos
    - Oferecer ferramenta de estudo gratuita
    
    **⚙️ Tecnologias:**
    - Streamlit para interface web
    - Python como linguagem principal
    - APIs jurídicas para dados atualizados
    - Plotly para visualizações interativas
    
    **📞 Fontes Oficiais:**
    - STF (Supremo Tribunal Federal)
    - STJ (Superior Tribunal de Justiça)
    - Câmara dos Deputados
    - Base de dados do Planalto
    """)

# App principal
def main():
    st.markdown('<h1 class="main-header">⚖️ Glossário Jurídico</h1>', unsafe_allow_html=True)
    st.markdown("### Descomplicando o Direito para estudantes e leigos")
    
    df = carregar_dados_juridicos()
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn.pixabay.com/photo/2017/01/31/14/26/law-2024670_1280.png", width=80)
        st.title("🔍 Navegação")
        
        st.subheader("Buscar Termo")
        termo_busca = st.text_input("Digite o termo jurídico:")
        
        st.subheader("🎯 Filtros")
        area_selecionada = st.selectbox("Área do Direito", ["Todas"] + list(df['area'].unique()))
        fonte_selecionada = st.selectbox("Fonte", ["Todas"] + list(df['fonte'].unique()))
        
        st.subheader("🔥 Termos Populares")
        for termo in df['termo'].head(6):
            if st.button(termo, key=f"side_{termo}"):
                st.session_state.termo_selecionado = termo
                st.rerun()
        
        st.markdown("---")
        st.metric("Total de Termos", len(df))
    
    # Rotas
    if st.session_state.termo_selecionado:
        exibir_pagina_termo(df, st.session_state.termo_selecionado)
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["🏠 Início", "📚 Explorar", "📰 Notícias", "ℹ️ Sobre"])
        with tab1: exibir_pagina_inicial(df)
        with tab2: exibir_explorar_termos(df, area_selecionada, fonte_selecionada, termo_busca)
        with tab3: exibir_pagina_noticias(df)
        with tab4: exibir_pagina_sobre()

if __name__ == "__main__":
    main()
