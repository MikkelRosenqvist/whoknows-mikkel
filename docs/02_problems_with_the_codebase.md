# Problems with the Codebase — WhoKnows Legacy Application

## Critical Security Vulnerabilities

### 1. SQL Injection (Multiple Locations)

Every database query uses Python string formatting (`%s`) instead of parameterized queries. This allows attackers to inject arbitrary SQL.

**Examples:**

```python
# app.py - get_user_id()
g.db.execute("SELECT id FROM users WHERE username = '%s'" % username)

# app.py - search route
query_db("SELECT * FROM pages WHERE language = '%s' AND content LIKE '%%%s%%'" % (language, q))

# app.py - api_login
query_db("SELECT * FROM users WHERE username = '%s'" % request.form['username'], one=True)
```

An attacker could log in as any user, extract the entire database, or delete all data by crafting a malicious username or search query.

**Fix:** Use parameterized queries: `g.db.execute("SELECT id FROM users WHERE username = ?", (username,))`

### 2. MD5 Password Hashing (Insecure + No Salt)

```python
def hash_password(password):
    hash_object = hashlib.md5(password_bytes)
    password_hash = hash_object.hexdigest()
    return password_hash
```

MD5 is cryptographically broken and fast to brute-force. There is also no salt, meaning identical passwords produce identical hashes, making rainbow table attacks trivial.

**Fix:** Use `bcrypt` or `argon2` with automatic salting.

### 3. Hardcoded Secret Key

```python
SECRET_KEY = 'development key'
```

The Flask session secret key is hardcoded in the source code. Anyone who reads the code (it's on public GitHub) can forge session cookies and impersonate any user.

**Fix:** Store in a `.env` file and load via `os.environ.get('SECRET_KEY')`.

### 4. Default Admin User with Known Password

```sql
-- schema.sql
INSERT INTO users (username, email, password)
    VALUES ('admin', 'keamonk1@stud.kea.dk', '5f4dcc3b5aa765d61d8327deb882cf99');
```

The MD5 hash `5f4dcc3b5aa765d61d8327deb882cf99` is the hash of the word "password" — one of the most commonly known hashes. Anyone can log in as admin.

### 5. No CSRF Protection

The login and register forms have no CSRF tokens. An attacker could craft a malicious page that submits requests on behalf of a logged-in user.

---

## Code Quality Issues

### 6. Python 2 (End of Life)

The entire application runs on Python 2, which reached end of life on January 1, 2020. It no longer receives security patches. The code uses Python 2 syntax:

```python
print "Database not found"  # Python 2 print statement
```

### 7. Ancient Dependencies

```
Flask==0.5
Jinja2==2.4
Werkzeug==0.6.1
```

These are from 2009-2010 and contain known CVEs. The README itself acknowledges this and recommends upgrading.

### 8. No Separation of Concerns

All application logic — configuration, database functions, routes, security, templates — lives in a single `app.py` file (~180 lines). This makes the code hard to maintain, test, and extend. There is no MVC/service layer pattern.

### 9. Hardcoded Configuration Values

```python
DATABASE_PATH = '/tmp/whoknows.db'
PER_PAGE = 30
DEBUG = False
SECRET_KEY = 'development key'
```

Configuration is hardcoded directly in the source file. There is no `.env` file, no environment variable usage, and no distinction between development and production config.

### 10. Database Stored in /tmp

```python
DATABASE_PATH = '/tmp/whoknows.db'
```

The `/tmp` directory is cleared on reboot on most systems. All data will be lost when the server restarts. This is not suitable for any environment.

---

## Architectural & Operational Issues

### 11. No Error Handling

There are no try/except blocks anywhere in the application. A database connection failure, malformed request, or any unexpected error will crash the server with an unhandled exception and potentially expose stack traces to users.

### 12. Incomplete Tests

```python
def test_search(self):
    """Make sure the search works."""
    pass  # Empty test
```

The test for the core feature (search) is not implemented. The test file also references `app.DATABASE` which doesn't match the actual variable name `DATABASE_PATH`.

### 13. Template References Non-Existent Field

In `search.html`:
```html
<p class="search-result-description">{{ result.description }}</p>
```

But the database schema defines `content`, not `description`. This would either show nothing or error out.

### 14. No Logging

There is no logging configured. When something goes wrong in production, there would be no way to diagnose issues. The only output mechanism is `print` statements.

### 15. No CI/CD Pipeline

There are no GitHub Actions, no automated testing on push, no automated deployment. The `run_forever.sh` script is a naive process manager that just restarts the app in an infinite loop.

### 16. No Docker / Containerization

The app has no Dockerfile and relies on system-level Python 2 being available. This makes deployment inconsistent across environments.

### 17. No Input Validation

Beyond a basic check for `@` in email addresses, there is no input validation or sanitization. Usernames, passwords, and search queries are passed directly into SQL queries without any cleaning.

### 18. No Rate Limiting

There is no rate limiting on login attempts, registration, or search. This makes the application vulnerable to brute-force attacks and denial-of-service.

---

## Summary

| Category | Count | Severity |
|----------|-------|----------|
| Security vulnerabilities | 5 | Critical |
| Code quality issues | 5 | High |
| Architectural/operational | 8 | Medium-High |
| **Total** | **18** | |

The most urgent fixes are the SQL injection vulnerabilities and the migration to Python 3 with modern dependencies. The hardcoded secret key and MD5 hashing should also be addressed immediately in any rewrite.
