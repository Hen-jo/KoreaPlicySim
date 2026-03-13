# Korea Political Response Simulation Preset

`simulation_preset = korea_society_policy`

This preset narrows KoreaPolicySim into a **Seoul political and policy-response simulator**.

## Intent

- Observe how a policy, campaign pledge, scandal, or speech changes public reaction in Seoul.
- Compare response differences across districts, constituencies, generations, and voter blocs.
- Estimate directional shifts in approval, favorability, and support rather than claiming exact election forecasts.

## Recommended Topics

- Seoul mayoral or district-level races
- Redevelopment and housing policy
- Transportation and infrastructure promises
- Education, childcare, and youth policy
- Local tax, welfare, and budget priorities
- Candidate scandals, debates, and endorsements
- District-specific issue salience and swing-voter reaction

## Recommended Source Material

- Candidate pledge documents
- Seoul city or district policy announcements
- Poll summaries and approval snapshots
- News bundles from multiple outlets
- District issue briefs and civic group statements
- Speech transcripts, interviews, and commentary posts

## What This Preset Changes

- Ontology generation prioritizes `candidate`, `party`, `district voter`, `district government`, `polling`, `media`, and `civic groups`.
- Agent persona generation emphasizes `district`, `constituency`, `occupation`, `class position`, `party leaning`, `media habits`, and `policy gain/loss perception`.
- Event and behavior configuration focuses on `policy announcements`, `campaign pledges`, `media framing`, `approval changes`, `district differences`, and `support shifts`.

## Operating Principles

- Do not treat the output as a literal election forecast.
- Use it as a structured sandbox for comparing likely response paths.
- Start with one city, one district cluster, or one election frame before expanding.
- Compare simulated reactions against polling, district vote history, and reporting whenever possible.
