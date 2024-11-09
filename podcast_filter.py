def filter_podcast_feed(original_feed_url, filter_words, output_file='filtered_feed.xml'):
    """
    Creates a filtered RSS feed from a podcast feed URL.
    
    Args:
        original_feed_url (str): URL of the original podcast RSS feed
        filter_words (list): List of words to filter titles by (case insensitive)
        output_file (str): Path to save the filtered RSS feed
    """
    # Parse the original feed
    feed = feedparser.parse(original_feed_url)
    
    # Create a new feed
    fg = FeedGenerator()
    
    # Copy over feed metadata
    fg.title(feed.feed.title)
    fg.link(href=feed.feed.link)
    fg.description(feed.feed.description)
    fg.language(feed.feed.language)
    #fg.podcast.itunes_author(feed.feed.author if 'author' in feed.feed else '')
    
    # Filter and add entries
    for entry in feed.entries:
        # Check if any filter word appears in the title
        title = entry.title.lower()
        if any(word.lower() in title for word in filter_words):
            fe = fg.add_entry()
            fe.title(entry.title)
            #fe.link(href=entry.link)
            fe.description(entry.description)
            
            # Add audio enclosure
            if 'enclosures' in entry and len(entry.enclosures) > 0:
                fe.enclosure(entry.enclosures[0].href, 
                           length=entry.enclosures[0].length,
                           type=entry.enclosures[0].type)
            
            # Add publication date
            if 'published' in entry:
                fe.published(entry.published)
    
    # Save the filtered feed
    fg.rss_file(output_file)
    return output_file

# Example usage
if __name__ == "__main__":
    feed_url = "https://feeds.megaphone.fm/tmastl"
    filter_words = ["TMA", "Hour"]
    filtered_feed = filter_podcast_feed(feed_url, filter_words)