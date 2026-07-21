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
-- View für aktuelle Daten (Power BI Seite 1)
CREATE OR REPLACE VIEW crypto_aktuell AS
SELECT 
    coin_id AS name,
    CAST(current_price AS DECIMAL(18,8)) AS current_price,
    market_cap_rank,
    CAST(high_24h AS DECIMAL(18,8)) AS high_24h,
    CAST(low_24h AS DECIMAL(18,8)) AS low_24h,
    CAST(price_change_24h AS DECIMAL(18,8)) AS price_change_24h,
    CAST(total_volume AS UNSIGNED) AS total_volume,
    collected_at
FROM market_history
WHERE coin_id REGEXP '^[a-zA-Z]'
AND collected_at = (
    SELECT MAX(m2.collected_at) 
    FROM market_history m2
    WHERE m2.coin_id = market_history.coin_id
);

-- View für historische Daten (Power BI Seite 2)
CREATE OR REPLACE VIEW crypto_historisch AS
SELECT 
    coin_id AS name,
    current_price,
    market_cap_rank,
    price_change_24h,
    total_volume,
    DATE(collected_at) AS datum
FROM market_history
WHERE coin_id REGEXP '^[a-zA-Z]'
ORDER BY coin_id, collected_at;
