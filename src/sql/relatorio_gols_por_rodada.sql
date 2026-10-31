SELECT p.rodada, COUNT(g.id_gol) AS total_gols_rodada
FROM partidas p
JOIN gols g ON g.id_partida = p.id_partida
GROUP BY p.rodada
ORDER BY p.rodada;
