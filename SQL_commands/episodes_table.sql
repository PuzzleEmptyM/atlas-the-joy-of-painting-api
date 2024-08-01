-- Create Episodes Table
CREATE TABLE Episodes (
    episode_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    season INT NOT NULL,
    episode_number INT NOT NULL,
    broadcast_date DATE,
    img_src VARCHAR(255),
    youtube_src VARCHAR(255),
    num_colors INT
);
