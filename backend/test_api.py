#!/usr/bin/env python3
"""
Shine Jobs API Test Suite
Run with: python3 test_api.py
Tests the live api.py server on localhost:8000
"""
import json
import time
import urllib.request
import urllib.error
from urllib.parse import urlencode

BASE_URL = 'http://localhost:8000'
TESTS_PASSED = 0
TESTS_TOTAL = 0
FIRST_JOB_ID = None

def api_call(endpoint, params=None):
    """Make HTTP request to API."""
    url = f"{BASE_URL}{endpoint}"
    if params:
        url += '?' + urlencode(params)
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return response.status, data
    except urllib.error.HTTPError as e:
        try:
            data = json.loads(e.read().decode())
        except:
            data = {'error': str(e)}
        return e.code, data
    except Exception as e:
        return None, {'error': str(e)}

def test(name, fn):
    """Run a single test."""
    global TESTS_PASSED, TESTS_TOTAL
    TESTS_TOTAL += 1
    try:
        fn()
        TESTS_PASSED += 1
        print(f"[PASS] {name}")
        return True
    except AssertionError as e:
        print(f"[FAIL] {name}: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {name}: {e}")
        return False

def test_1_health():
    """TEST 1: Health check"""
    status, data = api_call('/api/health')
    assert status == 200, f"Expected 200, got {status}"
    assert data.get('status') == 'ok', f"Expected status='ok', got {data.get('status')}"
    assert 'cohorts' in data, "Missing 'cohorts' key"
    assert isinstance(data['cohorts'], list), "cohorts should be a list"

def test_2_cohorts():
    """TEST 2: List cohorts"""
    status, data = api_call('/api/cohorts')
    assert status == 200, f"Expected 200, got {status}"
    assert 'cohorts' in data, "Missing 'cohorts' key"
    cohorts = data['cohorts']
    assert 'work-from-home' in cohorts, "'work-from-home' not in cohorts"
    assert 'ai-ml' in cohorts, "'ai-ml' not in cohorts"

def test_3_jobs_fetch():
    """TEST 3: Fetch jobs - valid cohort"""
    global FIRST_JOB_ID
    status, data = api_call('/api/jobs', {'cohort': 'work-from-home'})
    assert status == 200, f"Expected 200, got {status}"
    assert 'jobs' in data, "Missing 'jobs' key in response"
    jobs = data['jobs']
    assert len(jobs) > 0, "No jobs returned"
    
    first_job = jobs[0]
    assert 'id' in first_job, "Job missing 'id'"
    assert 'title' in first_job, "Job missing 'title'"
    assert 'company' in first_job, "Job missing 'company'"
    assert 'location' in first_job, "Job missing 'location'"
    
    FIRST_JOB_ID = first_job['id']
    print(f"  → Fetched {len(jobs)} jobs, stored id: {FIRST_JOB_ID[:8]}...")

def test_4_invalid_cohort():
    """TEST 4: Fetch jobs - invalid cohort"""
    status, data = api_call('/api/jobs', {'cohort': 'invalid-cohort'})
    assert status == 400, f"Expected 400, got {status}"

def test_5_single_job():
    """TEST 5: Fetch single job by id"""
    if not FIRST_JOB_ID:
        raise AssertionError("No job ID stored from test 3")
    status, data = api_call(f'/api/jobs/{FIRST_JOB_ID}', {'cohort': 'work-from-home'})
    assert status == 200, f"Expected 200, got {status}"
    assert 'title' in data, "Missing 'title' in job response"
    assert data.get('id') == FIRST_JOB_ID, f"ID mismatch: {data.get('id')} != {FIRST_JOB_ID}"

def test_6_cache_clear():
    """TEST 6: Cache clear"""
    status, data = api_call('/api/cache/clear', {'cohort': 'work-from-home'})
    assert status == 200, f"Expected 200, got {status}"
    assert data.get('status') == 'ok', f"Expected status='ok', got {data.get('status')}"
    assert 'cleared' in data, "Missing 'cleared' key"
    assert 'work-from-home' in data.get('cleared', []), "'work-from-home' not in cleared list"

def test_7_live_fetch():
    """TEST 7: Fetch after cache clear (forces live SerpAPI call)"""
    status, data = api_call('/api/jobs', {'cohort': 'work-from-home'})
    assert status == 200, f"Expected 200, got {status}"
    assert 'jobs' in data, "Missing 'jobs' key"
    assert len(data['jobs']) > 0, "No jobs returned after cache clear"
    # First fetch after clear should have cached=false (or might take time to fetch)
    print(f"  → Live fetch complete, cached={data.get('cached')}")

if __name__ == '__main__':
    print("═" * 50)
    print("Shine Jobs API Test Suite")
    print("═" * 50)
    print()
    
    # Give server time to start if just launched
    time.sleep(0.5)
    
    test("Health check", test_1_health)
    test("Cohorts list", test_2_cohorts)
    test("Jobs fetch — valid cohort", test_3_jobs_fetch)
    test("Jobs fetch — invalid cohort", test_4_invalid_cohort)
    test("Single job fetch", test_5_single_job)
    test("Cache clear", test_6_cache_clear)
    test("Live fetch after cache clear", test_7_live_fetch)
    
    print()
    print("═" * 50)
    print(f"Results: {TESTS_PASSED}/{TESTS_TOTAL} tests passed")
    print("═" * 50)
    
    if TESTS_PASSED == TESTS_TOTAL:
        exit(0)
    else:
        exit(1)
