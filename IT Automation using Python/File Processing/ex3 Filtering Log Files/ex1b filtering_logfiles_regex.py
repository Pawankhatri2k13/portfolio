
import re
import sys

logfile = sys.argv[1]
string_search = "CRON"
usernames = {}
with open(logfile) as f:
	for line in f:
		if string_search not in line:
			continue

		pattern = r"USER \((\w+)\)$"
		result = re.search(pattern, line)

		if result is None:
			continue
		name = result[1]
		usernames[name] = usernames.get(name,0)+1

print(usernames)
			