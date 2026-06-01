#!/usr/bin/env python3
"""
Shine Jobs Backend API
Serves job listings from SerpAPI with local caching.
Run: python3 api.py
"""
import json
import os
import sys
import hashlib
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs, urlparse
from io import StringIO

# SerpAPI configuration
SERP_API_KEY = "4dd5346115933770466bd9c0c0840964c5c2369374bfc94b20b7b6b7c3adf45d"
PORT = 8000
CACHE_DIR = "cache"

# Load keywords.json
KEYWORDS_FILE = "keywords.json"
COHORTS = {}

try:
    with open(KEYWORDS_FILE, 'r') as f:
        config = json.load(f)
        COHORTS = config.get('cohorts', {})
except Exception as e:
    print(f"[ERROR] Failed to load {KEYWORDS_FILE}: {e}")
    sys.exit(1)

# Create cache directory
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_cache_file(cohort):
    """Return cache file path for cohort."""
    return os.path.join(CACHE_DIR, f"{cohort}.json")

def is_cache_fresh(cohort):
    """Check if cache for cohort is still valid."""
    if cohort not in COHORTS:
        return False
    cache_file = get_cache_file(cohort)
    if not os.path.exists(cache_file):
        return False
    try:
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        fetched_at = datetime.fromisoformat(cache_data.get('fetched_at', ''))
        ttl_hours = COHORTS[cohort].get('cache_ttl_hours', 6)
        age = datetime.now() - fetched_at
        return age < timedelta(hours=ttl_hours)
    except Exception:
        return False

def get_cache_age_hours(cohort):
    """Return age of cache in hours, or None if doesn't exist."""
    cache_file = get_cache_file(cohort)
    if not os.path.exists(cache_file):
        return None
    try:
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        fetched_at = datetime.fromisoformat(cache_data.get('fetched_at', ''))
        age = datetime.now() - fetched_at
        return age.total_seconds() / 3600
    except Exception:
        return None

def read_cache(cohort):
    """Read and return cached jobs, or None."""
    cache_file = get_cache_file(cohort)
    if not os.path.exists(cache_file):
        return None
    try:
        with open(cache_file, 'r') as f:
            return json.load(f)
    except Exception:
        return None

def write_cache(cohort, jobs_data):
    """Write jobs to cache with timestamp."""
    cache_file = get_cache_file(cohort)
    cache_payload = {
        'fetched_at': datetime.now().isoformat(),
        'jobs': jobs_data
    }
    try:
        with open(cache_file, 'w') as f:
            json.dump(cache_payload, f)
        return True
    except Exception:
        return False

def md5_hash(text):
    """Generate MD5 hash of text."""
    return hashlib.md5(text.encode()).hexdigest()

def map_job_from_serp(job_raw):
    """Map SerpAPI job response to our job object."""
    title = job_raw.get('title', '')
    company = job_raw.get('company_name', '')
    location = job_raw.get('location', '')
    
    job_id = md5_hash(f"{title}{company}{location}")
    apply_options = job_raw.get('apply_options', [])
    apply_url = apply_options[0].get('link', '') if apply_options else ''
    
    return {
        'id': job_id,
        'title': title,
        'company': company,
        'location': location,
        'description': job_raw.get('description', '')[:300],
        'via': job_raw.get('via'),
        'thumbnail': job_raw.get('thumbnail'),
        'extensions': job_raw.get('extensions', []),
        'detected': job_raw.get('detected_extensions', {}),
        'apply_options': apply_options,
        'apply_url': apply_url
    }

def fetch_from_serp(cohort):
    """Fetch jobs from SerpAPI for cohort."""
    if cohort not in COHORTS:
        return None
    
    cohort_config = COHORTS[cohort]
    query = cohort_config.get('query')
    location = cohort_config.get('location', 'India')
    limit = cohort_config.get('limit', 50)
    
    try:
        from serpapi import Client
        client = Client(api_key=SERP_API_KEY)
        results = client.search({
            'q': query,
            'location': location,
            'engine': 'google_jobs',
            'start': 0,
            'num': limit
        })
        
        jobs_raw = results.get('jobs_results', [])
        jobs_mapped = [map_job_from_serp(j) for j in jobs_raw]
        
        # Cache the results
        write_cache(cohort, jobs_mapped)
        
        return jobs_mapped
    except Exception as e:
        print(f"[ERROR] SerpAPI fetch failed for {cohort}: {e}")
        return None

def get_jobs(cohort):
    """Get jobs for cohort: from cache if fresh, else fetch."""
    if cohort not in COHORTS:
        return None
    
    if is_cache_fresh(cohort):
        cached = read_cache(cohort)
        if cached:
            return cached.get('jobs', []), True, cached.get('fetched_at')
    
    jobs = fetch_from_serp(cohort)
    if jobs is None:
        # Try fallback to stale cache
        cached = read_cache(cohort)
        if cached:
            return cached.get('jobs', []), True, cached.get('fetched_at')
        return [], False, None
    
    return jobs, False, datetime.now().isoformat()

class JobAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for job API."""
    
    def do_GET(self):
        """Handle GET requests."""
        self.send_cors_headers()
        
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        # Extract single-value params (parse_qs returns lists)
        params = {k: v[0] if v else None for k, v in query_params.items()}
        
        # Route handling
        if path == '/api/health':
            self.handle_health()
        elif path == '/api/cohorts':
            self.handle_cohorts()
        elif path == '/api/jobs' and not path.endswith('/'):
            cohort = params.get('cohort')
            self.handle_jobs_list(cohort)
        elif path.startswith('/api/jobs/') and len(path) > len('/api/jobs/'):
            job_id = path.split('/api/jobs/')[1].split('?')[0]
            cohort = params.get('cohort')
            self.handle_job_detail(job_id, cohort)
        elif path == '/api/cache/clear':
            cohort = params.get('cohort')
            self.handle_cache_clear(cohort)
        else:
            self.send_error(404, "Not Found")
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_cors_headers()
        self.send_response(200)
        self.end_headers()
    
    def send_cors_headers(self):
        """Send CORS headers."""
        # Will be added to response by send_response
        pass
    
    def send_json_response(self, status_code, data):
        """Send JSON response with CORS headers."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def handle_health(self):
        """GET /api/health"""
        cache_status = {}
        for cohort in COHORTS.keys():
            age = get_cache_age_hours(cohort)
            cache_status[cohort] = {
                'cached': age is not None,
                'age_hours': round(age, 1) if age is not None else None
            }
        
        response = {
            'status': 'ok',
            'cohorts': list(COHORTS.keys()),
            'cache_status': cache_status
        }
        self.send_json_response(200, response)
    
    def handle_cohorts(self):
        """GET /api/cohorts"""
        response = {'cohorts': COHORTS}
        self.send_json_response(200, response)
    
    def handle_jobs_list(self, cohort):
        """GET /api/jobs?cohort=..."""
        if not cohort or cohort not in COHORTS:
            self.send_json_response(400, {
                'error': 'Invalid or missing cohort parameter',
                'available_cohorts': list(COHORTS.keys())
            })
            return
        
        jobs, from_cache, fetched_at = get_jobs(cohort)
        
        response = {
            'cohort': cohort,
            'total': len(jobs),
            'cached': from_cache,
            'fetched_at': fetched_at,
            'jobs': jobs
        }
        self.send_json_response(200, response)
    
    def handle_job_detail(self, job_id, cohort):
        """GET /api/jobs/<id>?cohort=..."""
        if not cohort or cohort not in COHORTS:
            self.send_json_response(400, {
                'error': 'Invalid or missing cohort parameter',
                'available_cohorts': list(COHORTS.keys())
            })
            return
        
        jobs, _, _ = get_jobs(cohort)
        
        for job in jobs:
            if job.get('id') == job_id:
                self.send_json_response(200, job)
                return
        
        self.send_json_response(404, {
            'error': f'Job {job_id} not found in cohort {cohort}'
        })
    
    def handle_cache_clear(self, cohort):
        """GET /api/cache/clear?cohort=..."""
        if not cohort:
            self.send_json_response(400, {
                'error': 'Missing cohort parameter (use "all" for all cohorts)'
            })
            return
        
        cleared = []
        
        if cohort == 'all':
            for c in COHORTS.keys():
                cache_file = get_cache_file(c)
                if os.path.exists(cache_file):
                    try:
                        os.remove(cache_file)
                        cleared.append(c)
                    except Exception:
                        pass
        elif cohort in COHORTS:
            cache_file = get_cache_file(cohort)
            if os.path.exists(cache_file):
                try:
                    os.remove(cache_file)
                    cleared.append(cohort)
                except Exception:
                    pass
        else:
            self.send_json_response(400, {
                'error': f'Unknown cohort: {cohort}',
                'available_cohorts': list(COHORTS.keys())
            })
            return
        
        response = {
            'cleared': cleared,
            'status': 'ok'
        }
        self.send_json_response(200, response)
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        return

if __name__ == '__main__':
    server = HTTPServer(('localhost', PORT), JobAPIHandler)
    
    print(f"[API] Shine Jobs Backend")
    print(f"[API] Port     : {PORT}")
    print(f"[API] Cohorts  : {', '.join(COHORTS.keys())}")
    print(f"[API] Docs     : http://localhost:{PORT}/api/health")
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[API] Shutting down...")
        server.server_close()
        sys.exit(0)
