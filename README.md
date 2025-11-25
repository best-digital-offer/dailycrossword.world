# Daily Crossword World - Static Site Generator

Complete static website project for **dailycrossword.world** - A daily crossword puzzle platform with multiple categories, SEO optimization, and AdSense readiness.

## Features

✅ **Daily Puzzle Generation** - Pre-generate N days of crossword puzzles as static HTML  
✅ **Multi-Category Support** - General, Tech, Travel, Kids, Devotional, Holiday, Cryptic  
✅ **Interactive Grid** - Keyboard navigation, auto-advance, check answers  
✅ **Print & PDF** - Print-friendly CSS for offline solving  
✅ **SEO Optimized** - Meta tags, Open Graph, structured data, 600+ words per page  
✅ **AdSense Ready** - Ad placeholders, legal pages, privacy policy  
✅ **Mobile-First** - Responsive design for all devices  
✅ **Accessibility** - ARIA labels, keyboard navigation, high contrast  
✅ **Social Sharing** - Twitter, Facebook, LinkedIn integration  
✅ **RSS Feed** - Automatic feed generation  
✅ **Sitemap** - XML sitemap for search engines  

## Project Structure

```
puzzle maker/
├── generate.py              # Main Python generator script
├── site/                    # Generated static site (deploy this)
│   ├── index.html          # Homepage
│   ├── puzzles/            # Daily puzzle pages
│   │   └── YYYY-MM-DD.html
│   ├── categories/         # Category archive pages
│   │   └── {category}/index.html
│   ├── assets/
│   │   ├── style.css       # Main stylesheet
│   │   ├── print.css       # Print-specific styles
│   │   ├── main.js         # Puzzle interactivity
│   │   └── logo.png        # Site logo (add your own)
│   ├── privacy.html        # Privacy policy
│   ├── terms.html          # Terms of service
│   ├── about.html          # About page
│   ├── contact.html        # Contact page
│   ├── sitemap.xml         # XML sitemap
│   ├── feed.xml            # RSS feed
│   └── robots.txt          # Robots.txt
├── .github/
│   └── workflows/
│       └── generate.yml    # GitHub Actions workflow
└── README.md               # This file
```

## Quick Start

### 1. Generate Puzzles

```bash
# Generate 30 days of puzzles starting from today
python generate.py --start 2025-01-01 --days 30 --out site --difficulty easy --categories general,tech,travel,kids,devotional,holiday

# Generate with different difficulty
python generate.py --start 2025-01-01 --days 30 --out site --difficulty medium --categories general,tech
```

### 2. Test Locally

Open `site/index.html` in your browser or use a local server:

```bash
# Python 3
cd site
python -m http.server 8000

# Then visit http://localhost:8000
```

### 3. Deploy to Netlify

#### Option A: Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd site
netlify deploy --prod
```

#### Option B: Netlify Dashboard

1. Push your code to GitHub
2. Go to [Netlify](https://netlify.com)
3. Click "Add new site" → "Import an existing project"
4. Connect your GitHub repo
5. Set build settings:
   - **Build command:** `python generate.py --start $(date -I) --days 30 --out site --difficulty easy --categories general,tech,travel,kids,devotional,holiday`
   - **Publish directory:** `site`
6. Deploy!

#### Option C: GitHub Pages

1. Push to GitHub
2. Go to Settings → Pages
3. Set source to `main` branch, `/site` folder
4. Save

### 4. Automate Daily Generation

The included GitHub Actions workflow (`.github/workflows/generate.yml`) automatically:
- Runs daily at 00:05 UTC
- Generates next 7 days of puzzles
- Commits and pushes to repo
- Triggers Netlify auto-deploy

**Setup:**
1. Push code to GitHub
2. Enable GitHub Actions in repo settings
3. Workflow runs automatically

## Configuration

### Categories

Edit `GENRES` dictionary in `generate.py` to add/modify categories:

```python
GENRES = {
    "general": [
        ("PYTHON", "Popular programming language"),
        ("RIVER", "A flowing body of water"),
        # Add more words...
    ],
    "yourcategory": [
        ("WORD", "Clue for word"),
    ]
}
```

### Difficulty Levels

Modify `DIFFICULTY` dictionary to adjust grid size:

```python
DIFFICULTY = {
    "easy": (9, 9, 8),      # (width, height, word_count)
    "medium": (13, 13, 12),
    "hard": (15, 15, 18)
}
```

### Site Branding

Update in `generate.py`:

```python
SITE_TITLE = "Daily Crossword"
DOMAIN = "dailycrossword.world"
```

## SEO & AdSense Checklist

### ✅ SEO Optimization

- [x] Unique title tags (60-70 chars)
- [x] Meta descriptions (150-160 chars)
- [x] Open Graph tags for social sharing
- [x] Structured data (JSON-LD Article schema)
- [x] XML sitemap
- [x] RSS feed
- [x] Robots.txt
- [x] Mobile-responsive design
- [x] Fast loading (static HTML)
- [x] Internal linking (breadcrumbs, category links)
- [x] 600+ words per puzzle page
- [x] FAQ sections
- [x] Alt text for images (add logo with alt text)

### ✅ AdSense Requirements

- [x] Privacy Policy page
- [x] Terms of Service page
- [x] Contact page
- [x] About page
- [x] Original content (600+ words per page)
- [x] Ad placeholder blocks (3 per page)
- [x] Clean, professional design
- [x] Mobile-friendly
- [x] Fast loading
- [ ] Domain must be 6+ months old (wait period)
- [ ] Add actual AdSense code after approval

### Adding AdSense Code

After approval, replace ad placeholders in `generate.py`:

```python
# Replace this:
'<div class="ad-placeholder">Advertisement</div>'

# With actual AdSense code:
'''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXX"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''
```

## Advanced: Better Clues with LLM

For natural-sounding clues, integrate an LLM API:

```python
import openai  # or anthropic, etc.

def get_clue_from_llm(word, category):
    prompt = f"""Generate a crossword clue for the word "{word}" in the {category} category.
    Make it concise, clever, and appropriate difficulty.
    Format: Just the clue text, no extra formatting."""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Use in render_puzzle_html():
clue = get_clue_from_llm(word, category)
```

## Image Prompt for Logo/Hero

**DALL-E / Midjourney Prompt:**

```
A modern, minimalist logo for a daily crossword puzzle website. 
Features a stylized crossword grid with letters forming a globe or world map. 
Color scheme: blue (#1e90ff) and purple gradients. 
Clean, professional, suitable for web header. 
Flat design, vector style, white background.
```

**Alternative Hero Image Prompt:**

```
A vibrant illustration of diverse people solving crossword puzzles together. 
Modern flat design style with gradient colors (blue to purple). 
Includes puzzle grids, pencils, coffee cups, and happy expressions. 
Suitable for website hero section, wide aspect ratio 16:9.
```

## Performance Tips

1. **Optimize Images** - Compress logo.png with TinyPNG
2. **Minify CSS/JS** - Use online minifiers before production
3. **Enable Caching** - Configure Netlify headers:

Create `site/_headers`:
```
/*
  Cache-Control: public, max-age=31536000, immutable

/puzzles/*
  Cache-Control: public, max-age=86400
```

4. **Lazy Load Ads** - Use AdSense async loading (already included)

## Troubleshooting

### Puzzle Generation Fails

- Increase `max_attempts` in `place_words_into_grid()`
- Reduce `target_words` for difficulty level
- Add more words to category word banks

### GitHub Actions Not Running

- Check Actions tab in GitHub repo
- Verify workflow file is in `.github/workflows/`
- Check repo permissions allow Actions

### Netlify Deploy Fails

- Verify `site/` directory exists
- Check build logs for Python errors
- Ensure Python 3.10+ is specified in build settings

## License

MIT License - Free to use and modify for your projects.

## Support

For questions or issues:
- Email: contact@dailycrossword.world
- GitHub Issues: [Create an issue](https://github.com/yourusername/dailycrossword/issues)

## Roadmap

- [ ] User accounts and progress tracking
- [ ] Leaderboards and timing
- [ ] Hints system
- [ ] Mobile app (PWA)
- [ ] Multiplayer mode
- [ ] Custom puzzle creator
- [ ] API for third-party integrations

---

**Built with ❤️ for crossword enthusiasts worldwide**
