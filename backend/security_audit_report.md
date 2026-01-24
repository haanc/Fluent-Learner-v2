# 🔒 Security Audit Report

**Project:** `/mnt/c/Users/hancao/.gemini/antigravity/scratch/language-learner/fluent-learner-v2/backend`
**Audit Time:** 2026-01-23T18:24:04.958242
**Rules File:** `/home/hancao/.claude/skills/security-audit/rules.yaml`
**Files Scanned:** 29

---

## 📊 Summary

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | 24 |
| 🟠 HIGH | 23 |
| 🟡 MEDIUM | 3 |
| 🟢 LOW | 23 |
| 🔵 INFO | 0 |
| **Total** | **73** |

---

## 📋 Authorization

### 1. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/ai.py:49`

**Code:**
```python
def lookup_word(req: LookupRequest, llm_provider: LLMProvider = Depends(get_request_llm_provider)):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 2. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/ai.py:68`

**Code:**
```python
def explain_context(req: ExplainRequest, llm_provider: LLMProvider = Depends(get_request_llm_provider)):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 3. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/ai.py:78`

**Code:**
```python
def chat_tutor(req: ChatRequest, llm_provider: LLMProvider = Depends(get_request_llm_provider)):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 4. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/ai.py:91`

**Code:**
```python
def test_llm_connection(llm_provider: LLMProvider = Depends(get_request_llm_provider)):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 5. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/ai.py:183`

**Code:**
```python
def download_whisper_model(req: ModelDownloadRequest, background_tasks: BackgroundTasks):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 6. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/ai.py:254`

**Code:**
```python
def get_download_progress(model_name: str):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 7. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/ai.py:284`

**Code:**
```python
def delete_whisper_model(model_name: str):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 8. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/media.py:246`

**Code:**
```python
def list_media(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 9. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/media.py:259`

**Code:**
```python
def get_media(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 10. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/media.py:274`

**Code:**
```python
def create_media(media: MediaSource, session: Session = Depends(get_session)):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 11. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/media.py:282`

**Code:**
```python
def download_media(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 12. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/media.py:308`

**Code:**
```python
def retranscribe_media(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 13. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/media.py:342`

**Code:**
```python
def delete_media(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 14. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/media.py:387`

**Code:**
```python
def list_segments(media_id: UUID, session: Session = Depends(get_session)):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 15. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/media.py:401`

**Code:**
```python
def create_segments(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 16. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/media.py:421`

**Code:**
```python
def translate_segments(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 17. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/streaming.py:123`

**Code:**
```python
async def stream_bilibili_realtime(url: str, request: Request):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 18. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/streaming.py:168`

**Code:**
```python
async def get_stream_url(url: str):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 19. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/streaming.py:189`

**Code:**
```python
async def proxy_video(url: str, request: Request):
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 20. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/vocab.py:35`

**Code:**
```python
def list_saved_words(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 21. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/vocab.py:55`

**Code:**
```python
def save_word(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 22. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/vocab.py:84`

**Code:**
```python
def review_word(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

### 23. 🟠 [HIGH] API route may be missing authentication

**Rule ID:** `auth-missing-decorator`

**Description:** Route handler does not appear to have an authentication decorator

**Location:** `routes/vocab.py:142`

**Code:**
```python
def delete_saved_word(
```

**Fix:** Add @login_required, @auth_required, or use Depends() for authentication

---

## 📋 Injection

### 1. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `chunked_transcription.py:219`

**Code:**
```python
executor.submit(self.transcribe_chunk, chunk, whisper_provider): chunk
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 2. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `routes/media.py:255`

**Code:**
```python
return db.exec(statement).all()
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 3. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `routes/media.py:324`

**Code:**
```python
existing_segments = session.exec(
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 4. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `routes/media.py:373`

**Code:**
```python
subtitles = session.exec(
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 5. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `routes/media.py:392`

**Code:**
```python
segments = session.exec(
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 6. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `routes/media.py:435`

**Code:**
```python
segments = session.exec(
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 7. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `routes/streaming.py:42`

**Code:**
```python
proc = await asyncio.create_subprocess_exec(
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 8. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `routes/streaming.py:94`

**Code:**
```python
proc = await asyncio.create_subprocess_exec(
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 9. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `routes/streaming.py:210`

**Code:**
```python
proc = await asyncio.create_subprocess_exec(
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 10. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `routes/streaming.py:312`

**Code:**
```python
proc = await asyncio.create_subprocess_exec(
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 11. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `routes/vocab.py:51`

**Code:**
```python
return session.exec(query).all()
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 12. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_db.py:10`

**Code:**
```python
session.exec(text("ALTER TABLE savedword ADD COLUMN language VARCHAR DEFAULT 'en'"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 13. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_db.py:19`

**Code:**
```python
session.exec(text("ALTER TABLE savedword ADD COLUMN next_review_at DATETIME"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 14. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_db.py:26`

**Code:**
```python
session.exec(text("ALTER TABLE savedword ADD COLUMN interval FLOAT DEFAULT 0.0"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 15. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_db.py:33`

**Code:**
```python
session.exec(text("ALTER TABLE savedword ADD COLUMN easiness_factor FLOAT DEFAULT 2.5"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 16. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_db.py:40`

**Code:**
```python
session.exec(text("ALTER TABLE savedword ADD COLUMN repetitions INTEGER DEFAULT 0"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 17. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_db.py:47`

**Code:**
```python
session.exec(text("ALTER TABLE savedword ADD COLUMN owner_id VARCHAR DEFAULT 'guest'"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 18. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_db.py:48`

**Code:**
```python
session.exec(text("CREATE INDEX ix_savedword_owner_id ON savedword (owner_id)"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 19. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_db.py:55`

**Code:**
```python
session.exec(text("ALTER TABLE mediasource ADD COLUMN owner_id VARCHAR DEFAULT 'guest'"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 20. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_db.py:56`

**Code:**
```python
session.exec(text("CREATE INDEX ix_mediasource_owner_id ON mediasource (owner_id)"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 21. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_v1.py:10`

**Code:**
```python
conn.execute(text("ALTER TABLE mediasource ADD COLUMN status VARCHAR DEFAULT 'ready'"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 22. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_v1.py:17`

**Code:**
```python
conn.execute(text("ALTER TABLE mediasource ADD COLUMN error_message VARCHAR"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

### 23. 🔴 [CRITICAL] exec() function call detected

**Rule ID:** `injection-exec`

**Description:** exec() can execute arbitrary code and is a major security risk

**Location:** `scripts/migrations/migrate_v1.py:24`

**Code:**
```python
conn.execute(text("ALTER TABLE mediasource ADD COLUMN cover_image VARCHAR"))
```

**Fix:** Avoid dynamic code execution; use safer alternatives

---

## 📋 RateLimit

### 1. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/ai.py:49`

**Code:**
```python
def lookup_word(req: LookupRequest, llm_provider: LLMProvider = Depends(get_request_llm_provider)):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 2. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/ai.py:68`

**Code:**
```python
def explain_context(req: ExplainRequest, llm_provider: LLMProvider = Depends(get_request_llm_provider)):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 3. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/ai.py:78`

**Code:**
```python
def chat_tutor(req: ChatRequest, llm_provider: LLMProvider = Depends(get_request_llm_provider)):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 4. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/ai.py:91`

**Code:**
```python
def test_llm_connection(llm_provider: LLMProvider = Depends(get_request_llm_provider)):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 5. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/ai.py:183`

**Code:**
```python
def download_whisper_model(req: ModelDownloadRequest, background_tasks: BackgroundTasks):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 6. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/ai.py:254`

**Code:**
```python
def get_download_progress(model_name: str):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 7. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/ai.py:284`

**Code:**
```python
def delete_whisper_model(model_name: str):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 8. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/media.py:246`

**Code:**
```python
def list_media(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 9. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/media.py:259`

**Code:**
```python
def get_media(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 10. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/media.py:274`

**Code:**
```python
def create_media(media: MediaSource, session: Session = Depends(get_session)):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 11. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/media.py:282`

**Code:**
```python
def download_media(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 12. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/media.py:308`

**Code:**
```python
def retranscribe_media(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 13. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/media.py:342`

**Code:**
```python
def delete_media(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 14. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/media.py:387`

**Code:**
```python
def list_segments(media_id: UUID, session: Session = Depends(get_session)):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 15. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/media.py:401`

**Code:**
```python
def create_segments(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 16. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/media.py:421`

**Code:**
```python
def translate_segments(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 17. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/streaming.py:123`

**Code:**
```python
async def stream_bilibili_realtime(url: str, request: Request):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 18. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/streaming.py:168`

**Code:**
```python
async def get_stream_url(url: str):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 19. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/streaming.py:189`

**Code:**
```python
async def proxy_video(url: str, request: Request):
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 20. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/vocab.py:35`

**Code:**
```python
def list_saved_words(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 21. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/vocab.py:55`

**Code:**
```python
def save_word(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 22. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/vocab.py:84`

**Code:**
```python
def review_word(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

### 23. 🟢 [LOW] API route may be missing rate limiting

**Rule ID:** `ratelimit-missing`

**Description:** Route handler does not appear to have rate limiting

**Location:** `routes/vocab.py:142`

**Code:**
```python
def delete_saved_word(
```

**Fix:** Consider adding rate limiting with slowapi or flask-limiter

---

## 📋 SSRF

### 1. 🟡 [MEDIUM] Localhost reference in code

**Rule ID:** `ssrf-localhost`

**Description:** Hardcoded localhost may cause issues in production or indicate SSRF risk

**Location:** `main.py:82`

**Code:**
```python
uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
```

**Fix:** Use environment variables for service URLs

---

### 2. 🟡 [MEDIUM] Localhost reference in code

**Rule ID:** `ssrf-localhost`

**Description:** Hardcoded localhost may cause issues in production or indicate SSRF risk

**Location:** `ai/providers/llm.py:57`

**Code:**
```python
if host_lower in ('localhost', '127.0.0.1', '::1', '0.0.0.0'):
```

**Fix:** Use environment variables for service URLs

---

### 3. 🟡 [MEDIUM] Localhost reference in code

**Rule ID:** `ssrf-localhost`

**Description:** Hardcoded localhost may cause issues in production or indicate SSRF risk

**Location:** `ai/providers/llm.py:57`

**Code:**
```python
if host_lower in ('localhost', '127.0.0.1', '::1', '0.0.0.0'):
```

**Fix:** Use environment variables for service URLs

---

### 4. 🔴 [CRITICAL] Cloud metadata service URL detected

**Rule ID:** `ssrf-metadata-service`

**Description:** Reference to cloud metadata service could enable credential theft via SSRF

**Location:** `ai/providers/llm.py:74`

**Code:**
```python
if host_lower.startswith('169.254.') or host_lower == '169.254.169.254':
```

**Fix:** Remove hardcoded metadata URLs; if needed, use proper IAM roles

---


*Report generated by Security Audit Skill*