
CREATE TABLE IF NOT EXISTS setup_locale (
    locale_id   VARCHAR PRIMARY KEY,
    locale_name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS text_resources (
    key     VARCHAR NOT NULL,
    locale  VARCHAR NOT NULL,
    text    VARCHAR,

    PRIMARY KEY (key, locale),
    FOREIGN KEY (locale) REFERENCES setup_locale(locale_id)
);
