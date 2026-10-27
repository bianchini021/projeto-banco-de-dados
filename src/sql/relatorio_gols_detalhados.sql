SELECT p.id_partida, p.data_partida,
       mand.nome AS mandante, visit.nome AS visitante,
       j.nome AS jogador, c.nome AS clube_jogador, g.minuto
FROM gols g
JOIN partidas p ON p.id_partida = g.id_partida
JOIN jogadores j ON j.id_jogador = g.id_jogador
JOIN clubes c ON c.id_clube = j.id_clube
JOIN clubes mand ON mand.id_clube = p.id_mandante
JOIN clubes visit ON visit.id_clube = p.id_visitante
ORDER BY p.id_partida, g.minuto, j.nome;
