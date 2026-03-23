import os
import json
import hashlib
from datetime import datetime

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

def log_assessment(session_id: str, org: str, scores: dict, overall: float, narrative: str):
    entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'session_id': session_id,
        'organisation': org,
        'overall_score': round(overall, 2),
        'dimension_scores': scores,
        'narrative_hash': hashlib.sha256(narrative.encode()).hexdigest()[:16],
    }
    log_file = os.path.join(LOG_DIR, f'assessments_{datetime.utcnow().strftime("%Y%m%d")}.jsonl')
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')
