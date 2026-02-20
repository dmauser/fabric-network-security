# Microsoft Fabric Network Security


## Getting started

More detailed instructions are coming soon. For now, to get the most out of this repo:

1. **Fork** this repository to your GitHub account.
2. **Clone** your fork locally.
3. Open the folder in **Visual Studio Code**.
4. Install the `Excalidraw` editor extension for VS Code:  
    [Excalidraw Editor (VS Code Marketplace)](https://marketplace.visualstudio.com/items?itemName=pomdtr.excalidraw-editor)

After installing, you can open and visualize/edit any `.excalidraw` diagrams directly in VS Code.

### 🧩 Microsoft Fabric Connectivity — What Works with MPE vs Data Gateways

---

## Managed Private Endpoints (MPE) ✔️

**Supported workloads & item types** (workspace-level; subject to region/capacity availability)  
- **Data Engineering (Spark)**  
  - Notebooks (Spark & Python runtimes) [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-data-engineering)  
  - Spark job definitions [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-data-engineering)  
  - Lakehouses [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-data-engineering)  
  - Environments (called out under Data Engineering outbound access protection) [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-data-engineering)  
- **Eventstream** (supported as a workload; details/limitations are workload-specific) [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)  
- **OneLake workloads** (MPE is the mechanism used for OneLake connectivity under outbound access protection) [3](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)  

**Important notes / limitations**  
- MPE availability is tied to regions where **Fabric Data Engineering workloads** are available, and there are limitations (for example, OneLake shortcuts not yet supporting some MPE scenarios). [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)  

**Supported data sources (examples mentioned by Microsoft)**  
- Azure Storage, Azure SQL Database, Azure Synapse Analytics, Azure Cosmos DB, Azure Key Vault, and more (varies by supported data sources list). [4](https://blog.fabric.microsoft.com/en-us/blog/introducing-managed-private-endpoints-for-microsoft-fabric-in-public-preview?ft=All)[1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)  

---

## Data Gateways ✔️

> Fabric “Copy Data” scenarios often rely on gateways when private networking isn’t natively used by the copy experience (for example, Azure SQL with public access disabled). [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)  

### 1️⃣ On‑premises Data Gateway

**Supported workloads & items (common usage in Fabric)**  
- Fabric **Data Factory** experiences such as **Copy Data / pipeline copy activities** for on-prem or restricted sources. [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)  

**When it’s typically needed**  
- When a source (e.g., Azure SQL with *Deny Public Network Access*) is private and the Copy Data experience does not utilize MPE end-to-end, a gateway may be required. [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)  

---

### 2️⃣ VNet Data Gateway (Managed VNet / Azure-managed pattern)

**Supported workloads & items (conceptual fit in Fabric)**  
- Used for **Data Factory** style data movement where execution needs to occur inside a **managed VNet** to reach private Azure resources (Private Endpoint patterns). [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)  

> Note: Microsoft’s Fabric documentation formally positions **Data connection rules** (not MPE) as the governance mechanism for **Data Factory workloads and mirrored databases**, while MPE is positioned for **Data Engineering and OneLake** workloads. This is why gateways/VNet-managed execution patterns show up most often in pipeline-based connectivity designs. [3](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)  

---

## 🧠 Summary by Fabric Feature

- **Spark & Data Engineering** → **Managed Private Endpoints (MPE)** [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-data-engineering)  
- **Lakehouses** → **Managed Private Endpoints (MPE)** [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-data-engineering)  
- **OneLake workloads** → **Managed Private Endpoints (MPE)** (as the MPE mechanism under outbound access protection) [3](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)  
- **Eventstream** → **Managed Private Endpoints (MPE)** (workload-specific) [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)  
- **Pipelines / Copy Data** → **Data Gateways** (commonly required in private-source scenarios) [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)  
- **Mirrored Databases** → Governed via **Data connection rules** (and may require gateway-managed connectivity paths depending on source) [3](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)  

---

## ✅ How to Choose

- Use **Managed Private Endpoints** when working with **Spark-based Data Engineering** (and related OneLake scenarios) where you need true private connectivity without gateway infrastructure. [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[3](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)  
- Use **Data Gateways** for **pipeline-based data movement (Copy Data)** when the source is private/on‑prem and Copy Data does not natively use MPE for that connection. [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)  

---

## 🔗 Reference Links

- Overview of managed private endpoints for Fabric (supported item types + limitations):  
  https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)

- Workspace outbound access protection overview (MPE for Data Engineering/OneLake; DCR for Data Factory/mirroring):  
  https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview [3](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)

- Workspace outbound access protection for data engineering (explicit supported item types like notebooks/lakehouses/Spark job definitions/environments):  
  https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-data-engineering [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-data-engineering)

- Fabric blog: Introducing Managed Private Endpoints (examples of supported Azure data sources):  
  https://blog.fabric.microsoft.com/en-us/blog/introducing-managed-private-endpoints-for-microsoft-fabric-in-public-preview [4](https://blog.fabric.microsoft.com/en-us/blog/introducing-managed-private-endpoints-for-microsoft-fabric-in-public-preview?ft=All)

- Fabric Community thread (Copy Data + Azure SQL private endpoint limitation; gateway required in that scenario):  
  https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250 [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)