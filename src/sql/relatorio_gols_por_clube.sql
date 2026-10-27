SELECT c.nome AS clube, COUNT(g.id_gol) AS total_gols
FROM clubes c
LEFT JOIN jogadores j ON j.id_clube = c.id_clube
LEFT JOIN gols g ON g.id_jogador = j.id_jogador
GROUP BY c.id_clube, c.nome
ORDER BY total_gols DESC, c.nome;
