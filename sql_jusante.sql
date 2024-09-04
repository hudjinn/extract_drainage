WITH RECURSIVE downstream_segments AS (
    -- Começa com o segmento fornecido
    SELECT
        s1.id,
        s1.node_a,
        s1.node_b,
        s1."order",
        s1.geom
    FROM
        drainage s1
    WHERE
        s1.id = 1234  -- Substitua 1234 pelo ID do segmento fornecido

    UNION ALL

    -- Adiciona todos os segmentos conectados a jusante
    SELECT
        s2.id,
        s2.node_a,
        s2.node_b,
        s2."order",
        s2.geom
    FROM
        drainage s2
        JOIN downstream_segments ds ON s2.node_a = ds.node_b
    WHERE
        s2."order" >= (SELECT "order" FROM drainage WHERE id = 1234)  -- Ordem de Strahler do segmento fornecido
)
SELECT DISTINCT
    id,
    node_a,
    node_b,
    "order",
    geom
FROM
    downstream_segments
