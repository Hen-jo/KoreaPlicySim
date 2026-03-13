# KoreaPolicySim

<div align="center">
  <p>A Seoul-focused political and policy response simulation engine built on document-grounded graphs and multi-agent interaction.</p>
  <p><a href="./README-EN.md">English</a></p>
</div>

## Overview

**KoreaPolicySim** turns policy documents, campaign pledges, political commentary, district issue briefs, polling summaries, and news bundles into a graph-backed simulation environment. It extracts entities and relationships from uploaded material, builds a Zep graph, generates agent personas, runs an OASIS-based social simulation, and produces reports plus interactive follow-up analysis.

This repo is now oriented toward **Korean political and policy-response scenarios**, with a default preset for Seoul-centered simulations such as mayoral races, district-level sentiment shifts, policy approval changes, campaign pledge reactions, and constituency-specific issue dynamics.

In practical terms, this project is designed as a **Seoul election and policy response simulator**. You upload a policy brief, campaign pledge, issue memo, polling summary, or news bundle, and the system models how different Seoul voter blocs may react by district. The output is not a literal election prophecy. It is a scenario engine that helps you estimate:

- which districts are likely to respond positively or negatively
- which voter blocs are activated, persuaded, alienated, or unchanged
- where favorability, approval pressure, and swing-voter movement may shift
- what kinds of backlash or momentum narratives may emerge

## What This Project Does

KoreaPolicySim is built for questions like these:

- If a Seoul mayoral candidate announces a youth rent support pledge, which districts react favorably and which ones push back?
- If a redevelopment policy includes stronger tenant protections, does that improve support in renter-heavy districts while weakening support in homeowner-heavy districts?
- If a campaign focuses on commuting costs, childcare, safety, or welfare, which Seoul voter groups become more persuadable?
- If a controversy breaks out, where is the likely reputational damage concentrated and which blocs are resilient?

The system combines:

- uploaded source documents
- district-based Seoul voter bloc models
- official/public-news civic signals
- previous election baseline tendencies
- LLM-based multi-agent interaction

to generate a structured simulation output for political strategy and policy testing.

## Project Lineage

**KoreaPolicySim** is an adapted and renamed continuation of the original **MiroFish** codebase. This repository started from the earlier `MiroFish` project structure and has been reworked toward a Seoul-focused political and election-response simulator.

The current project keeps the core document-to-graph, agent generation, simulation, and reporting pipeline from that earlier base while changing:

- the product identity from `MiroFish` to `KoreaPolicySim`
- the primary domain from general document/social simulation to Seoul political response and campaign simulation
- the default presets, voter bloc modeling, district signals, and support dashboard outputs

If you redistribute or modify this repository, you should preserve the upstream attribution context and comply with the license terms in this repository.

## Workflow

1. **Graph Build**: ingest documents, extract structure, and build GraphRAG memory
2. **Environment Setup**: generate entities, personas, and scenario configuration
3. **Simulation Run**: execute the agent simulation and accumulate timeline memory
4. **Report Generation**: analyze the run with tool-assisted report agents
5. **Deep Interaction**: ask questions against the simulation state and generated report

## Seoul Politics Preset

The default `korea_society_policy` preset now acts as a Seoul political response simulator. It is designed to model how policies, campaign pledges, controversies, or public statements shift support and approval across districts, constituencies, and voter groups. See [docs/korea-social-simulation.md](./docs/korea-social-simulation.md).

Starter material:

- [docs/seoul-politics-prompts.md](./docs/seoul-politics-prompts.md)
- [docs/sample-seoul-politics-brief.md](./docs/sample-seoul-politics-brief.md)
- [docs/sample-seoul-policy-brief-ko.md](./docs/sample-seoul-policy-brief-ko.md)
- [docs/seoul-civic-signals.md](./docs/seoul-civic-signals.md)

## Example Scenario

Example input:

- a policy brief announcing youth rent support, commuter transit subsidies, and tenant relocation protection
- a campaign action memo explaining how the policy is framed in public
- supporting articles or polling summaries about housing pressure, commuting burden, and redevelopment conflict

Example question:

> 서울시장이 청년 월세 지원, 출퇴근 교통비 완화, 신혼가구 보증 지원, 재개발 지역 임차인 보호를 묶은 생활안정 패키지를 발표했을 때, 서울 25개 구 시민 블록이 어떻게 반응하고 어느 지역에서 지지 압력과 반발이 커지는가?

Example output:

- 관악구, 마포구, 성동구 청년 임차층에서 긍정 반응 확대
- 강남구, 서초구 자가 보유층에서 재정 부담과 시장 개입 우려 증가
- 동작구, 광진구, 영등포구 경합 블록에서 메시지 프레이밍에 따라 결과가 크게 달라질 수 있다는 신호
- 재개발 이슈가 큰 용산구, 동대문구, 성북구에서 임차인 보호 문구가 갈등 완화 또는 개발 반발을 동시에 유발할 수 있다는 리스크

## Output Model

The current output is a **directional campaign dashboard**, not an exact vote-count model.

Typical results include:

- district-by-district support pressure
- bloc-level favorability and vote-intent movement
- positive drivers and backlash drivers
- swing-risk notes by district
- uncertainty notes explaining what is grounded vs inferred

This means the tool is best used for **strategy simulation**, **message testing**, and **policy stress testing**, rather than as a final election forecast engine.

## Quick Start

### Prerequisites

| Tool | Version |
|------|---------|
| Node.js | 18+ |
| Python | 3.11 - 3.12 |
| uv | latest |

### 1. Configure environment variables

```bash
cp .env.example .env
```

Example:

```env
LLM_API_KEY=your_openai_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-5.2

ZEP_API_KEY=your_zep_api_key_here
```

### 2. Install dependencies

```bash
npm run setup:all
```

### 3. Start the app

```bash
npm run dev
```

Service URLs:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5001`
- Health check: `http://localhost:5001/health`

### Docker

```bash
cp .env.example .env
docker compose up -d
```

## Planned Repo Rename

The codebase identity has been renamed to `KoreaPolicySim`, but the local folder and GitHub repository may still use the original `MiroFish` slug until the repo move is completed. The planned operational rename steps are documented in [docs/repo-rename.md](./docs/repo-rename.md).

## License And Attribution

This repository is distributed under **AGPL-3.0**. See [LICENSE](./LICENSE).

Attribution notes:

- This project is based on the earlier `MiroFish` codebase and retains that lineage for copyright and license notice purposes.
- The current repository name, UI, prompts, and simulation focus have been substantially modified into `KoreaPolicySim`.
- Upstream components and external dependencies, including **OASIS** and **Zep Cloud**, remain subject to their own licenses and terms.

## Acknowledgments

The simulation runtime is powered by **[OASIS](https://github.com/camel-ai/oasis)** and the graph memory layer uses **Zep Cloud**.
