import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Azure Solution Recommender", layout="wide")

@st.cache_data(ttl=3600)
def fetch_azure_services():
    # FULL Azure product list as of mid-2024. (Shortened for brevity; use your full list in production)
    return [
        {"name": "Azure Cache for Redis", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cache/"},
        {"name": "Azure Container Apps", "category": "Containers", "docs": "https://learn.microsoft.com/en-us/azure/container-apps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-apps/"},
        {"name": "Azure Container Instances", "category": "Containers", "docs": "https://learn.microsoft.com/en-us/azure/container-instances/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-instances/"},
        {"name": "Azure Data Lake Storage", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/storage/data-lake-storage/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/data-lake/"},
        {"name": "Azure Database for MariaDB", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/mariadb/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/mariadb/"},
        {"name": "Azure Database for MySQL", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/mysql/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/mysql/"},
        {"name": "Azure Database for PostgreSQL", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/postgresql/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/postgresql/"},
        {"name": "Azure Kubernetes Service (AKS)", "category": "Containers", "docs": "https://learn.microsoft.com/en-us/azure/aks/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/"},
        # ... (add all other services here, as in the previous full version)
    ]

SERVICE_OVERVIEWS = {
    "Azure Cache for Redis": {
        "overview": "A fully managed, in-memory cache that enables high-performance and scalable architectures. Commonly used for session storage, caching, and pub/sub.",
        "pros": ["Low latency", "Highly scalable", "Fully managed"],
        "cons": ["Additional cost", "No persistent storage"]
    },
    "Azure Container Apps": {
        "overview": "Enables you to build and deploy microservices and containerized apps on a serverless platform.",
        "pros": ["Serverless containers", "Easy scaling", "Kubernetes-based"],
        "cons": ["Limited advanced customizations compared to AKS"]
    },
    "Azure Kubernetes Service (AKS)": {
        "overview": "Managed Kubernetes container orchestration service for deploying, managing, and scaling containerized applications.",
        "pros": ["Full Kubernetes control", "Integration with Azure ecosystem", "Scalability"],
        "cons": ["Steeper learning curve", "Requires cluster management"]
    },
    "Azure Data Lake Storage": {
        "overview": "A scalable and secure data lake for high-performance analytics workloads.",
        "pros": ["Massive scalability", "Fine-grained security", "Optimized for analytics"],
        "cons": ["Requires data governance", "Possible overkill for small data"]
    },
    "Azure Database for MariaDB": {
        "overview": "Fully managed MariaDB database with built-in high availability and security.",
        "pros": ["Managed service", "Automatic patching", "High availability"],
        "cons": ["Limited to MariaDB workloads"]
    },
    "Azure Database for MySQL": {
        "overview": "Managed MySQL database service for app development and deployment.",
        "pros": ["Automatic backups", "High availability", "Security features"],
        "cons": ["Cost", "Some feature limitations vs. self-hosted"]
    },
    "Azure Database for PostgreSQL": {
        "overview": "Managed PostgreSQL database service with high availability, security, and scalability.",
        "pros": ["Fully managed", "Scalable", "Automatic patching"],
        "cons": ["More expensive than self-hosted"]
    },
    "Azure Container Instances": {
        "overview": "Run containers without managing servers or clusters. Great for simple, stateless apps or jobs.",
        "pros": ["Fast startup", "No cluster management", "Pay-per-use"],
        "cons": ["Not for complex orchestrations", "Short-lived workloads"]
    }
    # Add more as needed!
}

def get_service_overview(name, category):
    if name in SERVICE_OVERVIEWS:
        return SERVICE_OVERVIEWS[name]
    return {
        "overview": f"A Microsoft Azure service in the {category} category. See documentation for details.",
        "pros": [],
        "cons": []
    }

def extract_features_from_input(use_case, capabilities):
    features = set()
    for cap, sel in capabilities.items():
        if sel:
            features.add(cap.lower())
    key_phrases = [
        "ai/ml", "ai", "ml", "machine learning", "analytics", "bi", "dashboard", "etl", "pipeline", 
        "data warehouse", "integration", "storage", "serverless", "devops", "web app", "container", 
        "monitoring", "hybrid", "database", "cosmos", "kubernetes", "app service", "functions", "logic app",
        "iot", "event", "event grid", "event hub", "stream", "batch", "data ingestion", "messaging", "workflow", 
        "anomaly", "real-time"
    ]
    use_case_lower = use_case.lower()
    for phrase in key_phrases:
        if phrase in use_case_lower:
            features.add(phrase)
    for word in use_case_lower.split():
        features.add(word.strip(".,"))
    return features

def product_score(service, features, compliance):
    score = 0
    name = service["name"].lower()
    category = service.get("category", "").lower()
    for feature in features:
        if feature in name or feature in category:
            score += 2
        if any(feature in kw for kw in [name, category]):
            score += 1
    if compliance and compliance.lower() in name:
        score += 2
    return score

def recommend_architecture(inputs, services, min_score=3, top_n=8):
    use_case = f"{inputs['use_case']} {inputs['non_func']} {inputs['compliance']}".lower()
    compliance = inputs['compliance']
    capabilities = inputs["capabilities"]

    features = extract_features_from_input(use_case, capabilities)
    scored_services = []
    for svc in services:
        score = product_score(svc, features, compliance)
        if score > 0:
            svc_copy = svc.copy()
            svc_copy["score"] = score
            scored_services.append(svc_copy)
    filtered_services = [svc for svc in scored_services if svc["score"] >= min_score]
    filtered_services.sort(key=lambda x: (-x["score"], x["name"]))
    filtered_services = filtered_services[:top_n]
    seen = set()
    filtered_services = [svc for svc in filtered_services if not (svc["name"] in seen or seen.add(svc["name"]))]
    categories = {}
    for svc in filtered_services:
        categories.setdefault(svc["category"], []).append(svc)
    summary_rows = []
    for svc in filtered_services:
        name = svc["name"]
        cat = svc.get("category", "")
        alt_names = [s["name"] for s in categories.get(cat, []) if s["name"] != name][:3]
        alt_links = []
        for alt in alt_names:
            alt_svc = next((s for s in filtered_services if s["name"] == alt), None)
            if alt_svc:
                alt_links.append(f"[{alt}]({alt_svc['docs']})")
        alt_str = ", ".join(alt_links) if alt_links else "None"
        overview = get_service_overview(name, cat)
        summary_rows.append({
            "Score": svc["score"],
            "Service": name,
            "Docs": svc.get("docs", ""),
            "Category": cat,
            "Overview": overview["overview"],
            "Pros": overview["pros"],
            "Cons": overview["cons"],
            "Alternatives": alt_str,
            "Pricing": svc.get("pricing", "")
        })
    return summary_rows

def generate_solution_overview(use_case, summary_rows):
    # Group by category for clearer narrative
    categories = {}
    for row in summary_rows:
        categories.setdefault(row["Category"], []).append(row["Service"])
    flows = []
    if any("IoT" in c for c in categories):
        flows.append("Device data is ingested via IoT services (such as Azure IoT Hub or IoT Central).")
    if "Integration" in categories:
        flows.append("Data/events are integrated and routed using Integration services (e.g., Event Grid, Logic Apps, API Management).")
    if "Compute" in categories or "Containers" in categories:
        flows.append("Processing is handled by Compute (Functions, VMs) or Container services (AKS, Container Apps, Container Instances).")
    if "Databases" in categories or "Storage" in categories:
        flows.append("Data is stored in managed Databases or Storage services (SQL, Cosmos DB, Data Lake, Blob Storage).")
    if "Analytics" in categories or "AI + ML" in categories:
        flows.append("Analytics and AI/ML services provide insights, dashboards, or predictions (e.g., Synapse, Power BI, Cognitive Services).")
    if "Security" in categories:
        flows.append("Security and compliance are enforced using services like Azure Key Vault, Sentinel, or Firewall.")
    if not flows:
        flows = ["The recommended Azure services address your specified requirements."]
    all_services = ', '.join([row["Service"] for row in summary_rows])
    return (
        f"**Architecture Overview:**\n"
        f"For your use case: *{use_case}*, the architecture brings together these Azure services: {all_services}.<br>\n"
        f"{' '.join(flows)}"
    )

def generate_mermaid_diagram(summary_rows):
    # Group services by category, then connect likely flows
    category_to_services = {}
    for row in summary_rows:
        category_to_services.setdefault(row["Category"], []).append(row["Service"])
    nodes = []
    links = []
    node_ids = {}
    idx = 0
    for cat in category_to_services:
        for svc in category_to_services[cat]:
            node_id = f"N{idx}"
            node_ids[svc] = node_id
            nodes.append(f'{node_id}["{svc}"]')
            idx += 1
    category_order = [
        "IoT", "Integration", "Web", "Compute", "Containers", "Databases", "Storage", "Analytics", "AI + ML", "Security", "Monitoring"
    ]
    prev_services = []
    for cat in category_order:
        if cat in category_to_services:
            curr_services = category_to_services[cat]
            for prev in prev_services:
                for curr in curr_services:
                    links.append(f'{node_ids[prev]} --> {node_ids[curr]}')
            prev_services = curr_services
    if not links:
        arch_diagram = "flowchart LR\n    " + "\n    ".join(nodes)
    else:
        arch_diagram = "flowchart LR\n    " + "\n    ".join(nodes + links)
    return arch_diagram

def mermaid_to_svg(mermaid_code: str):
    url = "https://kroki.io/mermaid/svg"
    resp = requests.post(url, data=mermaid_code.encode("utf-8"))
    resp.raise_for_status()
    return resp.text

def render_condensed_table(summary_rows):
    table_rows = []
    for row in summary_rows:
        table_rows.append({
            "Score": row["Score"],
            "Service": f"[{row['Service']}]({row['Docs']})",
            "Category": row["Category"],
            "Overview": row["Overview"][:60] + "..." if len(row["Overview"]) > 60 else row["Overview"],
            "Pros": ", ".join(row["Pros"]) if row["Pros"] else "-",
            "Cons": ", ".join(row["Cons"]) if row["Cons"] else "-",
            "Alternatives": row["Alternatives"],
            "Docs": f"[Docs]({row['Docs']})" if row["Docs"] else "-",
            "Pricing": f"[Pricing]({row["Pricing"]})" if row["Pricing"] else "-"
        })
    df = pd.DataFrame(table_rows)
    st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

st.title("Azure Solution Recommender :cloud:")

st.sidebar.header("Recommendation Controls")
min_score = st.sidebar.slider("Minimum Score Threshold", 1, 10, 3, 1)
top_n = st.sidebar.slider("Number of Top Recommendations (N)", 3, 20, 8, 1)

with st.form("requirements_form"):
    use_case = st.text_area("Briefly describe your use case or business goal", height=80)
    tech_stack = st.text_input("Current technology stack (e.g., React, Node.js, PostgreSQL)")
    non_func = st.text_input("Non-functional requirements (e.g., high availability, compliance)")
    languages = st.text_input("Preferred programming languages/frameworks (comma-separated)")
    compliance = st.text_input("Security/compliance needs (e.g., HIPAA, GDPR, SOC 2)")
    st.markdown("**Which capabilities do you need?**")
    col1, col2, col3, col4, col5 = st.columns(5)
    ai_ml = col1.checkbox("AI/ML")
    analytics = col2.checkbox("Data Analytics")
    devops = col3.checkbox("DevOps")
    serverless = col4.checkbox("Serverless")
    hybrid = col5.checkbox("Hybrid Cloud")
    migrate_data = st.checkbox("Do you want to migrate existing data?", key="migrate_data")
    migration_size = 0
    migration_method = ""
    if migrate_data:
        migration_size = st.number_input("How much data do you want to migrate? (in TB)", min_value=0.0, step=0.1)
        migration_method = st.selectbox(
            "How will you migrate the data?",
            ["Online (AzCopy, Storage Explorer, etc.)", "Offline (Azure Data Box)", "Other"]
        )
    submitted = st.form_submit_button("Recommend Azure Solution")

if submitted:
    st.info("Fetching Azure product catalog and generating your recommendation...")
    azure_services = fetch_azure_services()
    user_input = {
        "use_case": use_case,
        "tech_stack": tech_stack,
        "non_func": non_func,
        "languages": [x.strip() for x in languages.split(",") if x.strip()],
        "compliance": compliance,
        "capabilities": {
            "ai/ml": ai_ml,
            "data analytics": analytics,
            "devops": devops,
            "serverless": serverless,
            "hybrid cloud": hybrid
        }
    }
    summary_rows = recommend_architecture(user_input, azure_services, min_score=min_score, top_n=top_n)

    if summary_rows:
        st.markdown("### Solution Architecture Overview")
        st.markdown(generate_solution_overview(use_case, summary_rows), unsafe_allow_html=True)

        st.markdown("### Recommended Components")
        render_condensed_table(summary_rows)
    else:
        st.warning("No relevant Azure products matched your requirements. Please try adjusting your input, score threshold, or Top N.")

    if migrate_data and migration_size > 0:
        # Ballpark Data Box cost (as of 2024: $250 per 8TB device + shipping)
        data_box_tb_cost = 250 / 8  # $31.25 per TB
        migration_cost = migration_size * data_box_tb_cost if migration_method == "Offline (Azure Data Box)" else 0
        # Ballpark storage cost (Standard LRS hot, $0.0184/GB/month as of 2024)
        storage_gb_cost = 0.0184
        monthly_storage_cost = migration_size * 1024 * storage_gb_cost  # TB to GB
        st.markdown(f"#### Data Migration and Storage Estimate")
        st.markdown(f"**Migration method:** {migration_method}")
        if migration_method == "Offline (Azure Data Box)":
            st.markdown(f"**Estimated migration cost:** ${migration_cost:,.2f} (using Azure Data Box, not including shipping)")
        else:
            st.markdown(f"**Estimated migration cost:** $0 (online ingress to Azure is typically free)")
        st.markdown(f"**Estimated monthly storage cost:** ${monthly_storage_cost:,.2f} (Standard Hot Blob Storage, LRS)")
        st.markdown("> _Note: Actual costs may vary depending on redundancy, access tier, region, and transfer method. Use the [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) for a precise estimate._")

    # Mermaid diagram
    if summary_rows:
        arch_diagram = generate_mermaid_diagram(summary_rows)
        st.markdown("### Architecture Diagram (Mermaid format)")
        st.code(arch_diagram.strip(), language="mermaid")
        try:
            svg = mermaid_to_svg(arch_diagram)
            st.markdown("### Rendered Architecture Diagram")
            st.markdown(svg, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Failed to render diagram: {e}")

    st.markdown("**To get a detailed architecture diagram, try [diagrams.net](https://app.diagrams.net/) or export to Markdown below.**")

    if st.button("Export Recommendation as Markdown"):
        md = f"# Azure Solution Recommendation\n\n"
        md += f"**Use case:** {use_case}\n\n"
        md += f"**Technology stack:** {tech_stack}\n\n"
        md += f"**Non-functional requirements:** {non_func}\n\n"
        md += f"**Preferred languages/frameworks:** {languages}\n\n"
        md += f"**Security/compliance:** {compliance}\n\n"
        md += f"**Capabilities:** {', '.join([k for k,v in user_input['capabilities'].items() if v])}\n\n"
        if migrate_data and migration_size > 0:
            md += "## Data Migration and Storage Estimate\n"
            md += f"- **Migration method:** {migration_method}\n"
            if migration_method == "Offline (Azure Data Box)":
                md += f"- **Estimated migration cost:** ${migration_cost:,.2f} (using Azure Data Box, not including shipping)\n"
            else:
                md += f"- **Estimated migration cost:** $0 (online ingress to Azure is typically free)\n"
            md += f"- **Estimated monthly storage cost:** ${monthly_storage_cost:,.2f} (Standard Hot Blob Storage, LRS)\n"
            md += "> _Note: Actual costs may vary depending on redundancy, access tier, region, and transfer method. Use the [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) for a precise estimate._\n\n"
        if summary_rows:
            md += "## Solution Architecture Overview\n"
            md += generate_solution_overview(use_case, summary_rows)
            md += "\n\n## Recommended Components\n"
            md += "| Score | Service | Category | Overview | Pros | Cons | Alternatives | Docs | Pricing |\n"
            md += "|---|---|---|---|---|---|---|---|---|\n"
            for row in summary_rows:
                md += f"| {row['Score']} | [{row['Service']}]({row['Docs']}) | {row['Category']} | {row['Overview']} | {'; '.join(row['Pros']) if row['Pros'] else '-'} | {'; '.join(row['Cons']) if row['Cons'] else '-'} | {row['Alternatives']} | [Docs]({row['Docs']}) | [Pricing]({row['Pricing']}) |\n"
        if summary_rows:
            arch_diagram = generate_mermaid_diagram(summary_rows)
            md += "\n## Architecture Diagram (Mermaid)\n```mermaid\n" + arch_diagram.strip() + "\n```\n"
        st.download_button("Download Markdown", data=md, file_name="azure_solution.md", mime="text/markdown")
