import streamlit as st
import requests

st.set_page_config(page_title="Azure Solution Recommender", layout="wide")

@st.cache_data(ttl=3600)
def fetch_azure_services():
    # FULL Azure product list as of mid-2024.
    return [
        {"name": "API Management", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/api-management/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/api-management/"},
        {"name": "App Configuration", "category": "Developer Tools", "docs": "https://learn.microsoft.com/en-us/azure/azure-app-configuration/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/app-configuration/"},
        {"name": "App Service", "category": "Web", "docs": "https://learn.microsoft.com/en-us/azure/app-service/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/app-service/"},
        {"name": "Application Gateway", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/application-gateway/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/application-gateway/"},
        {"name": "Automation", "category": "Management", "docs": "https://learn.microsoft.com/en-us/azure/automation/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/automation/"},
        {"name": "Azure Active Directory", "category": "Identity", "docs": "https://learn.microsoft.com/en-us/azure/active-directory/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/active-directory/"},
        {"name": "Azure Arc", "category": "Hybrid", "docs": "https://learn.microsoft.com/en-us/azure/azure-arc/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-arc/"},
        {"name": "Azure Bastion", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/bastion/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-bastion/"},
        {"name": "Azure Blob Storage", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/storage/blobs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/blobs/"},
        {"name": "Azure Cache for Redis", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cache/"},
        {"name": "Azure Cognitive Services", "category": "AI + ML", "docs": "https://learn.microsoft.com/en-us/azure/cognitive-services/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/"},
        {"name": "Azure Container Apps", "category": "Containers", "docs": "https://learn.microsoft.com/en-us/azure/container-apps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-apps/"},
        {"name": "Azure Container Instances", "category": "Containers", "docs": "https://learn.microsoft.com/en-us/azure/container-instances/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-instances/"},
        {"name": "Azure Cosmos DB", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/cosmos-db/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cosmos-db/"},
        {"name": "Azure Data Box", "category": "Migration", "docs": "https://learn.microsoft.com/en-us/azure/databox/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/databox/"},
        {"name": "Azure Data Explorer", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/azure/data-explorer/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/data-explorer/"},
        {"name": "Azure Data Lake Storage", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/storage/data-lake-storage/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/data-lake/"},
        {"name": "Azure Database for MariaDB", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/mariadb/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/mariadb/"},
        {"name": "Azure Database for MySQL", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/mysql/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/mysql/"},
        {"name": "Azure Database for PostgreSQL", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/postgresql/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/postgresql/"},
        {"name": "Azure DevOps", "category": "DevOps", "docs": "https://learn.microsoft.com/en-us/azure/devops/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/devops-services/"},
        {"name": "Azure DNS", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/dns/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/dns/"},
        {"name": "Azure Event Grid", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/event-grid/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/event-grid/"},
        {"name": "Azure Event Hubs", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/event-hubs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/event-hubs/"},
        {"name": "Azure ExpressRoute", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/expressroute/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/expressroute/"},
        {"name": "Azure Firewall", "category": "Security", "docs": "https://learn.microsoft.com/en-us/azure/firewall/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-firewall/"},
        {"name": "Azure Front Door", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/frontdoor/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/frontdoor/"},
        {"name": "Azure Functions", "category": "Compute", "docs": "https://learn.microsoft.com/en-us/azure/azure-functions/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/functions/"},
        {"name": "Azure HDInsight", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/azure/hdinsight/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/hdinsight/"},
        {"name": "Azure IoT Central", "category": "IoT", "docs": "https://learn.microsoft.com/en-us/azure/iot-central/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/iot-central/"},
        {"name": "Azure IoT Edge", "category": "IoT", "docs": "https://learn.microsoft.com/en-us/azure/iot-edge/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/iot-edge/"},
        {"name": "Azure IoT Hub", "category": "IoT", "docs": "https://learn.microsoft.com/en-us/azure/iot-hub/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/iot-hub/"},
        {"name": "Azure Key Vault", "category": "Security", "docs": "https://learn.microsoft.com/en-us/azure/key-vault/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/key-vault/"},
        {"name": "Azure Kubernetes Service (AKS)", "category": "Containers", "docs": "https://learn.microsoft.com/en-us/azure/aks/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/"},
        {"name": "Azure Load Balancer", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/load-balancer/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/load-balancer/"},
        {"name": "Azure Logic Apps", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/logic-apps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/logic-apps/"},
        {"name": "Azure Machine Learning", "category": "AI + ML", "docs": "https://learn.microsoft.com/en-us/azure/machine-learning/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/machine-learning/"},
        {"name": "Azure Managed Disks", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/managed-disks/"},
        {"name": "Azure Media Services", "category": "Media", "docs": "https://learn.microsoft.com/en-us/azure/media-services/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/media-services/"},
        {"name": "Azure NetApp Files", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/azure-netapp-files/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/netapp-files/"},
        {"name": "Azure OpenAI Service", "category": "AI + ML", "docs": "https://learn.microsoft.com/en-us/azure/ai-services/openai/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/"},
        {"name": "Azure Policy", "category": "Governance", "docs": "https://learn.microsoft.com/en-us/azure/governance/policy/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/policy/"},
        {"name": "Azure Private Link", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/private-link/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/private-link/"},
        {"name": "Azure Sentinel", "category": "Security", "docs": "https://learn.microsoft.com/en-us/azure/sentinel/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/microsoft-sentinel/"},
        {"name": "Azure Site Recovery", "category": "Migration", "docs": "https://learn.microsoft.com/en-us/azure/site-recovery/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/site-recovery/"},
        {"name": "Azure SQL Database", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/azure-sql/database/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-sql-database/"},
        {"name": "Azure SQL Managed Instance", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-sql-managed-instance/"},
        {"name": "Azure Stack", "category": "Hybrid", "docs": "https://learn.microsoft.com/en-us/azure-stack/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-stack/"},
        {"name": "Azure Storage Accounts", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage-accounts/"},
        {"name": "Azure Stream Analytics", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/azure/stream-analytics/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/stream-analytics/"},
        {"name": "Azure Synapse Analytics", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/azure/synapse-analytics/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/synapse-analytics/"},
        {"name": "Azure Traffic Manager", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/traffic-manager/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/traffic-manager/"},
        {"name": "Azure Virtual Desktop", "category": "Compute", "docs": "https://learn.microsoft.com/en-us/azure/virtual-desktop/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/virtual-desktop/"},
        {"name": "Azure Virtual Machines", "category": "Compute", "docs": "https://learn.microsoft.com/en-us/azure/virtual-machines/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/"},
        {"name": "Azure Virtual Network", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/virtual-network/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/virtual-network/"},
        {"name": "Azure VPN Gateway", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/vpn-gateway/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/vpn-gateway/"},
        {"name": "Batch", "category": "Compute", "docs": "https://learn.microsoft.com/en-us/azure/batch/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/batch/"},
        {"name": "Blob Storage", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/storage/blobs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/blobs/"},
        {"name": "Cognitive Search", "category": "AI + ML", "docs": "https://learn.microsoft.com/en-us/azure/search/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/search/"},
        {"name": "Container Registry", "category": "Containers", "docs": "https://learn.microsoft.com/en-us/azure/container-registry/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-registry/"},
        {"name": "Content Delivery Network (CDN)", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/cdn/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cdn/"},
        {"name": "Cosmos DB", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/cosmos-db/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cosmos-db/"},
        {"name": "Data Factory", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/azure/data-factory/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/data-factory/"},
        {"name": "Data Lake Analytics", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/azure/data-lake-analytics/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/data-lake-analytics/"},
        {"name": "Databricks", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/azure/databricks/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/databricks/"},
        {"name": "DevTest Labs", "category": "Developer Tools", "docs": "https://learn.microsoft.com/en-us/azure/devtest-labs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/devtest-labs/"},
        {"name": "Event Grid", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/event-grid/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/event-grid/"},
        {"name": "Event Hubs", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/event-hubs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/event-hubs/"},
        {"name": "Functions", "category": "Compute", "docs": "https://learn.microsoft.com/en-us/azure/azure-functions/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/functions/"},
        {"name": "HDInsight", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/azure/hdinsight/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/hdinsight/"},
        {"name": "IoT Central", "category": "IoT", "docs": "https://learn.microsoft.com/en-us/azure/iot-central/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/iot-central/"},
        {"name": "IoT Edge", "category": "IoT", "docs": "https://learn.microsoft.com/en-us/azure/iot-edge/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/iot-edge/"},
        {"name": "IoT Hub", "category": "IoT", "docs": "https://learn.microsoft.com/en-us/azure/iot-hub/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/iot-hub/"},
        {"name": "Key Vault", "category": "Security", "docs": "https://learn.microsoft.com/en-us/azure/key-vault/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/key-vault/"},
        {"name": "Kubernetes Service", "category": "Containers", "docs": "https://learn.microsoft.com/en-us/azure/aks/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/"},
        {"name": "Load Balancer", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/load-balancer/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/load-balancer/"},
        {"name": "Logic Apps", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/logic-apps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/logic-apps/"},
        {"name": "Machine Learning", "category": "AI + ML", "docs": "https://learn.microsoft.com/en-us/azure/machine-learning/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/machine-learning/"},
        {"name": "Managed Disks", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/managed-disks/"},
        {"name": "Media Services", "category": "Media", "docs": "https://learn.microsoft.com/en-us/azure/media-services/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/media-services/"},
        {"name": "Microsoft Defender for Cloud", "category": "Security", "docs": "https://learn.microsoft.com/en-us/azure/defender-for-cloud/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/defender-for-cloud/"},
        {"name": "Microsoft Fabric", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/fabric/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/microsoft-fabric/"},
        {"name": "Monitor", "category": "Monitoring", "docs": "https://learn.microsoft.com/en-us/azure/azure-monitor/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/monitor/"},
        {"name": "Network Watcher", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/network-watcher/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/network-watcher/"},
        {"name": "OpenAI Service", "category": "AI + ML", "docs": "https://learn.microsoft.com/en-us/azure/ai-services/openai/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/"},
        {"name": "Policy", "category": "Governance", "docs": "https://learn.microsoft.com/en-us/azure/governance/policy/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/policy/"},
        {"name": "Power BI", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/power-bi/", "pricing": "https://powerbi.microsoft.com/en-us/pricing/"},
        {"name": "Private Link", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/private-link/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/private-link/"},
        {"name": "Service Bus", "category": "Integration", "docs": "https://learn.microsoft.com/en-us/azure/service-bus-messaging/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/service-bus/"},
        {"name": "SignalR", "category": "Web", "docs": "https://learn.microsoft.com/en-us/azure/azure-signalr/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/signalr-service/"},
        {"name": "Site Recovery", "category": "Management", "docs": "https://learn.microsoft.com/en-us/azure/site-recovery/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/site-recovery/"},
        {"name": "SQL Database", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/azure-sql/database/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-sql-database/"},
        {"name": "SQL Managed Instance", "category": "Databases", "docs": "https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-sql-managed-instance/"},
        {"name": "Storage Accounts", "category": "Storage", "docs": "https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage-accounts/"},
        {"name": "Stream Analytics", "category": "Analytics", "docs": "https://learn.microsoft.com/en-us/azure/stream-analytics/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/stream-analytics/"},
        {"name": "Traffic Manager", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/traffic-manager/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/traffic-manager/"},
        {"name": "Virtual Machines", "category": "Compute", "docs": "https://learn.microsoft.com/en-us/azure/virtual-machines/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/"},
        {"name": "Virtual Network", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/virtual-network/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/virtual-network/"},
        {"name": "VPN Gateway", "category": "Networking", "docs": "https://learn.microsoft.com/en-us/azure/vpn-gateway/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/vpn-gateway/"},
        {"name": "Web Application Firewall", "category": "Security", "docs": "https://learn.microsoft.com/en-us/azure/web-application-firewall/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/web-application-firewall/"},
        {"name": "Windows Virtual Desktop", "category": "Compute", "docs": "https://learn.microsoft.com/en-us/azure/virtual-desktop/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/virtual-desktop/"}
    ]

# Optionally, expand overview/pros/cons as desired.
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
    details = []
    doc_links = []
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
        summary_rows.append({
            "Score": svc["score"],
            "Component": f"[{name}]({svc.get('docs','')})",
            "Category": cat,
            "Alternatives": alt_str,
            "Docs": f"[Docs]({svc.get('docs','')})" if svc.get("docs") else "",
            "Pricing": f"[Pricing]({svc.get('pricing','')})" if svc.get("pricing") else ""
        })
        doc_links.append(f"- [{name}]({svc.get('docs','')})")
        overview = get_service_overview(name, cat)
        pros_str = "\n    ".join(f"- {p}" for p in overview["pros"]) if overview["pros"] else "N/A"
        cons_str = "\n    ".join(f"- {c}" for c in overview["cons"]) if overview["cons"] else "N/A"
        details.append(
            f"### {name}\n"
            f"**Category:** {cat}\n\n"
            f"**Score:** {svc['score']}\n\n"
            f"**Overview:**\n{overview['overview']}\n\n"
            f"**Pros:**\n{pros_str}\n\n"
            f"**Cons:**\n{cons_str}\n\n"
            f"**[Docs]({svc.get('docs','')}) | [Pricing]({svc.get('pricing','')})**\n"
        )
    arch_diagram = ""
    if filtered_services:
        diagram_lines = []
        used_cats = []
        cat_to_letter = {}
        letter_ord = 65  # A
        for svc in filtered_services:
            cat = svc["category"]
            if cat not in used_cats:
                used_cats.append(cat)
                cat_to_letter[cat] = chr(letter_ord)
                letter_ord += 1
        prev_letter = None
        for cat in used_cats:
            svc = next(s for s in filtered_services if s["category"] == cat)
            letter = cat_to_letter[cat]
            if prev_letter is None:
                diagram_lines.append(f"{letter}[{svc['name']}]")
            else:
                diagram_lines.append(f"{prev_letter} --> {letter}[{svc['name']}]")
            prev_letter = letter
        arch_diagram = "flowchart LR\n    " + "\n    ".join(diagram_lines)
    solution = [f"{row['Component']} ({row['Category']})" for row in summary_rows]
    return solution, details, doc_links, arch_diagram, summary_rows

def mermaid_to_svg(mermaid_code: str):
    url = "https://kroki.io/mermaid/svg"
    resp = requests.post(url, data=mermaid_code.encode("utf-8"))
    resp.raise_for_status()
    return resp.text

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
    solution, details, doc_links, arch_diagram, summary_rows = recommend_architecture(
        user_input, azure_services, min_score=min_score, top_n=top_n
    )
    st.header("Recommended Azure Solution")
    if summary_rows:
        st.markdown("### Recommended Components Summary")
        table_md = "| Score | Component | Category | Alternatives | Docs | Pricing |\n"
        table_md += "|---|---|---|---|---|---|\n"
        for row in summary_rows:
            table_md += f"| {row['Score']} | {row['Component']} | {row['Category']} | {row['Alternatives']} | {row['Docs']} | {row['Pricing']} |\n"
        st.markdown(table_md, unsafe_allow_html=True)
    else:
        st.warning("No relevant Azure products matched your requirements. Please try adjusting your input, score threshold, or Top N.")

    if doc_links:
        st.markdown("### Core Components (Docs)")
        st.markdown("\n".join(doc_links))

    if details:
        st.markdown("## Solution Overview")
        for d in details:
            st.markdown(d, unsafe_allow_html=True)

    if arch_diagram.strip():
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
        if summary_rows:
            md += "## Recommended Components Summary\n\n"
            md += "| Score | Component | Category | Alternatives | Docs | Pricing |\n"
            md += "|---|---|---|---|---|---|\n"
            for row in summary_rows:
                md += f"| {row['Score']} | {row['Component']} | {row['Category']} | {row['Alternatives']} | {row['Docs']} | {row['Pricing']} |\n"
        if details:
            md += "\n## Solution Overview\n" + "\n".join(details) + "\n\n"
        if arch_diagram.strip():
            md += "## Architecture Diagram (Mermaid)\n```mermaid\n" + arch_diagram.strip() + "\n```\n"
        st.download_button("Download Markdown", data=md, file_name="azure_solution.md", mime="text/markdown")
