from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import pickle, sqlite3, datetime, smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'cyberguard_secret_2024')

# ── Load ML model ──────────────────────────────────────────────
model      = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# ── Email config ───────────────────────────────────────────────
EMAIL_SENDER   = os.environ.get('EMAIL_SENDER', 'your_email@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'your_app_password')
EMAIL_RECEIVER = os.environ.get('EMAIL_RECEIVER', 'admin@cyberguard.com')

# ── DB init ────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT, prediction TEXT, confidence REAL,
        advice TEXT, timestamp TEXT, ip TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        username  TEXT UNIQUE,
        password  TEXT,
        role      TEXT DEFAULT 'user',
        last_login TEXT,
        created_at TEXT
    )''')
    # Default admin
    try:
        c.execute("INSERT INTO users (username,password,role,created_at) VALUES (?,?,?,?)",
                  ('admin','admin123','admin',
                   datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except:
        pass
    conn.commit(); conn.close()

init_db()

# ── Advice map ─────────────────────────────────────────────────
ADVICE = {
    'OTP Fraud':       'Never share OTP with anyone. Call 1930 immediately.',
    'UPI Fraud':       'Block UPI immediately. Report to your bank within 24 hrs.',
    'Job Scam':        'Do not pay any registration fees. Verify company on MCA portal.',
    'Phishing':        'Change all passwords now. Enable 2FA on all accounts.',
    'Account Hacking': 'Freeze account immediately. Report to cybercrime.gov.in',
    'Lottery Scam':    'Ignore all prize claims. Never pay to claim winnings.',
}

# ── Auth decorators ────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Admin access required.')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

# ── Email alert ────────────────────────────────────────────────
def send_alert(text, prediction, confidence):
    try:
        msg = MIMEMultipart()
        msg['From']    = EMAIL_SENDER
        msg['To']      = EMAIL_RECEIVER
        msg['Subject'] = f"🚨 CyberGuard Alert: {prediction} Detected"
        body = f"""
        <h2>🛡️ CyberGuard Alert</h2>
        <p><b>Category:</b> {prediction}</p>
        <p><b>Confidence:</b> {confidence}%</p>
        <p><b>Complaint:</b> {text}</p>
        <p><b>Time:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><b>Action:</b> {ADVICE.get(prediction, 'Investigate immediately.')}</p>
        """
        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Email error: {e}")

# ══════════════════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════════════════

# ── LOGIN ──────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username'].strip()
        p = request.form['password']
        conn = sqlite3.connect('complaints.db')
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (u, p)
        ).fetchone()
        if user:
            # Save last login time
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn.execute("UPDATE users SET last_login=? WHERE username=?", (now, u))
            conn.commit()
            conn.close()
            session['user']    = user[1]
            session['role']    = user[3]
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        conn.close()
        flash('Invalid username or password.')
    return render_template('login.html')

# ── SIGNUP ─────────────────────────────────────────────────────
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        u = request.form['username'].strip()
        p = request.form['password']
        c = request.form['confirm_password']

        if len(u) < 3:
            flash('Username must be at least 3 characters.')
            return render_template('login.html', show_signup=True)
        if len(p) < 6:
            flash('Password must be at least 6 characters.')
            return render_template('login.html', show_signup=True)
        if p != c:
            flash('Passwords do not match.')
            return render_template('login.html', show_signup=True)

        conn = sqlite3.connect('complaints.db')
        try:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn.execute(
                "INSERT INTO users (username,password,role,created_at) VALUES (?,?,?,?)",
                (u, p, 'user', now)
            )
            conn.commit()
            conn.close()
            flash('Account created! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            flash('Username already taken. Try another.')
            return render_template('login.html', show_signup=True)

    return render_template('login.html', show_signup=True)

# ── LOGOUT ─────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── DASHBOARD ──────────────────────────────────────────────────
@app.route('/')
@login_required
def index():
    conn  = sqlite3.connect('complaints.db')
    total = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
    conn.close()
    return render_template('index.html', total=total,
                           user=session.get('user'),
                           role=session.get('role'))

# ── ANALYZE PAGE ───────────────────────────────────────────────
@app.route('/analyze')
@login_required
def analyze():
    return render_template('analyze.html',
                           user=session.get('user'),
                           role=session.get('role'))

# ── PREDICT ────────────────────────────────────────────────────
@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'GET':
        return redirect(url_for('analyze'))
    
    text = request.form['text']
    vec  = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    prob = round(max(model.predict_proba(vec)[0]) * 100, 1)
    adv  = ADVICE.get(pred, 'Report to cybercrime.gov.in')

    conn = sqlite3.connect('complaints.db')
    conn.execute(
        "INSERT INTO complaints (text,prediction,confidence,advice,timestamp,ip) VALUES (?,?,?,?,?,?)",
        (text, pred, prob, adv,
         datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         request.remote_addr)
    )
    conn.commit(); conn.close()
    send_alert(text, pred, prob)

    return render_template('analyze.html', prediction=pred, confidence=prob,
                           advice=adv,
                           user=session.get('user'),
                           role=session.get('role'))

# ── HISTORY ────────────────────────────────────────────────────
@app.route('/history')
@login_required
def history():
    conn = sqlite3.connect('complaints.db')
    rows = conn.execute("SELECT * FROM complaints ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('history.html', complaints=rows,
                           user=session.get('user'),
                           role=session.get('role'))

# ── ANALYTICS ──────────────────────────────────────────────────
@app.route('/analytics')
@login_required
def analytics():
    conn     = sqlite3.connect('complaints.db')
    cats     = conn.execute("SELECT prediction, COUNT(*) FROM complaints GROUP BY prediction").fetchall()
    daily    = conn.execute("SELECT DATE(timestamp), COUNT(*) FROM complaints GROUP BY DATE(timestamp) ORDER BY DATE(timestamp)").fetchall()
    total    = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
    resolved = conn.execute("SELECT COUNT(*) FROM complaints WHERE prediction IS NOT NULL").fetchone()[0]
    conn.close()
    return render_template('analytics.html', cats=cats, daily=daily,
                           total=total, resolved=resolved,
                           user=session.get('user'),
                           role=session.get('role'))

# ── API STATS ──────────────────────────────────────────────────
@app.route('/api/stats')
@login_required
def api_stats():
    conn  = sqlite3.connect('complaints.db')
    cats  = conn.execute("SELECT prediction, COUNT(*) FROM complaints GROUP BY prediction").fetchall()
    daily = conn.execute("SELECT DATE(timestamp), COUNT(*) FROM complaints GROUP BY DATE(timestamp) ORDER BY DATE(timestamp) DESC LIMIT 7").fetchall()
    total = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
    conn.close()
    return jsonify({
        'categories': [{'name': r[0], 'count': r[1]} for r in cats],
        'daily':      [{'date': r[0], 'count': r[1]} for r in daily],
        'total':      total
    })

# ── ADMIN ──────────────────────────────────────────────────────
@app.route('/admin')
@login_required
@admin_required
def admin():
    conn       = sqlite3.connect('complaints.db')
    # Fetch all user details including last_login
    users      = conn.execute(
        "SELECT id, username, role, last_login, created_at FROM users"
    ).fetchall()
    complaints = conn.execute(
        "SELECT * FROM complaints ORDER BY id DESC LIMIT 20"
    ).fetchall()
    conn.close()
    return render_template('admin.html', users=users, complaints=complaints,
                           user=session.get('user'),
                           role=session.get('role'))

# ── ADMIN: DELETE USER ─────────────────────────────────────────
@app.route('/admin/delete_user/<int:uid>')
@login_required
@admin_required
def delete_user(uid):
    conn = sqlite3.connect('complaints.db')
    conn.execute("DELETE FROM users WHERE id=? AND username != 'admin'", (uid,))
    conn.commit(); conn.close()
    flash('User deleted.')
    return redirect(url_for('admin'))

# ── ADMIN: ADD USER ────────────────────────────────────────────
@app.route('/admin/add_user', methods=['POST'])
@login_required
@admin_required
def add_user():
    u    = request.form['username'].strip()
    p    = request.form['password']
    role = request.form['role']
    conn = sqlite3.connect('complaints.db')
    try:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute(
            "INSERT INTO users (username,password,role,created_at) VALUES (?,?,?,?)",
            (u, p, role, now)
        )
        conn.commit()
        flash(f'User "{u}" added successfully.')
    except sqlite3.IntegrityError:
        flash('Username already exists.')
    conn.close()
    return redirect(url_for('admin'))

# ── MAP ────────────────────────────────────────────────────────
@app.route('/map')
@login_required
def map_view():
    state_data = {
        'Punjab': 12, 'Delhi': 4, 'Maharashtra': 3,
        'West Bengal': 1, 'Kerala': 2, 'Telangana': 2,
        'Karnataka': 1, 'Gujarat': 1, 'Rajasthan': 1,
        'Uttar Pradesh': 2,
    }
    return render_template('map.html', state_data=state_data,
                           user=session.get('user'),
                           role=session.get('role'))

# ── ALERTS ─────────────────────────────────────────────────────
@app.route('/alerts')
@login_required
def alerts():
    # Sample alerts
    alert_list = [
        {
            'icon': '🔴',
            'title': 'High Risk: Multiple OTP Fraud Attempts',
            'description': '3 new OTP fraud complaints detected in the last 24 hours from Punjab region. Pattern suggests coordinated attack.',
            'level': 'critical',
            'time': '2 hours ago',
            'source': 'Auto Detection'
        },
        {
            'icon': '🟠',
            'title': 'Unusual Activity: UPI Transaction Spike',
            'description': 'UPI fraud cases increased by 45% this week. Recommend sending public awareness notice.',
            'level': 'high',
            'time': '5 hours ago',
            'source': 'Analytics Engine'
        },
        {
            'icon': '🔵',
            'title': 'New User Registration: Pannu Family Member',
            'description': 'A new complaint was filed by a Pannu family member. Total family complaints now: 12.',
            'level': 'medium',
            'time': '1 day ago',
            'source': 'System'
        },
    ]
    return render_template('alerts.html', alerts=alert_list,
                           user=session.get('user'),
                           role=session.get('role'))

# ── SETTINGS ───────────────────────────────────────────────────
@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html',
                           user=session.get('user'),
                           role=session.get('role'))

@app.route('/settings/update_profile', methods=['POST'])
@login_required
def update_profile():
    flash('Profile updated successfully!')
    return redirect(url_for('settings'))

@app.route('/settings/change_password', methods=['POST'])
@login_required
def change_password():
    current = request.form['current_password']
    new_pwd = request.form['new_password']
    confirm = request.form['confirm_password']
    
    if new_pwd != confirm:
        flash('Error: Passwords do not match.')
        return redirect(url_for('settings'))
    
    conn = sqlite3.connect('complaints.db')
    user = conn.execute(
        "SELECT password FROM users WHERE username=?",
        (session.get('user'),)
    ).fetchone()
    conn.close()
    
    if user and user[0] == current:
        conn = sqlite3.connect('complaints.db')
        conn.execute(
            "UPDATE users SET password=? WHERE username=?",
            (new_pwd, session.get('user'))
        )
        conn.commit()
        conn.close()
        flash('Password changed successfully!')
    else:
        flash('Error: Current password is incorrect.')
    
    return redirect(url_for('settings'))

@app.route('/settings/update_preferences', methods=['POST'])
@login_required
def update_preferences():
    flash('Preferences saved!')
    return redirect(url_for('settings'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)