import streamlit as st
import requests
import pandas as pd
import json
from typing import Dict, List, Any, Tuple
import re

st.set_page_config(page_title="Azure Solution Recommender Pro", layout="wide", page_icon="☁️")

# Comprehensive Azure Service Catalog
@st.cache_data(ttl=3600)
def fetch_azure_services():
    """Comprehensive Azure service catalog with enhanced metadata"""
    return [
        # Analytics & BI
        {"name": "Azure Synapse Analytics", "category": "Analytics", "cost_tier": "high", "use_cases": ["data_warehouse", "analytics", "big_data"], "integrates_with": ["Power BI", "Azure Data Lake Storage", "Azure Machine Learning"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/synapse-analytics/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/synapse-analytics/"},
        {"name": "Power BI", "category": "Analytics", "cost_tier": "medium", "use_cases": ["visualization", "dashboards", "business_intelligence"], "integrates_with": ["Azure Synapse Analytics", "Azure Data Factory", "Office 365"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/power-bi/", "pricing": "https://powerbi.microsoft.com/en-us/pricing/"},
        {"name": "Azure Data Factory", "category": "Analytics", "cost_tier": "medium", "use_cases": ["etl", "data_integration", "pipeline"], "integrates_with": ["Azure Synapse Analytics", "Azure Data Lake Storage", "Azure SQL Database"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/data-factory/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/data-factory/"},
        {"name": "Azure Databricks", "category": "Analytics", "cost_tier": "high", "use_cases": ["machine_learning", "analytics", "spark"], "integrates_with": ["Azure Machine Learning", "Azure Data Lake Storage", "Power BI"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/databricks/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/databricks/"},
        {"name": "Azure Stream Analytics", "category": "Analytics", "cost_tier": "medium", "use_cases": ["real_time", "streaming", "iot"], "integrates_with": ["Event Hubs", "IoT Hub", "Power BI"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/stream-analytics/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/stream-analytics/"},
        {"name": "Azure Analysis Services", "category": "Analytics", "cost_tier": "medium", "use_cases": ["olap", "tabular_models", "business_intelligence"], "integrates_with": ["Power BI", "Excel", "Azure SQL Database"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/analysis-services/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/analysis-services/"},
        {"name": "Microsoft Purview", "category": "Analytics", "cost_tier": "medium", "use_cases": ["data_governance", "data_catalog", "compliance"], "integrates_with": ["Azure Synapse Analytics", "Azure Data Factory", "Power BI"], "compliance": ["SOC", "HIPAA", "ISO", "GDPR"], "docs": "https://learn.microsoft.com/en-us/purview/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-purview/"},
        
        # AI & ML
        {"name": "Azure Machine Learning", "category": "AI + ML", "cost_tier": "high", "use_cases": ["machine_learning", "model_training", "mlops"], "integrates_with": ["Azure Databricks", "Azure Synapse Analytics", "Azure Container Instances"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/machine-learning/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/machine-learning/"},
        {"name": "Azure Cognitive Services", "category": "AI + ML", "cost_tier": "medium", "use_cases": ["ai", "computer_vision", "nlp", "speech"], "integrates_with": ["Azure Bot Service", "Azure Functions", "Logic Apps"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/cognitive-services/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/"},
        {"name": "Azure OpenAI Service", "category": "AI + ML", "cost_tier": "high", "use_cases": ["generative_ai", "chatbot", "content_generation"], "integrates_with": ["Azure Cognitive Services", "Azure Bot Service", "Azure Functions"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/ai-services/openai/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/"},
        {"name": "Azure Bot Service", "category": "AI + ML", "cost_tier": "low", "use_cases": ["chatbot", "conversational_ai", "customer_service"], "integrates_with": ["Azure Cognitive Services", "Azure OpenAI Service", "Teams"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/bot-service/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/bot-service/"},
        {"name": "Azure Form Recognizer", "category": "AI + ML", "cost_tier": "medium", "use_cases": ["document_processing", "ocr", "form_extraction"], "integrates_with": ["Azure Cognitive Services", "Logic Apps", "Power Automate"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/ai-services/form-recognizer/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/form-recognizer/"},
        {"name": "Azure Computer Vision", "category": "AI + ML", "cost_tier": "medium", "use_cases": ["image_processing", "ocr", "object_detection"], "integrates_with": ["Azure Cognitive Services", "Azure Functions", "Logic Apps"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/computer-vision/"},
        
        # Compute
        {"name": "Azure Virtual Machines", "category": "Compute", "cost_tier": "variable", "use_cases": ["windows", "linux", "legacy_apps", "custom_software"], "integrates_with": ["Virtual Network", "Load Balancer", "Azure Monitor"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/virtual-machines/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/"},
        {"name": "Azure Functions", "category": "Compute", "cost_tier": "low", "use_cases": ["serverless", "microservices", "event_driven", "api"], "integrates_with": ["Logic Apps", "Event Grid", "Cosmos DB"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-functions/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/functions/"},
        {"name": "Azure Batch", "category": "Compute", "cost_tier": "medium", "use_cases": ["batch_processing", "hpc", "parallel_workloads"], "integrates_with": ["Azure Storage", "Virtual Networks", "Azure Monitor"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/batch/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/batch/"},
        {"name": "Azure Service Fabric", "category": "Compute", "cost_tier": "medium", "use_cases": ["microservices", "distributed_systems", "stateful_services"], "integrates_with": ["Azure Monitor", "Key Vault", "Load Balancer"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/service-fabric/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/service-fabric/"},
        
        # Containers
        {"name": "Azure Kubernetes Service (AKS)", "category": "Containers", "cost_tier": "medium", "use_cases": ["kubernetes", "microservices", "container_orchestration"], "integrates_with": ["Azure Container Registry", "Azure Monitor", "Azure Active Directory"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/aks/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/"},
        {"name": "Azure Container Apps", "category": "Containers", "cost_tier": "low", "use_cases": ["serverless_containers", "microservices", "event_driven"], "integrates_with": ["Event Grid", "Service Bus", "Azure Monitor"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/container-apps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-apps/"},
        {"name": "Azure Container Instances", "category": "Containers", "cost_tier": "low", "use_cases": ["simple_containers", "batch_jobs", "dev_test"], "integrates_with": ["Virtual Network", "Azure Files", "Azure Monitor"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/container-instances/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-instances/"},
        {"name": "Azure Container Registry", "category": "Containers", "cost_tier": "low", "use_cases": ["container_images", "docker_registry", "devops"], "integrates_with": ["AKS", "Container Apps", "Azure DevOps"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/container-registry/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/container-registry/"},
        
        # Databases
        {"name": "Azure SQL Database", "category": "Databases", "cost_tier": "medium", "use_cases": ["relational_database", "sql_server", "managed_database"], "integrates_with": ["Power BI", "Azure Data Factory", "Azure Functions"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/azure-sql/database/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-sql-database/"},
        {"name": "Azure Cosmos DB", "category": "Databases", "cost_tier": "medium", "use_cases": ["nosql", "global_distribution", "multi_model"], "integrates_with": ["Azure Functions", "Azure Synapse Analytics", "Power BI"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/cosmos-db/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cosmos-db/"},
        {"name": "Azure Database for PostgreSQL", "category": "Databases", "cost_tier": "medium", "use_cases": ["postgresql", "open_source", "managed_database"], "integrates_with": ["Azure Data Factory", "Power BI", "Azure Monitor"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/postgresql/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/postgresql/"},
        {"name": "Azure Database for MySQL", "category": "Databases", "cost_tier": "medium", "use_cases": ["mysql", "open_source", "managed_database"], "integrates_with": ["Azure Data Factory", "Power BI", "Azure Monitor"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/mysql/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/mysql/"},
        {"name": "Azure Cache for Redis", "category": "Databases", "cost_tier": "low", "use_cases": ["caching", "session_storage", "real_time"], "integrates_with": ["Azure Functions", "App Service", "AKS"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cache/"},
        
        # Storage
        {"name": "Azure Blob Storage", "category": "Storage", "cost_tier": "low", "use_cases": ["object_storage", "backup", "archival", "static_content"], "integrates_with": ["Azure CDN", "Azure Data Factory", "Power BI"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/storage/blobs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/blobs/"},
        {"name": "Azure Data Lake Storage", "category": "Storage", "cost_tier": "medium", "use_cases": ["big_data", "analytics", "data_lake"], "integrates_with": ["Azure Synapse Analytics", "Azure Databricks", "Power BI"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/data-lake/"},
        {"name": "Azure Files", "category": "Storage", "cost_tier": "low", "use_cases": ["file_shares", "smb", "nfs"], "integrates_with": ["Virtual Machines", "Container Instances", "AKS"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/storage/files/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/storage/files/"},
        {"name": "Azure NetApp Files", "category": "Storage", "cost_tier": "high", "use_cases": ["enterprise_nas", "hpc", "high_performance"], "integrates_with": ["Virtual Machines", "AKS", "Azure VMware Solution"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-netapp-files/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/netapp/"},
        
        # Networking
        {"name": "Azure Virtual Network", "category": "Networking", "cost_tier": "low", "use_cases": ["network_isolation", "hybrid_connectivity", "security"], "integrates_with": ["Virtual Machines", "AKS", "Application Gateway"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/virtual-network/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/virtual-network/"},
        {"name": "Azure Application Gateway", "category": "Networking", "cost_tier": "medium", "use_cases": ["load_balancer", "ssl_termination", "waf"], "integrates_with": ["Virtual Network", "AKS", "App Service"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/application-gateway/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/application-gateway/"},
        {"name": "Azure Load Balancer", "category": "Networking", "cost_tier": "low", "use_cases": ["load_balancing", "high_availability", "traffic_distribution"], "integrates_with": ["Virtual Machines", "Virtual Network", "AKS"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/load-balancer/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/load-balancer/"},
        {"name": "Azure Front Door", "category": "Networking", "cost_tier": "medium", "use_cases": ["global_load_balancer", "cdn", "waf"], "integrates_with": ["App Service", "Application Gateway", "Blob Storage"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/frontdoor/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/frontdoor/"},
        {"name": "Azure ExpressRoute", "category": "Networking", "cost_tier": "high", "use_cases": ["hybrid_connectivity", "private_connection", "enterprise"], "integrates_with": ["Virtual Network", "Virtual WAN", "Azure Monitor"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/expressroute/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/expressroute/"},
        {"name": "Azure VPN Gateway", "category": "Networking", "cost_tier": "low", "use_cases": ["vpn", "site_to_site", "point_to_site"], "integrates_with": ["Virtual Network", "Azure Monitor", "Network Watcher"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/vpn-gateway/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/vpn-gateway/"},
        
        # Security
        {"name": "Azure Key Vault", "category": "Security", "cost_tier": "low", "use_cases": ["secrets_management", "encryption", "certificates"], "integrates_with": ["App Service", "Azure Functions", "Virtual Machines"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/key-vault/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/key-vault/"},
        {"name": "Microsoft Defender for Cloud", "category": "Security", "cost_tier": "medium", "use_cases": ["security_monitoring", "threat_detection", "compliance"], "integrates_with": ["Azure Monitor", "Sentinel", "Logic Apps"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/defender-for-cloud/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/defender-for-cloud/"},
        {"name": "Microsoft Sentinel", "category": "Security", "cost_tier": "medium", "use_cases": ["siem", "soar", "security_analytics"], "integrates_with": ["Azure Monitor", "Logic Apps", "Defender for Cloud"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/sentinel/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/microsoft-sentinel/"},
        {"name": "Azure Active Directory", "category": "Security", "cost_tier": "variable", "use_cases": ["identity", "authentication", "authorization"], "integrates_with": ["All Azure Services", "Office 365", "Third-party apps"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/active-directory/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/active-directory/"},
        {"name": "Azure Firewall", "category": "Security", "cost_tier": "medium", "use_cases": ["network_firewall", "traffic_filtering", "security"], "integrates_with": ["Virtual Network", "Azure Monitor", "Sentinel"], "compliance": ["SOC", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/firewall/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-firewall/"},
        {"name": "Azure DDoS Protection", "category": "Security", "cost_tier": "medium", "use_cases": ["ddos_protection", "network_security", "availability"], "integrates_with": ["Virtual Network", "Application Gateway", "Azure Monitor"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/ddos-protection/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/ddos-protection/"},
        
        # Web & Mobile
        {"name": "Azure App Service", "category": "Web", "cost_tier": "medium", "use_cases": ["web_apps", "api", "mobile_backend"], "integrates_with": ["Azure SQL Database", "Key Vault", "Application Insights"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/app-service/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/app-service/"},
        {"name": "Azure Static Web Apps", "category": "Web", "cost_tier": "low", "use_cases": ["static_sites", "jamstack", "frontend"], "integrates_with": ["GitHub", "Azure DevOps", "Azure Functions"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/static-web-apps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/app-service/static/"},
        {"name": "Azure CDN", "category": "Web", "cost_tier": "low", "use_cases": ["content_delivery", "performance", "global_distribution"], "integrates_with": ["Blob Storage", "App Service", "Front Door"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/cdn/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/cdn/"},
        
        # Integration
        {"name": "Azure Logic Apps", "category": "Integration", "cost_tier": "low", "use_cases": ["workflow", "integration", "automation"], "integrates_with": ["Office 365", "Dynamics 365", "SAP"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/logic-apps/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/logic-apps/"},
        {"name": "Azure Event Grid", "category": "Integration", "cost_tier": "low", "use_cases": ["event_routing", "reactive_programming", "serverless"], "integrates_with": ["Azure Functions", "Logic Apps", "Event Hubs"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/event-grid/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/event-grid/"},
        {"name": "Azure Service Bus", "category": "Integration", "cost_tier": "low", "use_cases": ["messaging", "queues", "pub_sub"], "integrates_with": ["Azure Functions", "Logic Apps", "Service Fabric"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/service-bus-messaging/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/service-bus/"},
        {"name": "Azure API Management", "category": "Integration", "cost_tier": "medium", "use_cases": ["api_gateway", "api_management", "developer_portal"], "integrates_with": ["App Service", "Azure Functions", "Logic Apps"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/api-management/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/api-management/"},
        {"name": "Azure Event Hubs", "category": "Integration", "cost_tier": "medium", "use_cases": ["big_data_streaming", "telemetry", "event_ingestion"], "integrates_with": ["Stream Analytics", "Azure Functions", "Databricks"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/event-hubs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/event-hubs/"},
        
        # IoT
        {"name": "Azure IoT Hub", "category": "IoT", "cost_tier": "medium", "use_cases": ["iot_connectivity", "device_management", "telemetry"], "integrates_with": ["Stream Analytics", "Event Grid", "Time Series Insights"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/iot-hub/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/iot-hub/"},
        {"name": "Azure IoT Central", "category": "IoT", "cost_tier": "low", "use_cases": ["iot_saas", "device_templates", "no_code_iot"], "integrates_with": ["Power BI", "Logic Apps", "Event Grid"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/iot-central/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/iot-central/"},
        {"name": "Azure Digital Twins", "category": "IoT", "cost_tier": "medium", "use_cases": ["digital_twins", "iot_modeling", "spatial_intelligence"], "integrates_with": ["IoT Hub", "Time Series Insights", "Azure Maps"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/digital-twins/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/digital-twins/"},
        {"name": "Azure Time Series Insights", "category": "IoT", "cost_tier": "medium", "use_cases": ["time_series", "iot_analytics", "operational_intelligence"], "integrates_with": ["IoT Hub", "Event Hubs", "Power BI"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/time-series-insights/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/time-series-insights/"},
        
        # DevOps
        {"name": "Azure DevOps", "category": "DevOps", "cost_tier": "low", "use_cases": ["ci_cd", "project_management", "source_control"], "integrates_with": ["GitHub", "Azure Container Registry", "AKS"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/devops/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/"},
        {"name": "GitHub Actions", "category": "DevOps", "cost_tier": "low", "use_cases": ["ci_cd", "automation", "workflows"], "integrates_with": ["Azure Container Registry", "AKS", "App Service"], "compliance": ["SOC", "ISO"], "docs": "https://docs.github.com/en/actions", "pricing": "https://github.com/pricing"},
        {"name": "Azure Artifacts", "category": "DevOps", "cost_tier": "low", "use_cases": ["package_management", "npm", "nuget", "maven"], "integrates_with": ["Azure DevOps", "Visual Studio", "Azure Pipelines"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/devops/artifacts/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/"},
        
        # Monitoring
        {"name": "Azure Monitor", "category": "Monitoring", "cost_tier": "medium", "use_cases": ["monitoring", "logging", "metrics"], "integrates_with": ["All Azure Services", "Application Insights", "Log Analytics"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/azure-monitor/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/monitor/"},
        {"name": "Application Insights", "category": "Monitoring", "cost_tier": "low", "use_cases": ["apm", "performance_monitoring", "diagnostics"], "integrates_with": ["App Service", "Azure Functions", "AKS"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/monitor/"},
        {"name": "Azure Log Analytics", "category": "Monitoring", "cost_tier": "medium", "use_cases": ["log_analysis", "queries", "dashboards"], "integrates_with": ["Azure Monitor", "Sentinel", "Defender for Cloud"], "compliance": ["SOC", "HIPAA", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/monitor/"},
        
        # Management
        {"name": "Azure Resource Manager", "category": "Management", "cost_tier": "free", "use_cases": ["resource_management", "templates", "deployment"], "integrates_with": ["All Azure Services", "Azure DevOps", "Terraform"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/resource-manager/"},
        {"name": "Azure Policy", "category": "Management", "cost_tier": "free", "use_cases": ["governance", "compliance", "resource_policies"], "integrates_with": ["Azure Monitor", "Resource Manager", "Blueprints"], "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "docs": "https://learn.microsoft.com/en-us/azure/governance/policy/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/azure-policy/"},
        {"name": "Azure Automation", "category": "Management", "cost_tier": "low", "use_cases": ["automation", "configuration_management", "update_management"], "integrates_with": ["Azure Monitor", "Log Analytics", "Virtual Machines"], "compliance": ["SOC", "ISO"], "docs": "https://learn.microsoft.com/en-us/azure/automation/", "pricing": "https://azure.microsoft.com/en-us/pricing/details/automation/"},
    ]

# Enhanced Service Metadata
SERVICE_RELATIONSHIPS = {
    "Azure Synapse Analytics": {
        "works_well_with": ["Power BI", "Azure Data Lake Storage", "Azure Data Factory", "Azure Machine Learning"],
        "data_sources": ["Azure SQL Database", "Cosmos DB", "Blob Storage", "Azure Data Lake Storage"],
        "outputs_to": ["Power BI", "Azure Machine Learning", "Azure Databricks"],
        "architectural_pattern": "modern_data_platform"
    },
    "Power BI": {
        "works_well_with": ["Azure Synapse Analytics", "Azure Data Factory", "Azure SQL Database"],
        "data_sources": ["Azure Synapse Analytics", "Azure SQL Database", "Cosmos DB", "Excel"],
        "outputs_to": ["SharePoint", "Teams", "Power Apps"],
        "architectural_pattern": "business_intelligence"
    },
    "Azure Kubernetes Service (AKS)": {
        "works_well_with": ["Azure Container Registry", "Azure Monitor", "Application Gateway", "Key Vault"],
        "dependencies": ["Virtual Network", "Azure Active Directory"],
        "outputs_to": ["Load Balancer", "Application Gateway"],
        "architectural_pattern": "microservices"
    },
    "Azure Machine Learning": {
        "works_well_with": ["Azure Databricks", "Azure Synapse Analytics", "Azure Data Factory"],
        "data_sources": ["Azure Data Lake Storage", "Blob Storage", "Azure SQL Database"],
        "outputs_to": ["Azure Container Instances", "AKS", "Azure Functions"],
        "architectural_pattern": "ml_platform"
    }
}

# Architecture Patterns
ARCHITECTURE_PATTERNS = {
    "modern_data_platform": {
        "name": "Modern Data Platform",
        "required": ["Azure Data Factory", "Azure Data Lake Storage", "Azure Synapse Analytics"],
        "recommended": ["Power BI", "Azure Machine Learning", "Microsoft Purview"],
        "optional": ["Azure Databricks", "Azure Stream Analytics"],
        "description": "Complete modern data platform for analytics, ML, and business intelligence",
        "use_cases": ["data_warehouse", "analytics", "business_intelligence", "machine_learning"]
    },
    "serverless_web_app": {
        "name": "Serverless Web Application",
        "required": ["Azure Functions", "Azure Cosmos DB", "Azure Static Web Apps"],
        "recommended": ["Azure CDN", "Application Insights", "Key Vault"],
        "optional": ["Azure API Management", "Azure Active Directory"],
        "description": "Scalable serverless web application with global distribution",
        "use_cases": ["web_app", "api", "serverless", "global_distribution"]
    },
    "microservices_platform": {
        "name": "Microservices Platform",
        "required": ["Azure Kubernetes Service (AKS)", "Azure Container Registry", "Virtual Network"],
        "recommended": ["Application Gateway", "Azure Monitor", "Key Vault"],
        "optional": ["Service Bus", "Azure Cache for Redis", "Azure API Management"],
        "description": "Enterprise-grade microservices platform with container orchestration",
        "use_cases": ["microservices", "containers", "scalability", "enterprise"]
    },
    "ml_platform": {
        "name": "Machine Learning Platform",
        "required": ["Azure Machine Learning", "Azure Data Lake Storage", "Azure Databricks"],
        "recommended": ["Azure Data Factory", "Azure Synapse Analytics", "Azure Container Registry"],
        "optional": ["Azure Cognitive Services", "Power BI", "Azure Functions"],
        "description": "End-to-end machine learning platform for model development and deployment",
        "use_cases": ["machine_learning", "ai", "data_science", "model_deployment"]
    },
    "iot_platform": {
        "name": "IoT Analytics Platform",
        "required": ["Azure IoT Hub", "Azure Stream Analytics", "Azure Data Lake Storage"],
        "recommended": ["Power BI", "Azure Functions", "Event Grid"],
        "optional": ["Azure Digital Twins", "Time Series Insights", "Azure Machine Learning"],
        "description": "Comprehensive IoT platform for device management and real-time analytics",
        "use_cases": ["iot", "real_time", "telemetry", "device_management"]
    }
}

# Industry Templates
INDUSTRY_TEMPLATES = {
    "healthcare": {
        "name": "Healthcare & Life Sciences",
        "compliance_requirements": ["HIPAA", "HITECH", "FDA"],
        "required_services": ["Key Vault", "Microsoft Defender for Cloud", "Azure Monitor"],
        "recommended_services": ["Azure API for FHIR", "Confidential Computing", "Private Link"],
        "data_governance": "strict",
        "encryption": "required"
    },
    "financial": {
        "name": "Financial Services",
        "compliance_requirements": ["PCI DSS", "SOX", "GDPR"],
        "required_services": ["Key Vault", "Azure Firewall", "DDoS Protection"],
        "recommended_services": ["Azure Confidential Computing", "Private Link", "Sentinel"],
        "data_governance": "strict",
        "encryption": "required"
    },
    "government": {
        "name": "Government",
        "compliance_requirements": ["FedRAMP", "FISMA", "ITAR"],
        "required_services": ["Azure Government", "Key Vault", "Azure Monitor"],
        "recommended_services": ["Azure Firewall", "DDoS Protection", "Sentinel"],
        "data_governance": "strict",
        "encryption": "required"
    },
    "retail": {
        "name": "Retail & E-commerce",
        "compliance_requirements": ["PCI DSS", "GDPR"],
        "required_services": ["Azure CDN", "Application Gateway", "Key Vault"],
        "recommended_services": ["Azure Cache for Redis", "Cosmos DB", "Cognitive Services"],
        "data_governance": "moderate",
        "encryption": "recommended"
    },
    "manufacturing": {
        "name": "Manufacturing",
        "compliance_requirements": ["ISO 27001", "SOC 2"],
        "required_services": ["IoT Hub", "Azure Monitor", "Key Vault"],
        "recommended_services": ["Digital Twins", "Stream Analytics", "Machine Learning"],
        "data_governance": "moderate",
        "encryption": "recommended"
    }
}

def extract_enhanced_features(use_case: str, capabilities: Dict, industry: str = None) -> set:
    """Extract features using advanced NLP and pattern matching"""
    features = set()
    
    # Add selected capabilities
    for cap, selected in capabilities.items():
        if selected:
            features.add(cap.lower().replace(" ", "_"))
    
    # Industry-specific features
    if industry and industry in INDUSTRY_TEMPLATES:
        template = INDUSTRY_TEMPLATES[industry]
        features.update([svc.lower().replace(" ", "_") for svc in template["required_services"]])
        features.add(f"compliance_{industry}")
    
    # Advanced keyword extraction
    use_case_lower = use_case.lower()
    
    # Technical patterns
    patterns = {
        "data_warehouse": ["warehouse", "dwh", "dimensional", "olap", "analytics"],
        "real_time": ["real-time", "realtime", "streaming", "live", "instant"],
        "machine_learning": ["ml", "ai", "prediction", "model", "algorithm"],
        "microservices": ["microservice", "micro-service", "service-oriented", "distributed"],
        "serverless": ["serverless", "event-driven", "lambda", "function"],
        "iot": ["iot", "sensor", "device", "telemetry", "industrial"],
        "web_app": ["web", "website", "portal", "frontend", "ui"],
        "mobile": ["mobile", "ios", "android", "app", "responsive"],
        "api": ["api", "rest", "graphql", "endpoint", "integration"],
        "database": ["database", "db", "sql", "nosql", "data storage"],
        "caching": ["cache", "redis", "memory", "session"],
        "messaging": ["queue", "message", "pub/sub", "event", "notification"],
        "security": ["security", "authentication", "authorization", "identity"],
        "monitoring": ["monitoring", "logging", "observability", "metrics"],
        "backup": ["backup", "disaster recovery", "dr", "resilience"],
        "global": ["global", "worldwide", "multi-region", "geo-distributed"]
    }
    
    for feature, keywords in patterns.items():
        if any(keyword in use_case_lower for keyword in keywords):
            features.add(feature)
    
    return features

def calculate_advanced_score(service: Dict, features: set, architecture_context: Dict, industry: str = None) -> Tuple[int, Dict]:
    """Advanced scoring algorithm with detailed breakdown"""
    score_breakdown = {
        "functional_match": 0,
        "integration_bonus": 0,
        "pattern_bonus": 0,
        "compliance_bonus": 0,
        "cost_optimization": 0,
        "industry_bonus": 0
    }
    
    # Base functional matching
    service_name = service["name"].lower()
    service_category = service.get("category", "").lower()
    service_use_cases = service.get("use_cases", [])
    
    for feature in features:
        if feature in service_name or feature in service_category:
            score_breakdown["functional_match"] += 3
        
        if any(feature in use_case for use_case in service_use_cases):
            score_breakdown["functional_match"] += 2
    
    # Integration synergy bonus
    if service["name"] in SERVICE_RELATIONSHIPS:
        relationships = SERVICE_RELATIONSHIPS[service["name"]]
        selected_services = architecture_context.get("selected_services", [])
        
        for selected in selected_services:
            if selected in relationships.get("works_well_with", []):
                score_breakdown["integration_bonus"] += 3
            elif selected in relationships.get("data_sources", []) or selected in relationships.get("outputs_to", []):
                score_breakdown["integration_bonus"] += 2
    
    # Architecture pattern bonus
    for pattern_name, pattern in ARCHITECTURE_PATTERNS.items():
        if any(keyword in features for keyword in pattern["use_cases"]):
            if service["name"] in pattern["required"]:
                score_breakdown["pattern_bonus"] += 5
            elif service["name"] in pattern["recommended"]:
                score_breakdown["pattern_bonus"] += 3
            elif service["name"] in pattern["optional"]:
                score_breakdown["pattern_bonus"] += 1
    
    # Compliance bonus
    if industry and industry in INDUSTRY_TEMPLATES:
        template = INDUSTRY_TEMPLATES[industry]
        if service["name"] in template["required_services"]:
            score_breakdown["compliance_bonus"] += 4
        elif service["name"] in template["recommended_services"]:
            score_breakdown["compliance_bonus"] += 2
        
        # Check service compliance features
        service_compliance = service.get("compliance", [])
        for req in template["compliance_requirements"]:
            if req in service_compliance:
                score_breakdown["compliance_bonus"] += 1
    
    # Cost optimization bonus
    cost_tier = service.get("cost_tier", "medium")
    if cost_tier == "low" or cost_tier == "free":
        score_breakdown["cost_optimization"] += 2
    elif cost_tier == "variable":
        score_breakdown["cost_optimization"] += 1
    
    # Industry-specific bonus
    if industry:
        industry_keywords = {
            "healthcare": ["health", "medical", "fhir", "patient"],
            "financial": ["financial", "banking", "payment", "fraud"],
            "government": ["government", "public", "citizen", "compliance"],
            "retail": ["retail", "commerce", "customer", "inventory"],
            "manufacturing": ["manufacturing", "industrial", "production", "iot"]
        }
        
        if industry in industry_keywords:
            for keyword in industry_keywords[industry]:
                if keyword in service_name or keyword in " ".join(service_use_cases):
                    score_breakdown["industry_bonus"] += 2
    
    total_score = sum(score_breakdown.values())
    return total_score, score_breakdown

def detect_architecture_patterns(selected_services: List[str]) -> List[Dict]:
    """Detect which architecture patterns are present"""
    detected_patterns = []
    
    for pattern_name, pattern in ARCHITECTURE_PATTERNS.items():
        required_coverage = sum(1 for svc in pattern["required"] if svc in selected_services)
        recommended_coverage = sum(1 for svc in pattern["recommended"] if svc in selected_services)
        optional_coverage = sum(1 for svc in pattern["optional"] if svc in selected_services)
        
        total_required = len(pattern["required"])
        total_recommended = len(pattern["recommended"])
        
        if required_coverage == total_required:
            completeness = "complete"
        elif required_coverage >= total_required * 0.7:
            completeness = "mostly_complete"
        elif required_coverage > 0:
            completeness = "partial"
        else:
            completeness = "not_detected"
        
        if completeness != "not_detected":
            detected_patterns.append({
                "name": pattern["name"],
                "completeness": completeness,
                "required_coverage": f"{required_coverage}/{total_required}",
                "recommended_coverage": f"{recommended_coverage}/{total_recommended}",
                "optional_coverage": optional_coverage,
                "missing_required": [svc for svc in pattern["required"] if svc not in selected_services],
                "missing_recommended": [svc for svc in pattern["recommended"] if svc not in selected_services]
            })
    
    return detected_patterns

def validate_architecture(selected_services: List[Dict], industry: str = None) -> Tuple[List[str], List[str]]:
    """Validate architecture for best practices and completeness"""
    warnings = []
    suggestions = []
    
    service_names = [svc["name"] for svc in selected_services]
    categories = set(svc["category"] for svc in selected_services)
    
    # Check for essential components
    if "Monitoring" not in categories and "Azure Monitor" not in service_names:
        warnings.append("No monitoring solution detected")
        suggestions.append("Add Azure Monitor and Application Insights for observability")
    
    if "Security" not in categories:
        warnings.append("No explicit security services")
        suggestions.append("Consider Azure Key Vault, Defender for Cloud, and proper identity management")
    
    # Check for backup and disaster recovery
    storage_services = [svc for svc in selected_services if svc["category"] == "Storage"]
    if storage_services and "backup" not in " ".join(svc.get("use_cases", []) for svc in selected_services):
        suggestions.append("Consider backup and disaster recovery strategy for your data")
    
    # Check for high availability
    if len(selected_services) > 3 and "load_balancer" not in " ".join(svc.get("use_cases", []) for svc in selected_services):
        suggestions.append("Consider load balancing for high availability")
    
    # Industry-specific validations
    if industry and industry in INDUSTRY_TEMPLATES:
        template = INDUSTRY_TEMPLATES[industry]
        missing_required = [svc for svc in template["required_services"] if svc not in service_names]
        if missing_required:
            warnings.append(f"Missing required services for {template['name']}: {', '.join(missing_required)}")
    
    # Check for proper network security
    if "Virtual Network" not in service_names and any("Compute" in svc["category"] or "Containers" in svc["category"] for svc in selected_services):
        suggestions.append("Consider using Azure Virtual Network for network isolation")
    
    return warnings, suggestions

def calculate_detailed_costs(selected_services: List[Dict], usage_estimates: Dict = None) -> Dict:
    """Calculate detailed cost estimates with scaling"""
    if usage_estimates is None:
        usage_estimates = {"users": 1000, "data_gb": 100, "compute_hours": 730}
    
    # Base monthly costs (simplified estimates)
    base_costs = {
        "low": 50,
        "medium": 200,
        "high": 800,
        "variable": 100,
        "free": 0
    }
    
    costs = {}
    total_monthly = 0
    
    for service in selected_services:
        cost_tier = service.get("cost_tier", "medium")
        base_cost = base_costs[cost_tier]
        
        # Apply scaling factors based on service type
        if "Database" in service["category"]:
            scaling_factor = max(1, usage_estimates["data_gb"] / 100)
        elif "Compute" in service["category"] or "Container" in service["category"]:
            scaling_factor = max(1, usage_estimates["compute_hours"] / 730)
        elif "Analytics" in service["category"]:
            scaling_factor = max(1, usage_estimates["data_gb"] / 50)
        else:
            scaling_factor = max(1, usage_estimates["users"] / 1000)
        
        monthly_cost = base_cost * scaling_factor
        annual_cost = monthly_cost * 12 * 0.85  # 15% annual discount
        
        costs[service["name"]] = {
            "monthly_estimate": monthly_cost,
            "annual_estimate": annual_cost,
            "cost_tier": cost_tier,
            "scaling_factor": scaling_factor
        }
        
        total_monthly += monthly_cost
    
    return {
        "services": costs,
        "total_monthly": total_monthly,
        "total_annual": total_monthly * 12 * 0.85,
        "cost_breakdown": {
            "low_cost": sum(cost["monthly_estimate"] for cost in costs.values() if cost["cost_tier"] == "low"),
            "medium_cost": sum(cost["monthly_estimate"] for cost in costs.values() if cost["cost_tier"] == "medium"),
            "high_cost": sum(cost["monthly_estimate"] for cost in costs.values() if cost["cost_tier"] == "high")
        }
    }

def get_enhanced_service_overview(service: Dict) -> Dict:
    """Get enhanced service overview with comprehensive details"""
    name = service["name"]
    category = service.get("category", "")
    use_cases = service.get("use_cases", [])
    
    # Enhanced overviews for key services
    enhanced_overviews = {
        "Azure Synapse Analytics": {
            "overview": "Enterprise data warehouse that unites data integration, data warehousing, and analytics workloads. Supports both serverless and dedicated resources.",
            "pros": ["Unified analytics platform", "Supports both T-SQL and Spark", "Integrates with Power BI", "Serverless and dedicated options"],
            "cons": ["Complex pricing model", "Learning curve for optimization", "Can be expensive for small workloads"],
            "best_for": ["Large-scale analytics", "Data warehousing", "Complex ETL workflows"],
            "data_flow": "Ingests from multiple sources, processes with T-SQL or Spark, outputs to BI tools"
        },
        "Azure Kubernetes Service (AKS)": {
            "overview": "Managed Kubernetes service that simplifies deploying, managing, and scaling containerized applications using Kubernetes.",
            "pros": ["Fully managed control plane", "Integration with Azure services", "Advanced networking", "Auto-scaling"],
            "cons": ["Kubernetes complexity", "Requires container expertise", "Can be over-engineered for simple apps"],
            "best_for": ["Microservices architecture", "Container orchestration", "DevOps workflows"],
            "data_flow": "Receives traffic via load balancers, processes in containers, connects to databases and storage"
        },
        "Azure Machine Learning": {
            "overview": "Cloud-based machine learning platform for building, training, and deploying ML models at scale with MLOps capabilities.",
            "pros": ["End-to-end ML lifecycle", "AutoML capabilities", "Model deployment options", "MLOps integration"],
            "cons": ["Can be complex for beginners", "Requires ML expertise", "Potentially high costs"],
            "best_for": ["Machine learning projects", "Model deployment", "Data science teams"],
            "data_flow": "Ingests training data, trains models, deploys to endpoints or containers"
        }
    }
    
    if name in enhanced_overviews:
        return enhanced_overviews[name]
    
    # Generate overview for other services
    return {
        "overview": f"Azure {category} service for {', '.join(use_cases[:3]) if use_cases else 'various use cases'}. See documentation for detailed information.",
        "pros": ["Managed service", "Azure integration", "Enterprise-grade"],
        "cons": ["Learning curve", "Cost considerations"],
        "best_for": use_cases[:3] if use_cases else ["General use cases"],
        "data_flow": "Standard Azure service data flow patterns"
    }

def recommend_enhanced_architecture(inputs: Dict, services: List[Dict], min_score: int = 3, top_n: int = 12) -> List[Dict]:
    """Enhanced architecture recommendation with comprehensive analysis"""
    use_case = inputs.get("use_case", "")
    industry = inputs.get("industry")
    capabilities = inputs.get("capabilities", {})
    
    # Extract features
    features = extract_enhanced_features(use_case, capabilities, industry)
    
    # Score all services
    scored_services = []
    architecture_context = {"selected_services": []}
    
    for service in services:
        score, score_breakdown = calculate_advanced_score(service, features, architecture_context, industry)
        
        if score >= min_score:
            service_copy = service.copy()
            service_copy["score"] = score
            service_copy["score_breakdown"] = score_breakdown
            scored_services.append(service_copy)
    
    # Sort by score and select top services
    scored_services.sort(key=lambda x: (-x["score"], x["name"]))
    top_services = scored_services[:top_n]
    
    # Remove duplicates
    seen = set()
    filtered_services = []
    for svc in top_services:
        if svc["name"] not in seen:
            filtered_services.append(svc)
            seen.add(svc["name"])
    
    # Group by category for alternatives
    categories = {}
    for svc in filtered_services:
        categories.setdefault(svc["category"], []).append(svc)
    
    # Build summary with enhanced information
    summary_rows = []
    for svc in filtered_services:
        name = svc["name"]
        category = svc.get("category", "")
        
        # Find alternatives
        alt_services = [s for s in categories.get(category, []) if s["name"] != name][:3]
        alternatives = ", ".join([f"[{alt['name']}]({alt.get('docs', '#')})" for alt in alt_services]) if alt_services else "None"
        
        # Get enhanced overview
        overview_data = get_enhanced_service_overview(svc)
        
        summary_rows.append({
            "Score": svc["score"],
            "Service": name,
            "Category": category,
            "Overview": overview_data["overview"],
            "Pros": overview_data["pros"],
            "Cons": overview_data["cons"],
            "Best For": overview_data["best_for"],
            "Data Flow": overview_data["data_flow"],
            "Alternatives": alternatives,
            "Cost Tier": svc.get("cost_tier", "unknown"),
            "Compliance": ", ".join(svc.get("compliance", [])),
            "Docs": svc.get("docs", ""),
            "Pricing": svc.get("pricing", ""),
            "Score Breakdown": svc["score_breakdown"]
        })
    
    return summary_rows

def generate_enhanced_solution_overview(use_case: str, summary_rows: List[Dict], detected_patterns: List[Dict]) -> str:
    """Generate comprehensive solution overview"""
    categories = {}
    for row in summary_rows:
        categories.setdefault(row["Category"], []).append(row["Service"])
    
    # Architecture flow description
    flows = []
    if "Analytics" in categories or "AI + ML" in categories:
        flows.append("🔍 **Analytics & Intelligence**: Data flows through analytics services for insights and predictions")
    
    if "Integration" in categories:
        flows.append("🔗 **Integration Layer**: Events and data are routed through integration services")
    
    if "Compute" in categories or "Containers" in categories:
        flows.append("⚙️ **Processing Layer**: Application logic runs on compute and container services")
    
    if "Databases" in categories or "Storage" in categories:
        flows.append("💾 **Data Layer**: Information is persisted in databases and storage services")
    
    if "Security" in categories:
        flows.append("🔒 **Security Layer**: Security services protect the entire architecture")
    
    if "Monitoring" in categories:
        flows.append("📊 **Observability**: Monitoring services provide insights into system health and performance")
    
    # Pattern detection summary
    pattern_summary = ""
    if detected_patterns:
        complete_patterns = [p for p in detected_patterns if p["completeness"] == "complete"]
        partial_patterns = [p for p in detected_patterns if p["completeness"] in ["mostly_complete", "partial"]]
        
        if complete_patterns:
            pattern_summary += f"\n\n**✅ Detected Complete Patterns**: {', '.join([p['name'] for p in complete_patterns])}"
        
        if partial_patterns:
            pattern_summary += f"\n\n**⚠️ Partially Implemented Patterns**: {', '.join([p['name'] for p in partial_patterns])}"
    
    all_services = ', '.join([row["Service"] for row in summary_rows])
    
    overview = f"""
## 🏗️ Architecture Overview

**For your use case**: *{use_case}*

**Recommended Services**: {all_services}

### Data Flow Architecture:
{chr(10).join(flows) if flows else "The recommended services address your specific requirements with optimized data flow patterns."}

{pattern_summary}

### Service Distribution:
"""
    
    for category, services in categories.items():
        overview += f"\n- **{category}**: {', '.join(services)}"
    
    return overview

def generate_enhanced_mermaid_diagram(summary_rows: List[Dict]) -> str:
    """Generate enhanced Mermaid diagram with better grouping and flow"""
    category_to_services = {}
    for row in summary_rows:
        category_to_services.setdefault(row["Category"], []).append(row["Service"])
    
    # Define logical flow order
    flow_order = [
        "Integration", "IoT", "Web", "Compute", "Containers", 
        "AI + ML", "Analytics", "Databases", "Storage", 
        "Security", "Monitoring", "Management"
    ]
    
    # Create subgraphs for categories
    diagram_parts = ["flowchart TB"]
    
    # Add subgraphs for each category
    for i, category in enumerate(flow_order):
        if category in category_to_services:
            services = category_to_services[category]
            diagram_parts.append(f"    subgraph {category.replace(' ', '_')}{i} [\"{category}\"]")
            
            for j, service in enumerate(services):
                node_id = f"{category.replace(' ', '_')}{i}_{j}"
                # Truncate long service names for better visualization
                short_name = service.replace("Azure ", "").replace("Microsoft ", "")
                if len(short_name) > 20:
                    short_name = short_name[:20] + "..."
                diagram_parts.append(f"        {node_id}[\"{short_name}\"]")
            
            diagram_parts.append("    end")
    
    # Add connections between related categories
    connections = [
        ("Integration", "Compute"), ("Integration", "Containers"),
        ("IoT", "Analytics"), ("IoT", "Databases"),
        ("Web", "Compute"), ("Web", "Containers"),
        ("Compute", "Databases"), ("Containers", "Databases"),
        ("Analytics", "Storage"), ("AI_+_ML", "Storage"),
        ("Databases", "Storage"),
        ("Security", "Compute"), ("Security", "Containers"),
        ("Monitoring", "Compute"), ("Monitoring", "Containers")
    ]
    
    # Add connections if both categories exist
    for source, target in connections:
        source_exists = any(source.replace('_', ' ') in cat for cat in category_to_services.keys())
        target_exists = any(target.replace('_', ' ') in cat for cat in category_to_services.keys())
        
        if source_exists and target_exists:
            # Find the actual category names
            source_cat = next((cat for cat in category_to_services.keys() if source.replace('_', ' ') in cat), None)
            target_cat = next((cat for cat in category_to_services.keys() if target.replace('_', ' ') in cat), None)
            
            if source_cat and target_cat:
                source_idx = flow_order.index(source_cat) if source_cat in flow_order else 0
                target_idx = flow_order.index(target_cat) if target_cat in flow_order else 0
                diagram_parts.append(f"    {source.replace(' ', '_')}{source_idx} --> {target.replace(' ', '_')}{target_idx}")
    
    return "\n".join(diagram_parts)

def render_enhanced_table(summary_rows: List[Dict]):
    """Render enhanced table with comprehensive information"""
    # Create expandable sections for detailed information
    for i, row in enumerate(summary_rows):
        with st.expander(f"🔍 {row['Service']} (Score: {row['Score']}) - {row['Category']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Overview**: {row['Overview']}")
                st.markdown(f"**Cost Tier**: {row['Cost Tier']}")
                st.markdown(f"**Compliance**: {row['Compliance'] if row['Compliance'] else 'Standard'}")
                
                if row['Pros']:
                    st.markdown("**Pros**:")
                    for pro in row['Pros']:
                
