import streamlit as st

st.set_page_config(page_title="Azure Solution Recommender", layout="wide")

@st.cache_data(ttl=3600)
def fetch_azure_services():
    return [
        {"name": "Azure Event Grid", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/event-grid/"},
        {"name": "Azure Event Hubs", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/event-hubs/"},
        {"name": "Azure IoT Hub", "category": "IoT", "docs": "https://learn.microsoft.com/en-us/azure/iot-hub/"},
        {"name": "Azure Logic Apps", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/logic-apps/"},
        {"name": "Azure Functions", "category": "Compute", "docs": "https://learn.microsoft.com/en-us/azure/azure-functions/"},
        {"name": "Azure Machine Learning", "category": "AI + ML", "docs": "https://learn.microsoft.com/en-us/azure/machine-learning/"},
        {"name": "Azure Databricks", "category": "AI + ML", "docs": "https://learn.microsoft.com/en-us/azure/databricks/"},
        {"name": "Azure Synapse Analytics", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/azure/synapse-analytics/"},
        {"name": "Azure Data Lake Storage", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/storage/data-lake-storage/"},
        {"name": "Azure Blob Storage", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/storage/blobs/"},
        {"name": "Azure SQL Database", "category": "Database", "docs": "https://learn.microsoft.com/en-us/azure/azure-sql/database/"},
        {"name": "Azure Cosmos DB", "category": "Database", "docs": "https://learn.microsoft.com/en-us/azure/cosmos-db/"},
        {"name": "Azure App Service", "category": "Web", "docs": "https://learn.microsoft.com/en-us/azure/app-service/"},
        {"name": "Azure Kubernetes Service", "category": "Container", "docs": "https://learn.microsoft.com/en-us/azure/aks/"},
        {"name": "Microsoft Fabric", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/fabric/"},
        {"name": "Power BI", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/power-bi/"},
        {"name": "Azure Monitor", "category": "Monitoring", "docs": "https://learn.microsoft.com/en-us/azure/azure-monitor/"},
        {"name": "Azure DevOps", "category": "DevOps", "docs": "https://learn.microsoft.com/en-us/azure/devops/"},
    ]

def get_service_docs_and_pricing():
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
        },
        "Azure Event Grid": {
            "docs": "https://learn.microsoft.com/en-us/azure/event-grid/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/event-grid/"
        },
        "Azure Event Hubs": {
            "docs": "https://learn.microsoft.com/en-us/azure/event-hubs/",
            "pricing": "https://azure.microsoft.com/en-us/pricing/details/event-hubs/"
        }
    }

FEATURE_KEYWORDS = {
    "ai/ml": ["machine learning", "databricks", "cognitive services", "ai", "bot"],
    "data analytics": ["analytics", "bi", "synapse", "fabric", "power bi", "databricks"],
    "devops": ["devops", "pipelines", "repos", "artifacts", "test plans"],
    "serverless": ["functions", "logic apps", "event grid", "event hub"],
    "hybrid cloud": ["arc", "stack", "expressroute"],
    "storage": ["storage", "blob", "data lake", "cosmos db", "sql database"],
    "web app": ["app service", "web app"],
    "container": ["kubernetes", "container", "aks"],
    "monitoring": ["monitor", "log analytics", "insights"],
    "integration": ["data factory", "logic apps", "event grid", "service bus"],
    "iot": ["iot", "event hub", "event grid", "stream", "edge"]
}

COMPLIANCE_KEYWORDS = {
    "gdpr": ["sql", "data factory", "fabric", "power bi", "synapse", "storage", "machine learning"],
    "hipaa": ["sql", "data factory", "fabric", "power bi", "synapse", "storage", "machine learning"],
    "soc 2": ["sql", "data factory", "fabric", "power bi", "synapse", "storage", "machine learning"],
}

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
    },
    "Azure Event Grid": {
        "pros": "Serverless event routing, seamless integration, supports millions of events per second.",
        "cons": "Complex event-driven architectures can be hard to debug.",
        "compliance": "Built-in security, compliance certifications.",
    },
    "Azure Event Hubs": {
        "pros": "Big data streaming, real-time ingestion, integrates with analytics services.",
        "cons": "Requires partition management for high throughput.",
        "compliance": "Enterprise security and compliance.",
    }
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

def product_matches(service, features, compliance):
    name = service["name"].lower()
    category = service.get("category", "").lower()
    for feature in features:
        for kw_list in FEATURE_KEYWORDS.values():
            for kw in kw_list:
                if kw in name or kw in category or kw == feature:
                    return True
        if feature in name or feature in category:
            return True
    if compliance:
        for c_key, svcs in COMPLIANCE_KEYWORDS.items():
            if c_key in compliance.lower():
                for kw in svcs:
                    if kw in name:
                        return True
    return False

def recommend_architecture(inputs, services):
    service_info = get_service_docs_and_pricing()
    use_case = f"{inputs['use_case']} {inputs['non_func']} {inputs['compliance']}".lower()
    compliance = inputs['compliance']
    capabilities = inputs["capabilities"]

    features = extract_features_from_input(use_case, capabilities)

    relevant_services = []
    for svc in services:
        if product_matches(svc, features, compliance):
            relevant_services.append(svc)

    seen = set()
    filtered_services = []
    for svc in relevant_services:
        if svc["name"] not in seen:
            filtered_services.append(svc)
            seen.add(svc["name"])

    filtered_services = sorted(filtered_services, key=lambda x: (x.get("category",""), x["name"]))

    summary_rows = []
    details = []
    doc_links = []
    for svc in filtered_services:
        name = svc["name"]
        info = service_info.get(name, {})
        alt_names = [s["name"] for s in filtered_services if s["category"] == svc["category"] and s["name"] != name]
        alt_links = []
        for alt in alt_names[:3]:
            alt_info = service_info.get(alt, {})
            if alt_info.get("docs"):
                alt_links.append(f"[{alt}]({alt_info['docs']})")
        alt_str = ", ".join(alt_links) if alt_links else "None"
        summary_rows.append({
            "Component": name,
            "Category": svc.get("category", ""),
            "Alternatives": alt_str,
            "Docs": f"[Link]({info.get('docs', svc.get('docs',''))})" if info.get("docs") or svc.get("docs") else "",
            "Pricing": f"[Link]({info.get('pricing','')})" if info.get("pricing") else ""
        })
        rich = RICH_DETAILS.get(name, {})
        details.append(
            f"- **{name}**\n"
            f"  *Category*: {svc.get('category')}\n"
            f"  *Pros*: {rich.get('pros','N/A')}\n"
            f"  *Cons*: {rich.get('cons','N/A')}\n"
            f"  *Compliance*: {rich.get('compliance','N/A')}\n"
            f"  [Docs]({info.get('docs', svc.get('docs',''))}) [Pricing]({info.get('pricing','')})"
        )
        doc_links.append(f"- [{name}]({info.get('docs', svc.get('docs',''))})")

    arch_diagram = ""
    if filtered_services:
        diagram_lines = []
        idx = 1
        last = None
        categories = list(dict.fromkeys([svc.get("category","Other") for svc in filtered_services]))
        first_by_cat = {cat: next((s for s in filtered_services if s.get("category")==cat), None) for cat in categories}
        if "Integration" in categories:
            diagram_lines.append(f"A[Data Sources] --> B[{first_by_cat['Integration']['name']}]")
            last = "B"
            idx = 3
        for cat in categories:
            if cat == "Integration":
                continue
            svc = first_by_cat[cat]
            if svc:
                key = chr(64+idx)
                diagram_lines.append(f"{last or 'A'} --> {key}[{svc['name']}]")
                last = key
                idx += 1
        arch_diagram = "flowchart LR\n    " + "\n    ".join(diagram_lines)

    solution = [f"{row['Component']} ({row['Category']})" for row in summary_rows]

    return solution, details, doc_links, arch_diagram, summary_rows

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
    solution, details, doc_links, arch_diagram, summary_rows = recommend_architecture(user_input, azure_services)
    st.header("Recommended Azure Solution")

    if summary_rows:
        st.markdown("### Recommended Components Summary")
        st.table(summary_rows)
    else:
        st.warning("No relevant Azure products matched your requirements. Please try adjusting your input.")

    if doc_links:
        st.markdown("### Core Components (Docs)")
        st.markdown("\n".join(doc_links))

    if details:
        st.markdown("### Solution Overview")
        for d in details:
            st.markdown(d)

    if arch_diagram.strip():
        st.markdown("### Architecture Diagram (Mermaid format)")
        st.code(arch_diagram.strip(), language="mermaid")
    st.markdown("**To get a detailed architecture diagram, try [diagrams.net](https://app.diagrams.net/) or export to Markdown below.**")

    if st.button("Export Recommendation as Markdown"):
        md = f"# Azure Solution Recommendation\n\n"
        md += f"**Use case:** {use_case}\n\n"
        md += f"**Technology stack:** {tech_stack}\n\n"
        md += f"**Non-functional requirements:** {non_func}\n\n"
        md += f"**Preferred languages/frameworks:** {languages}\n\n"
        md += f"**Security/compliance:** {compliance}\n\n"
        md += f"**Capabilities:** {', '.join([k for k,v in user_input['capabilities'].items() if v])}\n\n"
        if summary_rows:
            md += "## Recommended Components Summary\n\n"
            md += "| Component | Category | Alternatives | Docs | Pricing |\n"
            md += "|---|---|---|---|---|\n"
            for row in summary_rows:
                md += f"| {row['Component']} | {row['Category']} | {row['Alternatives']} | {row['Docs']} | {row['Pricing']} |\n"
        if details:
            md += "\n## Solution Overview\n" + "\n".join(details) + "\n\n"
        if arch_diagram.strip():
            md += "## Architecture Diagram (Mermaid)\n```mermaid\n" + arch_diagram.strip() + "\n```\n"
        st.download_button("Download Markdown", data=md, file_name="azure_solution.md", mime="text/markdown")
