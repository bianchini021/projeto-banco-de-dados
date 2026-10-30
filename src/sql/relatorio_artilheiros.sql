SELECT j.nome AS jogador, c.nome AS clube, COUNT(g.id_gol) AS total_gols
FROM jogadores j
JOIN clubes c ON c.id_clube = j.id_clube
JOIN gols g ON g.id_jogador = j.id_jogador
GROUP BY j.id_jogador, j.nome, c.nome
ORDER BY total_gols DESC, j.nome;