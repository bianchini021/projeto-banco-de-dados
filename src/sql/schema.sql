-- Esquema relacional do campeonato de futebol
-- SGBD: PostgreSQL

-- 1. Clubes
CREATE TABLE IF NOT EXISTS clubes (
    id_clube BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    cidade VARCHAR(80)
);

-- 2. Jogadores
CREATE TABLE IF NOT EXISTS jogadores (
    id_jogador BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    posicao VARCHAR(20) NOT NULL,
    id_clube BIGINT NOT NULL,
    CONSTRAINT fk_jogadores_clube FOREIGN KEY (id_clube) 
        REFERENCES clubes(id_clube) ON DELETE RESTRICT,
    CONSTRAINT chk_posicao_valida CHECK (
        posicao IN ('Goleiro', 'Zagueiro', 'Lateral', 'Volante', 'Meio-Campo', 'Atacante')
    )
);

-- 3. Partidas
CREATE TABLE IF NOT EXISTS partidas (
    id_partida BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_mandante BIGINT NOT NULL,
    id_visitante BIGINT NOT NULL,
    rodada INTEGER NOT NULL,
    data_partida DATE NOT NULL,
    status VARCHAR(10) DEFAULT 'ABERTA' NOT NULL,
    gols_mandante INTEGER,
    gols_visitante INTEGER,
    CONSTRAINT fk_partidas_mandante FOREIGN KEY (id_mandante) 
        REFERENCES clubes(id_clube) ON DELETE RESTRICT,
    CONSTRAINT fk_partidas_visitante FOREIGN KEY (id_visitante) 
        REFERENCES clubes(id_clube) ON DELETE RESTRICT,
    CONSTRAINT chk_times_diferentes CHECK (id_mandante <> id_visitante),
    CONSTRAINT chk_rodada_positiva CHECK (rodada > 0),
    CONSTRAINT chk_status_valido CHECK (status IN ('ABERTA', 'FINALIZADA')),
    CONSTRAINT chk_estado_placar CHECK (
        (status = 'ABERTA' AND gols_mandante IS NULL AND gols_visitante IS NULL) OR
        (status = 'FINALIZADA' AND gols_mandante IS NOT NULL AND gols_mandante >= 0 AND gols_visitante IS NOT NULL AND gols_visitante >= 0)
    )
);

-- 4. Gols
CREATE TABLE IF NOT EXISTS gols (
    id_gol BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_partida BIGINT NOT NULL,
    id_jogador BIGINT NOT NULL,
    minuto SMALLINT NOT NULL,
    CONSTRAINT fk_gols_partida FOREIGN KEY (id_partida) 
        REFERENCES partidas(id_partida) ON DELETE RESTRICT,
    CONSTRAINT fk_gols_jogador FOREIGN KEY (id_jogador) 
        REFERENCES jogadores(id_jogador) ON DELETE RESTRICT,
    CONSTRAINT chk_minuto_valido CHECK (minuto BETWEEN 1 AND 130)
);