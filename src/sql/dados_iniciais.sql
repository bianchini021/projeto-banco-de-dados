BEGIN;

DO $$
DECLARE
    id_c1 INT; id_c2 INT; id_c3 INT; id_c4 INT;
    id_j3 INT; id_j6 INT;
    id_p1 INT;
BEGIN
    -- Inserir clubes e capturar os IDs gerados
    INSERT INTO clubes (nome, cidade) VALUES ('Capixaba FC', 'Vitória') RETURNING id_clube INTO id_c1;
    INSERT INTO clubes (nome, cidade) VALUES ('Serrano', 'Domingos Martins') RETURNING id_clube INTO id_c2;
    INSERT INTO clubes (nome, cidade) VALUES ('Litorâneo', 'Vila Velha') RETURNING id_clube INTO id_c3;
    INSERT INTO clubes (nome, cidade) VALUES ('Noroeste', 'Colatina') RETURNING id_clube INTO id_c4;

    -- Inserir jogadores usando os IDs dos clubes
    INSERT INTO jogadores (nome, posicao, id_clube) VALUES ('João Silva', 'Goleiro', id_c1);
    INSERT INTO jogadores (nome, posicao, id_clube) VALUES ('Pedro Zagueiro', 'Zagueiro', id_c1);
    INSERT INTO jogadores (nome, posicao, id_clube) VALUES ('Lucas Atacante', 'Atacante', id_c1) RETURNING id_jogador INTO id_j3;

    INSERT INTO jogadores (nome, posicao, id_clube) VALUES ('Marcos Goleiro', 'Goleiro', id_c2);
    INSERT INTO jogadores (nome, posicao, id_clube) VALUES ('Paulo Volante', 'Volante', id_c2);
    INSERT INTO jogadores (nome, posicao, id_clube) VALUES ('Gabriel Meia', 'Meio-Campo', id_c2) RETURNING id_jogador INTO id_j6;

    INSERT INTO jogadores (nome, posicao, id_clube) VALUES ('Felipe Lateral', 'Lateral', id_c3);
    INSERT INTO jogadores (nome, posicao, id_clube) VALUES ('Diego Atacante', 'Atacante', id_c3);

    INSERT INTO jogadores (nome, posicao, id_clube) VALUES ('Bruno Goleiro', 'Goleiro', id_c4);
    INSERT INTO jogadores (nome, posicao, id_clube) VALUES ('Thiago Meia', 'Meio-Campo', id_c4);

    -- Inserir partidas usando os IDs dos clubes
    INSERT INTO partidas (id_mandante, id_visitante, rodada, data_partida, status, gols_mandante, gols_visitante) 
    VALUES (id_c1, id_c2, 1, '2026-10-25', 'FINALIZADA', 2, 1) RETURNING id_partida INTO id_p1;

    INSERT INTO partidas (id_mandante, id_visitante, rodada, data_partida, status) 
    VALUES (id_c3, id_c4, 1, '2026-10-26', 'ABERTA');

    INSERT INTO partidas (id_mandante, id_visitante, rodada, data_partida, status) 
    VALUES (id_c2, id_c3, 2, '2026-10-28', 'ABERTA');

    -- Inserir golos usando os IDs capturados da partida e dos jogadores
    INSERT INTO gols (id_partida, id_jogador, minuto) VALUES 
    (id_p1, id_j3, 15), (id_p1, id_j3, 42), (id_p1, id_j6, 75);
END $$;

COMMIT;