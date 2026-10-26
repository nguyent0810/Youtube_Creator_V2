import subprocess
r = subprocess.run(["wmic", "process", "where", "ProcessId=14596", "get", "CommandLine,CreationDate,WorkingSetSize", "/FORMAT:LIST"], capture_output=True, text=True, errors="replace")
print(r.stdout)
r2 = subprocess.run(["wmic", "process", "where", "ProcessId=4996", "get", "CommandLine,CreationDate", "/FORMAT:LIST"], capture_output=True, text=True, errors="replace")
print("---4996---")
print(r2.stdout)
