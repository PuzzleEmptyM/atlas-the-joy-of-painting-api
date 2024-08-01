-- Create Episodes Table
CREATE TABLE Episodes (
    id SERIAL PRIMARY KEY,
    date DATE,
    title VARCHAR(255) NOT NULL,
    painting_index INT,
    season INT NOT NULL,
    episode INT NOT NULL,
    notes TEXT,
    yt_link VARCHAR(255),
    website_link VARCHAR(255)
);
