import json
import os
import shutil

print("Initiating MASWOS integration into Antigravity...")

ag_path = os.path.expanduser(r"~/.gemini/antigravity")
ag_mcp_config = os.path.join(ag_path, "mcp_config.json")
maswos_mcp_config = "mcp_servers_config.json"

if os.path.exists(ag_mcp_config):
    with open(ag_mcp_config, "r", encoding="utf-8") as f:
        ag_mcp = json.load(f)
else:
    ag_mcp = {"mcpServers": {}}

if os.path.exists(maswos_mcp_config):
    with open(maswos_mcp_config, "r", encoding="utf-8") as f:
        maswos_mcp = json.load(f)
    
    # Merge servers
    for name, config in maswos_mcp.get("mcpServers", {}).items():
        ag_mcp["mcpServers"][name] = config
    
    # Copy maswos specific config
    if "maswos_config" in maswos_mcp:
        ag_mcp["maswos_config"] = maswos_mcp["maswos_config"]
        
    with open(ag_mcp_config, "w", encoding="utf-8") as f:
        json.dump(ag_mcp, f, indent=2)
    print("Merged MCP configs.")

ag_skills = os.path.join(ag_path, "skills")
maswos_skills = os.path.join(".agent", "skills")

if os.path.exists(maswos_skills):
    for skill_dir in os.listdir(maswos_skills):
        src = os.path.join(maswos_skills, skill_dir)
        dst = os.path.join(ag_skills, skill_dir)
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
    print(f"Copied all skills from {maswos_skills} to {ag_skills}.")

ag_maswos = os.path.join(ag_path, "maswos")
if not os.path.exists(ag_maswos):
    os.makedirs(ag_maswos)

# Create rags, templates directories in Antigravity
for folder in ["rags", "templates", "agents", "env"]:
    os.makedirs(os.path.join(ag_maswos, folder), exist_ok=True)

# Copy python agents and orchestrators
files_to_copy = [
    f for f in os.listdir(".") if f.endswith(".py") or f.endswith(".json") or f.endswith(".md") or f.endswith(".env") or f == ".env"
]
for f in files_to_copy:
    if os.path.isfile(f):
        shutil.copy2(f, os.path.join(ag_maswos, f))
print("Copied Python agents, configs, and MD files to global Antigravity folder.")

# Also handle `.agent` dir agents
maswos_agents_dir = os.path.join(".agent", "agents")
if os.path.exists(maswos_agents_dir):
    ag_maswos_agents = os.path.join(ag_maswos, "agents")
    for a in os.listdir(maswos_agents_dir):
        src = os.path.join(maswos_agents_dir, a)
        dst = os.path.join(ag_maswos_agents, a)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            
# RAGs and other subdirs
for d in ["rag", "mcp-ecossistema-tese", "mcp-tese-completa"]:
    if os.path.exists(d):
        dst = os.path.join(ag_maswos, d)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(d, dst)

print("MASWOS ecosystem fully integrated exactly like a Transformer Network into Antigravity.")
