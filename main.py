from table_loaders.episodes import load_episodes
from table_loaders.colors import load_colors
from table_loaders.subjects import load_subjects
from table_loaders.episode_colors import load_episode_colors
from table_loaders.episode_subjects import load_episode_subjects

def main():
    load_episodes()
    load_colors()
    load_subjects()
    load_episode_colors()
    load_episode_subjects()

if __name__ == '__main__':
    main()
