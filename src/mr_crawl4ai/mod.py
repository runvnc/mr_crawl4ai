print("Loading mod.py for Crawl4AI Web Fetcher")

import asyncio
from lib.providers.commands import command
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, DFSDeepCrawlStrategy

@command()
async def fetch_webpage(url, context=None):
    """Fetch and extract the main content from a given URL using Crawl4AI.

    Args:
        url (str): The URL to fetch and extract content from.
        context (object, optional): The context object for the current session.

    Returns:
        str: The extracted main content of the webpage in Markdown format, or an error message if extraction fails.

    Example:
        [
            { "fetch_webpage": { "url": "https://www.example.com/article" } }
        ]
    """
    try:
        browser_config = BrowserConfig(
            headless=True,
            verbose=False,
        )
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=run_config
            )
            
            if result.success:
                content = result.markdown
                if content and content.strip():
                    return f"Extracted content from {url}:\n\n{content}"
                else:
                    return f"Successfully fetched {url} but no content was extracted."
            else:
                return f"Failed to fetch content from {url}: {result.error_message if hasattr(result, 'error_message') else 'Unknown error'}"
                
    except Exception as e:
        return f"Error fetching webpage {url}: {str(e)}"


@command()
async def crawl_site(url, max_pages=20, max_depth=2, page_limit=10000, total_limit=30000, strategy="bfs", context=None):
    """Deep crawl a website starting from a URL, following internal links.

    Args:
        url (str): The starting URL to crawl.
        max_pages (int, optional): Maximum number of pages to crawl. Defaults to 20.
        max_depth (int, optional): Maximum link depth to follow. Defaults to 2.
        page_limit (int, optional): Maximum characters per page content. Defaults to 10000.
        total_limit (int, optional): Maximum total characters across all pages. Defaults to 30000.
        strategy (str, optional): Crawl strategy - 'bfs' (breadth-first) or 'dfs' (depth-first). Defaults to 'bfs'.
        context (object, optional): The context object for the current session.

    Returns:
        str: Formatted results showing crawled pages with their content.

    Example:
        [
            { "crawl_site": { "url": "https://docs.example.com", "max_pages": 10, "max_depth": 2 } }
        ]
    """
    try:
        browser_config = BrowserConfig(
            headless=True,
            verbose=False,
        )
        
        # Choose strategy
        if strategy.lower() == "dfs":
            crawl_strategy = DFSDeepCrawlStrategy(
                max_depth=max_depth,
                max_pages=max_pages,
            )
        else:
            crawl_strategy = BFSDeepCrawlStrategy(
                max_depth=max_depth,
                max_pages=max_pages,
            )
        
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
            deep_crawl_strategy=crawl_strategy,
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            results = await crawler.arun(
                url=url,
                config=run_config
            )
            
            if not results:
                return f"No pages crawled from {url}"
            
            # Handle single result or list of results
            if not isinstance(results, list):
                results = [results]
            
            output_lines = [f"Crawled {len(results)} pages from {url} (max depth: {max_depth}, strategy: {strategy.upper()})\n"]
            
            total_chars = 0
            
            for i, result in enumerate(results, 1):
                if not result.success:
                    output_lines.append(f"\n---\nPage {i}: {result.url}\nStatus: Failed - {result.error_message if hasattr(result, 'error_message') else 'Unknown error'}\n")
                    continue
                
                depth = getattr(result, 'depth', 'unknown')
                title = getattr(result, 'title', 'No title')
                content = result.markdown if result.markdown else "No content extracted"
                
                # Truncate content to page_limit
                if len(content) > page_limit:
                    content = content[:page_limit] + "\n\n[Content truncated...]"
                
                page_output = f"\n---\nPage {i}: {result.url}\nDepth: {depth}\nTitle: {title}\nContent:\n{content}\n"
                
                # Check total limit
                total_chars += len(page_output)
                if total_chars > total_limit:
                    remaining = total_limit - (total_chars - len(page_output))
                    if remaining > 100:
                        output_lines.append(page_output[:remaining])
                    output_lines.append(f"\n[Total content limit of {total_limit} characters reached. Stopping output.]\n")
                    break
                
                output_lines.append(page_output)
            
            return "".join(output_lines)
                
    except Exception as e:
        return f"Error crawling site {url}: {str(e)}"


print("Loaded mod.py for Crawl4AI Web Fetcher")
