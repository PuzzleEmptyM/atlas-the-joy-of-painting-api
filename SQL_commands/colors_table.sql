-- Create Colors Table
CREATE TABLE Colors (
    color_id SERIAL PRIMARY KEY,
    color_name VARCHAR(100) NOT NULL,
    color_hex VARCHAR(7)
);
