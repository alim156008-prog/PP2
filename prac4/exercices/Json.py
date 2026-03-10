import json

with open('sample-data.json') as f:
    data = json.load(f)

print("Interface Status")
print("=" * 81)
print(f"{'DN':51} {'Description':20} {'Speed':9} {'MTU':6}")
print("-" * 51, '-' * 18, ' ', '-' * 6, ' ', '-' * 6)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    
    dn = attributes.get("dn", "")
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")
    
    print(f"{dn:51} {descr:19} {speed:10} {mtu:6}")