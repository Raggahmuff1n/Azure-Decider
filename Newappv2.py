import streamlit as st
import pandas as pd
import json
from typing import Dict, List, Any, Tuple
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Azure Solution Architect Pro", 
    layout="wide", 
    page_icon="☁️",
    initial_sidebar_state="expanded"
)

# Enhanced Azure Service Catalog with Full Coverage
@st.cache_data(ttl=3600)
def get_comprehensive_azure_services():
    """Comprehensive Azure service catalog covering all major categories"""
    return [
        # ============ ANALYTICS & BUSINESS INTELLIGENCE ============
        {
            "name": "Azure Synapse Analytics",
            "category": "Analytics & BI",
            "subcategory": "Data Warehousing",
            "cost_tier": "high",
            "use_cases": ["data_warehouse", "analytics", "big_data", "etl", "reporting"],
            "integrates_with": ["Power BI", "Azure Data Lake", "Azure ML", "Data Factory"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Enterprise data warehouse that unites data integration, warehousing, and analytics",
            "data_role": "Central analytics hub for processing and analyzing large datasets",
            "architectural_importance": "critical",
            "pricing_model": "Pay-per-use + Reserved capacity",
            "docs": "https://learn.microsoft.com/azure/synapse-analytics/",
            "pricing": "https://azure.microsoft.com/pricing/details/synapse-analytics/"
        },
        {
            "name": "Power BI",
            "category": "Analytics & BI",
            "subcategory": "Visualization",
            "cost_tier": "medium",
            "use_cases": ["visualization", "dashboards", "reporting", "business_intelligence"],
            "integrates_with": ["Synapse", "Data Factory", "Office 365", "Dynamics"],
            "compliance": ["SOC", "ISO"],
            "description": "Business analytics platform for creating interactive dashboards and reports",
            "data_role": "Visualizes insights from data sources and presents to stakeholders",
            "architectural_importance": "high",
            "pricing_model": "Per-user subscription",
            "docs": "https://learn.microsoft.com/power-bi/",
            "pricing": "https://powerbi.microsoft.com/pricing/"
        },
        {
            "name": "Azure Data Factory",
            "category": "Analytics & BI",
            "subcategory": "Data Integration",
            "cost_tier": "medium",
            "use_cases": ["etl", "data_integration", "pipeline", "orchestration"],
            "integrates_with": ["Synapse", "Data Lake", "SQL Database", "Cosmos DB"],
            "compliance": ["SOC", "HIPAA", "ISO"],
            "description": "Cloud-based data integration service for creating ETL/ELT pipelines",
            "data_role": "Orchestrates data movement and transformation between sources",
            "architectural_importance": "high",
            "pricing_model": "Pay-per-execution",
            "docs": "https://learn.microsoft.com/azure/data-factory/",
            "pricing": "https://azure.microsoft.com/pricing/details/data-factory/"
        },
        {
            "name": "Azure Databricks",
            "category": "Analytics & BI",
            "subcategory": "Advanced Analytics",
            "cost_tier": "high",
            "use_cases": ["machine_learning", "big_data", "spark", "analytics"],
            "integrates_with": ["Azure ML", "Data Lake", "Synapse", "Power BI"],
            "compliance": ["SOC", "HIPAA", "ISO"],
            "description": "Apache Spark-based analytics platform for big data and machine learning",
            "data_role": "Processes large datasets and builds ML models collaboratively",
            "architectural_importance": "high",
            "pricing_model": "Compute + DBU charges",
            "docs": "https://learn.microsoft.com/azure/databricks/",
            "pricing": "https://azure.microsoft.com/pricing/details/databricks/"
        },
        {
            "name": "Azure Stream Analytics",
            "category": "Analytics & BI",
            "subcategory": "Real-time Analytics",
            "cost_tier": "medium",
            "use_cases": ["real_time", "streaming", "iot", "event_processing"],
            "integrates_with": ["Event Hubs", "IoT Hub", "Power BI", "Functions"],
            "compliance": ["SOC", "ISO"],
            "description": "Real-time analytics service for streaming data",
            "data_role": "Processes streaming data in real-time for immediate insights",
            "architectural_importance": "medium",
            "pricing_model": "Streaming Units per hour",
            "docs": "https://learn.microsoft.com/azure/stream-analytics/",
            "pricing": "https://azure.microsoft.com/pricing/details/stream-analytics/"
        },
        {
            "name": "Microsoft Fabric",
            "category": "Analytics & BI",
            "subcategory": "Unified Analytics",
            "cost_tier": "high",
            "use_cases": ["unified_analytics", "data_lakehouse", "governance", "collaboration"],
            "integrates_with": ["Power BI", "Synapse", "Data Factory", "Purview"],
            "compliance": ["SOC", "HIPAA", "ISO"],
            "description": "All-in-one analytics solution that covers everything from data movement to data science",
            "data_role": "Unified platform for end-to-end analytics and data science workflows",
            "architectural_importance": "critical",
            "pricing_model": "Capacity-based",
            "docs": "https://learn.microsoft.com/fabric/",
            "pricing": "https://azure.microsoft.com/pricing/details/microsoft-fabric/"
        },

        # ============ ARTIFICIAL INTELLIGENCE & MACHINE LEARNING ============
        {
            "name": "Azure OpenAI Service",
            "category": "AI & Machine Learning",
            "subcategory": "Generative AI",
            "cost_tier": "high",
            "use_cases": ["generative_ai", "chatbot", "content_generation", "language_models"],
            "integrates_with": ["Cognitive Services", "Bot Service", "Functions", "Logic Apps"],
            "compliance": ["SOC", "ISO"],
            "description": "Access to OpenAI's powerful language models including GPT-4",
            "data_role": "Generates content, answers questions, and processes natural language",
            "architectural_importance": "high",
            "pricing_model": "Token-based usage",
            "docs": "https://learn.microsoft.com/azure/ai-services/openai/",
            "pricing": "https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/"
        },
        {
            "name": "Azure Machine Learning",
            "category": "AI & Machine Learning",
            "subcategory": "ML Platform",
            "cost_tier": "high",
            "use_cases": ["machine_learning", "model_training", "mlops", "deployment"],
            "integrates_with": ["Databricks", "Synapse", "Container Registry", "Functions"],
            "compliance": ["SOC", "HIPAA", "ISO"],
            "description": "End-to-end machine learning lifecycle management platform",
            "data_role": "Trains, deploys, and manages machine learning models at scale",
            "architectural_importance": "high",
            "pricing_model": "Compute + Storage",
            "docs": "https://learn.microsoft.com/azure/machine-learning/",
            "pricing": "https://azure.microsoft.com/pricing/details/machine-learning/"
        },
        {
            "name": "Azure Cognitive Services",
            "category": "AI & Machine Learning",
            "subcategory": "Pre-built AI",
            "cost_tier": "medium",
            "use_cases": ["computer_vision", "speech", "language", "decision_apis"],
            "integrates_with": ["Bot Service", "Functions", "Logic Apps", "Power Platform"],
            "compliance": ["SOC", "ISO"],
            "description": "Pre-built AI services for vision, speech, language, and decision making",
            "data_role": "Adds AI capabilities to applications without custom model development",
            "architectural_importance": "medium",
            "pricing_model": "Transaction-based",
            "docs": "https://learn.microsoft.com/azure/cognitive-services/",
            "pricing": "https://azure.microsoft.com/pricing/details/cognitive-services/"
        },
        {
            "name": "Azure Bot Service",
            "category": "AI & Machine Learning",
            "subcategory": "Conversational AI",
            "cost_tier": "low",
            "use_cases": ["chatbot", "virtual_assistant", "customer_service"],
            "integrates_with": ["OpenAI", "Cognitive Services", "Teams", "QnA Maker"],
            "compliance": ["SOC", "ISO"],
            "description": "Platform for building intelligent, enterprise-grade bots",
            "data_role": "Handles conversational interactions and routes to appropriate services",
            "architectural_importance": "medium",
            "pricing_model": "Message-based",
            "docs": "https://learn.microsoft.com/azure/bot-service/",
            "pricing": "https://azure.microsoft.com/pricing/details/bot-service/"
        },

        # ============ COMPUTE SERVICES ============
        {
            "name": "Azure Virtual Machines",
            "category": "Compute",
            "subcategory": "IaaS",
            "cost_tier": "variable",
            "use_cases": ["legacy_apps", "custom_software", "lift_shift", "windows", "linux"],
            "integrates_with": ["Virtual Network", "Load Balancer", "Monitor", "Backup"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "On-demand, scalable computing resources with full OS control",
            "data_role": "Hosts applications and services requiring specific OS configurations",
            "architectural_importance": "medium",
            "pricing_model": "Hourly compute + Storage",
            "docs": "https://learn.microsoft.com/azure/virtual-machines/",
            "pricing": "https://azure.microsoft.com/pricing/details/virtual-machines/"
        },
        {
            "name": "Azure Functions",
            "category": "Compute",
            "subcategory": "Serverless",
            "cost_tier": "low",
            "use_cases": ["serverless", "event_driven", "microservices", "triggers"],
            "integrates_with": ["Logic Apps", "Event Grid", "Cosmos DB", "Storage"],
            "compliance": ["SOC", "ISO"],
            "description": "Event-driven serverless compute platform",
            "data_role": "Executes code in response to events without managing infrastructure",
            "architectural_importance": "high",
            "pricing_model": "Consumption-based",
            "docs": "https://learn.microsoft.com/azure/azure-functions/",
            "pricing": "https://azure.microsoft.com/pricing/details/functions/"
        },
        {
            "name": "Azure App Service",
            "category": "Compute",
            "subcategory": "PaaS Web",
            "cost_tier": "medium",
            "use_cases": ["web_apps", "api", "mobile_backend", "rest_services"],
            "integrates_with": ["SQL Database", "Key Vault", "Application Insights", "CDN"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Fully managed platform for building web apps and APIs",
            "data_role": "Hosts web applications and APIs with automatic scaling",
            "architectural_importance": "high",
            "pricing_model": "App Service Plan",
            "docs": "https://learn.microsoft.com/azure/app-service/",
            "pricing": "https://azure.microsoft.com/pricing/details/app-service/"
        },
        {
            "name": "Azure Logic Apps",
            "category": "Compute",
            "subcategory": "Workflow Automation",
            "cost_tier": "low",
            "use_cases": ["workflow", "integration", "automation", "business_process"],
            "integrates_with": ["Office 365", "Dynamics", "SAP", "Salesforce"],
            "compliance": ["SOC", "HIPAA", "ISO"],
            "description": "Cloud-based platform for creating automated workflows",
            "data_role": "Orchestrates business processes and integrates systems",
            "architectural_importance": "medium",
            "pricing_model": "Per workflow execution",
            "docs": "https://learn.microsoft.com/azure/logic-apps/",
            "pricing": "https://azure.microsoft.com/pricing/details/logic-apps/"
        },

        # ============ CONTAINERS & KUBERNETES ============
        {
            "name": "Azure Kubernetes Service (AKS)",
            "category": "Containers",
            "subcategory": "Orchestration",
            "cost_tier": "medium",
            "use_cases": ["kubernetes", "microservices", "container_orchestration", "devops"],
            "integrates_with": ["Container Registry", "Monitor", "Active Directory", "Key Vault"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Managed Kubernetes service for deploying containerized applications",
            "data_role": "Orchestrates containerized applications with high availability",
            "architectural_importance": "high",
            "pricing_model": "Node pool compute costs",
            "docs": "https://learn.microsoft.com/azure/aks/",
            "pricing": "https://azure.microsoft.com/pricing/details/kubernetes-service/"
        },
        {
            "name": "Azure Container Apps",
            "category": "Containers",
            "subcategory": "Serverless Containers",
            "cost_tier": "low",
            "use_cases": ["serverless_containers", "microservices", "event_driven", "api"],
            "integrates_with": ["Event Grid", "Service Bus", "Monitor", "Key Vault"],
            "compliance": ["SOC", "ISO"],
            "description": "Serverless containers with built-in best practices",
            "data_role": "Runs containerized apps without managing infrastructure",
            "architectural_importance": "medium",
            "pricing_model": "vCPU and memory consumption",
            "docs": "https://learn.microsoft.com/azure/container-apps/",
            "pricing": "https://azure.microsoft.com/pricing/details/container-apps/"
        },
        {
            "name": "Azure Container Registry",
            "category": "Containers",
            "subcategory": "Registry",
            "cost_tier": "low",
            "use_cases": ["container_images", "docker_registry", "devops", "cicd"],
            "integrates_with": ["AKS", "Container Apps", "DevOps", "GitHub Actions"],
            "compliance": ["SOC", "ISO"],
            "description": "Private Docker registry service for managing container images",
            "data_role": "Stores and manages container images securely",
            "architectural_importance": "medium",
            "pricing_model": "Storage + operations",
            "docs": "https://learn.microsoft.com/azure/container-registry/",
            "pricing": "https://azure.microsoft.com/pricing/details/container-registry/"
        },

        # ============ DATABASES & DATA STORAGE ============
        {
            "name": "Azure SQL Database",
            "category": "Databases",
            "subcategory": "Relational",
            "cost_tier": "medium",
            "use_cases": ["relational_database", "sql_server", "oltp", "applications"],
            "integrates_with": ["Power BI", "Data Factory", "Functions", "App Service"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Fully managed relational database with AI-powered features",
            "data_role": "Stores structured data with ACID compliance and relationships",
            "architectural_importance": "high",
            "pricing_model": "DTU or vCore-based",
            "docs": "https://learn.microsoft.com/azure/azure-sql/database/",
            "pricing": "https://azure.microsoft.com/pricing/details/azure-sql-database/"
        },
        {
            "name": "Azure Cosmos DB",
            "category": "Databases",
            "subcategory": "NoSQL",
            "cost_tier": "medium",
            "use_cases": ["nosql", "global_distribution", "multi_model", "real_time"],
            "integrates_with": ["Functions", "Synapse", "Power BI", "Search"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Globally distributed, multi-model NoSQL database",
            "data_role": "Stores unstructured data with global distribution and consistency",
            "architectural_importance": "high",
            "pricing_model": "Request Units + Storage",
            "docs": "https://learn.microsoft.com/azure/cosmos-db/",
            "pricing": "https://azure.microsoft.com/pricing/details/cosmos-db/"
        },
        {
            "name": "Azure Cache for Redis",
            "category": "Databases",
            "subcategory": "Caching",
            "cost_tier": "low",
            "use_cases": ["caching", "session_storage", "real_time", "performance"],
            "integrates_with": ["App Service", "Functions", "AKS", "Virtual Machines"],
            "compliance": ["SOC", "ISO"],
            "description": "Fully managed in-memory data store based on Redis",
            "data_role": "Improves application performance through high-speed caching",
            "architectural_importance": "medium",
            "pricing_model": "Cache size tiers",
            "docs": "https://learn.microsoft.com/azure/azure-cache-for-redis/",
            "pricing": "https://azure.microsoft.com/pricing/details/cache/"
        },

        # ============ STORAGE SERVICES ============
        {
            "name": "Azure Blob Storage",
            "category": "Storage",
            "subcategory": "Object Storage",
            "cost_tier": "low",
            "use_cases": ["object_storage", "backup", "archival", "media", "data_lake"],
            "integrates_with": ["CDN", "Data Factory", "Synapse", "Functions"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Massively scalable object storage for unstructured data",
            "data_role": "Stores files, documents, media, and backup data",
            "architectural_importance": "high",
            "pricing_model": "Storage + transactions",
            "docs": "https://learn.microsoft.com/azure/storage/blobs/",
            "pricing": "https://azure.microsoft.com/pricing/details/storage/blobs/"
        },
        {
            "name": "Azure Data Lake Storage",
            "category": "Storage",
            "subcategory": "Data Lake",
            "cost_tier": "medium",
            "use_cases": ["big_data", "analytics", "data_lake", "hierarchical"],
            "integrates_with": ["Synapse", "Databricks", "Data Factory", "Power BI"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Scalable data lake storage for big data analytics",
            "data_role": "Central repository for structured and unstructured analytics data",
            "architectural_importance": "high",
            "pricing_model": "Storage + transactions",
            "docs": "https://learn.microsoft.com/azure/storage/blobs/data-lake-storage-introduction/",
            "pricing": "https://azure.microsoft.com/pricing/details/storage/data-lake/"
        },

        # ============ NETWORKING & CONTENT DELIVERY ============
        {
            "name": "Azure Virtual Network",
            "category": "Networking",
            "subcategory": "Core Networking",
            "cost_tier": "low",
            "use_cases": ["network_isolation", "hybrid_connectivity", "security", "subnets"],
            "integrates_with": ["Virtual Machines", "AKS", "Application Gateway", "Firewall"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Private network in Azure for connecting resources securely",
            "data_role": "Provides network isolation and secure communication paths",
            "architectural_importance": "critical",
            "pricing_model": "VPN Gateway + bandwidth",
            "docs": "https://learn.microsoft.com/azure/virtual-network/",
            "pricing": "https://azure.microsoft.com/pricing/details/virtual-network/"
        },
        {
            "name": "Azure Application Gateway",
            "category": "Networking",
            "subcategory": "Load Balancer",
            "cost_tier": "medium",
            "use_cases": ["load_balancer", "ssl_termination", "waf", "routing"],
            "integrates_with": ["Virtual Network", "AKS", "App Service", "Key Vault"],
            "compliance": ["SOC", "ISO"],
            "description": "Web traffic load balancer with application-level routing",
            "data_role": "Routes and load balances HTTP/HTTPS traffic to applications",
            "architectural_importance": "high",
            "pricing_model": "Gateway hours + data processing",
            "docs": "https://learn.microsoft.com/azure/application-gateway/",
            "pricing": "https://azure.microsoft.com/pricing/details/application-gateway/"
        },
        {
            "name": "Azure Front Door",
            "category": "Networking",
            "subcategory": "Global Load Balancer",
            "cost_tier": "medium",
            "use_cases": ["global_load_balancer", "cdn", "waf", "acceleration"],
            "integrates_with": ["App Service", "Application Gateway", "Storage", "Functions"],
            "compliance": ["SOC", "ISO"],
            "description": "Global load balancer and CDN service",
            "data_role": "Delivers content globally with edge optimization",
            "architectural_importance": "medium",
            "pricing_model": "Routing rules + data transfer",
            "docs": "https://learn.microsoft.com/azure/frontdoor/",
            "pricing": "https://azure.microsoft.com/pricing/details/frontdoor/"
        },

        # ============ SECURITY & IDENTITY ============
        {
            "name": "Azure Active Directory",
            "category": "Security & Identity",
            "subcategory": "Identity Platform",
            "cost_tier": "variable",
            "use_cases": ["identity", "authentication", "authorization", "sso"],
            "integrates_with": ["All Azure Services", "Office 365", "Third-party SaaS"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Cloud-based identity and access management service",
            "data_role": "Manages user identities and access across all services",
            "architectural_importance": "critical",
            "pricing_model": "Per-user/per-month",
            "docs": "https://learn.microsoft.com/azure/active-directory/",
            "pricing": "https://azure.microsoft.com/pricing/details/active-directory/"
        },
        {
            "name": "Azure Key Vault",
            "category": "Security & Identity",
            "subcategory": "Secrets Management",
            "cost_tier": "low",
            "use_cases": ["secrets", "keys", "certificates", "encryption"],
            "integrates_with": ["App Service", "Functions", "AKS", "Virtual Machines"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Secure storage for secrets, keys, and certificates",
            "data_role": "Protects and manages cryptographic keys and secrets",
            "architectural_importance": "critical",
            "pricing_model": "Operations-based",
            "docs": "https://learn.microsoft.com/azure/key-vault/",
            "pricing": "https://azure.microsoft.com/pricing/details/key-vault/"
        },
        {
            "name": "Microsoft Defender for Cloud",
            "category": "Security & Identity",
            "subcategory": "Security Posture",
            "cost_tier": "medium",
            "use_cases": ["security_monitoring", "threat_detection", "compliance", "cspm"],
            "integrates_with": ["Monitor", "Sentinel", "Logic Apps", "Security Center"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Unified security management and advanced threat protection",
            "data_role": "Monitors and protects cloud resources from threats",
            "architectural_importance": "high",
            "pricing_model": "Per-resource pricing",
            "docs": "https://learn.microsoft.com/azure/defender-for-cloud/",
            "pricing": "https://azure.microsoft.com/pricing/details/defender-for-cloud/"
        },

        # ============ MONITORING & MANAGEMENT ============
        {
            "name": "Azure Monitor",
            "category": "Monitoring & Management",
            "subcategory": "Observability",
            "cost_tier": "medium",
            "use_cases": ["monitoring", "logging", "metrics", "alerting", "diagnostics"],
            "integrates_with": ["All Azure Services", "Application Insights", "Log Analytics"],
            "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"],
            "description": "Full-stack monitoring service for applications and infrastructure",
            "data_role": "Collects, analyzes, and acts on telemetry from all environments",
            "architectural_importance": "critical",
            "pricing_model": "Data ingestion + retention",
            "docs": "https://learn.microsoft.com/azure/azure-monitor/",
            "pricing": "https://azure.microsoft.com/pricing/details/monitor/"
        },
        {
            "name": "Application Insights",
            "category": "Monitoring & Management",
            "subcategory": "APM",
            "cost_tier": "low",
            "use_cases": ["apm", "performance", "diagnostics", "user_analytics"],
            "integrates_with": ["App Service", "Functions", "AKS", "Monitor"],
            "compliance": ["SOC", "ISO"],
            "description": "Application performance monitoring and analytics service",
            "data_role": "Tracks application performance and user behavior",
            "architectural_importance": "high",
            "pricing_model": "Data volume-based",
            "docs": "https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview/",
            "pricing": "https://azure.microsoft.com/pricing/details/monitor/"
        },

        # ============ IOT & EDGE ============
        {
            "name": "Azure IoT Hub",
            "category": "IoT & Edge",
            "subcategory": "IoT Platform",
            "cost_tier": "medium",
            "use_cases": ["iot_connectivity", "device_management", "telemetry", "commands"],
            "integrates_with": ["Stream Analytics", "Functions", "Digital Twins", "Monitor"],
            "compliance": ["SOC", "HIPAA", "ISO"],
            "description": "Managed service for bi-directional communication with IoT devices",
            "data_role": "Collects telemetry and manages IoT devices at scale",
            "architectural_importance": "high",
            "pricing_model": "Messages per day",
            "docs": "https://learn.microsoft.com/azure/iot-hub/",
            "pricing": "https://azure.microsoft.com/pricing/details/iot-hub/"
        },
        {
            "name": "Azure Digital Twins",
            "category": "IoT & Edge",
            "subcategory": "Digital Modeling",
            "cost_tier": "medium",
            "use_cases": ["digital_twins", "iot_modeling", "spatial_intelligence", "simulation"],
            "integrates_with": ["IoT Hub", "Time Series Insights", "Maps", "Functions"],
            "compliance": ["SOC", "ISO"],
            "description": "IoT service for creating digital representations of real-world environments",
            "data_role": "Models and simulates real-world IoT environments",
            "architectural_importance": "medium",
            "pricing_model": "API operations + queries",
            "docs": "https://learn.microsoft.com/azure/digital-twins/",
            "pricing": "https://azure.microsoft.com/pricing/details/digital-twins/"
        },

        # ============ DEVOPS & DEVELOPER TOOLS ============
        {
            "name": "Azure DevOps",
            "category": "DevOps & Developer Tools",
            "subcategory": "DevOps Platform",
            "cost_tier": "low",
            "use_cases": ["cicd", "project_management", "source_control", "testing"],
            "integrates_with": ["GitHub", "Container Registry", "AKS", "Monitor"],
            "compliance": ["SOC", "ISO"],
            "description": "Complete DevOps toolchain for planning, developing, and deploying",
            "data_role": "Manages code, builds, tests, and deployment pipelines",
            "architectural_importance": "medium",
            "pricing_model": "Per-user basic/premium",
            "docs": "https://learn.microsoft.com/azure/devops/",
            "pricing": "https://azure.microsoft.com/pricing/details/devops/azure-devops-services/"
        },
        {
            "name": "GitHub Actions",
            "category": "DevOps & Developer Tools",
            "subcategory": "CI/CD",
            "cost_tier": "low",
            "use_cases": ["cicd", "automation", "workflows", "testing"],
            "integrates_with": ["Container Registry", "AKS", "App Service", "Functions"],
            "compliance": ["SOC", "ISO"],
            "description": "CI/CD platform integrated with GitHub repositories",
            "data_role": "Automates software workflows from code to deployment",
            "architectural_importance": "medium",
            "pricing_model": "Minutes + storage",
            "docs": "https://docs.github.com/actions",
            "pricing": "https://github.com/pricing"
        },

        # ============ INTEGRATION & MESSAGING ============
        {
            "name": "Azure Service Bus",
            "category": "Integration & Messaging",
            "subcategory": "Enterprise Messaging",
            "cost_tier": "low",
            "use_cases": ["messaging", "queues", "topics", "enterprise_integration"],
            "integrates_with": ["Functions", "Logic Apps", "Event Grid", "AKS"],
            "compliance": ["SOC", "HIPAA", "ISO"],
            "description": "Reliable cloud messaging as a service platform",
            "data_role": "Enables reliable communication between distributed applications",
            "architectural_importance": "medium",
            "pricing_model": "Messages + connections",
            "docs": "https://learn.microsoft.com/azure/service-bus-messaging/",
            "pricing": "https://azure.microsoft.com/pricing/details/service-bus/"
        },
        {
            "name": "Azure Event Grid",
            "category": "Integration & Messaging",
            "subcategory": "Event Routing",
            "cost_tier": "low",
            "use_cases": ["event_routing", "reactive_programming", "serverless", "automation"],
            "integrates_with": ["Functions", "Logic Apps", "Storage", "Cosmos DB"],
            "compliance": ["SOC", "ISO"],
            "description": "Fully managed event routing service for reactive programming",
            "data_role": "Routes events from any source to any destination at scale",
            "architectural_importance": "medium",
            "pricing_model": "Operations-based",
            "docs": "https://learn.microsoft.com/azure/event-grid/",
            "pricing": "https://azure.microsoft.com/pricing/details/event-grid/"
        },
        {
            "name": "Azure API Management",
            "category": "Integration & Messaging",
            "subcategory": "API Gateway",
            "cost_tier": "medium",
            "use_cases": ["api_gateway", "api_management", "developer_portal", "policies"],
            "integrates_with": ["App Service", "Functions", "Logic Apps", "Active Directory"],
            "compliance": ["SOC", "HIPAA", "ISO"],
            "description": "Hybrid, multicloud management platform for APIs",
            "data_role": "Manages, secures, and analyzes APIs across environments",
            "architectural_importance": "high",
            "pricing_model": "Gateway units + calls",
            "docs": "https://learn.microsoft.com/azure/api-management/",
            "pricing": "https://azure.microsoft.com/pricing/details/api-management/"
        }
    ]

# Enhanced Architecture Patterns with Complete Solutions
COMPREHENSIVE_PATTERNS = {
    "modern_data_platform": {
        "name": "Modern Data & Analytics Platform",
        "description": "Complete modern data platform for analytics, ML, and business intelligence with unified governance",
        "required_services": ["Azure Data Factory", "Azure Data Lake Storage", "Azure Synapse Analytics", "Power BI"],
        "recommended_services": ["Microsoft Fabric", "Azure Machine Learning", "Microsoft Purview", "Azure Monitor"],
        "optional_services": ["Azure Databricks", "Azure Stream Analytics", "Azure Cognitive Services"],
        "use_cases": ["data_warehouse", "analytics", "business_intelligence", "machine_learning", "reporting"],
        "industries": ["financial", "healthcare", "retail", "manufacturing"],
        "complexity": "high",
        "estimated_timeline": "3-6 months"
    },
    "intelligent_app_platform": {
        "name": "AI-Powered Application Platform",
        "description": "Modern application platform with integrated AI capabilities and intelligent automation",
        "required_services": ["Azure App Service", "Azure OpenAI Service", "Azure Cognitive Services", "Azure SQL Database"],
        "recommended_services": ["Azure Functions", "Azure API Management", "Application Insights", "Azure Key Vault"],
        "optional_services": ["Azure Bot Service", "Azure Search", "Azure Cache for Redis"],
        "use_cases": ["intelligent_apps", "chatbot", "automation", "ai_integration"],
        "industries": ["technology", "healthcare", "financial", "retail"],
        "complexity": "medium",
        "estimated_timeline": "2-4 months"
    },
    "cloud_native_microservices": {
        "name": "Cloud-Native Microservices Platform",
        "description": "Enterprise-grade microservices platform with container orchestration and DevOps integration",
        "required_services": ["Azure Kubernetes Service (AKS)", "Azure Container Registry", "Azure Virtual Network", "Azure Monitor"],
        "recommended_services": ["Azure Application Gateway", "Azure Key Vault", "Azure DevOps", "Azure Service Bus"],
        "optional_services": ["Azure API Management", "Azure Cache for Redis", "Microsoft Defender for Cloud"],
        "use_cases": ["microservices", "containers", "scalability", "devops", "cicd"],
        "industries": ["technology", "financial", "retail", "gaming"],
        "complexity": "high",
        "estimated_timeline": "4-8 months"
    },
    "serverless_event_driven": {
        "name": "Serverless Event-Driven Architecture",
        "description": "Scalable serverless architecture for event-driven applications with automatic scaling",
        "required_services": ["Azure Functions", "Azure Event Grid", "Azure Cosmos DB", "Azure Storage"],
        "recommended_services": ["Azure Logic Apps", "Azure API Management", "Application Insights", "Azure Key Vault"],
        "optional_services": ["Azure Service Bus", "Azure Stream Analytics", "Power BI"],
        "use_cases": ["serverless", "event_driven", "auto_scaling", "cost_optimization"],
        "industries": ["startup", "media", "iot", "retail"],
        "complexity": "medium",
        "estimated_timeline": "2-3 months"
    },
    "iot_analytics_platform": {
        "name": "IoT Analytics & Intelligence Platform",
        "description": "End-to-end IoT platform for device management, real-time analytics, and predictive insights",
        "required_services": ["Azure IoT Hub", "Azure Stream Analytics", "Azure Data Lake Storage", "Power BI"],
        "recommended_services": ["Azure Digital Twins", "Azure Machine Learning", "Azure Functions", "Azure Monitor"],
        "optional_services": ["Azure Time Series Insights", "Azure Maps", "Azure Cognitive Services"],
        "use_cases": ["iot", "real_time", "telemetry", "predictive_analytics", "device_management"],
        "industries": ["manufacturing", "energy", "transportation", "smart_cities"],
        "complexity": "high",
        "estimated_timeline": "4-6 months"
    },
    "secure_enterprise_platform": {
        "name": "Secure Enterprise Platform",
        "description": "Enterprise-grade platform with comprehensive security, compliance, and governance",
        "required_services": ["Azure Active Directory", "Azure Key Vault", "Microsoft Defender for Cloud", "Azure Monitor"],
        "recommended_services": ["Azure Virtual Network", "Azure Application Gateway", "Azure Policy", "Microsoft Sentinel"],
        "optional_services": ["Azure Firewall", "Azure Private Link", "Azure Backup"],
        "use_cases": ["enterprise_security", "compliance", "governance", "identity_management"],
        "industries": ["financial", "healthcare", "government", "enterprise"],
        "complexity": "high",
        "estimated_timeline": "3-6 months"
    }
}

# Industry-Specific Requirements
INDUSTRY_COMPLIANCE = {
    "healthcare": {
        "name": "Healthcare & Life Sciences",
        "compliance_frameworks": ["HIPAA", "HITECH", "FDA", "GxP"],
        "required_services": ["Azure Key Vault", "Microsoft Defender for Cloud", "Azure Monitor", "Azure Private Link"],
        "data_residency": "required",
        "encryption": "end_to_end",
        "audit_logging": "comprehensive",
        "special_considerations": ["PHI protection", "Clinical data integrity", "Regulatory compliance"]
    },
    "financial": {
        "name": "Financial Services",
        "compliance_frameworks": ["PCI DSS", "SOX", "GDPR", "Basel III"],
        "required_services": ["Azure Key Vault", "Microsoft Defender for Cloud", "Azure Firewall", "Azure Monitor"],
        "data_residency": "required",
        "encryption": "end_to_end",
        "audit_logging": "comprehensive",
        "special_considerations": ["Payment data security", "Trading compliance", "Risk management"]
    },
    "government": {
        "name": "Government & Public Sector",
        "compliance_frameworks": ["FedRAMP", "FISMA", "ITAR", "CJIS"],
        "required_services": ["Azure Government", "Azure Key Vault", "Microsoft Defender for Cloud"],
        "data_residency": "government_cloud",
        "encryption": "fips_140_2",
        "audit_logging": "comprehensive",
        "special_considerations": ["Citizen data protection", "National security", "Regulatory oversight"]
    },
    "retail": {
        "name": "Retail & E-commerce",
        "compliance_frameworks": ["PCI DSS", "GDPR", "CCPA"],
        "required_services": ["Azure Key Vault", "Azure CDN", "Azure Application Gateway"],
        "data_residency": "flexible",
        "encryption": "standard",
        "audit_logging": "standard",
        "special_considerations": ["Customer data privacy", "Payment processing", "Global scaling"]
    },
    "manufacturing": {
        "name": "Manufacturing & Industrial",
        "compliance_frameworks": ["ISO 27001", "SOC 2", "NIST"],
        "required_services": ["Azure IoT Hub", "Azure Monitor", "Azure Key Vault"],
        "data_residency": "flexible",
        "encryption": "standard",
        "audit_logging": "operational",
        "special_considerations": ["OT security", "Supply chain", "Predictive maintenance"]
    },
    "technology": {
        "name": "Technology & Software",
        "compliance_frameworks": ["SOC 2", "ISO 27001", "GDPR"],
        "required_services": ["Azure DevOps", "Azure Key Vault", "Azure Monitor"],
        "data_residency": "flexible",
        "encryption": "standard",
        "audit_logging": "development_focused",
        "special_considerations": ["DevSecOps", "API security", "Multi-tenancy"]
    }
}

def calculate_comprehensive_score(service: Dict, requirements: Dict, architecture_context: Dict) -> Tuple[int, Dict]:
    """Enhanced scoring algorithm with detailed analysis"""
    score_breakdown = {
        "functional_alignment": 0,
        "architectural_fit": 0,
        "compliance_match": 0,
        "integration_synergy": 0,
        "cost_efficiency": 0,
        "industry_relevance": 0,
        "innovation_factor": 0
    }
    
    use_case_text = requirements.get("use_case", "").lower()
    selected_capabilities = requirements.get("capabilities", {})
    industry = requirements.get("industry", "")
    
    # 1. Functional Alignment (0-25 points)
    service_use_cases = [uc.lower() for uc in service.get("use_cases", [])]
    capability_matches = sum(1 for cap, selected in selected_capabilities.items() 
                           if selected and cap.lower().replace(" ", "_") in " ".join(service_use_cases))
    
    text_matches = sum(3 for uc in service_use_cases if uc in use_case_text)
    score_breakdown["functional_alignment"] = min(25, capability_matches * 4 + text_matches)
    
    # 2. Architectural Fit (0-20 points)
    architectural_importance = service.get("architectural_importance", "medium")
    importance_scores = {"critical": 20, "high": 15, "medium": 10, "low": 5}
    score_breakdown["architectural_fit"] = importance_scores.get(architectural_importance, 10)
    
    # 3. Compliance Match (0-15 points)
    if industry in INDUSTRY_COMPLIANCE:
        industry_reqs = INDUSTRY_COMPLIANCE[industry]
        service_compliance = service.get("compliance", [])
        required_frameworks = industry_reqs["compliance_frameworks"]
        
        compliance_score = sum(3 for framework in required_frameworks if framework in service_compliance)
        if service["name"] in industry_reqs["required_services"]:
            compliance_score += 6
        score_breakdown["compliance_match"] = min(15, compliance_score)
    
    # 4. Integration Synergy (0-15 points)
    selected_services = architecture_context.get("selected_services", [])
    integration_partners = service.get("integrates_with", [])
    synergy_score = sum(2 for selected in selected_services 
                       if any(partner in selected for partner in integration_partners))
    score_breakdown["integration_synergy"] = min(15, synergy_score)
    
    # 5. Cost Efficiency (0-10 points)
    cost_tier = service.get("cost_tier", "medium")
    cost_scores = {"free": 10, "low": 8, "medium": 6, "high": 3, "variable": 5}
    score_breakdown["cost_efficiency"] = cost_scores.get(cost_tier, 6)
    
    # 6. Industry Relevance (0-10 points)
    if industry and industry in ["healthcare", "financial", "government"]:
        # High-compliance industries
        if service.get("category") in ["Security & Identity", "Monitoring & Management"]:
            score_breakdown["industry_relevance"] = 8
        elif "HIPAA" in service.get("compliance", []) or "FedRAMP" in service.get("compliance", []):
            score_breakdown["industry_relevance"] = 10
    elif industry in ["technology", "startup"]:
        # Innovation-focused industries
        if service.get("category") in ["AI & Machine Learning", "DevOps & Developer Tools"]:
            score_breakdown["industry_relevance"] = 8
    
    # 7. Innovation Factor (0-5 points)
    innovative_services = ["Azure OpenAI Service", "Microsoft Fabric", "Azure Digital Twins", 
                          "Azure Container Apps", "Azure Machine Learning"]
    if service["name"] in innovative_services:
        score_breakdown["innovation_factor"] = 5
    elif service.get("category") == "AI & Machine Learning":
        score_breakdown["innovation_factor"] = 3
    
    total_score = sum(score_breakdown.values())
    return total_score, score_breakdown

def detect_architecture_patterns(selected_services: List[str], requirements: Dict) -> List[Dict]:
    """Enhanced pattern detection with completeness analysis"""
    detected_patterns = []
    
    for pattern_name, pattern in COMPREHENSIVE_PATTERNS.items():
        required_services = pattern["required_services"]
        recommended_services = pattern["recommended_services"]
        optional_services = pattern["optional_services"]
        
        # Calculate coverage
        required_coverage = sum(1 for svc in required_services if svc in selected_services)
        recommended_coverage = sum(1 for svc in recommended_services if svc in selected_services)
        optional_coverage = sum(1 for svc in optional_services if svc in selected_services)
        
        total_required = len(required_services)
        total_recommended = len(recommended_services)
        
        # Determine completeness
        if required_coverage == total_required:
            if recommended_coverage >= total_recommended * 0.7:
                completeness = "complete"
            else:
                completeness = "core_complete"
        elif required_coverage >= total_required * 0.8:
            completeness = "mostly_complete"
        elif required_coverage >= total_required * 0.5:
            completeness = "partially_complete"
        else:
            completeness = "minimal"
        
        # Check use case alignment
        pattern_use_cases = pattern["use_cases"]
        use_case_text = requirements.get("use_case", "").lower()
        capabilities = requirements.get("capabilities", {})
        
        use_case_alignment = sum(1 for uc in pattern_use_cases 
                               if uc in use_case_text or 
                               any(uc in cap.lower() for cap, selected in capabilities.items() if selected))
        
        # Only include patterns with some relevance
        if completeness != "minimal" or use_case_alignment > 0:
            pattern_score = (required_coverage * 3 + recommended_coverage * 2 + 
                           optional_coverage + use_case_alignment * 2)
            
            detected_patterns.append({
                "name": pattern["name"],
                "description": pattern["description"],
                "completeness": completeness,
                "required_coverage": f"{required_coverage}/{total_required}",
                "recommended_coverage": f"{recommended_coverage}/{total_recommended}",
                "optional_coverage": optional_coverage,
                "missing_required": [svc for svc in required_services if svc not in selected_services],
                "missing_recommended": [svc for svc in recommended_services if svc not in selected_services],
                "pattern_score": pattern_score,
                "complexity": pattern["complexity"],
                "timeline": pattern["estimated_timeline"],
                "use_case_alignment": use_case_alignment
            })
    
    # Sort by pattern score
    detected_patterns.sort(key=lambda x: x["pattern_score"], reverse=True)
    return detected_patterns

def generate_cost_analysis(selected_services: List[Dict], requirements: Dict) -> Dict:
    """Enhanced cost analysis with detailed breakdown and optimization suggestions"""
    
    # Base cost estimates (monthly USD)
    base_costs = {
        "free": 0,
        "low": 75,
        "medium": 350,
        "high": 1200,
        "variable": 200
    }
    
    # Scaling factors based on requirements
    team_size = requirements.get("team_size", 10)
    data_volume = requirements.get("data_volume_gb", 500)
    expected_users = requirements.get("expected_users", 1000)
    
    cost_analysis = {
        "services": {},
        "category_totals": {},
        "scaling_assumptions": {
            "team_size": team_size,
            "data_volume_gb": data_volume,
            "expected_users": expected_users
        }
    }
    
    total_monthly = 0
    category_costs = {}
    
    for service in selected_services:
        cost_tier = service.get("cost_tier", "medium")
        category = service["category"]
        base_cost = base_costs[cost_tier]
        
        # Apply scaling based on service type
        if "Analytics" in category or "AI" in category:
            scaling_factor = max(1, data_volume / 100)
        elif "Compute" in category or "Container" in category:
            scaling_factor = max(1, expected_users / 500)
        elif "Database" in category:
            scaling_factor = max(1, (data_volume / 200) * (expected_users / 1000))
        elif "DevOps" in category:
            scaling_factor = max(1, team_size / 5)
        else:
            scaling_factor = max(1, expected_users / 1000)
        
        monthly_cost = base_cost * scaling_factor
        annual_cost = monthly_cost * 12 * 0.85  # Assume 15% annual discount
        
        cost_analysis["services"][service["name"]] = {
            "monthly_estimate": round(monthly_cost, 2),
            "annual_estimate": round(annual_cost, 2),
            "cost_tier": cost_tier,
            "scaling_factor": round(scaling_factor, 2),
            "category": category
        }
        
        total_monthly += monthly_cost
        category_costs[category] = category_costs.get(category, 0) + monthly_cost
    
    cost_analysis["total_monthly"] = round(total_monthly, 2)
    cost_analysis["total_annual"] = round(total_monthly * 12 * 0.85, 2)
    cost_analysis["category_totals"] = {k: round(v, 2) for k, v in category_costs.items()}
    
    # Cost optimization suggestions
    optimization_suggestions = []
    
    high_cost_services = [name for name, details in cost_analysis["services"].items() 
                         if details["monthly_estimate"] > 500]
    
    if high_cost_services:
        optimization_suggestions.append(
            f"Consider reserved instances for high-cost services: {', '.join(high_cost_services[:3])}"
        )
    
    if cost_analysis["total_monthly"] > 2000:
        optimization_suggestions.append(
            "Explore Azure Hybrid Benefit for Windows and SQL Server licensing savings"
        )
    
    serverless_alternatives = ["Azure Functions", "Azure Container Apps", "Azure Logic Apps"]
    compute_services = [name for name, details in cost_analysis["services"].items() 
                       if "Compute" in details["category"]]
    
    if compute_services and not any(alt in cost_analysis["services"] for alt in serverless_alternatives):
        optimization_suggestions.append(
            "Consider serverless alternatives for variable workloads to optimize costs"
        )
    
    cost_analysis["optimization_suggestions"] = optimization_suggestions
    
    return cost_analysis

def generate_architecture_diagram(selected_services: List[Dict], patterns: List[Dict]) -> str:
    """Generate comprehensive Mermaid architecture diagram"""
    
    # Group services by category
    service_groups = {}
    for service in selected_services:
        category = service["category"]
        if category not in service_groups:
            service_groups[category] = []
        service_groups[category].append(service["name"])
    
    # Define flow relationships
    flow_relationships = {
        "Integration & Messaging": ["Compute", "Analytics & BI", "AI & Machine Learning"],
        "IoT & Edge": ["Analytics & BI", "Storage", "AI & Machine Learning"],
        "Compute": ["Databases", "Storage", "AI & Machine Learning"],
        "Containers": ["Databases", "Storage", "Networking"],
        "Analytics & BI": ["Storage", "Databases"],
        "AI & Machine Learning": ["Storage", "Analytics & BI"],
        "DevOps & Developer Tools": ["Compute", "Containers"],
        "Networking": ["Security & Identity"],
        "Security & Identity": ["Monitoring & Management"]
    }
    
    # Build Mermaid diagram
    diagram = ["flowchart TB"]
    
    # Create subgraphs for each category
    node_counter = 0
    category_nodes = {}
    
    for category, services in service_groups.items():
        safe_category = category.replace(" ", "_").replace("&", "and")
        diagram.append(f"    subgraph {safe_category} [\"{category}\"]")
        category_nodes[category] = []
        
        for service in services:
            node_id = f"node{node_counter}"
            # Shorten service names for better display
            display_name = service.replace("Azure ", "").replace("Microsoft ", "")
            if len(display_name) > 25:
                display_name = display_name[:22] + "..."
            
            diagram.append(f"        {node_id}[\"{display_name}\"]")
            category_nodes[category].append(node_id)
            node_counter += 1
        
        diagram.append("    end")
    
    # Add relationships between categories
    for source_category, target_categories in flow_relationships.items():
        if source_category in service_groups:
            for target_category in target_categories:
                if target_category in service_groups:
                    # Connect first node of source to first node of target
                    if (category_nodes.get(source_category) and 
                        category_nodes.get(target_category)):
                        source_node = category_nodes[source_category][0]
                        target_node = category_nodes[target_category][0]
                        diagram.append(f"    {source_node} --> {target_node}")
    
    # Add styling
    diagram.extend([
        "    classDef compute fill:#e1f5fe",
        "    classDef storage fill:#f3e5f5",
        "    classDef analytics fill:#e8f5e8",
        "    classDef security fill:#ffebee",
        "    classDef ai fill:#fff3e0"
    ])
    
    return "\n".join(diagram)

def validate_architecture_completeness(selected_services: List[Dict], requirements: Dict) -> Tuple[List[str], List[str], List[str]]:
    """Comprehensive architecture validation"""
    
    service_names = [svc["name"] for svc in selected_services]
    categories = [svc["category"] for svc in selected_services]
    industry = requirements.get("industry", "")
    
    critical_gaps = []
    warnings = []
    recommendations = []
    
    # Essential architecture components
    if "Security & Identity" not in categories:
        critical_gaps.append("❌ No identity and security services - Critical security risk")
        recommendations.append("Add Azure Active Directory and Azure Key Vault for basic security")
    
    if "Monitoring & Management" not in categories:
        critical_gaps.append("❌ No monitoring solution - Cannot observe system health")
        recommendations.append("Add Azure Monitor and Application Insights for observability")
    
    # Data architecture validation
    has_storage = any("Storage" in cat or "Database" in cat for cat in categories)
    has_analytics = "Analytics & BI" in categories
    
    if has_analytics and not has_storage:
        warnings.append("⚠️ Analytics services without adequate storage layer")
        recommendations.append("Consider Azure Data Lake Storage for analytics workloads")
    
    # Networking validation
    has_compute = any(cat in ["Compute", "Containers"] for cat in categories)
    has_networking = "Networking" in categories
    
    if has_compute and not has_networking:
        warnings.append("⚠️ Compute services without network isolation")
        recommendations.append("Add Azure Virtual Network for security isolation")
    
    # High availability validation
    critical_services = [svc for svc in selected_services 
                        if svc.get("architectural_importance") == "critical"]
    
    if len(critical_services) > 2 and not any("load_balancer" in svc.get("use_cases", []) 
                                              for svc in selected_services):
        warnings.append("⚠️ No load balancing for high availability")
        recommendations.append("Consider Azure Load Balancer or Application Gateway")
    
    # Industry-specific validation
    if industry in INDUSTRY_COMPLIANCE:
        industry_reqs = INDUSTRY_COMPLIANCE[industry]
        missing_required = [svc for svc in industry_reqs["required_services"] 
                           if svc not in service_names]
        
        if missing_required:
            critical_gaps.append(f"❌ Missing required {industry} services: {', '.join(missing_required)}")
    
    # DevOps validation
    has_devops = "DevOps & Developer Tools" in categories
    if has_compute and not has_devops:
        recommendations.append("Consider adding CI/CD tools like Azure DevOps or GitHub Actions")
    
    # Cost optimization suggestions
    high_cost_services = [svc for svc in selected_services if svc.get("cost_tier") == "high"]
    if len(high_cost_services) > 3:
        warnings.append("⚠️ High number of expensive services - Review cost optimization")
        recommendations.append("Consider serverless alternatives for variable workloads")
    
    return critical_gaps, warnings, recommendations

# Streamlit UI Implementation
def main():
    st.title("🏗️ Azure Solution Architect Pro")
    st.markdown("*Comprehensive Azure architecture recommendations for enterprise solutions*")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📋 Requirements Gathering")
        
        # Use case description
        use_case = st.text_area(
            "Describe your use case and goals:",
            placeholder="e.g., Build a modern data platform for real-time analytics with AI capabilities...",
            height=100
        )
        
        # Industry selection
        industry = st.selectbox(
            "Industry:",
            [""] + list(INDUSTRY_COMPLIANCE.keys()),
            format_func=lambda x: INDUSTRY_COMPLIANCE[x]["name"] if x else "Select industry..."
        )
        
        # Team and scale information
        st.subheader("📊 Scale & Requirements")
        team_size = st.slider("Team size:", 1, 100, 10)
        expected_users = st.slider("Expected users:", 100, 100000, 1000, step=100)
        data_volume = st.slider("Data volume (GB):", 10, 10000, 500, step=50)
        
        # Capabilities selection
        st.subheader("🎯 Capabilities Needed")
        capabilities = {}
        
        capability_categories = {
            "Data & Analytics": [
                "Data Warehousing", "Real-time Analytics", "Business Intelligence", 
                "ETL/Data Integration", "Big Data Processing"
            ],
            "AI & Machine Learning": [
                "Machine Learning", "Generative AI", "Computer Vision", 
                "Natural Language Processing", "Predictive Analytics"
            ],
            "Application Platform": [
                "Web Applications", "APIs", "Microservices", "Serverless", 
                "Mobile Backend", "Integration"
            ],
            "Infrastructure": [
                "Containers", "Virtual Machines", "DevOps/CI-CD", 
                "Monitoring", "Security", "Networking"
            ],
            "Specialized": [
                "IoT", "Edge Computing", "Blockchain", "Gaming", 
                "Content Delivery", "Backup & DR"
            ]
        }
        
        for category, caps in capability_categories.items():
            with st.expander(f"{category}"):
                for cap in caps:
                    capabilities[cap] = st.checkbox(cap, key=f"cap_{cap}")
        
        # Compliance requirements
        if industry:
            st.subheader("🔒 Compliance")
            industry_info = INDUSTRY_COMPLIANCE[industry]
            st.info(f"**{industry_info['name']}** requires: {', '.join(industry_info['compliance_frameworks'])}")
        
        # Generate recommendations button
        generate_recommendations = st.button("🚀 Generate Architecture", type="primary", use_container_width=True)
    
    # Main content area
    if generate_recommendations and use_case:
        requirements = {
            "use_case": use_case,
            "industry": industry,
            "capabilities": capabilities,
            "team_size": team_size,
            "expected_users": expected_users,
            "data_volume_gb": data_volume
        }
        
        # Get Azure services and calculate scores
        all_services = get_comprehensive_azure_services()
        
        with st.spinner("🔍 Analyzing requirements and generating recommendations..."):
            scored_services = []
            architecture_context = {"selected_services": []}
            
            for service in all_services:
                score, score_breakdown = calculate_comprehensive_score(service, requirements, architecture_context)
                if score > 10:  # Minimum threshold
                    service_copy = service.copy()
                    service_copy["total_score"] = score
                    service_copy["score_breakdown"] = score_breakdown
                    scored_services.append(service_copy)
            
            # Sort and select top services
            scored_services.sort(key=lambda x: (-x["total_score"], x["name"]))
            top_services = scored_services[:15]  # Top 15 services
            
            # Update context with selected services
            architecture_context["selected_services"] = [svc["name"] for svc in top_services]
            
            # Detect architecture patterns
            detected_patterns = detect_architecture_patterns(
                architecture_context["selected_services"], 
                requirements
            )
            
            # Generate cost analysis
            cost_analysis = generate_cost_analysis(top_services, requirements)
            
            # Validate architecture
            critical_gaps, warnings, recommendations_list = validate_architecture_completeness(
                top_services, requirements
