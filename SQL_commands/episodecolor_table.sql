-- Create EpisodeColors Table
CREATE TABLE EpisodeColors (
    episode_id INT,
    color_id INT,
    PRIMARY KEY (episode_id, color_id),
    FOREIGN KEY (episode_id) REFERENCES Episodes (episode_id),
    FOREIGN KEY (color_id) REFERENCES Colors (color_id)
);
