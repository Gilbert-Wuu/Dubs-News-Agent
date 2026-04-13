from agent_tools_langgraph import graph
import datetime

print(f"\n--- Pipeline started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

if __name__ == "__main__":
    result = graph.invoke({"keyword": "Golden State Warriors"})
    print("\n--- Pipeline Complete ---")
    print(f"Articles scraped  : {len(result.get('scraped_articles', []))}")
    print(f"Summaries created : {len(result.get('summaries', []))}")
    print(f"Email sent        : {result.get('notification_sent', False)}")
