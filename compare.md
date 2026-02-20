# Compare Managed Private Endpoints (MPE) vs Data Connection Rules vs Gateways in Microsoft Fabric

Below is a clear, customer‑ready comparison of **Managed Private Endpoints (MPE)** vs **Data Connection Rules** vs **Gateways** in **Microsoft Fabric**, focused on **networking model**, **workload support**, **security posture**, and **when to use each**. [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)

---

## 1) Managed Private Endpoints (MPE)

### What it is
**Managed Private Endpoints** are workspace-admin managed connections that let certain Fabric workloads securely reach data sources that are behind a firewall or blocked from public internet access, without you building/owning the network plumbing yourself. [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)

### Networking model (how traffic flows)
- Uses **Azure Private Link semantics** from a **Fabric-managed** network boundary (Fabric manages the underlying networking for the endpoint). [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[3](https://blog.fabric.microsoft.com/en-us/blog/introducing-managed-private-endpoints-for-microsoft-fabric-in-public-preview?ft=All)
- Designed to keep connectivity **private** vs using public endpoints. [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)

### Workload support (where it works)
- ✅ **Fabric Data Engineering (Spark-based) items** such as notebooks and Spark job definitions. [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[4](https://learn.microsoft.com/en-us/fabric/security/connect-to-on-premise-sources-using-managed-private-endpoints)
- ⚠️ **Eventstream** support exists but is described as workload-specific (preview/limitations apply). [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)
- ❌ **Not a reliable solution for “Copy Data”** scenarios in Fabric Data Factory (many copy experiences still behave as if they need a gateway/public access). [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)

### Security posture
- Strongest option when the goal is **private network isolation** (no public exposure), assuming your scenario is supported (primarily Spark). [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[4](https://learn.microsoft.com/en-us/fabric/security/connect-to-on-premise-sources-using-managed-private-endpoints)
- Governance model: workspace admin creates the request; resource owner/admin approves it. [4](https://learn.microsoft.com/en-us/fabric/security/connect-to-on-premise-sources-using-managed-private-endpoints)[1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)

### When to use (rule of thumb)
Use MPE when:
- You’re doing **Spark / Data Engineering** ingestion or processing and need private connectivity to locked-down sources. [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[4](https://learn.microsoft.com/en-us/fabric/security/connect-to-on-premise-sources-using-managed-private-endpoints)
- You want to avoid deploying/operating gateway infrastructure. [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)

---

## 2) Data Connection Rules

### What it is
**Data Connection Rules** are **policy controls** that govern outbound connectivity from a workspace to external resources by allowing/denying access through specific connection methods (for example, through approved connectors or gateways). [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)

### Networking model (how traffic flows)
- Policy-based outbound control rather than “private endpoint per resource.” [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)
- Intended to allow admins to **block by default and allow by exception** for certain outbound paths. [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)

### Workload support (where it works)
- ✅ Primarily for **Data Factory workloads** and **mirrored databases** (per the Fabric outbound access protection model). [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)
- ❌ Not the mechanism used for Spark’s private connectivity (that’s where MPE fits). [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)[1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)

### Security posture
- Strong for **governance** (controlling which connectors/paths are permitted). [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)
- Not equivalent to private networking by itself; it’s about **restricting/allowlisting outbound connectivity**. [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)

### When to use (rule of thumb)
Use Data Connection Rules when:
- Your main need is **Data Factory** connectivity governance (especially when outbound access protection is enabled). [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)
- You need to centrally manage which connectors and connection paths are permitted for pipelines/mirroring. [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)

---

## 3) Gateways (On-premises Data Gateway)

### What it is
A **gateway** is customer-managed connectivity software that enables Fabric services (commonly “Copy Data”) to reach data sources that are otherwise not directly reachable (for example, due to private networking or firewall restrictions). [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)

### Networking model (how traffic flows)
- The gateway runs in your environment and brokers connections outward to the service (typical pattern: outbound connectivity from the gateway host). [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)

### Workload support (where it works)
- ✅ Commonly required/used for **Copy Data** scenarios where private endpoints or locked-down sources are involved and MPE isn’t honored by the copy experience. [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)

### Security posture
- Good when you need to keep sources private and don’t have a supported Private Link path for that workload (especially pipelines). [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)
- Tradeoff: you must operate and secure the gateway host(s) yourself. [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)

### When to use (rule of thumb)
Use a Gateway when:
- You must use **Data Factory “Copy Data”** against private/on-prem sources and the platform behavior indicates it won’t connect via MPE alone. [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)

---

## Quick decision guide

1. **Are you using Spark (Data Engineering) to access the source?**  
   - Yes → Prefer **Managed Private Endpoints (MPE)**. [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[4](https://learn.microsoft.com/en-us/fabric/security/connect-to-on-premise-sources-using-managed-private-endpoints)

2. **Are you using Data Factory “Copy Data” / pipeline copy activities?**  
   - Yes → Plan for **Data Connection Rules** (governance) and potentially a **Gateway** depending on the source and connectivity constraints. [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)[5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)

3. **Is private connectivity mandatory and the workload is pipeline-based?**  
   - Expect **Gateway** patterns to be required in many real-world cases today. [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)

---

## Key takeaway (customer-ready)

- **MPE** is the strongest private networking option, but it is primarily aligned with **Spark/Data Engineering** workloads. [1](https://learn.microsoft.com/en-us/fabric/security/security-managed-private-endpoints-overview)[4](https://learn.microsoft.com/en-us/fabric/security/connect-to-on-premise-sources-using-managed-private-endpoints)  
- **Data Connection Rules** provide governance for outbound connectivity in **Data Factory** scenarios. [2](https://learn.microsoft.com/en-us/fabric/security/workspace-outbound-access-protection-overview)  
- **Gateways** remain the practical tool for many **Copy Data** scenarios that must reach private/on-prem sources. [5](https://community.fabric.microsoft.com/t5/Fabric-platform/Managed-private-endpoint-and-Azure-SQL-Database/m-p/4367250)
