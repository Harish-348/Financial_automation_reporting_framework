create database financial_db;
use financial_db;
show tables;
drop database financial_db;

-- dim_company
-- dim_financial_metrics
-- dim_market
-- dim_time
-- fact_financials
-- Linking fact_financials to dim_company and dim_time

describe dim_company;
describe dim_financial_metrics;
describe dim_market;
describe dim_time;
describe fact_financials;

SELECT * FROM dim_company LIMIT 10;
SELECT * FROM dim_financial_metrics LIMIT 10;
SELECT * FROM dim_market LIMIT 10;
SELECT * FROM dim_time LIMIT 10;
SELECT * FROM fact_financials LIMIT 10;

-- modifying the date cols
ALTER TABLE fact_financials MODIFY report_date DATE;
ALTER TABLE dim_time MODIFY report_date DATE;

ALTER TABLE dim_company MODIFY ticker VARCHAR(100);
ALTER TABLE dim_financial_metrics MODIFY ticker VARCHAR(100);
ALTER TABLE dim_market MODIFY ticker VARCHAR(100);
ALTER TABLE fact_financials MODIFY ticker VARCHAR(100);

-- Add Primary Keys
ALTER TABLE dim_company ADD PRIMARY KEY (ticker);
ALTER TABLE dim_financial_metrics ADD PRIMARY KEY (ticker, report_date);
ALTER TABLE dim_market MODIFY report_date DATE;
ALTER TABLE dim_market ADD PRIMARY KEY (ticker, report_date);
ALTER TABLE dim_time ADD PRIMARY KEY (report_date);

-- Add Foreign Keys in fact_financials
ALTER TABLE fact_financials 
ADD CONSTRAINT fk_fact_company FOREIGN KEY (ticker) 
REFERENCES dim_company (ticker);

INSERT INTO dim_time (report_date)
SELECT DISTINCT report_date 
FROM fact_financials 
WHERE report_date NOT IN (SELECT report_date FROM dim_time);

ALTER TABLE fact_financials 
ADD CONSTRAINT fk_fact_time FOREIGN KEY (report_date) 
REFERENCES dim_time (report_date);

ALTER TABLE fact_financials 
ADD CONSTRAINT fk_fact_metrics FOREIGN KEY (ticker, report_date) 
REFERENCES dim_financial_metrics (ticker, report_date);

INSERT INTO dim_market (ticker, report_date, closing_price, volume)
SELECT DISTINCT ticker, report_date, 0, 0
FROM fact_financials 
WHERE (ticker, report_date) NOT IN (SELECT ticker, report_date FROM dim_market);

ALTER TABLE fact_financials 
ADD CONSTRAINT fk_fact_market FOREIGN KEY (ticker, report_date) 
REFERENCES dim_market (ticker, report_date);

show tables;
drop table kpi_metrics;
desc kpi_metrics;
desc profitability_mart;