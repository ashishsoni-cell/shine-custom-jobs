#!/usr/bin/env python3
"""
Shine CLP Engine Backend — server.py
Simple stdlib HTTP server with cohort management, caching, and SerpAPI integration.
"""
import json
import os
import re
import sys
import time
import threading
import hashlib
from datetime import datetime, timedelta
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# === Configuration ===
SERP_API_KEY = "YOUR_SERPAPI_KEY"
PORT = 8080
JOBS_PER_COHORT = 50
CACHE_TTL_HOURS = 6
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')
COHORTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'cohorts.json')
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')

# Cities to cycle through
CITIES = ["Delhi","Mumbai","Bangalore","Hyderabad","Pune","Chennai","Noida","Gurgaon"]

# Query templates (simple variations)
QUERY_TEMPLATES = ["{kw}", "{kw} hiring", "{kw} openings"]

# In-memory status tracking
cohort_status = {}
cohorts_lock = threading.Lock()
FETCH_PAUSED = True

# Ensure cache dir exists
os.makedirs(CACHE_DIR, exist_ok=True)

# Load or init cohorts.json
if not os.path.exists(COHORTS_FILE):
    with open(COHORTS_FILE, 'w') as f:
        json.dump({}, f)

with open(COHORTS_FILE, 'r') as f:
    try:
        COHORTS = json.load(f)
    except Exception:
        COHORTS = {}

# Helper: slugify
def slugify(text):
    text = (text or '').lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

# Helper: cache file path
def cache_path(slug):
    return os.path.join(CACHE_DIR, f"{slug}.json")

# Helper: read cache
def read_cache(slug):
    p = cache_path(slug)
    if not os.path.exists(p):
        return None
    try:
        with open(p, 'r') as f:
            return json.load(f)
    except Exception:
        return None

# Helper: write cache
def write_cache(slug, keyword, jobs):
    payload = {
        'slug': slug,
        'keyword': keyword,
        'jobs': jobs,
        'fetched_at': datetime.utcnow().isoformat(),
        'count': len(jobs)
    }
    with open(cache_path(slug), 'w') as f:
        json.dump(payload, f)
    return payload

# Hash for de-duping
def job_hash(title, company, location):
    raw = (title or '')[:80] + (company or '') + (location or '')
    cleaned = re.sub(r'[^a-z0-9]', '', raw.lower())
    return hashlib.sha1(cleaned.encode()).hexdigest()[:20]

# Attempt to import serpapi
SERP_AVAILABLE = False
try:
    from serpapi import GoogleSearch
    SERP_AVAILABLE = True
except Exception:
    SERP_AVAILABLE = False

# Background fetch thread
def fetch_jobs_for_cohort(slug, keyword, limit=JOBS_PER_COHORT):
    global FETCH_PAUSED
    print(f"[FETCH START] slug={slug} keyword={keyword}", flush=True)
    print(f"[SERP KEY] {'set' if SERP_API_KEY else 'MISSING'}", flush=True)
    with cohorts_lock:
        cohort_status[slug] = {'status': 'fetching', 'count': 0}
    jobs = []
    seen = set()
    # rotate queries and cities
    qi = 0
    ci = 0
    if not SERP_AVAILABLE:
        # fallback: create mock jobs so frontend can test
        for i in range(min(10, limit)):
            title = f"{keyword} Role {i+1}"
            company = f"Company {i+1}"
            loc = CITIES[i % len(CITIES)]
            jid = job_hash(title, company, loc)
            jobs.append({
                'id': jid,
                'title': title,
                'company': company,
                'location': loc,
                'via': 'mock',
                'posted_at': 'Today',
                'work_from_home': 'work from home' in (keyword or '').lower(),
                'schedule': 'Full Time',
                'salary': '',
                'description': f'Sample description for {title}'[:400],
                'apply_url': 'https://www.shine.com/pages/myshine/job-apply-flow?job-apply-flow=true',
                'thumbnail': '',
                'fetched_at': datetime.utcnow().isoformat()
            })
            seen.add(jid)
            with cohorts_lock:
                cohort_status[slug]['count'] = len(jobs)
            time.sleep(0.05)
        write_cache(slug, keyword, jobs)
        with cohorts_lock:
            cohort_status[slug]['status'] = 'done'
        return
    
    try:
        while len(jobs) < limit:
            if FETCH_PAUSED:
                with cohorts_lock:
                    cohort_status[slug] = {'status': 'paused', 'count': len(jobs)}
                time.sleep(5)
                continue
            qtmpl = QUERY_TEMPLATES[qi % len(QUERY_TEMPLATES)]
            city = CITIES[ci % len(CITIES)]
            query = qtmpl.format(kw=keyword)
            params = {
                'q': query,
                'engine': 'google_jobs',
                'location': city,
                'num': 10,
                'api_key': SERP_API_KEY,
                'gl': 'in'
            }
            try:
                search = GoogleSearch(params)
                results = search.get_dict()
                jobs_raw = results.get('jobs_results', [])
                print(f"[SERP CALL] query={query} results={len(jobs_raw)}", flush=True)
                for jr in jobs_raw:
                    title = jr.get('title')
                    company = jr.get('company_name')
                    location = jr.get('location')
                    jid = job_hash(title, company, location)
                    if jid in seen:
                        continue
                    seen.add(jid)
                    apply_options = jr.get('apply_options') or []
                    apply_url = apply_options[0].get('link','') if apply_options else ''
                    job = {
                        'id': jid,
                        'title': title,
                        'company': company,
                        'location': location,
                        'via': jr.get('via'),
                        'posted_at': jr.get('posted_date_parsed') or '',
                        'work_from_home': jr.get('work_from_home', False),
                        'schedule': jr.get('schedule', ''),
                        'salary': jr.get('salary', ''),
                        'description': (jr.get('description','') or '')[:400],
                        'apply_url': apply_url,
                        'thumbnail': jr.get('thumbnail',''),
                        'fetched_at': datetime.utcnow().isoformat()
                    }
                    jobs.append(job)
                    with cohorts_lock:
                        cohort_status[slug]['count'] = len(jobs)
                    if len(jobs) >= limit:
                        break
                # rotate
            except Exception as e:
                print(f"[fetch error] {e}")
            qi += 1
            ci += 1
            time.sleep(0.5)
        write_cache(slug, keyword, jobs)
        with cohorts_lock:
            cohort_status[slug]['status'] = 'done'
    except Exception as e:
        with cohorts_lock:
            cohort_status[slug] = {'status': 'error', 'count': len(jobs), 'error': str(e)}

# Thread starter
def start_fetch_thread(slug, keyword):
    t = threading.Thread(target=fetch_jobs_for_cohort, args=(slug, keyword), daemon=True)
    t.start()
    return t

# HTTP Handler
class CLPHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        # Routes
        if path == '/' or path == '/index.html':
            return self.serve_file('index.html')
        if path == '/admin':
            return self.serve_admin_inline()
        if path == '/home':
            return self.serve_home_inline()
        if path.startswith('/jobs/'):
            slug = path.split('/jobs/')[1].strip('/')
            return self.serve_clp(slug)
        if path.startswith('/api/'):
            return self.handle_api_get(path, qs)
        # static frontend files
        fn = path.lstrip('/')
        if fn:
            return self.serve_file(fn)
        return self.send_response(404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode() if length else ''
        data = {}
        try:
            data = json.loads(raw) if raw else {}
        except Exception:
            data = {}
        if path == '/api/cohorts/create':
            return self.handle_create_cohort(data)
        if path == '/api/cohorts/refresh':
            return self.handle_refresh_cohort(data)
        if path == '/api/fetch/pause':
            return self.handle_fetch_pause()
        if path == '/api/fetch/resume':
            return self.handle_fetch_resume()
        return self.send_json(404, {'error': 'Not found'})

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith('/api/cohorts/'):
            slug = path.split('/api/cohorts/')[1]
            return self.handle_delete_cohort(slug)
        return self.send_json(404, {'error': 'Not found'})

    # --- file serving ---
    def serve_file(self, relpath):
        fp = os.path.join(FRONTEND_DIR, relpath)
        if not os.path.exists(fp):
            return self.send_response(404)
        try:
            with open(fp, 'rb') as f:
                content = f.read()
            self.send_response(200)
            ctype = 'text/html'
            if relpath.endswith('.js'):
                ctype = 'application/javascript'
            elif relpath.endswith('.css'):
                ctype = 'text/css'
            elif relpath.endswith('.json'):
                ctype = 'application/json'
            self.send_header('Content-Type', ctype)
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(content)
        except Exception:
            self.send_response(500)

    def serve_clp(self, slug):
        # serve clp.html and inject slug via a small script
        fp = os.path.join(FRONTEND_DIR, 'clp.html')
        if not os.path.exists(fp):
            return self.send_response(404)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                html = f.read()
            inject = f"<script>window.COHORT_SLUG=\"{slug}\";</script>"
            if '<!-- INJECT_SLUG -->' in html:
                html = html.replace('<!-- INJECT_SLUG -->', inject)
            else:
                html = html.replace('</head>', inject + '\n</head>')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except Exception:
            self.send_response(500)

    def serve_admin_inline(self):
        # Serve admin.html as inline HTML
        fp = os.path.join(FRONTEND_DIR, 'admin.html')
        if not os.path.exists(fp):
            return self.send_response(404)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                html = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except Exception:
            self.send_response(500)

    def serve_home_inline(self):
        # Serve cohorts grid as inline HTML
        fp = os.path.join(FRONTEND_DIR, 'index.html')
        if not os.path.exists(fp):
            return self.send_response(404)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                html = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except Exception:
            self.send_response(500)

    def handle_fetch_pause(self):
        global FETCH_PAUSED
        FETCH_PAUSED = True
        return self.send_json(200, {'fetching': 'paused'})

    def handle_fetch_resume(self):
        global FETCH_PAUSED
        FETCH_PAUSED = False
        return self.send_json(200, {'fetching': 'active'})

    def api_fetch_status(self):
        return self.send_json(200, {'paused': FETCH_PAUSED})

    def api_serp_test(self):
        if not SERP_AVAILABLE:
            return self.send_json(400, {'error': 'serpapi not installed'})
        if not SERP_API_KEY or SERP_API_KEY == 'YOUR_SERPAPI_KEY':
            return self.send_json(400, {'error': 'Missing SERP_API_KEY'})
        params = {
            'q': 'test',
            'engine': 'google_jobs',
            'location': 'India',
            'num': 1,
            'api_key': SERP_API_KEY,
            'gl': 'in'
        }
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            return self.send_json(200, {'status': 'ok', 'results': results})
        except Exception as e:
            return self.send_json(500, {'error': str(e)})

    # --- API handlers ---
    def handle_api_get(self, path, qs):
        if path == '/api/cohorts':
            return self.api_cohorts()
        if path == '/api/serp/test':
            return self.api_serp_test()
        if path == '/api/fetch/status':
            return self.api_fetch_status()
        if path == '/api/status':
            slug = qs.get('cohort', [None])[0]
            return self.api_status(slug)
        if path == '/api/jobs':
            slug = qs.get('cohort', [None])[0]
            return self.api_jobs_list(slug)
        return self.send_json(404, {'error': 'Not found'})

    def api_cohorts(self):
        # Return cohorts with status + job count
        resp = {}
        for slug, meta in COHORTS.items():
            status = cohort_status.get(slug, {'status': 'pending', 'count': 0})
            # count from cache if exists
            cache = read_cache(slug)
            count = cache.get('count') if cache else status.get('count', 0)
            resp[slug] = {
                'name': meta.get('name'),
                'keyword': meta.get('keyword'),
                'slug': slug,
                'created': meta.get('created'),
                'status': status.get('status', 'pending'),
                'count': count
            }
        return self.send_json(200, {'cohorts': resp})

    def api_status(self, slug):
        if not slug or slug not in COHORTS:
            return self.send_json(400, {'error': 'Missing or unknown cohort'})
        status = cohort_status.get(slug, {'status': 'pending', 'count': 0})
        cache = read_cache(slug)
        count = cache.get('count') if cache else status.get('count', 0)
        return self.send_json(200, {'status': status.get('status','pending'), 'count': count})

    def api_jobs_list(self, slug):
        if not slug or slug not in COHORTS:
            return self.send_json(400, {'error': 'Missing or unknown cohort'})
        # Check cache freshness
        cache = read_cache(slug)
        if cache:
            fetched = cache.get('fetched_at')
            try:
                fetched_dt = datetime.fromisoformat(fetched)
                age = datetime.utcnow() - fetched_dt
                fresh = age < timedelta(hours=CACHE_TTL_HOURS)
            except Exception:
                fresh = False
        else:
            fresh = False
        # If not fresh and not already fetching, start a fetch
        if not fresh and cohort_status.get(slug, {}).get('status') != 'fetching':
            start_fetch_thread(slug, COHORTS[slug]['keyword'])
        # Return cache if exists otherwise empty + status
        resp = cache if cache else {'slug': slug, 'keyword': COHORTS[slug]['keyword'], 'jobs': [], 'fetched_at': None, 'count': 0}
        status = cohort_status.get(slug, {'status': 'pending', 'count': 0})
        resp['status'] = status.get('status', 'pending')
        return self.send_json(200, resp)

    # POST create cohort
    def handle_create_cohort(self, data):
        name = data.get('name')
        keyword = data.get('keyword')
        if not name or not keyword:
            return self.send_json(400, {'error': 'Missing name or keyword'})
        slug = slugify(name)
        if slug in COHORTS:
            return self.send_json(400, {'error': 'Cohort already exists', 'slug': slug})
        meta = {'name': name, 'keyword': keyword, 'slug': slug, 'created': datetime.utcnow().isoformat()}
        COHORTS[slug] = meta
        # persist
        with open(COHORTS_FILE, 'w') as f:
            json.dump(COHORTS, f)
        # start background fetch
        with cohorts_lock:
            cohort_status[slug] = {'status': 'fetching', 'count': 0}
        start_fetch_thread(slug, keyword)
        url = f"/jobs/{slug}"
        return self.send_json(200, {'slug': slug, 'url': url, 'message': 'Cohort created and fetch started'})

    def handle_refresh_cohort(self, data):
        slug = data.get('slug')
        if not slug or slug not in COHORTS:
            return self.send_json(400, {'error': 'Missing or unknown slug'})
        with cohorts_lock:
            cohort_status[slug] = {'status': 'fetching', 'count': 0}
        start_fetch_thread(slug, COHORTS[slug]['keyword'])
        return self.send_json(200, {'slug': slug, 'message': 'Refresh triggered'})

    def handle_delete_cohort(self, slug):
        if not slug or slug not in COHORTS:
            return self.send_json(400, {'error': 'Missing or unknown slug'})
        try:
            del COHORTS[slug]
            with open(COHORTS_FILE, 'w') as f:
                json.dump(COHORTS, f)
            cp = cache_path(slug)
            if os.path.exists(cp):
                os.remove(cp)
            with cohorts_lock:
                cohort_status.pop(slug, None)
            return self.send_json(200, {'deleted': slug, 'status': 'ok'})
        except Exception as e:
            return self.send_json(500, {'error': str(e)})

    # utility: write json response
    def send_json(self, code, obj):
        body = json.dumps(obj).encode('utf-8')
        self.send_response(code)
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

# Startup helpers

def auto_start_missing_fetches():
    for slug, meta in COHORTS.items():
        if not read_cache(slug):
            with cohorts_lock:
                cohort_status[slug] = {'status': 'fetching', 'count': 0}
            start_fetch_thread(slug, meta['keyword'])

# Run server
if __name__ == '__main__':
    banner = '\n'.join([
        '╔══════════════════════════════════════════════╗',
        '║       Shine CLP Engine — Starting up         ║',
        '╠══════════════════════════════════════════════╣',
        f'║  Home   →  http://localhost:{PORT}             ║',
        f'║  Admin  →  http://localhost:{PORT}/admin       ║',
        '╚══════════════════════════════════════════════╝',
    ])
    print(banner)
    server = ThreadingHTTPServer(('0.0.0.0', PORT), CLPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n[server] Shutting down')
        server.server_close()
