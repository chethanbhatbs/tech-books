# Deployment

The repo IS the site. There is no build step. The two `.html` books, the two `.pdf` files, the `index.html` landing page, and the assets under `docs/images/` are everything a host needs to serve. The only question is *which* host.

This guide covers four options, in order of how much I recommend them for a **private** repository that you want previewable on the open web.

## A · Cloudflare Pages — recommended

Free. Connects to private GitHub repos. Builds in seconds. Custom domains are one click.

1. Go to <https://dash.cloudflare.com> → **Pages** → **Create a project** → **Connect to Git**.
2. Install the **Cloudflare Pages** GitHub app on your account if asked, and grant it access to **`chethanbhatbs/python-mastery`**.
3. Pick the repo, then on the build screen:
   - **Framework preset:** *None*
   - **Build command:** *(leave blank)*
   - **Build output directory:** `/` (the repo root)
4. Click **Save and Deploy**.
5. Within about 30 seconds you get a URL like `https://python-mastery.pages.dev/`. Every push to `main` redeploys automatically.

Resulting URLs:

```
https://python-mastery.pages.dev/                    landing page
https://python-mastery.pages.dev/python-mastery.html the textbook
https://python-mastery.pages.dev/python-handbook.html the handbook
https://python-mastery.pages.dev/book                /python-mastery.html (via _redirects)
https://python-mastery.pages.dev/handbook            /python-handbook.html
```

Cloudflare Pages reads `_headers` and `_redirects` natively, so caching and aliases just work.

## B · Netlify

Also free, also supports private GitHub repos. Slightly more UI surface area, otherwise equivalent.

1. <https://app.netlify.com> → **Add new site** → **Import an existing project** → **GitHub**.
2. Authorise Netlify on `chethanbhatbs/python-mastery`.
3. Build settings:
   - **Branch to deploy:** `main`
   - **Build command:** *(leave blank — `netlify.toml` already sets this)*
   - **Publish directory:** `.`
4. **Deploy site.** You get a URL like `https://python-mastery.netlify.app/`.

`netlify.toml`, `_headers`, and `_redirects` are all read automatically.

## C · GitHub Pages

GitHub Pages works for **public** repositories on every plan, but only on **Pro / Team / Enterprise** for **private** repositories. If you are on a free plan and the repo is private, GitHub Pages is not an option.

If you are eligible:

1. Repository → **Settings** → **Pages**.
2. Source: **Deploy from a branch**, branch **`main`**, folder **`/ (root)`**.
3. Save. After a minute the site is live at `https://chethanbhatbs.github.io/python-mastery/`.

Note that GitHub Pages does not honour `netlify.toml`. `_headers` and `_redirects` are also ignored. Cache-Control headers fall back to GitHub's defaults.

## D · Make the repo public

If the work is meant to be read anyway, this is the simplest path. With the repo public, two free third-party previewers render the HTML directly from the raw file on GitHub:

- **htmlpreview.github.io** — paste the URL of the raw file:
  ```
  https://htmlpreview.github.io/?https://github.com/chethanbhatbs/python-mastery/blob/main/python-mastery.html
  https://htmlpreview.github.io/?https://github.com/chethanbhatbs/python-mastery/blob/main/python-handbook.html
  https://htmlpreview.github.io/?https://github.com/chethanbhatbs/python-mastery/blob/main/index.html
  ```
- **raw.githack.com** — same idea, paste a `github.com/.../blob/...` URL:
  ```
  https://rawcdn.githack.com/chethanbhatbs/python-mastery/main/python-mastery.html
  ```

Both work only while the repository is public.

## Recommendation

If you want preview links you can share without changing the repo's visibility, **Cloudflare Pages**. It is free, accepts private GitHub repos, builds in seconds, reads `_headers` and `_redirects`, and gives a stable `pages.dev` URL plus an optional custom domain. Netlify is a fine fallback if you already have an account.

If the project is meant to be read publicly anyway, the simplest possible path is to flip the repo to public and link to `htmlpreview.github.io`. No deployment to configure, no second account, nothing to maintain.
