import xmltodict
import sys

# simple utility to enable optional numerical features
vm_path = sys.argv[1]
config_path = sys.argv[2]

# extract unsatisfied constraints from feature model
with open(vm_path, "r") as f:
	vm = xmltodict.parse(f.read())

# read all configurations from sample
with open(config_path, "r") as f:
	configs = f.readlines()
	configs = list(map(lambda x: x.replace("\n", ""), configs))
		
nf = vm["vm"]["numericOptions"]["configurationOption"]

implications = dict()
for f in nf:
	implications[f["name"]] = f["parent"]
	
neo_configs = []
i=0
for config in configs:
	binaries = list(filter(lambda x: ';' not in x and x != "", config.split('"')[1].split('%')))
	not_satisfied = []
	for key in implications:
		if implications[key] not in binaries:
			not_satisfied.append(key)
	split3 = config.split('"')
	
	split31 = split3[1].split("%;%")[:-1]
	
	for feature in not_satisfied:
		split31 = list(filter(lambda s: not s.startswith(feature), split31))
	
	#print(split31)
	joined = "prefix \"" + "%;%".join(split31)+"%;%" + "\" postfix"
	
	neo_configs.append(joined)
	 
neo_configs = set(neo_configs)
neo_configs = list(neo_configs)

with open(config_path, 'w') as f:
    f.writelines(neo_conf + '\n' for neo_conf in neo_configs)

