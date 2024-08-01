-- Create Episodes_Subjects Table
CREATE TABLE Episodes_Subjects (
    subject_id INT,
    episode_id INT,
    PRIMARY KEY (subject_id, episode_id),
    FOREIGN KEY (subject_id) REFERENCES Subjects (id) ON DELETE CASCADE,
    FOREIGN KEY (episode_id) REFERENCES Episodes (id) ON DELETE CASCADE
);
