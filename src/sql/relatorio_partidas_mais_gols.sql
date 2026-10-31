SELECT p.id_partida, p.rodada, p.data_partida,
         mand.nome AS mandante, p.gols_mandante,
         visit.nome AS visitante, p.gols_visitante,
         COALESCE(p.gols_mandante, 0) + COALESCE(p.gols_visitante, 0) AS total_gols_partida
FROM partidas p
JOIN clubes mand ON mand.id_clube = p.id_mandante
JOIN clubes visit ON visit.id_clube = p.id_visitante
WHERE p.status = 'FINALIZADA'
ORDER BY total_gols_partida DESC, p.rodada;
