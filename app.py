from flask import Flask, render_template, request
import json
from collections import Counter

app = Flask(__name__)

def load_data():
    # Laden der Sprecher-Daten
    with open('data/10_2025_speakers_import.json', 'r', encoding='utf-8') as f:
        speakers = json.load(f)
    
    # Laden der Talk-Daten
    with open('data/20_2025_talks_import.json', 'r', encoding='utf-8') as f:
        talks = json.load(f)
    
    # Verknüpfen der Talks mit den Sprechern
    for talk_id, talk in talks.items():
        speaker_id = talk.get('speakerId')
        if speaker_id and str(speaker_id) in speakers:
            talk['speaker'] = speakers[str(speaker_id)]
        
        # Co-Sprecher hinzufügen, falls vorhanden
        co_speaker_ids = [talk.get('coSpeakerId1'), talk.get('coSpeakerId2')]
        talk['co_speakers'] = []
        for co_id in co_speaker_ids:
            if co_id and str(co_id) in speakers:
                talk['co_speakers'].append(speakers[str(co_id)])
    
    return talks, speakers

def get_all_keywords(talks):
    """Extrahiert alle Keywords aus den Talks und zählt ihre Häufigkeit"""
    all_keywords = []
    for talk in talks.values():
        if talk.get('keywords'):
            keywords = [k.strip() for k in talk['keywords'].split(',')]
            all_keywords.extend(keywords)
    
    # Zähle die Häufigkeit jedes Keywords
    keyword_counter = Counter(all_keywords)
    
    # Sortiere nach Häufigkeit (absteigend)
    sorted_keywords = sorted(keyword_counter.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_keywords

@app.route('/')
def index():
    talks, speakers = load_data()
    
    # Sammle alle einzigartigen Themen, Sprachen und Level
    topics = sorted(set(talk.get('topicId') for talk_id, talk in talks.items() if talk.get('topicId')))
    languages = sorted(set(talk.get('languageId') for talk_id, talk in talks.items() if talk.get('languageId')))
    levels = sorted(set(talk.get('levelId') for talk_id, talk in talks.items() if talk.get('levelId')))
    
    # Filterung nach Keyword, falls in der URL angegeben
    keyword_filter = request.args.get('keyword')
    if keyword_filter:
        filtered_talks = {}
        for talk_id, talk in talks.items():
            if talk.get('keywords') and keyword_filter.lower() in talk.get('keywords').lower():
                filtered_talks[talk_id] = talk
        talks = filtered_talks
    
    return render_template('index.html', 
                          talks=talks, 
                          speakers=speakers, 
                          topics=topics,
                          languages=languages,
                          levels=levels,
                          keyword_filter=keyword_filter)

@app.route('/keywords')
def keywords():
    talks, _ = load_data()
    keywords = get_all_keywords(talks)
    
    # Finde die maximale Häufigkeit für die Skalierung
    max_count = keywords[0][1] if keywords else 1
    
    return render_template('keywords.html', keywords=keywords, max_count=max_count)

@app.route('/talk/<talk_id>')
def talk_detail(talk_id):
    talks, speakers = load_data()
    if talk_id in talks:
        return render_template('talk_detail.html', talk=talks[talk_id])
    return "Talk nicht gefunden", 404

@app.route('/speaker/<speaker_id>')
def speaker_detail(speaker_id):
    talks, speakers = load_data()
    if speaker_id in speakers:
        # Finde alle Talks dieses Sprechers
        speaker_talks = {talk_id: talk for talk_id, talk in talks.items() 
                        if talk.get('speakerId') == int(speaker_id) or 
                           talk.get('coSpeakerId1') == int(speaker_id) or 
                           talk.get('coSpeakerId2') == int(speaker_id)}
        
        return render_template('speaker_detail.html', 
                              speaker=speakers[speaker_id], 
                              talks=speaker_talks)
    return "Sprecher nicht gefunden", 404

if __name__ == '__main__':
    app.run(debug=True)
