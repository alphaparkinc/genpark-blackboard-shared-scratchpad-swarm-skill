from client import BlackboardSwarm

bb = BlackboardSwarm()
bb.post_task("fetch_data", "Fetch user analytics logs", "network_io")
bb.post_task("summarize", "Summarize metric anomalies", "data_science")

bb.contribute("Agent_Scraper", "fetch_data", {"records": 1500, "status": "200 OK"})
bb.contribute("Agent_Analyst", "summarize", {"anomalies_detected": 2})

print("Blackboard Global State:", bb.state)
