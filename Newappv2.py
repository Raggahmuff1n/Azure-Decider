import streamlit as st
import pandas as pd
import json
from typing import Dict, List, Any, Tuple
import re
from datetime import datetime

st.set_page_config(page_title="Azure Solution Architect Pro", layout="wide", page_icon="☁️")

# Enhanced Azure Service Catalog with comprehensive coverage
@st.cache_data(ttl=3600)
def fetch_enhanced_azure_services():
    """Comprehensive Azure service catalog with enhanced metadata for solution architecture"""
    return [
        # Analytics & BI - Enhanced for complete data platform
        {"name": "Azure Synapse Analytics", "category": "Analytics", "cost_tier": "high", "use_cases": ["data_warehouse", "analytics", "big_data", "etl"], "integrates_with": ["Power BI", "Azure Data Lake Storage", "Azure Machine Learning", "Azure Data Factory"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/synapse-analytics/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/synapse-analytics/", "data_role": "processing", "architectural_tier": "analytics"},
        {"name": "Power BI", "category": "Analytics", "cost_tier": "medium", "use_cases": ["visualization", "dashboards", "business_intelligence", "reporting"], "integrates_with": ["Azure Synapse Analytics", "Azure Data Factory", "Azure SQL Database", "Office 365"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/power-bi/", "pricing": "https://powerbi.microsoft.com/en-us/pricing/", "data_role": "visualization", "architectural_tier": "presentation"},
        {"name": "Azure Data Factory", "category": "Analytics", "cost_tier": "medium", "use_cases": ["etl", "data_integration", "pipeline", "data_movement"], "integrates_with": ["Azure Synapse Analytics", "Azure Data Lake Storage", "Azure SQL Database", "Power BI"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/data-factory/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/data-factory/", "data_role": "ingestion", "architectural_tier": "integration"},
        {"name": "Azure Databricks", "category": "Analytics", "cost_tier": "high", "use_cases": ["machine_learning", "analytics", "spark", "data_science"], "integrates_with": ["Azure Machine Learning", "Azure Data Lake Storage", "Power BI", "Azure Synapse Analytics"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/databricks/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/databricks/", "data_role": "processing", "architectural_tier": "analytics"},
        {"name": "Azure Stream Analytics", "category": "Analytics", "cost_tier": "medium", "use_cases": ["real_time", "streaming", "iot", "event_processing"], "integrates_with": ["Event Hubs", "IoT Hub", "Power BI", "Azure Functions"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/stream-analytics/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/stream-analytics/", "data_role": "processing", "architectural_tier": "analytics"},
        {"name": "Azure Analysis Services", "category": "Analytics", "cost_tier": "medium", "use_cases": ["olap", "tabular_models", "business_intelligence", "semantic_layer"], "integrates_with": ["Power BI", "Excel", "Azure SQL Database"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/analysis-services/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/analysis-services/", "data_role": "processing", "architectural_tier": "analytics"},
        {"name": "Microsoft Purview", "category": "Analytics", "cost_tier": "medium", "use_cases": ["data_governance", "data_catalog", "compliance", "data_lineage"], "integrates_with": ["Azure Synapse Analytics", "Azure Data Factory", "Power BI"], "compliance": ["SOC", "HIPAA", "ISO", "GDPR"], "docs": "https://learn.microsoft.com/en-us/purview/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-purview/", "data_role": "governance", "architectural_tier": "management"},
        
        # AI & ML - Complete ML platform
        {"name": "Azure Machine Learning", "category": "AI + ML", "cost_tier": "high", "use_cases": ["machine_learning", "model_training", "mlops", "data_science"], "integrates_with": ["Azure Databricks", "Azure Synapse Analytics", "Azure Container Instances", "AKS"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/machine-learning/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/machine-learning/", "data_role": "processing", "architectural_tier": "analytics"},
        {"name": "Azure Cognitive Services", "category": "AI + ML", "cost_tier": "medium", "use_cases": ["ai", "computer_vision", "nlp", "speech", "translation"], "integrates_with": ["Azure Bot Service", "Azure Functions", "Logic Apps"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/cognitive-services/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/", "data_role": "processing", "architectural_tier": "application"},
        {"name": "Azure OpenAI Service", "category": "AI + ML", "cost_tier": "high", "use_cases": ["generative_ai", "chatbot", "content_generation", "llm"], "integrates_with": ["Azure Cognitive Services", "Azure Bot Service", "Azure Functions"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/ai-services/openai/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/", "data_role": "processing", "architectural_tier": "application"},
        {"name": "Azure Bot Service", "category": "AI + ML", "cost_tier": "low", "use_cases": ["chatbot", "conversational_ai", "customer_service"], "integrates_with": ["Azure Cognitive Services", "Azure OpenAI Service", "Teams"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/bot-service/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/bot-service/", "data_role": "interaction", "architectural_tier": "application"},
        {"name": "Azure Form Recognizer", "category": "AI + ML", "cost_tier": "medium", "use_cases": ["document_processing", "ocr", "form_extraction"], "integrates_with": ["Azure Cognitive Services", "Logic Apps", "Power Automate"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/ai-services/form-recognizer/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/form-recognizer/", "data_role": "processing", "architectural_tier": "application"},
        {"name": "Azure Computer Vision", "category": "AI + ML", "cost_tier": "medium", "use_cases": ["image_processing", "ocr", "object_detection"], "integrates_with": ["Azure Cognitive Services", "Azure Functions", "Logic Apps"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/computer-vision/", "data_role": "processing", "architectural_tier": "application"},
        
        # Compute - Enhanced for modern applications
        {"name": "Azure Virtual Machines", "category": "Compute", "cost_tier": "variable", "use_cases": ["windows", "linux", "legacy_apps", "custom_software"], "integrates_with": ["Virtual Network", "Load Balancer", "Azure Monitor"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/virtual-machines/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/", "data_role": "processing", "architectural_tier": "compute"},
        {"name": "Azure Functions", "category": "Compute", "cost_tier": "low", "use_cases": ["serverless", "microservices", "event_driven", "api"], "integrates_with": ["Logic Apps", "Event Grid", "Cosmos DB", "API Management"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-functions/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/functions/", "data_role": "processing", "architectural_tier": "compute"},
        {"name": "Azure Batch", "category": "Compute", "cost_tier": "medium", "use_cases": ["batch_processing", "hpc", "parallel_workloads"], "integrates_with": ["Azure Storage", "Virtual Networks", "Azure Monitor"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/batch/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/batch/", "data_role": "processing", "architectural_tier": "compute"},
        {"name": "Azure Service Fabric", "category": "Compute", "cost_tier": "medium", "use_cases": ["microservices", "distributed_systems", "stateful_services"], "integrates_with": ["Azure Monitor", "Key Vault", "Load Balancer"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/service-fabric/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/service-fabric/", "data_role": "processing", "architectural_tier": "compute"},
        
        # Containers - Complete container platform
        {"name": "Azure Kubernetes Service (AKS)", "category": "Containers", "cost_tier": "medium", "use_cases": ["kubernetes", "microservices", "container_orchestration"], "integrates_with": ["Azure Container Registry", "Azure Monitor", "Azure Active Directory", "Application Gateway"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/aks/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/", "data_role": "processing", "architectural_tier": "compute"},
        {"name": "Azure Container Apps", "category": "Containers", "cost_tier": "low", "use_cases": ["serverless_containers", "microservices", "event_driven"], "integrates_with": ["Event Grid", "Service Bus", "Azure Monitor"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/container-apps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-apps/", "data_role": "processing", "architectural_tier": "compute"},
        {"name": "Azure Container Instances", "category": "Containers", "cost_tier": "low", "use_cases": ["simple_containers", "batch_jobs", "dev_test"], "integrates_with": ["Virtual Network", "Azure Files", "Azure Monitor"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/container-instances/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-instances/", "data_role": "processing", "architectural_tier": "compute"},
        {"name": "Azure Container Registry", "category": "Containers", "cost_tier": "low", "use_cases": ["container_images", "docker_registry", "devops"], "integrates_with": ["AKS", "Container Apps", "Azure DevOps"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/container-registry/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-registry/", "data_role": "storage", "architectural_tier": "management"},
        
        # Databases - Complete data platform
        {"name": "Azure SQL Database", "category": "Databases", "cost_tier": "medium", "use_cases": ["relational_database", "sql_server", "managed_database"], "integrates_with": ["Power BI", "Azure Data Factory", "Azure Functions"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/azure-sql/database/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-sql-database/", "data_role": "storage", "architectural_tier": "data"},
        {"name": "Azure Cosmos DB", "category": "Databases", "cost_tier": "medium", "use_cases": ["nosql", "global_distribution", "multi_model"], "integrates_with": ["Azure Functions", "Azure Synapse Analytics", "Power BI"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/cosmos-db/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cosmos-db/", "data_role": "storage", "architectural_tier": "data"},
        {"name": "Azure Database for PostgreSQL", "category": "Databases", "cost_tier": "medium", "use_cases": ["postgresql", "open_source", "managed_database"], "integrates_with": ["Azure Data Factory", "Power BI", "Azure Monitor"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/postgresql/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/postgresql/", "data_role": "storage", "architectural_tier": "data"},
        {"name": "Azure Database for MySQL", "category": "Databases", "cost_tier": "medium", "use_cases": ["mysql", "open_source", "managed_database"], "integrates_with": ["Azure Data Factory", "Power BI", "Azure Monitor"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/mysql/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/mysql/", "data_role": "storage", "architectural_tier": "data"},
        {"name": "Azure Cache for Redis", "category": "Databases", "cost_tier": "low", "use_cases": ["caching", "session_storage", "real_time"], "integrates_with": ["Azure Functions", "App Service", "AKS"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cache/", "data_role": "storage", "architectural_tier": "data"},
        
        # Storage - Complete storage solutions
        {"name": "Azure Blob Storage", "category": "Storage", "cost_tier": "low", "use_cases": ["object_storage", "backup", "archival", "static_content"], "integrates_with": ["Azure CDN", "Azure Data Factory", "Power BI"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/storage/blobs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/blobs/", "data_role": "storage", "architectural_tier": "data"},
        {"name": "Azure Data Lake Storage", "category": "Storage", "cost_tier": "medium", "use_cases": ["big_data", "analytics", "data_lake"], "integrates_with": ["Azure Synapse Analytics", "Azure Databricks", "Power BI"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/data-lake/", "data_role": "storage", "architectural_tier": "data"},
        {"name": "Azure Files", "category": "Storage", "cost_tier": "low", "use_cases": ["file_shares", "smb", "nfs"], "integrates_with": ["Virtual Machines", "Container Instances", "AKS"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/storage/files/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/files/", "data_role": "storage", "architectural_tier": "data"},
        {"name": "Azure NetApp Files", "category": "Storage", "cost_tier": "high", "use_cases": ["enterprise_nas", "hpc", "high_performance"], "integrates_with": ["Virtual Machines", "AKS", "Azure VMware Solution"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-netapp-files/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/netapp/", "data_role": "storage", "architectural_tier": "data"},
        
        # Networking - Complete networking stack
        {"name": "Azure Virtual Network", "category": "Networking", "cost_tier": "low", "use_cases": ["network_isolation", "hybrid_connectivity", "security"], "integrates_with": ["Virtual Machines", "AKS", "Application Gateway"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/virtual-network/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/virtual-network/", "data_role": "infrastructure", "architectural_tier": "network"},
        {"name": "Azure Application Gateway", "category": "Networking", "cost_tier": "medium", "use_cases": ["load_balancer", "ssl_termination", "waf"], "integrates_with": ["Virtual Network", "AKS", "App Service"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/application-gateway/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/application-gateway/", "data_role": "infrastructure", "architectural_tier": "network"},
        {"name": "Azure Load Balancer", "category": "Networking", "cost_tier": "low", "use_cases": ["load_balancing", "high_availability", "traffic_distribution"], "integrates_with": ["Virtual Machines", "Virtual Network", "AKS"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/load-balancer/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/load-balancer/", "data_role": "infrastructure", "architectural_tier": "network"},
        {"name": "Azure Front Door", "category": "Networking", "cost_tier": "medium", "use_cases": ["global_load_balancer", "cdn", "waf"], "integrates_with": ["App Service", "Application Gateway", "Blob Storage"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/frontdoor/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/frontdoor/", "data_role": "infrastructure", "architectural_tier": "network"},
        {"name": "Azure ExpressRoute", "category": "Networking", "cost_tier": "high", "use_cases": ["hybrid_connectivity", "private_connection", "enterprise"], "integrates_with": ["Virtual Network", "Virtual WAN", "Azure Monitor"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/expressroute/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/expressroute/", "data_role": "infrastructure", "architectural_tier": "network"},
        {"name": "Azure VPN Gateway", "category": "Networking", "cost_tier": "low", "use_cases": ["vpn", "site_to_site", "point_to_site"], "integrates_with": ["Virtual Network", "Azure Monitor", "Network Watcher"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/vpn-gateway/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/vpn-gateway/", "data_role": "infrastructure", "architectural_tier": "network"},
        
        # Security - Comprehensive security stack
        {"name": "Azure Key Vault", "category": "Security", "cost_tier": "low", "use_cases": ["secrets_management", "encryption", "certificates"], "integrates_with": ["App Service", "Azure Functions", "Virtual Machines"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/key-vault/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/key-vault/", "data_role": "security", "architectural_tier": "security"},
        {"name": "Microsoft Defender for Cloud", "category": "Security", "cost_tier": "medium", "use_cases": ["security_monitoring", "threat_detection", "compliance"], "integrates_with": ["Azure Monitor", "Sentinel", "Logic Apps"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/defender-for-cloud/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/defender-for-cloud/", "data_role": "security", "architectural_tier": "security"},
        {"name": "Microsoft Sentinel", "category": "Security", "cost_tier": "medium", "use_cases": ["siem", "soar", "security_analytics"], "integrates_with": ["Azure Monitor", "Logic Apps", "Defender for Cloud"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/sentinel/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/microsoft-sentinel/", "data_role": "security", "architectural_tier": "security"},
        {"name": "Azure Active Directory", "category": "Security", "cost_tier": "variable", "use_cases": ["identity", "authentication", "authorization"], "integrates_with": ["All Azure Services", "Office 365", "Third-party apps"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/active-directory/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/active-directory/", "data_role": "security", "architectural_tier": "security"},
        {"name": "Azure Firewall", "category": "Security", "cost_tier": "medium", "use_cases": ["network_firewall", "traffic_filtering", "security"], "integrates_with": ["Virtual Network", "Azure Monitor", "Sentinel"], "compliance": ["SOC", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/firewall/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-firewall/", "data_role": "security", "architectural_tier": "security"},
        {"name": "Azure DDoS Protection", "category": "Security", "cost_tier": "medium", "use_cases": ["ddos_protection", "network_security", "availability"], "integrates_with": ["Virtual Network", "Application Gateway", "Azure Monitor"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/ddos-protection/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/ddos-protection/", "data_role": "security", "architectural_tier": "security"},
        
        # Web & Mobile - Complete web platform
        {"name": "Azure App Service", "category": "Web", "cost_tier": "medium", "use_cases": ["web_apps", "api", "mobile_backend"], "integrates_with": ["Azure SQL Database", "Key Vault", "Application Insights"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/app-service/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/app-service/", "data_role": "application", "architectural_tier": "application"},
        {"name": "Azure Static Web Apps", "category": "Web", "cost_tier": "low", "use_cases": ["static_sites", "jamstack", "frontend"], "integrates_with": ["GitHub", "Azure DevOps", "Azure Functions"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/static-web-apps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/app-service/static/", "data_role": "application", "architectural_tier": "application"},
        {"name": "Azure CDN", "category": "Web", "cost_tier": "low", "use_cases": ["content_delivery", "performance", "global_distribution"], "integrates_with": ["Blob Storage", "App Service", "Front Door"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/cdn/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cdn/", "data_role": "infrastructure", "architectural_tier": "network"},
        
        # Integration - Complete integration platform
        {"name": "Azure Logic Apps", "category": "Integration", "cost_tier": "low", "use_cases": ["workflow", "integration", "automation"], "integrates_with": ["Office 365", "Dynamics 365", "SAP"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/logic-apps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/logic-apps/", "data_role": "integration", "architectural_tier": "integration"},
        {"name": "Azure Event Grid", "category": "Integration", "cost_tier": "low", "use_cases": ["event_routing", "reactive_programming", "serverless"], "integrates_with": ["Azure Functions", "Logic Apps", "Event Hubs"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/event-grid/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/event-grid/", "data_role": "integration", "architectural_tier": "integration"},
        {"name": "Azure Service Bus", "category": "Integration", "cost_tier": "low", "use_cases": ["messaging", "queues", "pub_sub"], "integrates_with": ["Azure Functions", "Logic Apps", "Service Fabric"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/service-bus-messaging/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/service-bus/", "data_role": "integration", "architectural_tier": "integration"},
        {"name": "Azure API Management", "category": "Integration", "cost_tier": "medium", "use_cases": ["api_gateway", "api_management", "developer_portal"], "integrates_with": ["App Service", "Azure Functions", "Logic Apps"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/api-management/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/api-management/", "data_role": "integration", "architectural_tier": "integration"},
        {"name": "Azure Event Hubs", "category": "Integration", "cost_tier": "medium", "use_cases": ["big_data_streaming", "telemetry", "event_ingestion"], "integrates_with": ["Stream Analytics", "Azure Functions", "Databricks"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/event-hubs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/event-hubs/", "data_role": "ingestion", "architectural_tier": "integration"},
        
        # IoT - Complete IoT platform
        {"name": "Azure IoT Hub", "category": "IoT", "cost_tier": "medium", "use_cases": ["iot_connectivity", "device_management", "telemetry"], "integrates_with": ["Stream Analytics", "Event Grid", "Time Series Insights"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/iot-hub/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/iot-hub/", "data_role": "ingestion", "architectural_tier": "application"},
        {"name": "Azure IoT Central", "category": "IoT", "cost_tier": "low", "use_cases": ["iot_saas", "device_templates", "no_code_iot"], "integrates_with": ["Power BI", "Logic Apps", "Event Grid"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/iot-central/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/iot-central/", "data_role": "application", "architectural_tier": "application"},
        {"name": "Azure Digital Twins", "category": "IoT", "cost_tier": "medium", "use_cases": ["digital_twins", "iot_modeling", "spatial_intelligence"], "integrates_with": ["IoT Hub", "Time Series Insights", "Azure Maps"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/digital-twins/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/digital-twins/", "data_role": "processing", "architectural_tier": "application"},
        {"name": "Azure Time Series Insights", "category": "IoT", "cost_tier": "medium", "use_cases": ["time_series", "iot_analytics", "operational_intelligence"], "integrates_with": ["IoT Hub", "Event Hubs", "Power BI"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/time-series-insights/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/time-series-insights/", "data_role": "processing", "architectural_tier": "analytics"},
        
        # DevOps - Complete DevOps platform
        {"name": "Azure DevOps", "category": "DevOps", "cost_tier": "low", "use_cases": ["ci_cd", "project_management", "source_control"], "integrates_with": ["GitHub", "Azure Container Registry", "AKS"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/devops/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/", "data_role": "management", "architectural_tier": "management"},
        {"name": "GitHub Actions", "category": "DevOps", "cost_tier": "low", "use_cases": ["ci_cd", "automation", "workflows"], "integrates_with": ["Azure Container Registry", "AKS", "App Service"], "compliance": ["SOC", "ISO"], "docs": "https://docs.github.com/en/actions", "pricing": "https://github.com/pricing", "data_role": "management", "architectural_tier": "management"},
        {"name": "Azure Artifacts", "category": "DevOps", "cost_tier": "low", "use_cases": ["package_management", "npm", "nuget", "maven"], "integrates_with": ["Azure DevOps", "Visual Studio", "Azure Pipelines"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/devops/artifacts/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/", "data_role": "management", "architectural_tier": "management"},
        
        # Monitoring - Complete observability platform
        {"name": "Azure Monitor", "category": "Monitoring", "cost_tier": "medium", "use_cases": ["monitoring", "logging", "metrics"], "integrates_with": ["All Azure Services", "Application Insights", "Log Analytics"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/azure-monitor/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/monitor/", "data_role": "monitoring", "architectural_tier": "management"},
        {"name": "Application Insights", "category": "Monitoring", "cost_tier": "low", "use_cases": ["apm", "performance_monitoring", "diagnostics"], "integrates_with": ["App Service", "Azure Functions", "AKS"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/monitor/", "data_role": "monitoring", "architectural_tier": "management"},
        {"name": "Azure Log Analytics", "category": "Monitoring", "cost_tier": "medium", "use_cases": ["log_analysis", "queries", "dashboards"], "integrates_with": ["Azure Monitor", "Sentinel", "Defender for Cloud"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/monitor/", "data_role": "monitoring", "architectural_tier": "management"},
        
        # Management - Complete governance platform
        {"name": "Azure Resource Manager", "category": "Management", "cost_tier": "free", "use_cases": ["resource_management", "templates", "deployment"], "integrates_with": ["All Azure Services", "Azure DevOps", "Terraform"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/resource-manager/", "data_role": "management", "architectural_tier": "management"},
        {"name": "Azure Policy", "category": "Management", "cost_tier": "free", "use_cases": ["governance", "compliance", "resource_policies"], "integrates_with": ["Azure Monitor", "Resource Manager", "Blueprints"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/governance/policy/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-policy/", "data_role": "governance", "architectural_tier": "management"},
        {"name": "Azure Automation", "category": "Management", "cost_tier": "low", "use_cases": ["automation", "configuration_management", "update_management"], "integrates_with": ["Azure Monitor", "Log Analytics", "Virtual Machines"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/automation/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/automation/", "data_role": "management", "architectural_tier": "management"},

        # Additional industry-specific services
        {"name": "Azure API for FHIR", "category": "Healthcare", "cost_tier": "medium", "use_cases": ["healthcare", "fhir", "medical_data"], "integrates_with": ["Azure Active Directory", "Azure Monitor", "Power BI"], "compliance": ["HIPAA", "SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/healthcare-apis/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-api-for-fhir/", "data_role": "application", "architectural_tier": "application"},
        {"name": "Azure Maps", "category": "Location Services", "cost_tier": "low", "use_cases": ["mapping", "geospatial", "location"], "integrates_with": ["Power BI", "Logic Apps", "Azure Functions"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-maps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-maps/", "data_role": "application", "architectural_tier": "application"},
        {"name": "Azure Communication Services", "category": "Communication", "cost_tier": "low", "use_cases": ["chat", "voice", "video", "sms"], "integrates_with": ["Azure Functions", "Logic Apps", "Bot Service"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/communication-services/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/communication-services/", "data_role": "application", "architectural_tier": "application"},
    ]

# Enhanced Architecture Patterns with data flow awareness
ENHANCED_ARCHITECTURE_PATTERNS = {
    "modern_data_platform": {
        "name": "Modern Data Platform",
        "required": ["Azure Data Factory", "Azure Data Lake Storage", "Azure Synapse Analytics"],
        "recommended": ["Power BI", "Azure Machine Learning", "Microsoft Purview", "Azure Monitor"],
        "optional": ["Azure Databricks", "Azure Stream Analytics", "Azure Key Vault"],
        "description": "Complete modern data platform for analytics, ML, and business intelligence with data governance",
        "use_cases": ["data_warehouse", "analytics", "business_intelligence", "machine_learning"],
        "data_flow": "Data Factory → Data Lake → Synapse → Power BI",
        "tier_priority": {"integration": 9, "data": 9, "analytics": 10, "presentation": 8, "management": 7}
    },
    "serverless_web_app": {
        "name": "Serverless Web Application",
        "required": ["Azure Functions", "Azure Cosmos DB", "Azure Static Web Apps"],
        "recommended": ["Azure CDN", "Application Insights", "Key Vault", "API Management"],
        "optional": ["Azure Active Directory", "Azure Cache for Redis"],
        "description": "Scalable serverless web application with global distribution and monitoring",
        "use_cases": ["web_app", "api", "serverless", "global_distribution"],
        "data_flow": "Static Web Apps → API Management → Functions → Cosmos DB",
        "tier_priority": {"application": 10, "compute": 9, "data": 8, "network": 7, "security": 8}
    },
    "microservices_platform": {
        "name": "Microservices Platform",
        "required": ["Azure Kubernetes Service (AKS)", "Azure Container Registry", "Virtual Network"],
        "recommended": ["Application Gateway", "Azure Monitor", "Key Vault", "Service Bus"],
        "optional": ["Azure Cache for Redis", "Azure API Management", "Azure DevOps"],
        "description": "Enterprise-grade microservices platform with container orchestration and service mesh",
        "use_cases": ["microservices", "containers", "scalability", "enterprise"],
        "data_flow": "Application Gateway → AKS → Service Bus → Databases",
        "tier_priority": {"compute": 10, "network": 9, "integration": 8, "security": 9, "management": 8}
    },
    "ml_platform": {
        "name": "Machine Learning Platform",
        "required": ["Azure Machine Learning", "Azure Data Lake Storage", "Azure Databricks"],
        "recommended": ["Azure Data Factory", "Azure Synapse Analytics", "Azure Container Registry", "Azure Monitor"],
        "optional": ["Azure Cognitive Services", "Power BI", "Azure Functions"],
        "description": "End-to-end machine learning platform for model development, training, and deployment",
        "use_cases": ["machine_learning", "ai", "data_science", "model_deployment"],
        "data_flow": "Data Factory → Data Lake → Databricks → Azure ML → Deployment",
        "tier_priority": {"analytics": 10, "data": 9, "integration": 8, "compute": 8, "management": 7}
    },
    "iot_platform": {
        "name": "IoT Analytics Platform",
        "required": ["Azure IoT Hub", "Azure Stream Analytics", "Azure Data Lake Storage"],
        "recommended": ["Power BI", "Azure Functions", "Event Grid", "Azure Monitor"],
        "optional": ["Azure Digital Twins", "Time Series Insights", "Azure Machine Learning"],
        "description": "Comprehensive IoT platform for device management, real-time analytics, and insights",
        "use_cases": ["iot", "real_time", "telemetry", "device_management"],
        "data_flow": "IoT Hub → Stream Analytics → Data Lake → Power BI",
        "tier_priority": {"application": 10, "analytics": 9, "data": 8, "integration": 8, "management": 7}
    },
    "analytics_platform": {
        "name": "Advanced Analytics Platform",
        "required": ["Azure Synapse Analytics", "Power BI", "Azure Data Factory"],
        "recommended": ["Azure Data Lake Storage", "Azure Databricks", "Azure Machine Learning"],
        "optional": ["Microsoft Purview", "Azure Stream Analytics", "Azure Cognitive Services"],
        "description": "Comprehensive analytics platform for business intelligence and advanced analytics",
        "use_cases": ["analytics", "business_intelligence", "data_warehouse", "reporting"],
        "data_flow": "Data Factory → Synapse → Power BI / Databricks → ML Models",
        "tier_priority": {"analytics": 10, "data": 9, "integration": 8, "presentation": 9, "management": 7}
    },
    "security_first_architecture": {
        "name": "Security-First Architecture",
        "required": ["Azure Key Vault", "Microsoft Defender for Cloud", "Azure Active Directory"],
        "recommended": ["Microsoft Sentinel", "Azure Firewall", "Azure Monitor", "Azure Policy"],
        "optional": ["Azure DDoS Protection", "Azure VPN Gateway", "Azure Private Link"],
        "description": "Security-focused architecture with comprehensive threat protection and compliance",
        "use_cases": ["security", "compliance", "governance", "identity"],
        "data_flow": "AAD → Key Vault → Protected Resources → Monitoring → SIEM",
        "tier_priority": {"security": 10, "management": 9, "network": 8, "compute": 7, "data": 8}
    }
}

# Enhanced Industry Templates with specific service requirements
ENHANCED_INDUSTRY_TEMPLATES = {
    "healthcare": {
        "name": "Healthcare & Life Sciences",
        "compliance_requirements": ["HIPAA", "HITECH", "FDA", "GDPR"],
        "required_services": ["Azure Key Vault", "Microsoft Defender for Cloud", "Azure Monitor", "Azure API for FHIR"],
        "recommended_services": ["Azure Confidential Computing", "Private Link", "Azure Policy", "Microsoft Purview"],
        "data_governance": "strict",
        "encryption": "required",
        "specific_patterns": ["security_first_architecture", "modern_data_platform"],
        "prohibited_services": [],
        "scoring_boost": {"Security": 5, "Monitoring": 3, "Healthcare": 10}
    },
    "financial": {
        "name": "Financial Services",
        "compliance_requirements": ["PCI DSS", "SOX", "GDPR", "Basel III"],
        "required_services": ["Azure Key Vault", "Azure Firewall", "DDoS Protection", "Microsoft Sentinel"],
        "recommended_services": ["Azure Confidential Computing", "Private Link", "Azure Policy", "Azure Monitor"],
        "data_governance": "strict",
        "encryption": "required",
        "specific_patterns": ["security_first_architecture", "microservices_platform"],
        "prohibited_services": [],
        "scoring_boost": {"Security": 5, "Networking": 3, "Monitoring": 3}
    },
    "government": {
        "name": "Government",
        "compliance_requirements": ["FedRAMP", "FISMA", "ITAR", "CJIS"],
        "required_services": ["Azure Government", "Key Vault", "Azure Monitor", "Azure Policy"],
        "recommended_services": ["Azure Firewall", "DDoS Protection", "Sentinel", "Azure Automation"],
        "data_governance": "strict",
        "encryption": "required",
        "specific_patterns": ["security_first_architecture"],
        "prohibited_services": [],
        "scoring_boost": {"Security": 5, "Management": 4, "Monitoring": 3}
    },
    "retail": {
        "name": "Retail & E-commerce",
        "compliance_requirements": ["PCI DSS", "GDPR", "CCPA"],
        "required_services": ["Azure CDN", "Application Gateway", "Key Vault"],
        "recommended_services": ["Azure Cache for Redis", "Cosmos DB", "Cognitive Services", "Azure Monitor"],
        "data_governance": "moderate",
        "encryption": "recommended",
        "specific_patterns": ["serverless_web_app", "analytics_platform"],
        "prohibited_services": [],
        "scoring_boost": {"Web": 4, "AI + ML": 3, "Analytics": 3}
    },
    "manufacturing": {
        "name": "Manufacturing",
        "compliance_requirements": ["ISO 27001", "SOC 2", "IEC 62443"],
        "required_services": ["Azure IoT Hub", "Azure Monitor", "Key Vault"],
        "recommended_services": ["Digital Twins", "Stream Analytics", "Machine Learning", "Time Series Insights"],
        "data_governance": "moderate",
        "encryption": "recommended",
        "specific_patterns": ["iot_platform", "ml_platform"],
        "prohibited_services": [],
        "scoring_boost": {"IoT": 5, "Analytics": 4, "AI + ML": 3}
    },
    "media": {
        "name": "Media & Entertainment",
        "compliance_requirements": ["SOC 2", "ISO 27001"],
        "required_services": ["Azure CDN", "Azure Media Services", "Blob Storage"],
        "recommended_services": ["Cognitive Services", "Azure Functions", "Event Grid"],
        "data_governance": "moderate",
        "encryption": "recommended",
        "specific_patterns": ["serverless_web_app"],
        "prohibited_services": [],
        "scoring_boost": {"Web": 4, "Storage": 4, "AI + ML": 3}
    },
    "education": {
        "name": "Education",
        "compliance_requirements": ["FERPA", "SOC 2", "GDPR"],
        "required_services": ["Azure Active Directory", "Key Vault", "Azure Monitor"],
        "recommended_services": ["App Service", "Cognitive Services", "Power BI"],
        "data_governance": "moderate", 
        "encryption": "recommended",
        "specific_patterns": ["serverless_web_app", "analytics_platform"],
        "prohibited_services": [],
        "scoring_boost": {"Security": 3, "AI + ML": 3, "Analytics": 3}
    }
}

# Enhanced service relationships with detailed integration patterns
ENHANCED_SERVICE_RELATIONSHIPS = {
    "Azure Synapse Analytics": {
        "works_well_with": ["Power BI", "Azure Data Lake Storage", "Azure Data Factory", "Azure Machine Learning", "Microsoft Purview"],
        "data_sources": ["Azure SQL Database", "Cosmos DB", "Blob Storage", "Azure Data Lake Storage", "Event Hubs"],
        "outputs_to": ["Power BI", "Azure Machine Learning", "Azure Databricks", "Azure Functions"],
        "architectural_pattern": "modern_data_platform",
        "dependency_score": 8,
        "integration_complexity": "high"
    },
    "Power BI": {
        "works_well_with": ["Azure Synapse Analytics", "Azure Data Factory", "Azure SQL Database", "Azure Analysis Services"],
        "data_sources": ["Azure Synapse Analytics", "Azure SQL Database", "Cosmos DB", "Excel", "SharePoint"],
        "outputs_to": ["SharePoint", "Teams", "Power Apps", "Office 365"],
        "architectural_pattern": "analytics_platform",
        "dependency_score": 6,
        "integration_complexity": "medium"
    },
    "Azure Data Factory": {
        "works_well_with": ["Azure Synapse Analytics", "Azure Data Lake Storage", "Power BI", "Azure Databricks"],
        "data_sources": ["Multiple sources", "On-premises databases", "SaaS applications"],
        "outputs_to": ["Azure Data Lake Storage", "Azure Synapse Analytics", "Azure SQL Database"],
        "architectural_pattern": "modern_data_platform",
        "dependency_score": 9,
        "integration_complexity": "medium"
    },
    "Azure Kubernetes Service (AKS)": {
        "works_well_with": ["Azure Container Registry", "Azure Monitor", "Application Gateway", "Key Vault", "Azure DevOps"],
        "dependencies": ["Virtual Network", "Azure Active Directory", "Azure Container Registry"],
        "outputs_to": ["Load Balancer", "Application Gateway", "Azure Monitor"],
        "architectural_pattern": "microservices_platform",
        "dependency_score": 7,
        "integration_complexity": "high"
    },
    "Azure Machine Learning": {
        "works_well_with": ["Azure Databricks", "Azure Synapse Analytics", "Azure Data Factory", "Azure Container Registry"],
        "data_sources": ["Azure Data Lake Storage", "Blob Storage", "Azure SQL Database", "Cosmos DB"],
        "outputs_to": ["Azure Container Instances", "AKS", "Azure Functions", "Power BI"],
        "architectural_pattern": "ml_platform",
        "dependency_score": 8,
        "integration_complexity": "high"
    },
    "Azure IoT Hub": {
        "works_well_with": ["Azure Stream Analytics", "Event Grid", "Azure Functions", "Power BI"],
        "data_sources": ["IoT devices", "sensors", "gateways"],
        "outputs_to": ["Azure Stream Analytics", "Event Hubs", "Azure Functions", "Storage"],
        "architectural_pattern": "iot_platform",
        "dependency_score": 8,
        "integration_complexity": "medium"
    },
    "Azure Functions": {
        "works_well_with": ["Logic Apps", "Event Grid", "Cosmos DB", "API Management", "Key Vault"],
        "triggers": ["HTTP", "Event Grid", "Service Bus", "Timer", "Blob Storage"],
        "outputs_to": ["Cosmos DB", "SQL Database", "Service Bus", "Event Grid"],
        "architectural_pattern": "serverless_web_app",
        "dependency_score": 5,
        "integration_complexity": "low"
    }
}

def extract_comprehensive_features(use_case: str, capabilities: Dict, industry: str = None, solution_type: str = None) -> set:
    """Enhanced feature extraction with semantic analysis and domain knowledge"""
    features = set()
    
    # Add selected capabilities
    for cap, selected in capabilities.items():
        if selected:
            features.add(cap.lower().replace(" ", "_"))
    
    # Industry-specific features
    if industry and industry in ENHANCED_INDUSTRY_TEMPLATES:
        template = ENHANCED_INDUSTRY_TEMPLATES[industry]
        features.update([svc.lower().replace(" ", "_") for svc in template["required_services"]])
        features.add(f"compliance_{industry}")
        
        # Add industry-specific patterns
        for pattern in template.get("specific_patterns", []):
            features.add(f"pattern_{pattern}")
    
    # Solution type features
    if solution_type:
        features.add(f"solution_{solution_type.lower()}")
    
    # Advanced keyword extraction with semantic understanding
    use_case_lower = use_case.lower()
    
    # Enhanced technical patterns with broader coverage
    enhanced_patterns = {
        # Data & Analytics
        "data_warehouse": ["warehouse", "dwh", "dimensional", "olap", "analytics", "reporting", "etl"],
        "data_lake": ["data lake", "big data", "hadoop", "parquet", "delta", "raw data"],
        "real_time": ["real-time", "realtime", "streaming", "live", "instant", "event", "continuous"],
        "batch_processing": ["batch", "scheduled", "overnight", "bulk", "etl", "data processing"],
        
        # AI & ML
        "machine_learning": ["ml", "ai", "prediction", "model", "algorithm", "training", "inference"],
        "nlp": ["natural language", "text processing", "sentiment", "chatbot", "language"],
        "computer_vision": ["image", "vision", "ocr", "object detection", "facial recognition"],
        "generative_ai": ["gpt", "openai", "generative", "content generation", "llm"],
        
        # Architecture Patterns
        "microservices": ["microservice", "micro-service", "service-oriented", "distributed", "containers"],
        "serverless": ["serverless", "event-driven", "lambda", "function", "faas"],
        "monolithic": ["monolith", "single application", "traditional", "legacy"],
        
        # Technology Domains
        "iot": ["iot", "sensor", "device", "telemetry", "industrial", "smart", "connected"],
        "web_app": ["web", "website", "portal", "frontend", "ui", "spa", "progressive web"],
        "mobile": ["mobile", "ios", "android", "app", "responsive", "xamarin"],
        "api": ["api", "rest", "graphql", "endpoint", "integration", "service"],
        
        # Data Storage
        "database": ["database", "db", "sql", "nosql", "data storage", "persistence"],
        "relational": ["sql", "relational", "acid", "transactions", "normalized"],
        "nosql": ["nosql", "document", "key-value", "graph", "mongodb", "cassandra"],
        "caching": ["cache", "redis", "memory", "session", "performance"],
        
        # Integration & Communication
        "messaging": ["queue", "message", "pub/sub", "event", "notification", "async"],
        "workflow": ["workflow", "orchestration", "process", "automation", "business process"],
        "api_management": ["api gateway", "rate limiting", "authentication", "developer portal"],
        
        # Security & Compliance
        "security": ["security", "authentication", "authorization", "identity", "encryption"],
        "compliance": ["compliance", "regulation", "audit", "governance", "policy"],
        "identity": ["sso", "active directory", "oauth", "saml", "identity provider"],
        
        # Operations & Management
        "monitoring": ["monitoring", "logging", "observability", "metrics", "alerting"],
        "devops": ["ci/cd", "pipeline", "deployment", "automation", "git"],
        "backup": ["backup", "disaster recovery", "dr", "resilience", "availability"],
        
        # Scale & Performance
        "high_availability": ["ha", "availability", "uptime", "redundancy", "failover"],
        "scalability": ["scale", "elastic", "auto-scale", "performance", "load"],
        "global": ["global", "worldwide", "multi-region", "geo-distributed", "cdn"],
        
        # Industry Specific
        "healthcare": ["medical", "patient", "fhir", "healthcare", "clinical"],
        "financial": ["banking", "payment", "trading", "fintech", "financial"],
        "retail": ["e-commerce", "shopping", "inventory", "pos", "customer"],
        "manufacturing": ["production", "factory", "industrial", "supply chain"],
        "education": ["learning", "student", "course", "academic", "educational"]
    }
    
    # Apply pattern matching with scoring
    pattern_scores = {}
    for feature, keywords in enhanced_patterns.items():
        score = sum(1 for keyword in keywords if keyword in use_case_lower)
        if score > 0:
            features.add(feature)
            pattern_scores[feature] = score
    
    # Add contextual features based on strong patterns
    if pattern_scores.get("data_warehouse", 0) > 0 or pattern_scores.get("analytics", 0) > 0:
        features.update(["data_lake", "etl", "business_intelligence"])
    
    if pattern_scores.get("machine_learning", 0) > 0:
        features.update(["data_science", "model_deployment", "analytics"])
    
    if pattern_scores.get("iot", 0) > 0:
        features.update(["real_time", "telemetry", "analytics"])
    
    if pattern_scores.get("microservices", 0) > 0:
        features.update(["containers", "api", "monitoring"])
    
    return features

def calculate_solution_architecture_score(service: Dict, features: set, architecture_context: Dict, industry: str = None) -> Tuple[int, Dict]:
    """Advanced scoring algorithm focusing on complete solution architecture"""
    score_breakdown = {
        "functional_match": 0,
        "pattern_completion": 0,
        "integration_synergy": 0,
        "architectural_tier": 0,
        "industry_alignment": 0,
        "compliance_bonus": 0,
        "data_flow_bonus": 0,
        "operational_completeness": 0
    }
    
    service_name = service["name"].lower()
    service_category = service.get("category", "").lower()
    service_use_cases = service.get("use_cases", [])
    service_tier = service.get("architectural_tier", "application")
    
    # 1. Functional matching (base score)
    for feature in features:
        if feature in service_name or feature in service_category:
            score_breakdown["functional_match"] += 4
        elif any(feature in use_case for use_case in service_use_cases):
            score_breakdown["functional_match"] += 3
    
    # 2. Architecture pattern completion bonus
    selected_services = architecture_context.get("selected_services", [])
    for pattern_name, pattern in ENHANCED_ARCHITECTURE_PATTERNS.items():
        if any(f"pattern_{pattern_name}" in features for features in [features]):
            if service["name"] in pattern["required"]:
                score_breakdown["pattern_completion"] += 8
            elif service["name"] in pattern["recommended"]:
                score_breakdown["pattern_completion"] += 5
            elif service["name"] in pattern["optional"]:
                score_breakdown["pattern_completion"] += 2
            
            # Bonus for completing patterns
            required_in_selection = sum(1 for svc in pattern["required"] if svc in selected_services)
            total_required = len(pattern["required"])
            if required_in_selection >= total_required * 0.7:  # 70% completion
                score_breakdown["pattern_completion"] += 3
    
    # 3. Integration synergy (enhanced)
    if service["name"] in ENHANCED_SERVICE_RELATIONSHIPS:
        relationships = ENHANCED_SERVICE_RELATIONSHIPS[service["name"]]
        
        for selected in selected_services:
            if selected in relationships.get("works_well_with", []):
                score_breakdown["integration_synergy"] += 4
            elif selected in relationships.get("data_sources", []) or selected in relationships.get("outputs_to", []):
                score_breakdown["integration_synergy"] += 3
        
        # Dependency bonus
        dependency_score = relationships.get("dependency_score", 5)
        score_breakdown["integration_synergy"] += min(dependency_score, 5)
    
    # 4. Architectural tier prioritization
    tier_priorities = {
        "security": 10,      # Always high priority
        "management": 8,     # Monitoring, governance
        "integration": 7,    # Data flow, events
        "data": 6,          # Storage, databases
        "analytics": 6,     # Processing, insights
        "compute": 5,       # VMs, containers
        "application": 5,   # App services
        "network": 4,       # Infrastructure
        "presentation": 3   # UI, dashboards
    }
    
    base_tier_score = tier_priorities.get(service_tier, 3)
    
    # Adjust based on solution needs
    if "analytics" in features or "business_intelligence" in features:
        if service_tier in ["analytics", "data", "presentation"]:
            base_tier_score += 3
    
    if "security" in features or "compliance" in features:
        if service_tier == "security":
            base_tier_score += 5
    
    if "iot" in features:
        if service_tier in ["application", "integration", "analytics"]:
            base_tier_score += 3
    
    score_breakdown["architectural_tier"] = base_tier_score
    
    # 5. Industry alignment
    if industry and industry in ENHANCED_INDUSTRY_TEMPLATES:
        template = ENHANCED_INDUSTRY_TEMPLATES[industry]
        
        if service["name"] in template["required_services"]:
            score_breakdown["industry_alignment"] += 6
        elif service["name"] in template["recommended_services"]:
            score_breakdown["industry_alignment"] += 4
        
        # Category boost
        category_boost = template.get("scoring_boost", {}).get(service["category"], 0)
        score_
