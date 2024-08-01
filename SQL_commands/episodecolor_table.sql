-- Create Episodes_Colors Table
CREATE TABLE Episodes_Colors (
    episode_id INT,
    colors_id INT,
    PRIMARY KEY (episode_id, colors_id),
    FOREIGN KEY (episode_id) REFERENCES Episodes (id) ON DELETE CASCADE,
    FOREIGN KEY (colors_id) REFERENCES Colors (id) ON DELETE CASCADE
);
