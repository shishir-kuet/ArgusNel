import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, render_template_string
from search.search_engine import SearchEngine

app = Flask(__name__)

engine = SearchEngine()


HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>ArgusNel</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root{
            --bg:#ffffff; --muted:#6b7280; --accent:#1a73e8; --card:#ffffff; --shadow: 0 6px 18px rgba(15,23,42,0.08);
        }
        html,body{height:100%;margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#0f172a}
        body::before{content:'';position:fixed;inset:0;z-index:-2;background-image:url('/static/cloudscape_from_above-full.jpg');background-size:cover;background-position:center;opacity:1}
        /* subtle gradient overlay so background shows through */
        body::after{content:'';position:fixed;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(248,250,252,0.65) 0%,rgba(255,255,255,0.7) 100%);mix-blend-mode:normal;opacity:0.85}
        .container{max-width:960px;margin:48px auto;padding:0 20px}
            .brand{display:flex;align-items:center;gap:12px;margin-bottom:28px}
            .logo{display:flex;align-items:center;gap:12px}
            .logo-img{width:56px;height:56px;border-radius:12px;background:transparent;box-shadow:0 6px 18px rgba(15,23,42,0.06)}
        h1{font-size:20px;margin:0}

        .search-box{display:flex;align-items:center;gap:12px;background:var(--card);padding:16px;border-radius:12px;box-shadow:var(--shadow);}
        .search-input{flex:1;border:0;outline:0;font-size:18px;padding:8px 6px;background:transparent}
        .search-btn{background:var(--accent);color:white;border:0;padding:10px 16px;border-radius:8px;font-weight:600;cursor:pointer}

        .meta{margin-top:12px;color:var(--muted);font-size:13px}

        .results{margin-top:24px;display:grid;gap:14px}
        .result-card{background:#fff;border-radius:10px;padding:14px 16px;box-shadow:var(--shadow);}
        .result-title{font-size:16px;margin:0 0 6px 0}
        .result-title a{color:var(--accent);text-decoration:none}
        .result-url{color:#0f766e;font-size:13px;margin-bottom:8px}
        .result-snippet{color:#374151;font-size:14px}

        @media (max-width:640px){.container{margin:18px auto}.search-input{font-size:16px}}
    </style>
</head>
<body>
    <div class="container">
        <div class="brand">
               <img src="/static/logo.svg" alt="ArgusNel" class="logo-img" />
            <div>
                <h1>ArgusNel</h1>
                <div style="color:var(--muted);font-size:13px">Lightweight search engine demo</div>
            </div>
        </div>

        <form method="GET" class="search-box" onsubmit="document.getElementById('q').blur()">
            <input id="q" class="search-input" type="text" name="q" placeholder="Search the web" value="{{ request.args.get('q','')|e }}" autocomplete="off" autofocus />
            <button class="search-btn">Search</button>
        </form>

        {% if results is defined and results %}
            <div class="meta">Total results: {{ results|length }}</div>
            <div class="results">
                {% for r in results %}
                <article class="result-card">
                    <h3 class="result-title"><a href="{{ r.url }}" target="_blank" rel="noopener noreferrer">{{ r.title or r.url }}</a></h3>
                    <div class="result-url">{{ r.url }}</div>
                    <p class="result-snippet">{{ r.snippet }}</p>
                </article>
                {% endfor %}
            </div>
        {% elif request.args.get('q') %}
            <div class="meta">No results found.</div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def search():

    query = request.args.get("q")

    results = []

    if query:
        results = engine.search(query)

    return render_template_string(HTML, results=results)


if __name__ == "__main__":
    app.run(debug=True)