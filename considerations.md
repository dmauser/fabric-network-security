# Microsoft Fabric Connectivity — Summary and Recap

This document summarizes how **Microsoft Fabric connects to private and on‑premises data sources**, and clarifies **when to use Managed Private Endpoints (MPE), Data Connection Rules, and Data Gateways**.  
The key takeaway is that **the correct option depends primarily on which Fabric workload is being used**.

---

## 1. The Core Question

**How does Microsoft Fabric securely access private or on‑premises data sources, and which connectivity option should be used in each scenario?**

The answer depends less on the data source itself and more on **which Fabric workload is performing the access**:

- **Spark / Data Engineering workloads**
- **Data Factory / Copy Data workloads**

These workloads use **different network planes** inside Fabric.

---

## 2. Managed Private Endpoints (MPE)

### What they are

Managed Private Endpoints are **Fabric‑managed outbound private endpoints** built on **Azure Private Link / Private Link Service**.  
Fabric owns and manages:

- The virtual network
- DNS resolution
- Endpoint lifecycle

No customer‑managed networking infrastructure is required.

---

### Where MPEs work best

✅ **Fabric Data Engineering (Spark workloads)**

- Spark notebooks  
- Spark job definitions  
- Lakehouse ingestion  
- Secure access to Azure or on‑prem sources exposed via Private Link Service  

---

### Key characteristics

- No public internet exposure  
- True Private Link connectivity  
- No gateways or agents  
- Strong alignment with Zero Trust and regulated environments  

---

### Major limitation

❌ **Data Factory “Copy Data” activities do not reliably use Managed Private Endpoints**

As a result, MPEs should **not** be assumed to work for pipeline‑based data copy scenarios.

---

### Bottom line

> Managed Private Endpoints are the **preferred and strategic connectivity model** in Fabric today, but they are **Spark‑first**, not pipeline‑first.

---

## 3. Data Connection Rules (DCR)

### What they are

Data Connection Rules are **policy‑based outbound access controls** used by **Fabric Data Factory workloads**.  
They allow administrators to:

- Explicitly permit specific connectors
- Control which external services can be accessed

They **do not create private network paths**.

---

### Where they apply

✅ Fabric Data Factory workloads  
- Copy Data  
- Mirrored databases  

❌ Not used by Spark or Data Engineering workloads

---

### What they are not

- Not Private Link  
- Not network isolation  
- Not suitable for private‑only connectivity requirements  

---

### Bottom line

> Data Connection Rules are about **governance and control**, not private networking.  
> They exist because **Copy Data does not natively support Private Link today**.

---

## 4. Data Gateways

Data Gateways exist to bridge the gap between **Fabric Copy Data** and **private or on‑premises data sources**.

There are two main gateway models.

---

## 4.1 On‑premises Data Gateway

### What it is

A **Windows‑based agent** installed on:

- A physical on‑prem server  
- A VM (on‑prem or cloud)  
- A secured internal or DMZ network  

This is the same gateway family used by Power BI.

---

### Network model

- Outbound HTTPS (TCP 443) from the gateway to Fabric  
- No inbound firewall rules required  
- No Private Link involved  

---

### Used for

✅ Fabric Data Factory (Copy Data)  
✅ On‑premises data sources  
✅ Highly locked‑down environments  

---

### Tradeoffs

- Requires customer‑managed infrastructure  
- Requires HA and scaling planning  
- Windows‑only  
- Higher operational overhead  

---

### When to use

> When Copy Data must access on‑prem or private systems and Private Link is not supported.

---

## 4.2 VNet Data Gateway

### What it is

A **Microsoft‑managed gateway deployed inside an Azure Virtual Network**, conceptually similar to Azure Data Factory’s Managed VNet Integration Runtime.

---

### Network model

- Gateway runs inside an Azure VNet  
- Connects to private endpoints or service endpoints  
- No customer‑managed VM required  

---

### Used for

✅ Fabric Data Factory (Copy Data)  
✅ Azure PaaS or IaaS with public access disabled  

---

### Tradeoffs

- Azure‑only  
- Still gateway‑based (not Spark, not MPE)  
- Less “pure” than Private Link, but simpler than on‑prem gateways  

---

### When to use

> When the data source is in Azure, private‑only, and Copy Data is required without deploying a VM.

---

## 5. How Everything Fits Together

### Two connectivity planes in Fabric

#### Spark / Data Engineering plane

- Uses **Managed Private Endpoints**  
- True Private Link connectivity  
- No gateways  
- Strategic long‑term direction  

#### Pipeline / Data Factory plane

- Uses **Gateways or Data Connection Rules**  
- Gateway‑based connectivity  
- More mature and broadly compatible  
- Less network‑pure  

---

## 6. Decision Cheat Sheet

Ask these questions in order:

1. **Is this Spark or Copy Data?**  
   - Spark → Managed Private Endpoints  
   - Copy Data → Gateway or Data Connection Rules  

2. **Where is the data source?**  
   - On‑prem → On‑prem Data Gateway  
   - Azure private → VNet Data Gateway  

3. **Is customer‑managed infrastructure acceptable?**  
   - No → Spark + Managed Private Endpoints  
   - Yes → Gateway  

---

## 7. Common Real‑World Pattern

Most enterprise customers land on a **hybrid approach**:

- **Spark + Managed Private Endpoints** for secure ingestion  
- **Pipelines** for orchestration and downstream movement  

This balances:

- Security requirements  
- Platform maturity  
- Operational reality  

---

## 8. Final Takeaway

> **Managed Private Endpoints represent the long‑term direction for Fabric networking.**  
> **Gateways still exist because Copy Data has not fully transitioned to Private Link yet.**  
> Today, **both models are required**, depending on the workload.