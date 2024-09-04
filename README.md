# Análise de Drenagem com SAGA GIS

Este repositório contém um conjunto de scripts Python para processar um Modelo Digital de Elevação (DEM) e realizar análises de drenagem usando a ferramenta SAGA GIS. O objetivo é tratar o DEM, extrair bacias e sub-bacias, e gerar informações de drenagem com coordenadas Z e classificação de Strahler.

## Etapas do Processo

1. **Tratar DEM**
   - Preencher depressões e buracos no DEM.

2. **Extrair Bacias e Sub-Bacias**
   - Gerar as bacias e sub-bacias a partir do DEM.

3. **Extrair Drenagem**
   - Gerar a rede de drenagem com coordenadas Z e classificação de Strahler.

4. **Detectar Ângulos de 90º e Suavizar**
   - Suavizar a rede de drenagem, detectando e ajustando ângulos de 90º.

5. **Exportar como Vetor**
   - Exportar os resultados como arquivos vetoriais.