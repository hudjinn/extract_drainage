WITH RECURSIVE upstream_segments AS (
    -- Passo 1: Seleciona o segmento inicial
    SELECT
        seg.*
    FROM
        drainage AS seg
    WHERE
        seg.segment_id = 20735 -- Segmento inicial fornecido

    UNION ALL

    -- Passo 2: Seleciona todos os segmentos conectados a montante
    SELECT
        seg.*
    FROM
        drainage AS seg
    JOIN
        upstream_segments AS up ON up.NODE_A = seg.NODE_B
)
-- Passo 3: Retorna todos os segmentos a montante
SELECT *
FROM upstream_segments;
