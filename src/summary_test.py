from summarizer import OfflineSummarizer


def main():
    # Sample long-ish text (you can replace this later with real transcript)
    text = """
    Motivation isn't something you wait for, it's something you build.
    Every day you show up and put in the work, you train your mind and body
    to move even when you don't feel like it. Progress comes from discipline,
    not from random bursts of inspiration. If you rely only on motivation,
    you'll work only on the days you feel good. But if you build discipline,
    you'll work even on the days you feel tired, bored, or scared. That's how
    dreams are turned into reality – small, consistent actions over time.
    """

    summarizer = OfflineSummarizer(max_sentences=3)
    summary = summarizer.summarize(text)

    print("===== ORIGINAL TEXT =====\n")
    print(text.strip())
    print("\n===== SUMMARY =====\n")
    print(summary)


if __name__ == "__main__":
    main()
