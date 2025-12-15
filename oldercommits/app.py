import streamlit as st
import requests
from bs4 import BeautifulSoup

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
    # Official docs and pricing links for core services. Expand as needed.
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
        }
    }

def recommend_architecture(inputs, services):
    # Simple scoring and alternatives logic for demonstration
    service_info = get_service_docs_and_pricing()
    use_case = f"{inputs['use_case']} {inputs['non_func']} {inputs['compliance']}".lower()
    capabilities = inputs["capabilities"]

    solution = []
    details = []
    arch_diagram = ""
    summary_rows = []

    # Define architecture for analytics/data use case
    if (capabilities.get('data analytics') or 
        any(kw in use_case for kw in ['analytics', 'bi', 'report', 'dashboard', 'fabric', 'power bi', 'data warehouse'])):
        core_components = [
            "Azure Data Factory",
            "Azure Data Lake Storage",
            "Microsoft Fabric",
            "Power BI"
        ]
        # Scoring logic (could be made more advanced)
        scores = {
            "Azure Data Factory": 5,
            "Azure Data Lake Storage": 5,
            "Microsoft Fabric": 4,
            "Power BI": 5
        }
        # Alternatives
        alternatives = {
            "Azure Data Factory": [("Azure Synapse Analytics", service_info["Azure Synapse Analytics"]["docs"])],
            "Azure Data Lake Storage": [
                ("Azure Blob Storage", service_info["Azure Blob Storage"]["docs"]),
                ("Azure SQL Database", service_info["Azure SQL Database"]["docs"])
            ],
            "Microsoft Fabric": [
                ("Azure Synapse Analytics", service_info["Azure Synapse Analytics"]["docs"]),
                ("Azure Databricks", service_info["Azure Databricks"]["docs"])
            ],
            "Power BI": []
        }
        # Details for each service
        rich_details = {
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
            }
        }
        # Architecture diagram
        arch_diagram = """
flowchart LR
    A[Data Sources] --> B[Data Factory]
    B --> C[Data Lake Storage]
    C --> D[Microsoft Fabric]
    D --> E[Power BI]
"""
        # Build summary table rows
        for comp in core_components:
            info = service_info.get(comp, {})
            alt = ", ".join([f"[{n}]({u})" for n, u in alternatives.get(comp, [])]) if alternatives.get(comp, []) else "None"
            summary_rows.append({
                "Component": comp,
                "Score (1-5)": scores[comp],
                "Alternatives": alt,
                "Docs": f"[Link]({info.get('docs', '')})" if info.get('docs') else "",
                "Pricing": f"[Link]({info.get('pricing', '')})" if info.get('pricing') else ""
            })
            # Build details text
            details.append(
                f"- **{comp}**: {rich_details[comp]['pros']} "
                f"*Pros*: {rich_details[comp]['pros']} "
                f"*Cons*: {rich_details[comp]['cons']} "
                f"*Compliance*: {rich_details[comp]['compliance']} "
                f"[Docs]({info.get('docs', '')}) [Pricing]({info.get('pricing', '')})"
            )

        # Solution list for Markdown export
        solution = [f"{row['Component']} (Score: {row['Score (1-5)']})" for row in summary_rows]

    # Add more architectures for other use cases (AI/ML, DevOps, etc.) as needed

    # Build doc links for Markdown export
    doc_links = [f"- [{row['Component']}]({service_info[row['Component']]['docs']})" for row in summary_rows]

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
