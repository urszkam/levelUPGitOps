# 📊 Proof of Implementation – Cloud Monitoring & Logging  
### levelUPGitOps Project (LVL UP Program, Perspektywy Foundation)

---

## 🎯 Purpose  

This document provides **evidence of the successful implementation** of Cloud Logging and Cloud Monitoring within the *levelUPGitOps* project on Google Cloud Platform (GCP).  
It demonstrates that observability components: logs, metrics, dashboards, and alerts - are properly configured and integrated with the GKE environment.

---

## 🧾 Implementation Proofs  

### 1. Proof: Cloud Logging - Logs Explorer  

![Cloud Logging Proof](01_Cloud_Logging_Logs_Explorer.png)

Screenshot from **Logs Explorer** confirming active collection of over **42,000 system logs** (Kubernetes Apiserver, `kube-system`) from the **GKE cluster**.  
This validates that **Cloud Logging** is fully integrated with **Google Kubernetes Engine**, providing real-time access to system and application events.

---

### 2. Proof: Custom Log-Based Metrics (5xx Errors & Request Count)  

![Custom Metrics List Proof](02_Monitoring_Custom_Metrics.png)

Screenshot from the **Log-Based Metrics** section confirming the correct configuration of two custom counters:

- **`app_errors_5xx`** - counts all HTTP 5xx errors to monitor backend reliability and feed alerting policies.  
- **`app_request_count`** - counts all successful HTTP 200 requests to measure application traffic and load.  

This confirms that key metrics for tracking **application reliability and error rate** have been successfully implemented.

---

### 3. Proof: GKE Application Health Dashboard  

![GKE Dashboard Proof](03_Monitoring_Custom_Dashboard.png)

A custom **Cloud Monitoring dashboard** titled *“levelUPGitOps - GKE Application Health”* was created to visualize live metrics for the Kubernetes environment.

The dashboard includes key indicators:  
- **CPU usage time** – container CPU consumption.  
- **Memory usage** – container memory utilization.  
- **Container restarts** – instability or crash detection.  

This confirms that Cloud Monitoring provides **comprehensive visibility** into the system’s operational performance.

---

### 4. Proof: Alert Policy Configuration (Pod Restarts)  

![Alert Policy Proof](04_Monitoring_Alert_Policy_Example.png)

An **alerting policy** was configured to automatically notify the team when system instability occurs.

- **Policy Name:** `GKE Pod Restart Alert`  
- **Metric:** `Kubernetes Container – Restart count`  
- **Condition:** Triggered when the number of container restarts exceeds **3 restarts within a 5-minute window**.  

This closes the observability loop by providing **proactive system alerts** and fulfilling the alerting requirements.

---

## ✅ Summary  

The monitoring and logging setup demonstrates:  
- Active **log collection** from all Kubernetes components.  
- Functioning **custom metrics** for both successful and failed requests.  
- **Dashboard visualization** of system performance.  
- **Alert policies** for proactive issue detection.  

This confirms that the *levelUPGitOps* project fulfills the **DevOps observability principles**, ensuring transparency, reliability, and measurable system health.

---

## 👩‍💻 Authors  

*levelUPGitOps Team – Project 9, Group 4 (LVL UP Program, Perspektywy Foundation)*  

- **Justyna Gajdek** – Monitoring & Observability  
- **Joanna Kogut** – CI/CD & Cloud Build  
- **Urszula Kamińska** – Application Development  
- **Magdalena Krupa** – Infrastructure (GKE)  
- **Natalia Wróbel** – IAM & Security  
