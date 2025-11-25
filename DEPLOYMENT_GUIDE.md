# Deployment Guide for dailycrossword.world

## Quick Deploy Options

### Option 1: Netlify (Recommended - Easiest)

#### Method A: Drag & Drop (No Git Required)

1. **Generate your site:**
   ```bash
   python generate.py --start 2025-01-01 --days 30 --out site --difficulty easy --categories general,tech,travel,kids,devotional,holiday
   ```

2. **Go to Netlify:**
   - Visit [netlify.com](https://netlify.com)
   - Sign up for free account
   - Click "Add new site" → "Deploy manually"

3. **Drag & Drop:**
   - Drag the entire `site/` folder to the upload area
   - Wait 30 seconds for deployment
   - Your site is live at `random-name.netlify.app`

4. **Add Custom Domain:**
   - Go to Site settings → Domain management
   - Click "Add custom domain"
   - Enter `dailycrossword.world`
   - Follow DNS configuration instructions
   - Add these DNS records at your domain registrar:
     ```
     Type: A
     Name: @
     Value: 75.2.60.5
     
     Type: CNAME
     Name: www
     Value: your-site.netlify.app
     ```

5. **Enable HTTPS:**
   - Netlify automatically provisions SSL certificate
   - Wait 24 hours for DNS propagation
   - HTTPS will be enabled automatically

#### Method B: Git-Based Deployment (Recommended for Auto-Updates)

1. **Create GitHub Repository:**
   ```bash
   cd "c:\Users\pamar\OneDrive\Desktop\puzzle maker"
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/dailycrossword.git
   git push -u origin main
   ```

2. **Connect to Netlify:**
   - Go to [netlify.com](https://netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Choose "GitHub" and authorize
   - Select your repository

3. **Configure Build Settings:**
   ```
   Build command: python generate.py --start $(date +%Y-%m-%d) --days 30 --out site --difficulty easy --categories general,tech,travel,kids,devotional,holiday
   Publish directory: site
   ```

4. **Deploy:**
   - Click "Deploy site"
   - Netlify will build and deploy automatically
   - Every git push will trigger a new deployment

5. **Enable GitHub Actions (Optional):**
   - The included `.github/workflows/generate.yml` will auto-generate puzzles daily
   - GitHub Actions is free for public repositories
   - Netlify will auto-deploy when changes are pushed

---

### Option 2: Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd site
   vercel --prod
   ```

3. **Add Custom Domain:**
   - Go to Vercel dashboard
   - Project settings → Domains
   - Add `dailycrossword.world`
   - Configure DNS as instructed

---

### Option 3: GitHub Pages (Free)

1. **Create GitHub Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/dailycrossword.git
   git push -u origin main
   ```

2. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/site`
   - Save

3. **Add Custom Domain:**
   - In Pages settings, add custom domain: `dailycrossword.world`
   - Create `site/CNAME` file with content: `dailycrossword.world`
   - Configure DNS:
     ```
     Type: A
     Name: @
     Value: 185.199.108.153
     Value: 185.199.109.153
     Value: 185.199.110.153
     Value: 185.199.111.153
     
     Type: CNAME
     Name: www
     Value: yourusername.github.io
     ```

4. **Enable HTTPS:**
   - Check "Enforce HTTPS" in Pages settings
   - Wait for certificate provisioning (up to 24 hours)

---

### Option 4: AWS S3 + CloudFront

1. **Create S3 Bucket:**
   ```bash
   aws s3 mb s3://dailycrossword.world
   aws s3 website s3://dailycrossword.world --index-document index.html
   ```

2. **Upload Site:**
   ```bash
   aws s3 sync site/ s3://dailycrossword.world --delete
   ```

3. **Configure Bucket Policy:**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Sid": "PublicReadGetObject",
       "Effect": "Allow",
       "Principal": "*",
       "Action": "s3:GetObject",
       "Resource": "arn:aws:s3:::dailycrossword.world/*"
     }]
   }
   ```

4. **Create CloudFront Distribution:**
   - Origin: S3 bucket website endpoint
   - Alternate domain: `dailycrossword.world`, `www.dailycrossword.world`
   - SSL certificate: Request from ACM (free)
   - Default root object: `index.html`

5. **Configure DNS:**
   ```
   Type: A (Alias)
   Name: @
   Value: CloudFront distribution domain
   
   Type: CNAME
   Name: www
   Value: CloudFront distribution domain
   ```

---

### Option 5: Cloudflare Pages

1. **Connect GitHub:**
   - Go to [pages.cloudflare.com](https://pages.cloudflare.com)
   - Click "Create a project"
   - Connect GitHub account
   - Select repository

2. **Configure Build:**
   ```
   Build command: python generate.py --start $(date +%Y-%m-%d) --days 30 --out site
   Build output directory: site
   ```

3. **Add Custom Domain:**
   - Project settings → Custom domains
   - Add `dailycrossword.world`
   - Cloudflare will auto-configure DNS if domain is on Cloudflare

---

## Domain Registration

### Recommended Registrars

1. **Namecheap** - $8.88/year for .world domains
2. **Google Domains** - $12/year
3. **Cloudflare** - At-cost pricing (~$9/year)
4. **GoDaddy** - $11.99/year (often has sales)

### Purchase Steps

1. Search for `dailycrossword.world`
2. Add to cart
3. Disable auto-renewal of extras (privacy protection is free on most)
4. Complete purchase
5. Configure DNS (see deployment option above)

---

## DNS Configuration

### Netlify DNS Records
```
Type: A
Name: @
Value: 75.2.60.5
TTL: 3600

Type: CNAME
Name: www
Value: your-site.netlify.app
TTL: 3600
```

### Cloudflare DNS (if using Cloudflare Pages)
```
Type: CNAME
Name: @
Value: your-site.pages.dev
Proxy: Enabled (orange cloud)

Type: CNAME
Name: www
Value: your-site.pages.dev
Proxy: Enabled
```

### Verification
```bash
# Check DNS propagation
nslookup dailycrossword.world
dig dailycrossword.world

# Online tools
https://dnschecker.org
https://www.whatsmydns.net
```

---

## SSL/HTTPS Setup

### Netlify (Automatic)
- SSL certificate auto-provisioned via Let's Encrypt
- No configuration needed
- Renews automatically

### Cloudflare (Automatic)
- Universal SSL included free
- Enabled by default
- Full (strict) mode recommended

### AWS CloudFront
1. Request certificate in ACM (us-east-1 region)
2. Verify domain ownership via email or DNS
3. Attach certificate to CloudFront distribution
4. Enable "Redirect HTTP to HTTPS"

---

## Performance Optimization

### Enable Caching

#### Netlify `_headers` file
Create `site/_headers`:
```
/*
  Cache-Control: public, max-age=3600, must-revalidate

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/puzzles/*
  Cache-Control: public, max-age=86400
```

#### Cloudflare Page Rules
```
URL: dailycrossword.world/assets/*
Cache Level: Cache Everything
Edge Cache TTL: 1 month

URL: dailycrossword.world/puzzles/*
Cache Level: Cache Everything
Edge Cache TTL: 1 day
```

### Enable Compression

#### Netlify `netlify.toml`
Create `netlify.toml`:
```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "*.js"
  [headers.values]
    Content-Type = "application/javascript; charset=utf-8"

[[headers]]
  for = "*.css"
  [headers.values]
    Content-Type = "text/css; charset=utf-8"
```

---

## Monitoring & Analytics

### Google Analytics 4

1. **Create GA4 Property:**
   - Go to [analytics.google.com](https://analytics.google.com)
   - Create account and property
   - Get Measurement ID (G-XXXXXXXXXX)

2. **Add to Site:**
   Edit `generate.py` and add to HTML_HEAD:
   ```python
   GA_CODE = '''
   <!-- Google tag (gtag.js) -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   '''
   ```

3. **Regenerate Site:**
   ```bash
   python generate.py --start 2025-01-01 --days 30 --out site
   ```

### Google Search Console

1. **Add Property:**
   - Go to [search.google.com/search-console](https://search.google.com/search-console)
   - Add property: `dailycrossword.world`

2. **Verify Ownership:**
   - Method 1: HTML file upload (download verification file, add to `site/`)
   - Method 2: Meta tag (add to `<head>` in generate.py)
   - Method 3: DNS record (add TXT record to domain)

3. **Submit Sitemap:**
   - Go to Sitemaps section
   - Submit: `https://dailycrossword.world/sitemap.xml`

### Uptime Monitoring

**Free Tools:**
- [UptimeRobot](https://uptimerobot.com) - 50 monitors free
- [Pingdom](https://pingdom.com) - Free tier available
- [StatusCake](https://statuscake.com) - Free tier

**Setup:**
1. Create account
2. Add monitor for `https://dailycrossword.world`
3. Set check interval (5 minutes)
4. Add email/SMS alerts

---

## Backup Strategy

### Automated Git Backups

```bash
# Add to cron or Task Scheduler
cd "c:\Users\pamar\OneDrive\Desktop\puzzle maker"
git add site
git commit -m "Backup $(date +%Y-%m-%d)"
git push origin main
```

### Manual Backups

```bash
# Create zip archive
cd site
tar -czf ../backup-$(date +%Y%m%d).tar.gz .

# Or on Windows
powershell Compress-Archive -Path site -DestinationPath backup-$(Get-Date -Format 'yyyyMMdd').zip
```

### Cloud Backups

**Option 1: AWS S3**
```bash
aws s3 sync site/ s3://dailycrossword-backup/$(date +%Y%m%d)/
```

**Option 2: Google Drive**
- Use [rclone](https://rclone.org)
```bash
rclone sync site/ gdrive:dailycrossword-backup/
```

---

## Continuous Deployment

### GitHub Actions (Already Configured)

The included `.github/workflows/generate.yml` automatically:
1. Runs daily at 00:05 UTC
2. Generates next 7 days of puzzles
3. Commits to repository
4. Triggers Netlify/Vercel deployment

**To enable:**
1. Push code to GitHub
2. Ensure Actions are enabled (Settings → Actions → Allow all actions)
3. Workflow runs automatically

**Manual trigger:**
- Go to Actions tab
- Select "Generate Daily Crosswords"
- Click "Run workflow"

### Custom Schedule

Edit `.github/workflows/generate.yml`:
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Midnight UTC daily
    - cron: '0 12 * * *' # Noon UTC daily (twice daily)
```

---

## Troubleshooting

### Site Not Loading

1. **Check DNS:**
   ```bash
   nslookup dailycrossword.world
   ```
   Should return your hosting provider's IP

2. **Check SSL:**
   ```bash
   curl -I https://dailycrossword.world
   ```
   Should return 200 OK

3. **Clear Cache:**
   - Browser cache: Ctrl+Shift+R
   - Cloudflare cache: Purge Everything
   - Netlify cache: Clear cache and deploy

### Puzzles Not Generating

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.7+
   ```

2. **Check script errors:**
   ```bash
   python generate.py --start 2025-01-01 --days 1 --out test
   ```

3. **Check GitHub Actions logs:**
   - Go to Actions tab
   - Click on failed workflow
   - Review error messages

### GitHub Actions Not Running

1. **Check workflow file location:**
   - Must be in `.github/workflows/generate.yml`

2. **Check repository permissions:**
   - Settings → Actions → General
   - Workflow permissions: Read and write

3. **Check cron syntax:**
   - Use [crontab.guru](https://crontab.guru) to verify

### Slow Site Performance

1. **Enable caching** (see Performance Optimization above)

2. **Optimize images:**
   ```bash
   # Install ImageMagick
   magick convert logo.png -quality 85 -strip logo-optimized.png
   ```

3. **Minify CSS/JS:**
   - Use [CSS Minifier](https://cssminifier.com)
   - Use [JS Minifier](https://javascript-minifier.com)

4. **Enable CDN:**
   - Cloudflare (free tier)
   - AWS CloudFront
   - Netlify CDN (included)

---

## Cost Breakdown

### Free Tier (Recommended for Start)

| Service | Cost | Limits |
|---------|------|--------|
| Netlify | $0 | 100GB bandwidth/month |
| GitHub | $0 | Unlimited public repos |
| GitHub Actions | $0 | 2,000 minutes/month |
| Cloudflare | $0 | Unlimited bandwidth |
| Let's Encrypt SSL | $0 | Unlimited certificates |
| **Total** | **$0/month** | |

**Only cost:** Domain registration (~$9-12/year)

### Paid Tier (For High Traffic)

| Service | Cost | Features |
|---------|------|----------|
| Netlify Pro | $19/month | 400GB bandwidth |
| Domain | $9/year | .world TLD |
| Google Workspace | $6/month | Professional email |
| **Total** | **$25/month** | |

### Enterprise (100K+ visitors/month)

| Service | Cost | Features |
|---------|------|----------|
| AWS S3 + CloudFront | ~$50/month | Unlimited bandwidth |
| Domain | $9/year | .world TLD |
| AWS Route 53 | $0.50/month | DNS hosting |
| **Total** | **~$50/month** | |

---

## Launch Checklist

### Pre-Launch (Week 1)

- [ ] Register domain `dailycrossword.world`
- [ ] Generate 30 days of puzzles
- [ ] Test all pages locally
- [ ] Optimize images (logo, icons)
- [ ] Set up Google Analytics
- [ ] Set up Google Search Console
- [ ] Create social media accounts
- [ ] Write launch announcement

### Launch Day

- [ ] Deploy to Netlify/Vercel
- [ ] Configure custom domain
- [ ] Enable HTTPS
- [ ] Submit sitemap to Google
- [ ] Test on mobile devices
- [ ] Share on social media
- [ ] Post to Reddit (r/crossword, r/puzzles)
- [ ] Email friends/family

### Post-Launch (Week 1)

- [ ] Monitor analytics daily
- [ ] Fix any reported bugs
- [ ] Respond to user feedback
- [ ] Generate next 30 days of puzzles
- [ ] Start SEO content creation
- [ ] Build backlinks (5-10)
- [ ] Create Pinterest boards

### Month 1

- [ ] Reach 100 daily visitors
- [ ] Publish 5 blog posts
- [ ] Build 20 backlinks
- [ ] Grow social media (100 followers)
- [ ] Set up email newsletter
- [ ] Optimize top-performing pages

### Month 6

- [ ] Reach 500 daily visitors
- [ ] Apply to Google AdSense
- [ ] Launch premium features (optional)
- [ ] Create mobile app (PWA)
- [ ] Partner with puzzle bloggers

---

## Support & Resources

### Documentation
- [Netlify Docs](https://docs.netlify.com)
- [GitHub Actions Docs](https://docs.github.com/actions)
- [Python Docs](https://docs.python.org)

### Communities
- [r/crossword](https://reddit.com/r/crossword)
- [r/webdev](https://reddit.com/r/webdev)
- [Netlify Community](https://answers.netlify.com)

### Tools
- [Netlify CLI](https://docs.netlify.com/cli/get-started/)
- [GitHub CLI](https://cli.github.com)
- [VS Code](https://code.visualstudio.com)

---

## Next Steps

1. **Deploy Now:**
   ```bash
   # Quick deploy to Netlify
   cd site
   netlify deploy --prod
   ```

2. **Set Up Automation:**
   - Push to GitHub
   - Enable GitHub Actions
   - Connect to Netlify

3. **Start Marketing:**
   - Create social media accounts
   - Submit to puzzle directories
   - Write first blog post

4. **Monitor & Optimize:**
   - Check Google Analytics daily
   - Optimize based on user behavior
   - Generate more puzzles

**You're ready to launch! 🚀**
