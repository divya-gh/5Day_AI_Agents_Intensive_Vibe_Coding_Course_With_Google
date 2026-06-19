              
              # Security: The Evolution to Secure Agentic Development
              
              
                ┌────────────────────────────────────────┐
                │     SECURE VIBE CODING AGENT STACK     │
                └────────────────────────────────────────┘

                         ▲
                         │ Active Agentic Defense
                         │ (Real-time detection & response)
                         │
                ┌────────────────────────────────────────┐
                │   LAYER 3: ACTIVE DEFENSE              │
                └────────────────────────────────────────┘

                         ▲
                         │ High-Velocity Execution Controls
                         │ (Monitor dynamic code execution)
                         │
                ┌────────────────────────────────────────┐
                │   LAYER 2: EXECUTION CONTROLS          │
                └────────────────────────────────────────┘

                         ▲
                         │ 7 Foundational Pillars
                         │ (The security harness)
                         │
                ┌────────────────────────────────────────┐
                │   LAYER 1: SECURITY HARNESS            │
                └────────────────────────────────────────┘

                         ▲
                         │ Effective Trust
                         │ (Continuous, context-aware)
                         │
                ┌────────────────────────────────────────┐
                │   CONTINUOUS TRUST MODEL               │
                └────────────────────────────────────────┘

                         ▲
                         │ Agentic Development Reality
                         │ (Agents can run code, call APIs,
                         │  modify systems autonomously)
                         │
                ┌────────────────────────────────────────┐
                │   AGENTIC SYSTEMS & VIBE CODING        │
                └────────────────────────────────────────┘

# The Foundation: The 7-Pillar Agent Security Architecture

                 ┌──────────────────────────────┐
                 │     7-PILLAR SECURITY        │
                 └──────────────────────────────┘

   ┌──────────────────────────────────────────────────────────┐
   │  P7: Governance – Compliance, audits, risk controls       │
   ├──────────────────────────────────────────────────────────┤
   │  P6: Observability – Logs, traces, anomaly detection      │
   ├──────────────────────────────────────────────────────────┤
   │  P5: IAM – Strong identities, JIT credentials             │
   ├──────────────────────────────────────────────────────────┤
   │  P4: Runtime – LLM firewalls, hooks, agent gateways       │
   ├──────────────────────────────────────────────────────────┤
   │  P3: Model – Secure prompts, rule files, instructions     │
   ├──────────────────────────────────────────────────────────┤
   │  P2: Data – Encryption, least privilege, safe vectors     │
   ├──────────────────────────────────────────────────────────┤
   │  P1: Infrastructure – Sandboxes, network controls         │
   └──────────────────────────────────────────────────────────┘

                 ▼  Forms the secure “agent harness” ▼

1. Infrastructure & Networking
Keep the agent’s execution environment locked down.

Run code in isolated sandboxes

Control what the agent can reach on the network

Prevent data from leaking out

2. Data
Protect the sensitive context the agent sees.

Encrypt data

Use least‑privilege access

Partition vector databases to prevent cross‑tenant poisoning

3. Model
Secure the agent’s “brain” and instructions.

Treat prompts and rule files like source code

Protect them from tampering or injection attacks

4. Application & Runtime
Control what the agent does while it’s running.

Use LLM firewalls

Add hooks before/after tool calls

Use gateways to prevent agents from calling each other freely

5. Identity & Access Management (IAM)
Give every agent a unique, cryptographic identity.

Prevent “confused deputy” attacks

Use ABAC + just‑in‑time, short‑lived credentials

6. Observability & Security Ops
Watch the agent continuously.

Logs, traces, metrics

Detect infinite loops or drift

Blue/Red/Green teams simulate attacks and quarantine issues

7. Governance
Ensure agents follow laws, policies, and compliance rules.

EU AI Act, risk assessments, audits

Plain‑language logic reviews

Digital signatures on agent outputs

---------------------------------------------------------

# Sandboxes & Supply Chain Defence (Pillars 1 & 4)
1. Why this matters
Vibe‑coded agents write code fast, test it, fix errors, and try again.
Because this code is generated on the fly, you can’t trust it by default.

### A. Sandboxes (Safe Execution Environments)
What’s the problem?
Generated code may:

Contain bugs

Be insecure

Try to access things it shouldn’t

Be tricked into running harmful commands

The solution
Run all agent‑generated code inside ephemeral, isolated sandboxes:

Temporary (reset every run)

No access to the host machine

No open network access

Tools run in hardened containers or gVisor‑style environments

👉 This ensures even bad or broken code cannot escape or persist.

B. Hallucinated Packages (Supply Chain Risk)
What’s the problem?
LLMs often “invent” fake package names.
Attackers see these hallucinations and upload malware using those exact names.

This trick is called slopsquatting.

The solution
Only install packages from trusted internal registries

Use cryptographic version pinning

CI/CD must verify:

SBOM entries

Digital signatures

Binary authorization

👉 This stops agents from accidentally pulling malware into your system.

C. Egress Governance (Network Safety)
What’s the problem?
Agents may:

Push unverified code to production

Leak sensitive data

Visit malicious websites

Download poisoned packages

Allowlists alone don’t work because prompt injections can hide inside webpages.

The solution
Agents should NOT browse the internet directly

All external data must come through:

Offline caches

Sanitized internal crawlers

Controlled proxies

👉 This prevents agents from touching the open internet or malicious content.

The Big Picture
Even with perfect sandboxes and supply chain controls, agents can still write bad logic or call dangerous internal tools.
So after securing the environment, we must secure the application layer next.

                   ┌──────────────────────────────────────┐
                   │   PILLARS 1 & 4: SAFE EXECUTION      │
                   │   (Sandboxes + Supply Chain Defence) │
                   └──────────────────────────────────────┘

                         ▼  WHY THIS MATTERS
        ┌────────────────────────────────────────────────────────┐
        │  Vibe-coded agents generate code fast, test it, fix it │
        │  and repeat. This code is unpredictable and cannot be  │
        │  trusted to run directly on real systems.              │
        └────────────────────────────────────────────────────────┘

                         ▼  CORE PROBLEM
        ┌────────────────────────────────────────────────────────┐
        │  Generated code may be buggy, insecure, or manipulated │
        │  by attackers. Agents may also hallucinate fake        │
        │  packages that attackers exploit.                      │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                         A. SANDBOXING                            │
     └──────────────────────────────────────────────────────────────────┘
                         ▼  SAFE EXECUTION
        ┌────────────────────────────────────────────────────────┐
        │  All agent-generated code runs inside:                 │
        │   • Ephemeral sandboxes                                │
        │   • Network-isolated containers                        │
        │   • Hardened runtimes (e.g., gVisor)                   │
        └────────────────────────────────────────────────────────┘

                         ▼  WHY
        ┌────────────────────────────────────────────────────────┐
        │  • Prevents host access                                │
        │  • Blocks persistence of bad code                      │
        │  • Resets state every run                              │
        │  • Contains vulnerabilities safely                     │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     B. SUPPLY CHAIN DEFENCE                      │
     └──────────────────────────────────────────────────────────────────┘
                         ▼  HALLUCINATED PACKAGES
        ┌────────────────────────────────────────────────────────┐
        │  LLMs invent fake package names. Attackers upload      │
        │  malware using those names (slopsquatting).            │
        └────────────────────────────────────────────────────────┘

                         ▼  DEFENCE
        ┌────────────────────────────────────────────────────────┐
        │  • Only use trusted internal registries                │
        │  • Cryptographic version pinning                       │
        │  • CI/CD verifies SBOM + signatures                    │
        │  • Binary Authorization blocks unverified artifacts    │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     C. EGRESS GOVERNANCE                         │
     └──────────────────────────────────────────────────────────────────┘
                         ▼  NETWORK RISK
        ┌────────────────────────────────────────────────────────┐
        │  Agents may:                                           │
        │   • Push unverified code                               │
        │   • Leak sensitive data                                │
        │   • Visit malicious sites                              │
        │   • Download poisoned packages                         │
        └────────────────────────────────────────────────────────┘

                         ▼  DEFENCE
        ┌────────────────────────────────────────────────────────┐
        │  • No direct internet access                           │
        │  • Use offline caches + sanitized crawlers             │
        │  • Force all traffic through controlled proxies        │
        └────────────────────────────────────────────────────────┘


                   ┌──────────────────────────────────────┐
                   │   BIG PICTURE                        │
                   └──────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  Sandboxes + supply chain controls protect the system, │
        │  but they don’t guarantee the agent writes good logic. │
        │  Next layer: secure the application itself.            │
        └────────────────────────────────────────────────────────┘

----------------------------------

## Securing Application Logic (Pillar 4)
1. Why this is a problem
Vibe coding focuses on making things work fast, not making them secure.
So AI‑generated apps often look fine (they run, no errors) but hide serious security issues.


A. Common Vulnerabilities
1. Sensitive logic ends up in the frontend
AI often puts:

API keys

Password checks

User permissions

directly in the browser.

👉 Anyone can open DevTools and steal or change them.

2. Backend security is missing
Because AI builds apps quickly, it often skips:

Row‑level database security

Access controls

Proper authentication

👉 This can expose private data to the public internet.

B. How to Fix It (Without Slowing Developers Down)
1. Don’t block developers inside the IDE
Hard-blocking insecure prompts frustrates developers and is easy to bypass.

2. Use IDE linters for gentle guidance
Give warnings and suggestions while coding.

3. Enforce real security in CI/CD
The pipeline should run:

SAST (Static code security checks)

SCA (Dependency vulnerability checks)

before anything reaches production.

👉 This catches insecure code after development but before deployment.

Vibe-coded apps often look correct but hide big security gaps, so we guide developers lightly in the IDE and enforce strict security checks in CI/CD to keep the final application safe.

                 ┌──────────────────────────────────────────┐
                 │   PILLAR 4: SECURING APPLICATION LOGIC   │
                 │        (Vibe-Coding Specific Risks)       │
                 └──────────────────────────────────────────┘

                         ▼  CORE ISSUE
        ┌────────────────────────────────────────────────────────┐
        │  Vibe coding prioritizes “make it work now” over       │
        │  “make it secure.” Generated apps often run fine but   │
        │  hide serious security flaws.                          │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     A. COMMON VULNERABILITIES                    │
     └──────────────────────────────────────────────────────────────────┘

                         ▼  1. FRONTEND OVER-TRUST
        ┌────────────────────────────────────────────────────────┐
        │  AI often puts sensitive logic in the browser:         │
        │   • API keys                                           │
        │   • Password checks                                    │
        │   • User permissions                                   │
        │  Anyone can read or modify these via DevTools.         │
        └────────────────────────────────────────────────────────┘

                         ▼  2. BACKEND UNDER-PROTECTED
        ┌────────────────────────────────────────────────────────┐
        │  AI-generated apps often skip:                         │
        │   • Row-level security                                 │
        │   • Access controls                                    │
        │   • Proper authentication                              │
        │  Result: private data exposed to the internet.         │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                   B. FIXING THE PROBLEM SAFELY                   │
     └──────────────────────────────────────────────────────────────────┘

                         ▼  1. IDE GUIDANCE (SOFT)
        ┌────────────────────────────────────────────────────────┐
        │  Use Developer Advisory Linters to warn developers      │
        │  about insecure patterns without blocking them.         │
        └────────────────────────────────────────────────────────┘

                         ▼  2. CI/CD ENFORCEMENT (HARD)
        ┌────────────────────────────────────────────────────────┐
        │  Real security checks happen in the pipeline:          │
        │   • SAST (static security scanning)                    │
        │   • SCA (dependency vulnerability scanning)            │
        │  Code must pass these before deployment.               │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │               BIG PICTURE                │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  Vibe-coded apps often “work” but aren’t secure.       │
        │  IDE gives gentle hints; CI/CD enforces strict rules.  │
        │  This keeps developer speed high and risk low.         │
        └────────────────────────────────────────────────────────┘


## Identity, Trust & High‑Stakes Actions (Pillar 5)

1. Give every agent its own identity
Agents should not share the same login or credentials.
Each agent gets a unique, trackable identity, so you always know which agent did what.

2. Prevent the “Confused Deputy” attack
Sometimes a hidden malicious instruction can trick an over‑privileged agent into doing something dangerous.
To stop this:

Agents must not use the developer’s permissions

They must use their own limited identity with very small, safe permissions

3. Zero Ambient Authority
Agents should never have broad access “just in case.”
Instead, they get:

Tiny, temporary permissions

Only for the exact task they’re doing

Automatically expire when the task ends

4. High‑risk actions need strong human approval
For dangerous actions (like touching production or money), the system must:

Require hardware MFA (touch a physical security key)

Show a plain‑English explanation (“Vibe Diff”) of what the agent is about to do

This ensures the human truly understands what they’re approving.


                 ┌──────────────────────────────────────────┐
                 │     PILLAR 5: IDENTITY & TRUST           │
                 │   (Securing High‑Stakes Agent Actions)    │
                 └──────────────────────────────────────────┘

                         ▼  CORE PROBLEM
        ┌────────────────────────────────────────────────────────┐
        │  Vibe-coded agents act broadly because prompts are     │
        │  vague (“fix the backend routing”). If they share the  │
        │  same long-lived identity as developers, a single      │
        │  prompt injection can trigger dangerous actions.       │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     A. UNIQUE AGENT IDENTITIES                   │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  WHY
        ┌────────────────────────────────────────────────────────┐
        │  Shared service accounts = huge internal risk.         │
        │  Each agent needs its own cryptographic identity       │
        │  (e.g., SPIFFE ID) so its actions are traceable.       │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                B. THE CONFUSED DEPUTY PROBLEM                    │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  WHAT IT IS
        ┌────────────────────────────────────────────────────────┐
        │  A malicious prompt (hidden in code, docs, repos)      │
        │  tricks an over‑privileged agent into doing something  │
        │  the attacker wants.                                   │
        └────────────────────────────────────────────────────────┘

                         ▼  FIX
        ┌────────────────────────────────────────────────────────┐
        │  Agents must NOT use human credentials.                │
        │  They authenticate with a separate “agentic identity”  │
        │  with tightly limited permissions.                     │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │             C. ZERO AMBIENT AUTHORITY + JIT DOWNSCOPING          │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  PRINCIPLE
        ┌────────────────────────────────────────────────────────┐
        │  Agents should never inherit broad admin rights.       │
        │  They get tiny, temporary permissions only for the     │
        │  exact task they’re doing.                             │
        └────────────────────────────────────────────────────────┘

                         ▼  HOW
        ┌────────────────────────────────────────────────────────┐
        │  • Fresh, short-lived tokens per task                  │
        │  • File-tree allowlists                                │
        │  • Deny-by-default access to secrets & prod configs    │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │            D. HIGH‑STAKES ACTIONS NEED HUMAN VERIFICATION        │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  WHY
        ┌────────────────────────────────────────────────────────┐
        │  Developers often approve code they don’t fully        │
        │  understand (“It works, ship it”).                     │
        └────────────────────────────────────────────────────────┘

                         ▼  DEFENCE: TWO STRONG GATES
        ┌────────────────────────────────────────────────────────┐
        │  1. Hardware MFA                                       │
        │     • Physical security key tap required               │
        │                                                        │
        │  2. The “Vibe Diff”                                    │
        │     • System explains the generated code in plain      │
        │       English before execution                         │
        │     • Ensures the human truly understands the action   │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │      BIG PICTURE (PILLAR 5)              │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  Agents get unique identities, minimal permissions,     │
        │  and require explicit human approval for dangerous      │
        │  actions. This prevents silent privilege escalation.    │
        └────────────────────────────────────────────────────────┘

-   ---------------------------------------------------------------

## Red/Blue/Green Teaming (Pillar 6)
Because vibe coding moves fast, security must move fast too:

Red Team attacks the system to find weaknesses

Blue Team monitors and defends

Green Team fixes and quarantines issues

All three run continuously using AI.




                 ┌──────────────────────────────────────────┐
                 │      PILLAR 6: AGENTIC SECOPS            │
                 │   (Red, Blue & Green Teaming)            │
                 └──────────────────────────────────────────┘

                         ▼  CORE ISSUE
        ┌────────────────────────────────────────────────────────┐
        │  Vibe-coded logic is generated, executed, and thrown   │
        │  away extremely fast. Traditional manual security       │
        │  cannot keep up.                                       │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     THE AGENTIC SECURITY TRIAD                   │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  BLUE TEAM (DEFENCE)
        ┌────────────────────────────────────────────────────────┐
        │  • Uses logs, traces, telemetry                        │
        │  • Detects anomalies & infinite loops                  │
        │  • Monitors agent behavior in real time                │
        └────────────────────────────────────────────────────────┘

                         ▼  RED TEAM (OFFENCE)
        ┌────────────────────────────────────────────────────────┐
        │  • Simulates attacks                                   │
        │  • Injects malicious prompts                           │
        │  • Tests agent boundaries & sandbox escape attempts    │
        └────────────────────────────────────────────────────────┘

                         ▼  GREEN TEAM (RECOVERY)
        ┌────────────────────────────────────────────────────────┐
        │  • Quarantines suspicious agents                       │
        │  • Rolls back unsafe states                            │
        │  • Restores safe configurations                        │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │      BIG PICTURE (PILLAR 6)              │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  Security must run at the same speed as vibe coding.   │
        │  Automated Red/Blue/Green teams provide continuous,     │
        │  real-time protection as agents generate and execute    │
        │  new logic.                                             │
        └────────────────────────────────────────────────────────┘


## Invisible Payloads & Red/Blue/Green Teaming

1. Invisible Payloads (Hidden Malware in Repos)
Attackers can hide malicious code inside repositories using tricks like:

Zero‑width characters

Look‑alike letters (homoglyphs)

These are invisible to humans but agents copy code so fast that the infection can spread across many files before anyone notices.

2. Red Team (Agent Attacker)
The Red Team is an AI attacker that:

Injects fake malicious instructions (“adversarial vibes”)

Hides harmful prompts inside long text blocks or RAG context

Tests whether your agent can be tricked into insecure behavior

This helps find vulnerabilities before real attackers do.

🌱 3. Blue Team (Agent Defender)
The Blue Team is an AI defender that:

Watches how the agent behaves in real time

Tracks what tools, data, and models it is using (AgBOM)

Flags weird behavior like infinite loops or unusual tool usage

It detects when an agent starts drifting into unsafe territory.


🌱 4. Green Team (Agent Fixer)
The Green Team is an AI fixer that:

Quarantines a compromised agent safely (without breaking systems)

Keeps its memory for investigation

Automatically rewrites the insecure code and gives the developer a safe version

It repairs issues without needing human intervention.

5. Small Batch Sizes + 3‑Phase Protection
To stay safe:

Agents must only make small code changes at a time

Tests and code cannot be edited together

The triad protects the agent across three phases:

Planner → checks the plan

Evaluator → reviews the reasoning

Executor → monitors the real action

🌱 6. Big Idea
Security must look inside the agent’s reasoning, not just the final code.
We need a full audit trail showing how a fuzzy human request turned into a real action.

                 ┌──────────────────────────────────────────┐
                 │   INVISIBLE PAYLOADS & REPO POISONING    │
                 └──────────────────────────────────────────┘

                         ▼  HIDDEN THREATS
        ┌────────────────────────────────────────────────────────┐
        │  Attackers hide malicious code inside repos using:     │
        │   • Zero‑width characters                              │
        │   • Look‑alike letters (homoglyphs)                    │
        │  These are invisible to humans but agents copy them    │
        │  instantly, spreading the infection across files.      │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     THE AGENTIC SECURITY TRIAD                   │
     └──────────────────────────────────────────────────────────────────┐


                         ▼  RED TEAM (ATTACKER)
        ┌────────────────────────────────────────────────────────┐
        │  • Acts like an AI attacker                            │
        │  • Injects malicious prompts (“adversarial vibes”)     │
        │  • Hides harmful instructions in long text blocks      │
        │  • Tests if your agent can be tricked                  │
        └────────────────────────────────────────────────────────┘


                         ▼  BLUE TEAM (DEFENDER)
        ┌────────────────────────────────────────────────────────┐
        │  • Watches agent behavior in real time                 │
        │  • Uses Agent Behavioral Analytics (ABA)               │
        │  • Tracks tools/data the agent is using (AgBOM)        │
        │  • Flags weird behavior (loops, unusual tool calls)    │
        └────────────────────────────────────────────────────────┘


                         ▼  GREEN TEAM (FIXER)
        ┌────────────────────────────────────────────────────────┐
        │  • Quarantines compromised agents safely               │
        │  • Keeps memory for investigation                      │
        │  • Auto‑refactors insecure code                        │
        │  • Sends the fixed version back to the developer       │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     SMALL BATCH EXECUTION                        │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  WHY
        ┌────────────────────────────────────────────────────────┐
        │  Agents must not generate huge code changes at once.   │
        │  Small batches + test-driven loops keep changes safe.  │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     3‑PHASE PROTECTION MODEL                     │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  1. PLANNER PHASE
        ┌────────────────────────────────────────────────────────┐
        │  Threat‑modeling skill checks the plan for flaws       │
        └────────────────────────────────────────────────────────┘

                         ▼  2. EVALUATOR PHASE
        ┌────────────────────────────────────────────────────────┐
        │  Evaluator reviews reasoning while Blue Team monitors  │
        │  for drift or anomalies                                │
        └────────────────────────────────────────────────────────┘

                         ▼  3. EXECUTOR PHASE
        ┌────────────────────────────────────────────────────────┐
        │  Green Team watches real tool execution and can        │
        │  quarantine or auto‑fix instantly                      │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │               BIG PICTURE                │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  Security must look inside the agent’s reasoning, not  │
        │  just the final code. The triad protects the agent at  │
        │  every step and reacts instantly to hidden threats.    │
        └────────────────────────────────────────────────────────┘

## Observability : Auditing Agent's mind

1. You must see inside the agent’s reasoning
Agents can look like they’re working fine even when they’re stuck in hallucination loops or burning money. So observability becomes a security requirement, not just an operations tool.

2. Track every step the agent takes
We build a “Vibe Trajectory” — a timeline of prompts, tool calls, RAG lookups, and code generation — so we can answer: “Why did the agent do that?”

3. Detect intent drift
Agents can slowly drift away from the user’s goal. Observability tools track this drift and reduce the agent’s trust score when behavior becomes unsafe.

4. Use checkpoints and circuit breakers
Before the agent makes changes, the system saves a checkpoint.
If the agent starts acting weird, a circuit breaker rolls everything back and freezes the agent safely.

5. Big idea
Observability turns the agent into a glass box, letting us audit, secure, and correct its internal reasoning in real time.

                 ┌──────────────────────────────────────────┐
                 │   OBSERVABILITY: AUDITING THE MIND       │
                 │              (Pillars 6 & 7)              │
                 └──────────────────────────────────────────┘

                         ▼  CORE PROBLEM
        ┌────────────────────────────────────────────────────────┐
        │  An agent may show “success” while secretly looping,   │
        │  hallucinating, or burning money (DoW attack).         │
        │  We must see inside its reasoning, not just outputs.   │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     A. VIBE TRAJECTORY                           │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  WHAT WE TRACK
        ┌────────────────────────────────────────────────────────┐
        │  • Prompts                                             │
        │  • Tool calls                                          │
        │  • RAG lookups                                         │
        │  • Code generation steps                               │
        │  • API usage + latency                                 │
        │  All combined into a chronological “Vibe Trajectory.”  │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     B. CONTENT SCANNING                          │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  WHY
        ┌────────────────────────────────────────────────────────┐
        │  Scan all dynamic code the agent retrieves or writes   │
        │  to catch hidden malicious snippets.                   │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     C. INTENT DRIFT & TRUST DECAY                │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  LIVE MONITORING
        ┌────────────────────────────────────────────────────────┐
        │  • Track AgBOM (tools/data the agent is using now)     │
        │  • Detect when the agent’s goals drift from the prompt │
        │  • Reduce trust score when behavior becomes unsafe     │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     D. CHECKPOINTS & CIRCUIT BREAKERS            │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  SAFETY MECHANISM
        ┌────────────────────────────────────────────────────────┐
        │  • Save a version checkpoint before changes            │
        │  • If trust drops too low → trip circuit breaker       │
        │  • Roll back safely + freeze agent for analysis        │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │               BIG PICTURE                │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  Observability turns the agent into a “glass box.”     │
        │  We see its reasoning, detect drift, stop bad actions, │
        │  and maintain a full audit trail for security & audits.│
        └────────────────────────────────────────────────────────┘

# Security Recap:

1. Sandbox everything
Always run AI‑generated code inside isolated sandboxes so bad code can’t escape or damage real systems. Scan dependencies to catch fake or vulnerable packages.

2. Shift security left
Use trusted internal registries and run strict security checks in CI/CD. IDE warnings help, but the pipeline must enforce the rules.

3. Zero Ambient Authority
Never give an agent broad access. Use tiny, temporary permissions (JIT tokens). For risky actions, show a plain‑English Vibe Diff and require hardware MFA.

4. Agentic SecOps
Use AI Red Teams to attack your system, Blue Teams to monitor behavior, and Green Teams to auto‑fix issues.

5. Trace everything
Log the agent’s reasoning, tool calls, and API usage. If it drifts from the task, roll back using checkpoints.

Big Idea
These controls make agents safe, but safety alone isn’t enough — next comes Agent Evaluation to measure whether the agent actually did what the user intended.


                 ┌──────────────────────────────────────────┐
                 │              SECURITY RECAP               │
                 └──────────────────────────────────────────┘

     ┌──────────────────────────────────────────────────────────────────┐
     │                     1. SANDBOX THE VIBE LOOP                     │
     └──────────────────────────────────────────────────────────────────┘
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Run generated code in isolated sandboxes            │
        │  • Scan dependencies (SCA) for fake or risky packages  │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     2. SHIFT THE PERIMETER LEFT                  │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Use trusted internal registries                     │
        │  • IDE gives warnings, CI/CD enforces strict checks    │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     3. ZERO AMBIENT AUTHORITY                    │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • No broad “global keys”                              │
        │  • Use JIT tiny, temporary permissions                 │
        │  • High‑risk actions require MFA + Vibe Diff           │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     4. DEPLOY AGENTIC SECOPS                     │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Red Team injects adversarial vibes                  │
        │  • Blue Team monitors behavior (AgBOM)                 │
        │  • Green Team auto‑refactors and quarantines           │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     5. TRACE THE EXECUTION                       │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Log reasoning, tool calls, API usage                │
        │  • Detect drift and roll back using checkpoints        │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │               BIG PICTURE                │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  These controls make agents safe — but safety alone     │
        │  doesn’t guarantee correctness. Next step: evaluate     │
        │  whether the agent actually fulfilled the user’s intent.│
        └────────────────────────────────────────────────────────┘

--------------------------------------------------------------------------

# Orchestrating Quality in Intent‑Driven Agentic Systems

Security only tells you whether the agent stayed inside safe boundaries.
Evaluation answers the real question:
👉 Did the agent actually build what you wanted, and is the result any good?

Vibe‑coding evaluation is harder than normal software evaluation because:

There is no clear spec  
Prompts like “make it faster” are vague. The agent must guess the missing details.

Users can’t validate the output  
Most people can’t review hundreds of lines of code to check correctness.

The session is iterative and stateful  
Each turn changes real files, so early mistakes snowball.

Evaluation must therefore check whether the agent understood the intent, followed project conventions, and improved the codebase across the entire multi‑turn workflow.

        ┌──────────────────────────────────────────────────────────┐
        │   EVALUATION: ORCHESTRATING QUALITY IN AGENTIC SYSTEMS   │
        └──────────────────────────────────────────────────────────┘

                         ▼  CORE PURPOSE
        ┌────────────────────────────────────────────────────────┐
        │  Security = “Did it stay safe?”                         │
        │  Evaluation = “Did it build the right thing?”           │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     WHY EVALUATION IS DIFFERENT                  │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  1. UNDERSPECIFICATION GAP
        ┌────────────────────────────────────────────────────────┐
        │  Prompts are vague (“make it faster”).                 │
        │  Agent must infer missing details.                     │
        └────────────────────────────────────────────────────────┘

                         ▼  2. USERS CAN’T VERIFY OUTPUT
        ┌────────────────────────────────────────────────────────┐
        │  Humans can’t review large code dumps.                 │
        │  Agent “success” ≠ correct or high‑quality code.       │
        └────────────────────────────────────────────────────────┘

                         ▼  3. ITERATIVE, STATEFUL SESSIONS
        ┌────────────────────────────────────────────────────────┐
        │  Each turn edits real files.                           │
        │  Early mistakes compound over time.                    │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │               BIG PICTURE                │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  Evaluation checks whether the agent understood intent, │
        │  followed conventions, and improved the codebase across │
        │  the entire multi‑turn workflow.                        │
        └────────────────────────────────────────────────────────┘


# What to Evaluate

Vibe‑coding agents must be evaluated across seven dimensions to know whether they truly did a good job.
Some dimensions are user-facing (what you see), others are internal (what the agent does behind the scenes).
Safety cuts across all of them.

The seven things to evaluate:

Intent satisfaction — Did the agent build what the user meant, not just what they typed?

Functional correctness — Does the code run, build, and pass tests?

Visual & behavioral correctness — For UI work: does the page look and behave right?

Cost & efficiency — How many tokens, steps, retries, and corrections were needed?

Code quality & conventions — Does the code match the project’s style and patterns?

Trajectory quality — Did the agent take a sensible, structured path to the solution?

Self‑repair behavior — When things break, does the agent recover or make it worse?

These dimensions influence each other — good reasoning (trajectory) usually leads to better correctness and better intent satisfaction.

                 ┌──────────────────────────────────────────┐
                 │              WHAT TO EVALUATE             │
                 │      (7 Dimensions of Vibe Coding)        │
                 └──────────────────────────────────────────┘

     ┌──────────────────────────────────────────────────────────────────┐
     │                     USER-FACING DIMENSIONS                       │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  1. INTENT SATISFACTION
        ┌────────────────────────────────────────────────────────┐
        │  Did the agent build what the user *meant*?            │
        └────────────────────────────────────────────────────────┘

                         ▼  2. FUNCTIONAL CORRECTNESS
        ┌────────────────────────────────────────────────────────┐
        │  Does it run, build, and pass tests?                   │
        └────────────────────────────────────────────────────────┘

                         ▼  3. VISUAL & BEHAVIORAL CORRECTNESS
        ┌────────────────────────────────────────────────────────┐
        │  For UI: does it look right and behave right?          │
        └────────────────────────────────────────────────────────┘

                         ▼  4. COST & EFFICIENCY
        ┌────────────────────────────────────────────────────────┐
        │  Tokens, latency, tool calls, number of corrections.   │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     INTERNAL DIMENSIONS                          │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  5. CODE QUALITY & CONVENTIONS
        ┌────────────────────────────────────────────────────────┐
        │  Does the code match project style and patterns?       │
        └────────────────────────────────────────────────────────┘

                         ▼  6. TRAJECTORY QUALITY
        ┌────────────────────────────────────────────────────────┐
        │  Did the agent take a sensible, structured path?       │
        └────────────────────────────────────────────────────────┘

                         ▼  7. SELF-REPAIR BEHAVIOR
        ┌────────────────────────────────────────────────────────┐
        │  Does the agent recover gracefully when things break?  │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │                 SAFETY                    │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  Cross-cutting: code vulnerabilities, refusal logic,   │
        │  content safety, IP exposure. Evaluated across all 7.  │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │               BIG PICTURE                │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  These dimensions work together. Good reasoning leads   │
        │  to better correctness, which leads to better intent    │
        │  satisfaction — the ultimate goal.                      │
        └────────────────────────────────────────────────────────┘

# How to evaluate

No single method can evaluate a vibe‑coding agent.
Different dimensions require different tools, so real systems combine multiple evaluation methods:

Automated functional tests — Run builds, tests, and linters to check correctness.

Security & safety scans — Static analysis + red‑team probing for vulnerabilities and refusal behavior.

LLM‑as‑judge / Agent‑as‑judge — Models score intent satisfaction, style, and reasoning quality.

Browser‑based testing — For UI agents: check visual and behavioral correctness.

Trajectory inspection — Analyze reasoning traces, tool calls, and recovery behavior.

Human review — Experts review samples for intent, quality, and safety.

Online evaluation — Score real production sessions to catch long‑tail failures.

                 ┌──────────────────────────────────────────┐
                 │              HOW TO EVALUATE              │
                 └──────────────────────────────────────────┘

     ┌──────────────────────────────────────────────────────────────────┐
     │                     1. AUTOMATED TESTING                         │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Run builds, tests, linters                          │
        │  • Best for functional correctness + rule-based style  │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     2. SECURITY & SAFETY SCANS                   │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Static scanners (Snyk, Semgrep)                     │
        │  • Red-team refusal tests                              │
        │  • Cross-cuts all dimensions                           │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     3. LLM-AS-JUDGE / AGENT-AS-JUDGE             │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Score intent satisfaction                           │
        │  • Score code quality & trajectory                     │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     4. BROWSER-BASED TESTING                     │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Playwright-style UI tests                           │
        │  • Best for visual & behavioral correctness            │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     5. TRAJECTORY INSPECTION                     │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Inspect reasoning traces (OpenTelemetry)            │
        │  • Best for trajectory quality & self-repair           │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     6. HUMAN REVIEW                              │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Experts review samples                              │
        │  • Best for intent, style, nuanced safety              │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     7. ONLINE EVALUATION                         │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Score real production sessions                      │
        │  • Covers all dimensions at sample rate                │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │               BIG PICTURE                │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  No single method is enough. Combining all seven gives │
        │  a complete, reliable evaluation of agent quality.     │
        └────────────────────────────────────────────────────────┘

--------------------------------------------------------------------------

# Standardised Benchmarks & Kaggle Agent Exams

Standardised benchmarks test an agent’s core reasoning skills in a clean, controlled way.
They help you understand how strong the agent is independently of your custom environment.

What they do
Benchmarks like Vibe Code Bench, SWE‑bench Verified, and LiveCodeBench test coding, reasoning, and multi‑step problem solving.

Kaggle Standardised Agent Exams (SAE) let agents self‑register, fetch exam questions, run them in a sandbox, and publish scores automatically — zero setup.

Why they matter
They give a fair, comparable score across agents and teams.

The tradeoff
If you rely too much on benchmarks, agents may overfit — scoring high on tests but failing in messy real‑world vibe‑coding tasks.

Benchmarks are great for calibration, but they cannot replace evaluating real user intent.

        ┌──────────────────────────────────────────────────────────┐
        │   STANDARDISED BENCHMARKS & KAGGLE AGENT EXAMS           │
        └──────────────────────────────────────────────────────────┘

                         ▼  PURPOSE
        ┌────────────────────────────────────────────────────────┐
        │  Test core reasoning skills in a clean, controlled     │
        │  environment. Provide fair, comparable scores.         │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     A. STANDARDISED BENCHMARKS                   │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  WHAT THEY TEST
        ┌────────────────────────────────────────────────────────┐
        │  • Vibe Code Bench → zero-to-one web app generation    │
        │  • SWE-bench Verified → real GitHub repo fixes         │
        │  • LiveCodeBench → contamination-resistant coding       │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     B. KAGGLE AGENT EXAMS (SAE)                  │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  ZERO-SETUP EVALUATION
        ┌────────────────────────────────────────────────────────┐
        │  • Agent self-registers via SKILL.md                   │
        │  • Fetches exam questions                              │
        │  • Runs multi-step logic in sandbox                    │
        │  • Publishes score to live leaderboard                 │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     C. THE TRADEOFF: OVERFITTING                 │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  RISK
        ┌────────────────────────────────────────────────────────┐
        │  • Agents can be tuned to ace benchmarks               │
        │  • But fail on messy, ambiguous real-world intent      │
        │  • High SWE-bench score ≠ good vibe coder              │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │               BIG PICTURE                │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  Benchmarks calibrate cognitive ability, but real      │
        │  vibe-coding evaluation must still test intent, style, │
        │  reasoning, and multi-turn behavior.                   │
        └────────────────────────────────────────────────────────┘


# Observability: The Prerequisite for Evaluation

o evaluate an agent properly, you must see inside its reasoning.
Observability turns the agent into a glass box, letting you trace thoughts, measure costs, and detect drift.

Key ideas:
Tracing the Thought — Use OpenTelemetry to capture reasoning steps, tool calls, and actions.

Tracking Costs — Observability shows token usage, latency, and self‑repair overhead.

Tail‑Based Sampling — Only keep important traces (errors, long loops) to save storage.

Practical evaluation tips:
Use the session prefix as the intent rubric — The first messages define the user’s true intent.

Judge the rendered artifact, not the code — For UI, what matters is what the user sees.

Evaluate session convergence — Success = the session ends with a good result, not perfect turns.

Mine user corrections — Every “no, not like that” is labeled failure data that reveals systematic gaps.

        ┌──────────────────────────────────────────────────────────┐
        │      OBSERVABILITY: THE PREREQUISITE FOR EVALUATION      │
        └──────────────────────────────────────────────────────────┘

                         ▼  WHY IT MATTERS
        ┌────────────────────────────────────────────────────────┐
        │  You cannot evaluate an agent if you cannot see how    │
        │  it thinks. Observability turns the agent into a        │
        │  “glass box.”                                           │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     A. TRACING THE THOUGHT                       │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • OpenTelemetry spans:                                │
        │      agent.session → whole task                        │
        │      agent.think   → reasoning steps                   │
        │      agent.tool    → tool calls + latency              │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     B. TRACKING COSTS                            │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Token usage                                         │
        │  • Inference latency                                   │
        │  • Self-repair loop cost                               │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     C. TAIL-BASED SAMPLING                       │
     └──────────────────────────────────────────────────────────────────┐
                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Keep traces with errors or drift                    │
        │  • Drop routine successes to save storage              │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │            PRACTICAL TIPS FOR VIBE-CODING EVALUATION             │
     └──────────────────────────────────────────────────────────────────┐

                         ▼  1. SESSION PREFIX = INTENT RUBRIC
        ┌────────────────────────────────────────────────────────┐
        │  First messages define the unstated spec.              │
        │  Score all turns against them.                         │
        └────────────────────────────────────────────────────────┘

                         ▼  2. JUDGE THE ARTIFACT, NOT THE CODE
        ┌────────────────────────────────────────────────────────┐
        │  Use multimodal checks + Playwright for UI correctness │
        └────────────────────────────────────────────────────────┘

                         ▼  3. EVALUATE SESSION CONVERGENCE
        ┌────────────────────────────────────────────────────────┐
        │  Success = user reaches a good final result            │
        │  Failures = abandoned sessions                         │
        └────────────────────────────────────────────────────────┘

                         ▼  4. MINE USER CORRECTIONS
        ┌────────────────────────────────────────────────────────┐
        │  “No, not like that” = labeled failure data            │
        │  Cluster them to find systematic weaknesses            │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │               BIG PICTURE                │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  Observability enables true evaluation by exposing the │
        │  agent’s reasoning, drift, cost, and recovery patterns.│
        └────────────────────────────────────────────────────────┘

------------------------------------------------------------------------------

# Conclusion


Software development has shifted from writing syntax to guiding intent.
AI can generate code easily — the real work now is defining boundaries, securing execution, and evaluating whether the agent actually built what you wanted.

Key ideas:
Implicit trust is gone — agents must be wrapped in a strict 7‑pillar security harness (sandboxing, ABAC, Red/Blue/Green teaming).

Security ≠ usefulness — security only proves the agent didn’t cause harm.

Evaluation proves value — by measuring intent satisfaction, correctness, trajectory quality, UI behavior, and more.

Generation is solved — the new craft is verification, architecture, and disciplined agent engineering.

Teams that win will treat AI as a high‑speed implementation engine, while keeping strong engineering judgment and governance.

                 ┌──────────────────────────────────────────┐
                 │                 CONCLUSION                │
                 └──────────────────────────────────────────┘

                         ▼  THE SHIFT
        ┌────────────────────────────────────────────────────────┐
        │  Software bottlenecks moved from typing code →         │
        │  defining intent, securing agents, and evaluating       │
        │  their reasoning.                                       │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     A. SECURITY IS NECESSARY                     │
     └──────────────────────────────────────────────────────────────────┐

                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • 7-Pillar Security Architecture                      │
        │  • Sandboxing, ABAC, Red/Blue/Green teaming            │
        │  • Prevents harm, limits blast radius                  │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     B. BUT SECURITY IS NOT ENOUGH                │
     └──────────────────────────────────────────────────────────────────┐

                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  Security only proves the agent stayed safe.           │
        │  It does NOT prove the agent built the right thing.    │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     C. EVALUATION PROVES VALUE                   │
     └──────────────────────────────────────────────────────────────────┐

                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  • Intent satisfaction                                 │
        │  • Functional + visual correctness                     │
        │  • Trajectory quality                                  │
        │  • Code quality + conventions                          │
        │  • Multi-turn convergence                              │
        └────────────────────────────────────────────────────────┘


     ┌──────────────────────────────────────────────────────────────────┐
     │                     D. THE NEW CRAFT                             │
     └──────────────────────────────────────────────────────────────────┐

                         ▼
        ┌────────────────────────────────────────────────────────┐
        │  Generation is easy now.                               │
        │  The hard part is verification, security, and          │
        │  architectural judgment.                               │
        └────────────────────────────────────────────────────────┘


                 ┌──────────────────────────────────────────┐
                 │               BIG PICTURE                │
                 └──────────────────────────────────────────┘
        ┌────────────────────────────────────────────────────────┐
        │  The teams that thrive will pair high-velocity AI with │
        │  disciplined engineering to build software the world   │
        │  can depend on.                                        │
        └────────────────────────────────────────────────────────┘
