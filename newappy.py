import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

st.set_page_config(page_title="Azure Solution Recommender", layout="wide")

@st.cache_data(ttl=3600)
def fetch_azure_services():
    url = "https://azure.microsoft.com/en-us/products/"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    services = []
    for section in soup.select("section[data-test-id='products-list-section']"):
        category = section.select_one("h2")
        category_name = category.text.strip() if category else "Other"
        for prod in section.select("li"):
            name = prod.select_one("span.product-name")
            link = prod.select_one("a")
            if name and link:
                services.append({
                    "name": name.text.strip(),
                    "category": category_name,
                    "docs": "https://azure.microsoft.com" + link["href"]
                })
    # Add Fabric and Power BI explicitly if not present
    if not any('fabric' in s['name'].lower() for s in services):
        services.append({
            "name": "Microsoft Fabric",
            "category": "Analytics",
            "docs": "https://learn.microsoft.com/en-us/fabric/"
        })
    if not any('power bi' in s['name'].lower() for s in services):
        services.append({
            "name": "Power BI",
            "category": "Analytics",
            "docs": "https://powerbi.microsoft.com/"
        })
    return services

def get_service_docs_and_pricing():
    # Expanded docs and pricing for broader Azure services
    return {
        "Azure Data Factory": {
            "docs": "https://learn.microsoft.com/en-us/azure/data-factory/introduction",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/data-factory/"
        },
        "Azure Data Lake Storage": {
            "docs": "https://learn.microsoft.com/en-us/azure/storage/data-lake-storage/introduction",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/data-lake/"
        },
        "Microsoft Fabric": {
            "docs": "https://learn.microsoft.com/en-us/fabric/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/microsoft-fabric/"
        },
        "Power BI": {
            "docs": "https://learn.microsoft.com/en-us/power-bi/fundamentals/power-bi-overview",
            "pricing": "https://powerbi.microsoft.com/en-us/pricing/"
        },
        "Azure Synapse Analytics": {
            "docs": "https://learn.microsoft.com/en-us/azure/synapse-analytics/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/synapse-analytics/"
        },
        "Azure Databricks": {
            "docs": "https://learn.microsoft.com/en-us/azure/databricks/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/databricks/"
        },
        "Azure SQL Database": {
            "docs": "https://learn.microsoft.com/en-us/azure/azure-sql/database/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-sql-database/"
        },
        "Azure Blob Storage": {
            "docs": "https://learn.microsoft.com/en-us/azure/storage/blobs/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/blobs/"
        },
        "Azure Machine Learning": {
            "docs": "https://learn.microsoft.com/en-us/azure/machine-learning/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/machine-learning/"
        },
        "Azure Kubernetes Service": {
            "docs": "https://learn.microsoft.com/en-us/azure/aks/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/"
        },
        "Azure App Service": {
            "docs": "https://learn.microsoft.com/en-us/azure/app-service/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/app-service/"
        },
        "Azure Functions": {
            "docs": "https://learn.microsoft.com/en-us/azure/azure-functions/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/functions/"
        },
        "Azure Cosmos DB": {
            "docs": "https://learn.microsoft.com/en-us/azure/cosmos-db/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/cosmos-db/"
        },
        "Azure Monitor": {
            "docs": "https://learn.microsoft.com/en-us/azure/azure-monitor/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/monitor/"
        },
        "Azure DevOps": {
            "docs": "https://learn.microsoft.com/en-us/azure/devops/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/devops-services/"
        },
        "Azure Logic Apps": {
            "docs": "https://learn.microsoft.com/en-us/azure/logic-apps/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/logic-apps/"
        }
    }

# Mapping features/capabilities to Azure products
FEATURES_TO_PRODUCTS = {
    "data analytics": [
        "Azure Synapse Analytics", "Microsoft Fabric", "Power BI", "Azure Data Factory", "Azure Databricks", "Azure Data Lake Storage"
    ],
    "ai/ml": [
        "Azure Machine Learning", "Azure Databricks", "Azure Synapse Analytics", "Azure Data Lake Storage"
    ],
    "data integration": [
        "Azure Data Factory", "Azure Logic Apps"
    ],
    "data warehousing": [
        "Azure Synapse Analytics", "Azure SQL Database", "Microsoft Fabric"
    ],
    "bi": [
        "Power BI", "Microsoft Fabric"
    ],
    "dashboard": [
        "Power BI", "Microsoft Fabric"
    ],
    "storage": [
        "Azure Blob Storage", "Azure Data Lake Storage", "Azure SQL Database", "Azure Cosmos DB"
    ],
    "serverless": [
        "Azure Functions", "Azure Logic Apps"
    ],
    "devops": [
        "Azure DevOps", "GitHub Actions"
    ],
    "web app": [
        "Azure App Service", "Azure Functions", "Azure Kubernetes Service"
    ],
    "container": [
        "Azure Kubernetes Service", "Azure Container Instances"
    ],
    "monitoring": [
        "Azure Monitor", "Log Analytics"
    ],
    "hybrid cloud": [
        "Azure Arc", "Azure Stack"
    ]
}

# Mapping compliance keywords to Azure compliance info
COMPLIANCE_SUPPORT = {
    "gdpr": ["Azure Synapse Analytics", "Azure Data Factory", "Azure SQL Database", "Azure Data Lake Storage", "Microsoft Fabric", "Power BI", "Azure Machine Learning"],
    "hipaa": ["Azure Synapse Analytics", "Azure Data Factory", "Azure SQL Database", "Azure Data Lake Storage", "Microsoft Fabric", "Power BI", "Azure Machine Learning"],
    "soc 2": ["Azure Synapse Analytics", "Azure SQL Database", "Azure Data Factory", "Azure Data Lake Storage", "Microsoft Fabric", "Power BI", "Azure Machine Learning"],
}

# Pros/Cons/Compliance for core services (expand as needed)
RICH_DETAILS = {
    "Azure Data Factory": {
        "pros": "Highly scalable ETL, integrates with 90+ data sources, low-code UX.",
        "cons": "Complex orchestrations can be challenging to debug.",
        "compliance": "Supports Azure compliance standards (GDPR, HIPAA, etc.)",
    },
    "Azure Data Lake Storage": {
        "pros": "Massive scalability, hierarchical namespace, integrates with analytics engines.",
        "cons": "Performance tuning needed for many small files.",
        "compliance": "Supports data encryption, access control, GDPR, HIPAA.",
    },
    "Microsoft Fabric": {
        "pros": "Unified SaaS analytics, integrates data engineering, warehousing, AI, and BI.",
        "cons": "Newer product, features evolving.",
        "compliance": "Enterprise-grade security, compliance certifications.",
    },
    "Power BI": {
        "pros": "Top-class interactive dashboards, self-service BI, direct data source integration.",
        "cons": "Premium features require additional licensing.",
        "compliance": "Meets security/compliance standards, supports row-level security.",
    },
    "Azure Synapse Analytics": {
        "pros": "Integrated analytics service, supports big data & data warehousing, serverless options.",
        "cons": "Learning curve, cost management needed.",
        "compliance": "Built-in security, data protection and compliance standards.",
    },
    "Azure Databricks": {
        "pros": "Collaborative Apache Spark-based analytics, ML workflows, scalable compute.",
        "cons": "Requires Spark expertise, integration overhead.",
        "compliance": "Compliant with Azure security & compliance standards.",
    },
    "Azure SQL Database": {
        "pros": "Managed relational DB, high availability, scaling, T-SQL support.",
        "cons": "May require migration for non-Microsoft SQL workloads.",
        "compliance": "Meets enterprise security and compliance standards.",
    },
    "Azure Blob Storage": {
        "pros": "Low-cost, massively scalable, supports unstructured data.",
        "cons": "Not suitable for fast transactional workloads.",
        "compliance": "Encryption at rest, compliance certifications.",
    },
    "Azure Machine Learning": {
        "pros": "End-to-end ML, MLOps, AutoML, scalable training.",
        "cons": "Service complexity, usage costs.",
        "compliance": "Supports responsible AI, compliance, and security.",
    },
    "Azure Kubernetes Service": {
        "pros": "Managed Kubernetes, scaling, integration with Azure services.",
        "cons": "Requires container/Kubernetes expertise.",
        "compliance": "Built-in security and compliance.",
    },
    "Azure App Service": {
        "pros": "PaaS for web apps, auto-scaling, DevOps integration.",
        "cons": "Not ideal for highly customized OS requirements.",
        "compliance": "Supports ISO, SOC, PCI, and more.",
    },
    "Azure Functions": {
        "pros": "Event-driven serverless compute, pay-per-execution, easy scaling.",
        "cons": "Cold start, limited execution time.",
        "compliance": "Supports most Azure compliance certifications.",
    },
    "Azure Cosmos DB": {
        "pros": "Globally distributed, multi-model database, low-latency.",
        "cons": "Pricing can be complex.",
        "compliance": "Meets major compliance requirements.",
    },
    "Azure Monitor": {
        "pros": "Unified monitoring, metrics, and logs, integration with Azure services.",
        "cons": "Can generate large data volumes.",
        "compliance": "Supports Azure compliance certifications.",
    },
    "Azure DevOps": {
        "pros": "Comprehensive CI/CD, project tracking, integrations.",
        "cons": "Overlapping features with GitHub, learning curve.",
        "compliance": "Compliant with industry standards.",
    },
    "Azure Logic Apps": {
        "pros": "Automated workflows, connectors for 200+ services.",
        "cons": "Performance limits for high-throughput scenarios.",
        "compliance": "Supports Azure compliance certifications.",
    }
}

def extract_features_from_input(use_case, capabilities):
    # Gather features/capabilities from user input and checkbox selections
    features = set()
    for cap, sel in capabilities.items():
        if sel:
            features.add(cap.lower())
    # Extract keywords from use case (simple matching)
    key_phrases = [
        "ai/ml", "analytics", "bi", "dashboard", "etl", "pipeline", "data warehouse",
        "integration", "storage", "serverless", "devops", "web app", "container", "monitoring", "hybrid"
    ]
    for phrase in key_phrases:
        if phrase in use_case:
            features.add(phrase)
    return features

def score_service(service, features, compliance_needed):
    # Score based on feature and compliance match
    name = service["name"]
    score = 0
    # Feature match
    for feature in features:
        for k, v in FEATURES_TO_PRODUCTS.items():
            if feature in k and name in v:
                score += 4
    # Compliance match
    if compliance_needed:
        for c_key, svcs in COMPLIANCE_SUPPORT.items():
            if c_key in compliance_needed.lower() and name in svcs:
                score += 2
    # Popularity/Category bonus
    if service.get("category", "").lower() in ["analytics", "ai + machine learning", "compute"]:
        score += 1
    return score

def find_alternatives(selected_name, feature_set):
    # Find services with similar features that are not selected_name
    alternatives = set()
    for feature, prods in FEATURES_TO_PRODUCTS.items():
        if feature in feature_set:
            for prod in prods:
                if prod != selected_name:
                    alternatives.add(prod)
    return list(alternatives)[:3]  # Limit to 3

def find_architecture_layers(selected_services):
    # Group selected services by rough architecture layer
    compute, storage, integration, analytics, monitoring = [], [], [], [], []
    for s in selected_services:
        name = s["name"]
        cat = s.get("category", "").lower()
        if "analytics" in cat or "bi" in name.lower():
            analytics.append(name)
        elif "storage" in cat or "db" in name.lower():
            storage.append(name)
        elif "compute" in cat or "kubernetes" in name.lower() or "app service" in name.lower():
            compute.append(name)
        elif "integration" in cat or "factory" in name.lower() or "logic app" in name.lower():
            integration.append(name)
        elif "monitor" in cat or "monitor" in name.lower():
            monitoring.append(name)
    return compute, storage, integration, analytics, monitoring

def recommend_architecture(inputs, services):
    service_info = get_service_docs_and_pricing()
    use_case = f"{inputs['use_case']} {inputs['non_func']} {inputs['compliance']}".lower()
    compliance = inputs['compliance']
    capabilities = inputs["capabilities"]

    features = extract_features_from_input(use_case, capabilities)

    # Score all services dynamically
    scored_services = []
    for svc in services:
        score = score_service(svc, features, compliance)
        if score > 0:
            scored_services.append((score, svc))
    scored_services.sort(reverse=True, key=lambda x: x[0])
    selected_services = [svc for score, svc in scored_services[:6]]  # Top 6

    summary_rows = []
    details = []
    doc_links = []
    for svc in selected_services:
        name = svc["name"]
        info = service_info.get(name, {})
        alt_names = find_alternatives(name, features)
        alt_links = []
        for alt in alt_names:
            alt_info = service_info.get(alt, {})
            if alt_info.get("docs"):
                alt_links.append(f"[{alt}]({alt_info['docs']})")
        alt_str = ", ".join(alt_links) if alt_links else "None"
        summary_rows.append({
            "Component": name,
            "Score (1-5)": min(5, max(1, score_service(svc, features, compliance)//2)),
            "Alternatives": alt_str,
            "Docs": f"[Link]({info.get('docs', svc.get('docs',''))})" if info.get("docs") or svc.get("docs") else "",
            "Pricing": f"[Link]({info.get('pricing','')})" if info.get("pricing") else ""
        })
        rich = RICH_DETAILS.get(name, {})
        details.append(
            f"- **{name}**: {rich.get('pros','')}\n"
            f"  *Pros*: {rich.get('pros','N/A')}\n"
            f"  *Cons*: {rich.get('cons','N/A')}\n"
            f"  *Compliance*: {rich.get('compliance','N/A')}\n"
            f"  [Docs]({info.get('docs', svc.get('docs',''))}) [Pricing]({info.get('pricing','')})"
        )
        doc_links.append(f"- [{name}]({info.get('docs', svc.get('docs',''))})")

    # Dynamic architecture diagram (mermaid) based on roles/layers
    compute, storage, integration, analytics, monitoring = find_architecture_layers(selected_services)
    diagram_lines = []
    idx = 1
    last = None
    node_map = {}
    # Start with Data Sources if analytics or integration are present
    if integration or analytics:
        diagram_lines.append(f"A[Data Sources] --> B[{integration[0] if integration else analytics[0]}]")
        node_map['A'] = "Data Sources"
        node_map['B'] = integration[0] if integration else analytics[0]
        idx = 3
        last = "B"
    for layer in [integration, storage, compute, analytics, monitoring]:
        for node in layer:
            key = chr(64+idx)
            diagram_lines.append(f"{last or 'A'} --> {key}[{node}]")
            last = key
            node_map[key] = node
            idx += 1
    arch_diagram = "flowchart LR\n    " + "\n    ".join(diagram_lines)

    solution = [f"{row['Component']} (Score: {row['Score (1-5)']})" for row in summary_rows]

    return solution, details, doc_links, arch_diagram, summary_rows

# ---- UI ----
st.title("Azure Solution Recommender :cloud:")

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
    submitted = st.form_submit_button("Recommend Azure Solution")

if submitted:
    st.info("Fetching latest Azure product catalog and generating your recommendation...")
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
    solution, details, doc_links, arch_diagram, summary_rows = recommend_architecture(user_input, azure_services)
    st.header("Recommended Azure Solution")

    # Show summary table
    st.markdown("### Core Components Summary")
    st.table(summary_rows)

    st.markdown("### Core Components (Docs)")
    st.markdown("\n".join(doc_links))

    st.markdown("### Solution Overview")
    for d in details:
        st.markdown(d)
    if arch_diagram.strip():
        st.markdown("### Architecture Diagram (Mermaid format)")
        st.code(arch_diagram.strip(), language="mermaid")
    st.markdown("**To get a detailed architecture diagram, try [diagrams.net](https://app.diagrams.net/) or export to Markdown below.**")

    # Markdown export option
    if st.button("Export Recommendation as Markdown"):
        md = f"# Azure Solution Recommendation\n\n"
        md += f"**Use case:** {use_case}\n\n"
        md += f"**Technology stack:** {tech_stack}\n\n"
        md += f"**Non-functional requirements:** {non_func}\n\n"
        md += f"**Preferred languages/frameworks:** {languages}\n\n"
        md += f"**Security/compliance:** {compliance}\n\n"
        md += f"**Capabilities:** {', '.join([k for k,v in user_input['capabilities'].items() if v])}\n\n"
        md += "## Core Components Summary\n\n"
        md += "| Component | Score (1-5) | Alternatives | Docs | Pricing |\n"
        md += "|---|---|---|---|---|\n"
        for row in summary_rows:
            md += f"| {row['Component']} | {row['Score (1-5)']} | {row['Alternatives']} | {row['Docs']} | {row['Pricing']} |\n"
        md += "\n## Solution Overview\n" + "\n".join(details) + "\n\n"
        if arch_diagram.strip():
            md += "## Architecture Diagram (Mermaid)\n```mermaid\n" + arch_diagram.strip() + "\n```\n"
        st.download_button("Download Markdown", data=md, file_name="azure_solution.md", mime="text/markdown")
