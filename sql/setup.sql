-- Crypto Dashboard – Datenbankstruktur
-- Historisierung: jeder /coin-Aufruf schreibt neue Zeilen in market_history

CREATE DATABASE IF NOT EXISTS crypto;

USE crypto;

DROP TABLE IF EXISTS market_history;
DROP TABLE IF EXISTS coins;

CREATE TABLE IF NOT EXISTS coins (
    id          VARCHAR(100) PRIMARY KEY NOT NULL,
    symbol      VARCHAR(20),
    name        VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS market_history (
    id               INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    coin_id          VARCHAR(100) NOT NULL,
    current_price    DECIMAL(18, 8),   -- 8 Nachkommastellen für kleine Coins (z.B. Shiba Inu)
    market_cap_rank  INT,
    high_24h         DECIMAL(18, 8),
    low_24h          DECIMAL(18, 8),
    price_change_24h DECIMAL(18, 8),
    total_volume     BIGINT,
    last_updated     DATETIME,
    collected_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (coin_id) REFERENCES coins(id)
);
