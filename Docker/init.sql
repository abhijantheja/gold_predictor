
CREATE TABLE gold_prices (
    date_id DATE PRIMARY KEY,
    open DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    close DECIMAL(10,2),
    adj_close DECIMAL(10,2),
    volume BIGINT
);

-- 2. Stock Market Indices
CREATE TABLE stock_indices (
    date_id DATE PRIMARY KEY,
    -- S&P 500
    sp_open DECIMAL(10,2),
    sp_high DECIMAL(10,2),
    sp_low DECIMAL(10,2),
    sp_close DECIMAL(10,2),
    sp_ajclose DECIMAL(10,2),
    sp_volume BIGINT,
    -- Dow Jones
    dj_open DECIMAL(10,2),
    dj_high DECIMAL(10,2),
    dj_low DECIMAL(10,2),
    dj_close DECIMAL(10,2),
    dj_ajclose DECIMAL(10,2),
    dj_volume BIGINT,
    FOREIGN KEY (date_id) REFERENCES gold_prices(date_id)
);

-- 3. ETF Data
CREATE TABLE etf_data (
    date_id DATE PRIMARY KEY,
    -- GDX
    gdx_open DECIMAL(10,2),
    gdx_high DECIMAL(10,2),
    gdx_low DECIMAL(10,2),
    gdx_close DECIMAL(10,2),
    gdx_adj_close DECIMAL(10,2),
    gdx_volume BIGINT,
    -- USO
    uso_open DECIMAL(10,2),
    uso_high DECIMAL(10,2),
    uso_low DECIMAL(10,2),
    uso_close DECIMAL(10,2),
    uso_adj_close DECIMAL(10,2),
    uso_volume BIGINT,
    FOREIGN KEY (date_id) REFERENCES gold_prices(date_id)
);

-- 4. Exchange Rates
CREATE TABLE exchange_rates (
    date_id DATE PRIMARY KEY,
    -- Euro
    eu_price DECIMAL(10,4),
    eu_open DECIMAL(10,4),
    eu_high DECIMAL(10,4),
    eu_low DECIMAL(10,4),
    eu_trend VARCHAR(10),
    -- US Dollar Index
    usdi_price DECIMAL(10,4),
    usdi_open DECIMAL(10,4),
    usdi_high DECIMAL(10,4),
    usdi_low DECIMAL(10,4),
    usdi_volume BIGINT,
    usdi_trend VARCHAR(10),
    FOREIGN KEY (date_id) REFERENCES gold_prices(date_id)
);

-- 5. Futures Data
CREATE TABLE futures_data (
    date_id DATE PRIMARY KEY,
    -- Oil Futures
    of_price DECIMAL(10,2),
    of_open DECIMAL(10,2),
    of_high DECIMAL(10,2),
    of_low DECIMAL(10,2),
    of_volume BIGINT,
    of_trend VARCHAR(10),
    -- Silver Futures
    sf_price DECIMAL(10,2),
    sf_open DECIMAL(10,2),
    sf_high DECIMAL(10,2),
    sf_low DECIMAL(10,2),
    sf_volume BIGINT,
    sf_trend VARCHAR(10),
    FOREIGN KEY (date_id) REFERENCES gold_prices(date_id)
);

-- 6. Other Metals
CREATE TABLE other_metals (
    date_id DATE PRIMARY KEY,
    -- Platinum
    plt_price DECIMAL(10,2),
    plt_open DECIMAL(10,2),
    plt_high DECIMAL(10,2),
    plt_low DECIMAL(10,2),
    plt_trend VARCHAR(10),
    -- Palladium
    pld_price DECIMAL(10,2),
    pld_open DECIMAL(10,2),
    pld_high DECIMAL(10,2),
    pld_low DECIMAL(10,2),
    pld_trend VARCHAR(10),
    -- Rhodium
    rho_price DECIMAL(10,2),
    FOREIGN KEY (date_id) REFERENCES gold_prices(date_id)
);
CREATE TABLE final_gold_prediction (
    date_id DATE,
    open FLOAT, high FLOAT, low FLOAT, close FLOAT, adj_close FLOAT, volume INT,
    sp_open FLOAT, sp_high FLOAT, sp_low FLOAT, sp_close FLOAT, sp_ajclose FLOAT, sp_volume INT,
    dj_open FLOAT, dj_high FLOAT, dj_low FLOAT, dj_close FLOAT, dj_ajclose FLOAT, dj_volume INT,
    gdx_open FLOAT, gdx_high FLOAT, gdx_low FLOAT, gdx_close FLOAT, gdx_adj_close FLOAT, gdx_volume INT,
    uso_open FLOAT, uso_high FLOAT, uso_low FLOAT, uso_close FLOAT, uso_adj_close FLOAT, uso_volume INT,
    eu_price FLOAT, eu_open FLOAT, eu_high FLOAT, eu_low FLOAT, eu_trend FLOAT,
    usdi_price FLOAT, usdi_open FLOAT, usdi_high FLOAT, usdi_low FLOAT, usdi_volume INT, usdi_trend FLOAT,
    of_price FLOAT, of_open FLOAT, of_high FLOAT, of_low FLOAT, of_volume INT, of_trend FLOAT,
    sf_price FLOAT, sf_open FLOAT, sf_high FLOAT, sf_low FLOAT, sf_volume INT, sf_trend FLOAT,
    plt_price FLOAT, plt_open FLOAT, plt_high FLOAT, plt_low FLOAT, plt_trend FLOAT,
    pld_price FLOAT, pld_open FLOAT, pld_high FLOAT, pld_low FLOAT, pld_trend FLOAT,
    rho_price FLOAT
);
