from orchestrator import Orchestrator
import json

orch = Orchestrator('')

response = orch.request('get', orch.Jobs + '(7475429)')

print(response)
response = json.loads(response["OutputArguments"])
print(response)

departure_data = response["Departure_Data"]
arrival_data = response["Arrival_Data"]