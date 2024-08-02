from flask import Flask, request, jsonify
from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.orm import sessionmaker
from models import Base, Episodes, EpisodeColors, Colors, EpisodeSubjects, Subjects
from config import DATABASE_URI

app = Flask(__name__)

# Set up the database connection
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/episodes', methods=['GET'])
def get_episodes():
    month = request.args.get('month')
    subjects = request.args.getlist('subject')
    colors = request.args.getlist('color')
    filter_type = request.args.get('filter_type', 'and')

    query = session.query(Episodes).join(EpisodeColors).join(EpisodeSubjects)
    
    filters = []
    
    if month:
        filters.append(func.month(Episodes.broadcast_date) == month)
    
    if subjects:
        subject_filters = [EpisodeSubjects.subject_id.in_(
            session.query(Subjects.id).filter(Subjects.subject_name.in_(subjects))
        )]
        if filter_type == 'and':
            filters.append(and_(*subject_filters))
        else:
            filters.append(or_(*subject_filters))
    
    if colors:
        color_filters = [EpisodeColors.color_id.in_(
            session.query(Colors.id).filter(Colors.color_name.in_(colors))
        )]
        if filter_type == 'and':
            filters.append(and_(*color_filters))
        else:
            filters.append(or_(*color_filters))

    if filters:
        if filter_type == 'and':
            query = query.filter(and_(*filters))
        else:
            query = query.filter(or_(*filters))
    
    episodes = query.all()
    result = []
    
    for episode in episodes:
        result.append({
            'title': episode.title,
            'season': episode.season,
            'episode_number': episode.episode_number,
            'broadcast_date': episode.broadcast_date.strftime('%Y-%m-%d') if episode.broadcast_date else None,
            'youtube_src': episode.youtube_src,
            'image_url': episode.image_url
        })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
