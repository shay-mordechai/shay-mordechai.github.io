# Shay Mordechai | Application Security & Security Research Portfolio

[![Portfolio](https://img.shields.io/badge/Portfolio-Live-38bdf8?style=flat-square&logo=githubpages&logoColor=fff)](https://shay-mordechai.github.io)
[![AppSec Focus](https://img.shields.io/badge/Domain-Application%20Security-0ea5e9?style=flat-square&logo=security&logoColor=fff)](https://shay-mordechai.github.io)
[![Rust](https://img.shields.io/badge/Rust-Safe%20Systems-dea584?style=flat-square&logo=rust&logoColor=fff)](https://www.rust-lang.org/)
[![Python](https://img.shields.io/badge/Python-Security%20Tooling-3776ab?style=flat-square&logo=python&logoColor=fff)](https://www.python.org/)
[![Envoy & Wasm](https://img.shields.io/badge/Envoy%2FWasm-DLP%20Proxy-252627?style=flat-square&logo=envoyproxy&logoColor=fff)](https://www.envoyproxy.io/)
[![Linux Security](https://img.shields.io/badge/Linux-Sandboxing%20&%20OSTree-fcc624?style=flat-square&logo=linux&logoColor=000)](https://www.kernel.org/)

Welcome to my professional **Application Security (AppSec) Engineering & Security Research** repository. This portfolio chronicles advanced vulnerability research, runtime defense implementations, low-level binary analysis, and secure architecture designs—transitioning from deep reverse engineering and malware analysis to enterprise-grade Application Security and DevSecOps.

---

## 🚀 Flagship Disclosures & Research Highlights

- **CERT-IL #11265 (Compiler Trust Boundaries):** Behavioral research on SBCL and compiler-level execution boundaries, uncovering memory safety and trust violation patterns in dynamic code compilation.
- **OpenAI / Bugcrowd (AI Guardrail & Quota Enforcement Bypass):** Research into LLM session quota enforcement mechanisms, compute exhaustion vectors, and privilege escalation vulnerabilities in AI agent workflows.
- **Digital Whisper #187 (Android Bootstrap Hijacking):** Deep-dive analysis into early process initialization vulnerabilities in Android, evaluating Trust Boundaries and Binder transaction security.
- **High-Performance Envoy Wasm DLP Filter (Rust):** Engineered a sub-15ms proxy filter using Rust and WebAssembly for real-time JSON PII redaction and zero-trust API traffic governance.

---

## 📚 Categorized Articles & Technical Writeups

### 1. AI Security, Guardrails & SaaS Architecture
*Focusing on LLM security, trust boundaries, multi-tenant isolation, and zero-trust SaaS design.*

| Title & Link | Date | Primary Tech | Key AppSec Takeaway |
| :--- | :---: | :---: | :--- |
| [Browser Privilege Boundary: כש-AI הופך לסוכן](blog/he/browser-privilege-boundary.html) | May 2026 | AI Agents, DOM, Sandbox | Analyzing security risks in browser-based AI agents, focusing on broken trust boundaries and autonomous interface exploitation. |
| [Zero Trust AI SaaS Architecture](blog/he/myleads-saas-architecture.html) | — | Zero Trust, SaaS, AuthZ | Designing zero-trust multi-tenant SaaS architectures with strict privilege separation and rigorous AI workload verification. |
| [Data Hop Firewall (Rust & Envoy)](blog/he/rust-envoy-tunnel.html) | Mar 2026 | Rust, Envoy, Wasm | Implementing network security architecture and traffic inspection policies using Envoy and Rust for endpoint and API protection. |

### 2. Web, API & Network Security
*Focusing on API security, TLS inspection, traffic interception, and origin policy enforcement.*

| Title & Link | Date | Primary Tech | Key AppSec Takeaway |
| :--- | :---: | :---: | :--- |
| [Scapy TLS Packet Crafter](blog/he/scapy-tls-packet-crafter.html) | — | Python, Scapy, TLS | Constructing custom TLS packet generators to test cryptographic protocol resilience and perform vulnerability analysis. |
| [Multi-Stage Network CTF](blog/he/multistage-network-ctf.html) | — | Networking, CTF, Routing | Solving multi-stage network penetration challenges demonstrating security architecture and isolated network traversal. |
| [Life of a Packet: Routing Internals](blog/he/life-of-a-packet-routing.html) | — | Linux Networking, BPF | Analyzing packet routing mechanics to understand network attack vectors, traffic monitoring, and routing anomaly detection. |
| [DNS Rebinding Mitigation](blog/he/pt-dns-rebinding-mitigation.html) | — | DNS, Same-Origin Policy | Developing mitigation mechanisms against DNS Rebinding attacks to enforce SOP and prevent unauthorized internal resource access. |
| [Web Registration Diagnostic](blog/he/pt-web-registration-diagnostic.html) | — | Web Security, OWASP Top 10 | Diagnosing web application registration endpoints, identifying business logic flaws and access control bypasses. |

### 3. Mobile AppSec & Dynamic Instrumentation
*Focusing on mobile runtime security, Frida instrumentation, root/tamper detection, and inter-component communication (ICC).*

| Title & Link | Date | Primary Tech | Key AppSec Takeaway |
| :--- | :---: | :---: | :--- |
| [★ Android Bootstrap Hijacking](blog/he/android-bootstrap-hijacking.html) | May 2026 | Android, Native, Binder | Deep analysis of early process initialization vulnerabilities, focusing on trust boundary violations and component loading flaws. |
| [🔬 Android Malware Reverse Engineering Lab](https://github.com/shay-mordechai/malware-reversing-labs) | — | Java, Smali, Jadx | Structured lab environment for reverse engineering Android malware, demonstrating behavioral analysis of mobile threats. |
| [The Permission Paradox](blog/he/permission-paradox.html) | May 2026 | Android, Permissions | Critical evaluation of the Android permissions model, highlighting access control gaps and over-privileged components. |
| [Frida in Race - UnCrackable Level 2](blog/he/frida-in-race-level2.html) | Apr 2026 | Frida, Native, Anti-Tamper | Advanced research on bypassing anti-tampering defenses and race conditions using dynamic instrumentation frameworks. |
| [UnCrackable Level 2 - Mobile Security Writeup](blog/he/uncrackable-level2.html) | Apr 2026 | Android, Root Detection | Analysis of anti-debugging and code integrity checks in mobile apps, requiring rigorous risk assessment of root detection. |
| [UnCrackable Level 1 - Mobile Security Writeup](blog/he/uncrackable-level1.html) | Apr 2026 | Android, Jadx, Smali | Resolving basic Android security challenges demonstrating static and dynamic analysis, focusing on sensitive storage flaws. |
| [JNI as (Un-)Safe Bridge](blog/he/jni-unsafe-bridge.html) | Mar 2026 | JNI, C/C++, Java | Security assessment of the Java Native Interface (JNI), illustrating memory safety risks and trust boundary breaches. |

### 4. Low-Level Systems, Binary Analysis & Sandboxing
*Focusing on memory safety, compiler security, immutable operating systems, and process isolation.*

| Title & Link | Date | Primary Tech | Key AppSec Takeaway |
| :--- | :---: | :---: | :--- |
| [V8 Engine Execution & Sandbox Security](blog/he/v8-engine-security.html) | Dec 2025 | V8, JavaScript, Sandboxing | Investigating V8 execution sandboxing mechanisms, focusing on architectural vulnerability analysis and process isolation breaches. |
| [בניית סביבת Malware Analysis מבודדת עם Fedora Kinoite](blog/he/malware-lab-kinoite.html) | Dec 2025 | Fedora Kinoite, Podman, SELinux | Designing a secure, isolated malware analysis lab powered by immutable OS containers for absolute containment. |
| [Desktop RE Writeup: Multi-Stage DLL Decryption](blog/he/multi-stage-dll-re.html) | Apr 2024 | x86 ASM, IDA Pro, PE | Reverse engineering multi-stage DLL decryption mechanisms, demonstrating vulnerability analysis and binary inspection. |
| [Desktop RE Writeup: PE Extraction & Patching](blog/he/re-intro-patching.html) | Feb 2024 | PE Headers, C/C++, Patching | Practical research in PE extraction and binary patching for software resilience assessment and malicious code behavior analysis. |
| [Breaking the Compilation Boundary (SBCL)](blog/he/compiler-sbcl-behavioral-research.html) | Jul 2025 | Common Lisp, SBCL, Compilers | Behavioral research on compilation workflows and compiler-level security controls, demonstrating execution boundary breaches. |
| [Linux Internals: OSTree & Hibernation](blog/he/linux-internals-ostree-hibernation.html) | — | Linux Kernel, OSTree | Deep dive into Linux kernel internals (OSTree and hibernation), focusing on system integrity and memory state security. |
| [Flatpak Sandbox Isolation](blog/he/flatpak-sandbox-isolation.html) | — | Flatpak, cgroups, Bubblewrap | Evaluating Flatpak sandboxing and permissions mechanisms to assess isolation effectiveness against over-privileged apps. |

---

## 🗂️ Repository Structure

```tree
.
├── index.html                  # Root Landing Page (Portfolio & Timeline)
├── blog/
│   ├── he/                     # Hebrew Blog Vault & Articles
│   └── en/                     # English Blog Vault & Articles
├── assets/
│   ├── css/                    # Custom Stylesheets
│   └── js/                     # Frontend Scripts
└── scripts/                    # Automation & Portfolio Generation Scripts
    ├── build_timeline.py       # Timeline synchronization script
    └── sync_nested.py          # Vault synchronization script
```

---

## 🛠️ Local Development & Validation

To rebuild the portfolio vaults and synchronize timeline components across all vault directories:

```bash
# Run the timeline builder script
python3 scripts/build_timeline.py

# Run the vault synchronization script
python3 scripts/sync_nested.py
```

---

## 👤 Connect & Professional Profile

- **Portfolio Website:** [https://shay-mordechai.github.io](https://shay-mordechai.github.io)
- **GitHub:** [@shay-mordechai](https://github.com/shay-mordechai)
- **Focus:** Application Security, DevSecOps, Threat Modeling, Secure SDLC, and Cloud-Native Architecture.