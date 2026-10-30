INSERT INTO clubes (nome, cidade) VALUES 
('Capixaba FC', 'Vitória'), ('Serrano', 'Domingos Martins'),
('Litorâneo', 'Vila Velha'), ('Noroeste', 'Colatina');

INSERT INTO jogadores (nome, posicao, id_clube) VALUES 
('João Silva', 'Goleiro', 1), ('Pedro Zagueiro', 'Zagueiro', 1),
('Lucas Atacante', 'Atacante', 1), ('Marcos Goleiro', 'Goleiro', 2),
('Paulo Volante', 'Volante', 2), ('Gabriel Meia', 'Meio-Campo', 2),
('Felipe Lateral', 'Lateral', 3), ('Diego Atacante', 'Atacante', 3),
('Bruno Goleiro', 'Goleiro', 4), ('Thiago Meia', 'Meio-Campo', 4);

INSERT INTO partidas (id_mandante, id_visitante, rodada, data_partida, status, gols_mandante, gols_visitante) 
VALUES (1, 2, 1, '2026-10-25', 'FINALIZADA', 2, 1),
       (3, 4, 1, '2026-10-26', 'ABERTA', NULL, NULL),
       (2, 3, 2, '2026-10-28', 'ABERTA', NULL, NULL);

INSERT INTO gols (id_partida, id_jogador, minuto) VALUES 
(1, 3, 15), (1, 3, 42), (1, 6, 75);