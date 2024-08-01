-- Create EpisodeSubjects Table
CREATE TABLE EpisodeSubjects (
    episode_id INT,
    subject_id INT,
    PRIMARY KEY (episode_id, subject_id),
    FOREIGN KEY (episode_id) REFERENCES Episodes (episode_id),
    FOREIGN KEY (subject_id) REFERENCES Subjects (subject_id)
);
