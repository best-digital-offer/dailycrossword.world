#!/usr/bin/env python3
"""Daily Crossword Static Site Generator for dailycrossword.world"""
import os, sys, json, random, argparse, datetime
from collections import defaultdict

SITE_TITLE = "Daily Crossword"
DOMAIN = "dailycrossword.world"

GENRES = {
    "general": [
        ("PYTHON","Popular programming language"),
        ("RIVER","A flowing body of water"),
        ("MUSIC","Art of arranging sounds"),
        ("MOUNTAIN","Tall natural elevation"),
        ("STATION","Place for trains"),
        ("OCEAN","Large body of salt water"),
        ("FOREST","Dense area of trees"),
        ("BRIDGE","Structure spanning a gap"),
        ("GARDEN","Cultivated outdoor space"),
        ("LIBRARY","Place for books")
    ],
    "tech": [
        ("SERVER","Computer that serves data"),
        ("BROWSER","App to view websites"),
        ("CACHE","Temporary storage"),
        ("ALGORITHM","Step-by-step procedure"),
        ("BANDWIDTH","Network capacity"),
        ("DATABASE","Organized data collection"),
        ("FIREWALL","Security barrier"),
        ("ROUTER","Network device"),
        ("CLOUD","Remote computing"),
        ("KERNEL","OS core")
    ],
    "travel": [
        ("PASSPORT","Travel document"),
        ("AIRPORT","Plane terminal"),
        ("HOTEL","Place to stay"),
        ("BACKPACK","Traveler's bag"),
        ("TOURIST","Visitor"),
        ("LUGGAGE","Travel bags"),
        ("TICKET","Travel pass"),
        ("JOURNEY","Trip"),
        ("CRUISE","Sea voyage"),
        ("RESORT","Vacation spot")
    ],
    "kids": [
        ("CAT","Small pet"),
        ("BALL","Round toy"),
        ("APPLE","A fruit"),
        ("TRAIN","Transport with rails"),
        ("SUN","Star in our sky"),
        ("MOON","Night light"),
        ("STAR","Twinkle in sky"),
        ("TREE","Plant with trunk"),
        ("BIRD","Flying animal"),
        ("FISH","Water creature")
    ],
    "devotional": [
        ("GRACE","Divine favor"),
        ("PRAYER","Communication with God"),
        ("FAITH","Strong belief"),
        ("PSALM","Religious song"),
        ("TEMPLE","Place of worship"),
        ("BLESSING","Divine gift"),
        ("SPIRIT","Soul essence"),
        ("HEAVEN","Divine realm"),
        ("ANGEL","Divine messenger"),
        ("PEACE","Inner calm")
    ],
    "holiday": [
        ("SANTA","Festive gift giver"),
        ("FIREWORK","Colorful explosion"),
        ("DECOR","Festive ornament"),
        ("FESTIVAL","Public celebration"),
        ("CANDLES","Wax lights"),
        ("PARTY","Celebration"),
        ("GIFT","Present"),
        ("FEAST","Large meal"),
        ("CAROL","Holiday song"),
        ("WREATH","Circular decoration")
    ],
    "cryptic_easy": [
        ("NOTE","Short message"),
        ("TUNE","Melody"),
        ("CLUE","Hint"),
        ("WORD","Lexical unit"),
        ("TALE","Story")
    ]
}

DIFFICULTY = {
    "easy": (9, 9, 8),
    "medium": (13, 13, 12),
    "hard": (15, 15, 18)
}

def empty_grid(w, h):
    return [[" " for _ in range(w)] for __ in range(h)]

def can_place(grid, word, r, c, dr, dc):
    h, w = len(grid), len(grid[0])
    L = len(word)
    end_r, end_c = r + dr * (L - 1), c + dc * (L - 1)
    if not (0 <= end_r < h and 0 <= end_c < w):
        return False
    for i, ch in enumerate(word):
        rr, cc = r + dr * i, c + dc * i
        cell = grid[rr][cc]
        if cell != " " and cell != ch:
            return False
    return True

def place_word(grid, word, r, c, dr, dc):
    for i, ch in enumerate(word):
        rr, cc = r + dr * i, c + dc * i
        grid[rr][cc] = ch

def place_words_into_grid(width, height, words):
    attempts = 0
    max_attempts = 5000
    word_list = [w.upper() for w in words]
    while attempts < max_attempts:
        attempts += 1
        grid = empty_grid(width, height)
        placements = []
        ok = True
        random.shuffle(word_list)
        for word in word_list:
            placed = False
            trials = 0
            while trials < 300 and not placed:
                trials += 1
                dr, dc = random.choice([(0, 1), (1, 0)])
                r = random.randint(0, height - 1)
                c = random.randint(0, width - 1)
                if can_place(grid, word, r, c, dr, dc):
                    place_word(grid, word, r, c, dr, dc)
                    placements.append((word, r, c, dr, dc))
                    placed = True
            if not placed:
                ok = False
                break
        if ok:
            for i in range(height):
                for j in range(width):
                    if grid[i][j] == " ":
                        grid[i][j] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            return grid, placements
    raise Exception("Failed to generate grid")

def get_clue(word, category):
    for cat_words in GENRES.values():
        for w, clue in cat_words:
            if w == word:
                return clue
    return f"Definition (length {len(word)})"

def render_puzzle_html(date_str, category, difficulty, grid, placements, prev_link=None, next_link=None):
    h, w = len(grid), len(grid[0])
    table_html = '<div class="puzzle-container"><table class="puzzle-grid" cellspacing="0" cellpadding="0">\n'
    for i in range(h):
        table_html += "<tr>"
        for j in range(w):
            table_html += f'<td><input maxlength="1" data-r="{i}" data-c="{j}" data-answer="{grid[i][j]}" value="" aria-label="cell {i}-{j}"></td>'
        table_html += "</tr>\n"
    table_html += "</table></div>"

    across, down = [], []
    for idx, (word, r, c, dr, dc) in enumerate(placements, start=1):
        clue = get_clue(word, category)
        if dr == 0 and dc == 1:
            across.append((idx, r + 1, c + 1, word, clue))
        else:
            down.append((idx, r + 1, c + 1, word, clue))

    clues_html = '<div class="clues"><div class="clue-section"><h3>Across</h3><ol>'
    for num, r, c, word, clue in across:
        clues_html += f'<li><strong>{num}.</strong> {clue}</li>'
    clues_html += '</ol></div><div class="clue-section"><h3>Down</h3><ol>'
    for num, r, c, word, clue in down:
        clues_html += f'<li><strong>{num}.</strong> {clue}</li>'
    clues_html += '</ol></div></div>'

    solution_text = "<pre class='solution'>\n"
    for row in grid:
        solution_text += "".join(row) + "\n"
    solution_text += "</pre>"

    title = f"Daily Crossword — {date_str} — {category.capitalize()} — {DOMAIN}"
    meta = f"Solve today's {category} crossword puzzle for {date_str}. Free daily crosswords with {difficulty} difficulty level. Print or play online."

    seo_text = f"""<h2>About Today's {category.capitalize()} Crossword — {date_str}</h2>
<p>Welcome to today's {category} crossword puzzle dated {date_str}. This puzzle is carefully curated for {category} enthusiasts and designed at a {difficulty} difficulty level. Our daily crosswords help improve vocabulary, problem-solving skills, and provide entertaining mental exercise.</p>
<p>This {category} themed puzzle includes clues that test your knowledge of {category}-specific terminology and general vocabulary. Whether you're a beginner or experienced solver, you'll find this puzzle engaging and rewarding.</p>
<h3>How to Solve This Crossword</h3>
<p>Start by reading through all the clues for both Across and Down. Begin with the shortest words or clues you're most confident about. Use crossing letters to verify your answers. If you get stuck, take a break and return with fresh eyes. The "Check Puzzle" button helps verify your progress, and "Show Solution" reveals the complete answer grid.</p>
<h3>Benefits of Daily Crosswords</h3>
<p>Regular crossword solving improves memory, expands vocabulary, enhances problem-solving abilities, and provides stress relief. Studies show that daily mental exercises like crosswords can help maintain cognitive function and mental sharpness.</p>
<h3>Print or Play Online</h3>
<p>You can solve this puzzle directly in your browser with our interactive grid, or click the "Print" button for a traditional paper-and-pencil experience. Our puzzles are mobile-friendly and accessible on all devices.</p>
<p>Come back tomorrow for a brand new {category} crossword puzzle. We publish fresh puzzles daily across multiple categories including General Knowledge, Technology, Travel, Kids, Devotional, and Holiday themes.</p>"""

    faq_html = """<section class='faq'><h2>Frequently Asked Questions</h2><dl>
<dt>How difficult is this puzzle?</dt><dd>This puzzle is designed for casual to intermediate solvers with a balanced mix of straightforward and challenging clues.</dd>
<dt>Can I print this crossword?</dt><dd>Yes! Click the Print button to get a printer-friendly version perfect for solving offline.</dd>
<dt>Are new puzzles published daily?</dt><dd>Yes, we publish a fresh crossword puzzle every single day across multiple categories.</dd>
<dt>Is there a solution available?</dt><dd>Yes, click the "Show Solution" button to reveal the complete answer grid.</dd>
<dt>Can I play on mobile devices?</dt><dd>Absolutely! Our puzzles are fully responsive and work great on phones and tablets.</dd>
</dl></section>"""

    prev_html = f'<a class="nav-btn" href="{prev_link}">← Previous</a>' if prev_link else ''
    next_html = f'<a class="nav-btn" href="{next_link}">Next →</a>' if next_link else ''

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://{DOMAIN}/puzzles/{date_str}.html">
<meta property="og:image" content="https://{DOMAIN}/assets/logo.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{meta}">
<link rel="stylesheet" href="/assets/style.css">
<link rel="stylesheet" href="/assets/print.css" media="print">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "datePublished": "{date_str}",
  "description": "{meta}",
  "author": {{"@type": "Organization", "name": "{SITE_TITLE}"}},
  "publisher": {{"@type": "Organization", "name": "{SITE_TITLE}", "logo": {{"@type": "ImageObject", "url": "https://{DOMAIN}/assets/logo.png"}}}}
}}
</script>
</head>
<body>
<header class="site-header"><div class="container"><a class="logo" href="/index.html">{SITE_TITLE}</a><nav><a href="/categories/general/index.html">Categories</a><a href="/about.html">About</a></nav></div></header>
<main class="container">
<div class="breadcrumb"><a href="/">Home</a> › <a href="/categories/{category}/index.html">{category.capitalize()}</a> › {date_str}</div>
<h1>Daily Crossword — {date_str}</h1>
<div class="puzzle-meta">Category: <strong>{category.capitalize()}</strong> | Difficulty: <strong>{difficulty.capitalize()}</strong></div>
<div class="nav-row">{prev_html} {next_html}</div>
<div class="ad-placeholder">Advertisement</div>
{table_html}
{clues_html}
<div class="puzzle-controls">
<button id="checkPuzzle" class="btn">Check Puzzle</button>
<button id="showSolution" class="btn">Show Solution</button>
<button onclick="window.print()" class="btn">Print / PDF</button>
</div>
<div id="solution" style="display:none">{solution_text}</div>
<div class="ad-placeholder">Advertisement</div>
{seo_text}
<div class="ad-placeholder">Advertisement</div>
{faq_html}
<div class="share-buttons">
<h3>Share This Puzzle</h3>
<button onclick="shareTwitter()" class="share-btn">Twitter</button>
<button onclick="shareFacebook()" class="share-btn">Facebook</button>
<button onclick="shareLinkedIn()" class="share-btn">LinkedIn</button>
</div>
</main>
<footer class="site-footer"><div class="container">&copy; {datetime.date.today().year} {SITE_TITLE} — Daily crosswords. <a href="/privacy.html">Privacy</a> • <a href="/terms.html">Terms</a> • <a href="/contact.html">Contact</a></div></footer>
<script src="/assets/main.js"></script>
</body>
</html>"""
    return html

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate(start_date, days, outdir, category_sequence=None, difficulty="easy"):
    ensure_dir(outdir)
    
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    pages = []
    
    for i in range(days):
        date = start + datetime.timedelta(days=i)
        date_str = date.isoformat()
        cat = (category_sequence[i % len(category_sequence)] if category_sequence else random.choice(list(GENRES.keys())))
        bank = GENRES.get(cat, GENRES["general"])
        width, height, target_words = DIFFICULTY.get(difficulty, DIFFICULTY["easy"])
        words = [w for w, _ in random.sample(bank, min(len(bank), target_words))]
        grid, placements = place_words_into_grid(width, height, words)
        
        prev_link = f"/puzzles/{(date - datetime.timedelta(days=1)).isoformat()}.html" if i > 0 else None
        next_link = f"/puzzles/{(date + datetime.timedelta(days=1)).isoformat()}.html" if i < days - 1 else None
        
        html = render_puzzle_html(date_str, cat, difficulty, grid, placements, prev_link, next_link)
        outpath = os.path.join(outdir, "puzzles", f"{date_str}.html")
        write_file(outpath, html)
        pages.append((f"/puzzles/{date_str}.html", date_str, cat))
    
    create_index(outdir, pages)
    create_category_pages(outdir, pages)
    create_legal_pages(outdir)
    create_sitemap(outdir, pages)
    create_feed(outdir, pages)
    create_robots(outdir)
    
    print(f"Generated {len(pages)} puzzle pages in {outdir}/")
    return

def create_index(outdir, pages):
    latest = pages[-1] if pages else None
    categories = list(GENRES.keys())
    
    cat_html = '<div class="category-grid">'
    for cat in categories:
        cat_html += f'<a href="/categories/{cat}/index.html" class="category-card"><h3>{cat.capitalize()}</h3><p>Explore {cat} puzzles</p></a>'
    cat_html += '</div>'
    
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{SITE_TITLE} — Free Daily Crossword Puzzles</title>
<meta name="description" content="Solve free daily crossword puzzles online. New puzzles every day across multiple categories: General, Tech, Travel, Kids, Devotional, and more.">
<meta property="og:title" content="{SITE_TITLE}">
<meta property="og:description" content="Free daily crossword puzzles. Play online or print.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="site-header"><div class="container"><a class="logo" href="/index.html">{SITE_TITLE}</a><nav><a href="#categories">Categories</a><a href="/about.html">About</a></nav></div></header>
<main class="container">
<section class="hero">
<h1>Free Daily Crossword Puzzles</h1>
<p class="tagline">Challenge your mind with a new crossword every day. Play online or print!</p>
<a href="{latest[0] if latest else '#'}" class="cta-btn">Play Today's Puzzle</a>
</section>
<div class="ad-placeholder">Advertisement</div>
<section id="categories">
<h2>Browse by Category</h2>
{cat_html}
</section>
<section class="features">
<h2>Why Solve Daily Crosswords?</h2>
<div class="feature-grid">
<div class="feature"><h3>🧠 Brain Training</h3><p>Improve memory and cognitive skills</p></div>
<div class="feature"><h3>📚 Expand Vocabulary</h3><p>Learn new words daily</p></div>
<div class="feature"><h3>🎯 Problem Solving</h3><p>Enhance critical thinking</p></div>
<div class="feature"><h3>😌 Stress Relief</h3><p>Relax with engaging puzzles</p></div>
</div>
</section>
</main>
<footer class="site-footer"><div class="container">&copy; {datetime.date.today().year} {SITE_TITLE} — Daily crosswords. <a href="/privacy.html">Privacy</a> • <a href="/terms.html">Terms</a> • <a href="/contact.html">Contact</a></div></footer>
</body>
</html>"""
    write_file(os.path.join(outdir, "index.html"), html)

def create_category_pages(outdir, pages):
    by_cat = defaultdict(list)
    for url, date, cat in pages:
        by_cat[cat].append((url, date))
    
    for cat, puzzles in by_cat.items():
        puzzles.sort(key=lambda x: x[1], reverse=True)
        puzzle_list = '<ul class="puzzle-list">'
        for url, date in puzzles:
            puzzle_list += f'<li><a href="{url}">{date} — {cat.capitalize()} Crossword</a></li>'
        puzzle_list += '</ul>'
        
        html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cat.capitalize()} Crosswords — {SITE_TITLE}</title>
<meta name="description" content="Browse all {cat} crossword puzzles. Free daily puzzles to solve online or print.">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="site-header"><div class="container"><a class="logo" href="/index.html">{SITE_TITLE}</a></div></header>
<main class="container">
<h1>{cat.capitalize()} Crosswords</h1>
<p>All {cat} themed crossword puzzles.</p>
{puzzle_list}
</main>
<footer class="site-footer"><div class="container">&copy; {datetime.date.today().year} {SITE_TITLE}</div></footer>
</body>
</html>"""
        write_file(os.path.join(outdir, "categories", cat, "index.html"), html)

def create_legal_pages(outdir):
    privacy = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Privacy Policy — {SITE_TITLE}</title><link rel="stylesheet" href="/assets/style.css"></head>
<body>
<header class="site-header"><div class="container"><a class="logo" href="/index.html">{SITE_TITLE}</a></div></header>
<main class="container">
<h1>Privacy Policy</h1>
<p>Last updated: {datetime.date.today().isoformat()}</p>
<h2>Information We Collect</h2>
<p>We do not collect personal information. Our puzzles are solved entirely in your browser. We may use cookies for analytics and advertising purposes.</p>
<h2>Third-Party Services</h2>
<p>We use Google AdSense for advertisements. Google may use cookies to serve ads based on your prior visits. You can opt out of personalized advertising by visiting Google's Ads Settings.</p>
<h2>Contact</h2>
<p>For privacy questions, contact us at privacy@{DOMAIN}</p>
</main>
<footer class="site-footer"><div class="container">&copy; {datetime.date.today().year} {SITE_TITLE}</div></footer>
</body>
</html>"""
    
    terms = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Terms of Service — {SITE_TITLE}</title><link rel="stylesheet" href="/assets/style.css"></head>
<body>
<header class="site-header"><div class="container"><a class="logo" href="/index.html">{SITE_TITLE}</a></div></header>
<main class="container">
<h1>Terms of Service</h1>
<p>By using {SITE_TITLE}, you agree to these terms.</p>
<h2>Use of Service</h2>
<p>Our crossword puzzles are provided for personal, non-commercial use. You may print puzzles for personal use.</p>
<h2>Intellectual Property</h2>
<p>All puzzles and content are owned by {SITE_TITLE}. Unauthorized reproduction is prohibited.</p>
<h2>Disclaimer</h2>
<p>Puzzles are provided "as is" without warranties. We are not liable for any errors in puzzles.</p>
</main>
<footer class="site-footer"><div class="container">&copy; {datetime.date.today().year} {SITE_TITLE}</div></footer>
</body>
</html>"""
    
    about = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>About — {SITE_TITLE}</title><link rel="stylesheet" href="/assets/style.css"></head>
<body>
<header class="site-header"><div class="container"><a class="logo" href="/index.html">{SITE_TITLE}</a></div></header>
<main class="container">
<h1>About {SITE_TITLE}</h1>
<p>{SITE_TITLE} publishes free daily crossword puzzles across multiple categories. Our mission is to provide engaging, educational, and entertaining puzzles for solvers of all skill levels.</p>
<h2>Our Categories</h2>
<ul>
<li><strong>General Knowledge</strong> — Everyday vocabulary and trivia</li>
<li><strong>Technology</strong> — Tech terms and computing</li>
<li><strong>Travel</strong> — Places, destinations, and travel terms</li>
<li><strong>Kids</strong> — Simple, fun puzzles for children</li>
<li><strong>Devotional</strong> — Faith-based themes</li>
<li><strong>Holiday</strong> — Seasonal and festive puzzles</li>
</ul>
<p>New puzzles are published daily at midnight UTC. All puzzles can be solved online or printed.</p>
</main>
<footer class="site-footer"><div class="container">&copy; {datetime.date.today().year} {SITE_TITLE}</div></footer>
</body>
</html>"""
    
    contact = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Contact — {SITE_TITLE}</title><link rel="stylesheet" href="/assets/style.css"></head>
<body>
<header class="site-header"><div class="container"><a class="logo" href="/index.html">{SITE_TITLE}</a></div></header>
<main class="container">
<h1>Contact Us</h1>
<p>Have questions, feedback, or suggestions? We'd love to hear from you!</p>
<p><strong>Email:</strong> contact@{DOMAIN}</p>
<p><strong>Support:</strong> support@{DOMAIN}</p>
<p><strong>Advertising:</strong> ads@{DOMAIN}</p>
</main>
<footer class="site-footer"><div class="container">&copy; {datetime.date.today().year} {SITE_TITLE}</div></footer>
</body>
</html>"""
    
    write_file(os.path.join(outdir, "privacy.html"), privacy)
    write_file(os.path.join(outdir, "terms.html"), terms)
    write_file(os.path.join(outdir, "about.html"), about)
    write_file(os.path.join(outdir, "contact.html"), contact)

def create_sitemap(outdir, pages):
    urlset = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    urlset += f'<url><loc>https://{DOMAIN}/</loc><priority>1.0</priority></url>\n'
    for url, date, cat in pages:
        urlset += f'<url><loc>https://{DOMAIN}{url}</loc><lastmod>{date}</lastmod><priority>0.8</priority></url>\n'
    for cat in GENRES.keys():
        urlset += f'<url><loc>https://{DOMAIN}/categories/{cat}/index.html</loc><priority>0.7</priority></url>\n'
    urlset += "</urlset>"
    write_file(os.path.join(outdir, "sitemap.xml"), urlset)

def create_feed(outdir, pages):
    feed = f'<?xml version="1.0" encoding="utf-8"?><rss version="2.0"><channel><title>{SITE_TITLE}</title><link>https://{DOMAIN}/</link><description>Daily crossword puzzles</description>'
    for url, date, cat in pages[-10:][::-1]:
        feed += f'<item><title>Daily Crossword — {date} — {cat.capitalize()}</title><link>https://{DOMAIN}{url}</link><pubDate>{date}</pubDate><description>Solve today\'s {cat} crossword puzzle</description></item>'
    feed += "</channel></rss>"
    write_file(os.path.join(outdir, "feed.xml"), feed)

def create_robots(outdir):
    robots = f"""User-agent: *
Allow: /
Sitemap: https://{DOMAIN}/sitemap.xml"""
    write_file(os.path.join(outdir, "robots.txt"), robots)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True, help="start date YYYY-MM-DD")
    parser.add_argument("--days", required=True, type=int, help="number of days")
    parser.add_argument("--out", default="site", help="output folder")
    parser.add_argument("--difficulty", default="easy", choices=DIFFICULTY.keys())
    parser.add_argument("--categories", default="general,tech,travel,kids,devotional,holiday", help="comma separated")
    args = parser.parse_args()
    cats = args.categories.split(",")
    generate(args.start, args.days, args.out, category_sequence=cats, difficulty=args.difficulty)
