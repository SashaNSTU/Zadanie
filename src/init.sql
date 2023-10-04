CREATE TABLE IF NOT EXISTS buildings (
    id SERIAL PRIMARY KEY,
    year_of_construction INTEGER,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);