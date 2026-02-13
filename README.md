# mr_crawl4ai

MindRoot plugin for web crawling and content extraction using [Crawl4AI](https://github.com/unclecode/crawl4ai).

## Overview

This plugin provides enhanced web fetching capabilities for MindRoot agents, replacing the simpler trafilatura-based extraction in mr_tavily_search with a full browser-based approach that handles JavaScript-heavy sites, dynamic content, and deep crawling.

## Features

- **fetch_webpage** - Extract clean markdown from a single URL
- **crawl_site** - Deep crawl entire sites following links with configurable depth and limits

## Installation

```bash
cd /xfiles/plugins_ah/mr_crawl4ai
pip install -e .
crawl4ai-setup
```

The `crawl4ai-setup` command automatically installs and configures Playwright browsers. If you encounter browser-related issues, you can manually install:

```bash
python -m playwright install chromium
```

## Commands

### fetch_webpage

Extract markdown content from a single URL.

```json
{ "fetch_webpage": { "url": "https://example.com/article" } }
```

**Parameters:**
- `url` (required) - The URL to fetch

**Returns:** Extracted markdown content or error message.

---

### crawl_site

Deep crawl a website starting from a URL, following internal links.

```json
{ "crawl_site": { "url": "https://docs.example.com", "max_pages": 10, "max_depth": 2 } }
```

**Parameters:**
- `url` (required) - Starting URL for the crawl
- `max_pages` (optional) - Maximum pages to crawl (default: 20)
- `max_depth` (optional) - Maximum link depth (default: 2)
- `page_limit` (optional) - Max characters per page (default: 10000)
- `total_limit` (optional) - Max total characters output (default: 30000)
- `strategy` (optional) - 'bfs' or 'dfs' (default: 'bfs')

**Returns:** Formatted list of crawled pages with URL, depth, title, and content.

## Why Crawl4AI?

Compared to the trafilatura-based fetch in mr_tavily_search:

- **JavaScript rendering** - Full browser execution for SPAs and dynamic content
- **Better extraction** - Cleaner markdown with smart content filtering
- **Deep crawling** - Follow links and crawl entire site sections
- **More reliable** - Handles complex sites that trafilatura misses

## Dependencies

- crawl4ai
- playwright (auto-installed via crawl4ai-setup)

## License

Apache 2.0
