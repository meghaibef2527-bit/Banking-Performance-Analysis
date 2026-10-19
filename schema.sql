-- Works in SQLite, MySQL and PostgreSQL (minor type differences)
CREATE TABLE bank_quarterly (
    bank            VARCHAR(60) NOT NULL,
    sector          VARCHAR(10) NOT NULL,  -- 'PSU' or 'Private'
    quarter         VARCHAR(7)  NOT NULL,  -- e.g. 2024Q3
    deposits_crore  DECIMAL(14,1),
    advances_crore  DECIMAL(14,1),
    nii_crore       DECIMAL(14,1),
    casa_pct        DECIMAL(5,2),
    gnpa_pct        DECIMAL(5,2),
    PRIMARY KEY (bank, quarter)
);
