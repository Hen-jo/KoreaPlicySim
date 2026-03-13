"""
Support dashboard generation for Seoul mayoral campaign scenarios.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from ..utils.llm_client import LLMClient
from ..utils.logger import get_logger
from .campaign_models import (
    CampaignAction,
    CandidateProfile,
    CandidateShiftSummary,
    DistrictShiftSummary,
    SEOUL_DISTRICTS,
    SupportDashboard,
    VoterBlocShiftSummary,
    starter_blocs_for_districts,
)

logger = get_logger("koreapolicysim.support_dashboard")


class SupportDashboardGenerator:
    """Generate a directional support dashboard for Seoul mayoral scenarios."""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()

    def generate(
        self,
        simulation_requirement: str,
        document_text: str,
        race_type: str,
        target_city: str,
        target_districts: List[str],
        candidate_profiles: List[Dict[str, Any]],
        campaign_action_brief: str,
        entity_types: List[str],
    ) -> Dict[str, Any]:
        normalized_target_districts = target_districts or SEOUL_DISTRICTS
        blocs = starter_blocs_for_districts(normalized_target_districts)
        candidates = [
            CandidateProfile(
                name=(item or {}).get("name", "Candidate"),
                party=(item or {}).get("party", ""),
                slogan=(item or {}).get("slogan", ""),
            )
            for item in (candidate_profiles or [])
            if (item or {}).get("name")
        ]

        prompt = self._build_prompt(
            simulation_requirement=simulation_requirement,
            document_text=document_text,
            race_type=race_type,
            target_city=target_city,
            target_districts=normalized_target_districts,
            candidates=candidates,
            campaign_action_brief=campaign_action_brief,
            blocs=blocs,
            entity_types=entity_types,
        )

        try:
            result = self.llm_client.chat_json(
                messages=[
                    {"role": "system", "content": self._system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=4096,
            )
            return self._normalize_result(
                result,
                race_type=race_type,
                target_city=target_city,
                target_districts=normalized_target_districts,
                campaign_action_brief=campaign_action_brief,
                candidates=candidates,
                blocs=blocs,
            )
        except Exception as exc:
            logger.warning(f"Support dashboard generation failed, falling back: {exc}")
            return self._fallback_dashboard(
                race_type=race_type,
                target_city=target_city,
                target_districts=normalized_target_districts,
                campaign_action_brief=campaign_action_brief,
                candidates=candidates,
                blocs=blocs,
            ).to_dict()

    def _system_prompt(self) -> str:
        return (
            "You are a Seoul mayoral campaign analyst. Return valid JSON only. "
            "Use directional shifts, not exact forecast claims. "
            "Use the official_signals and modeled_scores in each bloc as evidence. "
            "Use district_indicators and election_baseline to infer baseline ideology, swing risk, and turnout pressure. "
            "Every shift must be phrased like '+2 support pressure', 'slightly negative', "
            "'flat', or 'moderately positive'."
        )

    def _build_prompt(
        self,
        simulation_requirement: str,
        document_text: str,
        race_type: str,
        target_city: str,
        target_districts: List[str],
        candidates: List[CandidateProfile],
        campaign_action_brief: str,
        blocs: List[Dict[str, Any]],
        entity_types: List[str],
    ) -> str:
        candidate_json = json.dumps([c.to_dict() for c in candidates], ensure_ascii=False, indent=2)
        bloc_json = json.dumps(blocs, ensure_ascii=False, indent=2)
        return f"""
Build a structured support dashboard for a Seoul mayoral campaign simulation.

Race type: {race_type}
Target city: {target_city}
Target districts: {', '.join(target_districts) if target_districts else 'All Seoul districts'}
Simulation requirement: {simulation_requirement}
Campaign action brief: {campaign_action_brief}
Available entity types: {', '.join(entity_types)}

Candidates:
{candidate_json if candidate_json != '[]' else '[]'}

Starter voter blocs:
{bloc_json}

Each bloc contains:
- official_signals: directly cited city/public-news metrics
- district_indicators: district-level profile tiers and ranked public indicator notes
- election_baseline: district baseline from previous presidential/general-election signals
- modeled_scores: normalized 1-5 scores derived from those signals and district profile
- source_context/source_refs: provenance and modeling notes

Source material:
{document_text[:12000]}

Return JSON with this shape:
{{
  "campaign_action": {{
    "action_type": "pledge_release|district_targeted_message|debate_response|scandal_response|endorsement|attack|apology|policy_clarification",
    "summary": "...",
    "target_districts": ["Gangnam"],
    "expected_focus": ["redevelopment", "trust"]
  }},
  "candidates": [
    {{
      "candidate_name": "...",
      "party": "...",
      "citywide_approval_shift": "...",
      "citywide_favorability_shift": "...",
      "citywide_vote_intent_shift": "...",
      "citywide_swing_voter_shift": "...",
      "strongest_districts": ["..."],
      "risk_districts": ["..."]
    }}
  ],
  "districts": [
    {{
      "district": "...",
      "approval_shift": "...",
      "favorability_shift": "...",
      "vote_intent_shift": "...",
      "swing_voter_shift": "...",
      "dominant_drivers": ["...", "..."]
    }}
  ],
  "blocs": [
    {{
      "district": "...",
      "bloc_key": "...",
      "bloc_label": "...",
      "party_lean": "...",
      "top_issues": ["...", "..."],
      "approval_shift": "...",
      "favorability_shift": "...",
      "vote_intent_shift": "...",
      "swing_voter_shift": "...",
      "likely_reaction": "..."
    }}
  ],
  "top_positive_drivers": ["...", "..."],
  "top_negative_drivers": ["...", "..."],
  "uncertainty_note": "..."
}}

If no candidate is declared yet, return an empty "candidates" array and focus on district/bloc sensitivity.
"""

    def _normalize_result(
        self,
        result: Dict[str, Any],
        race_type: str,
        target_city: str,
        target_districts: List[str],
        campaign_action_brief: str,
        candidates: List[CandidateProfile],
        blocs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        dashboard = SupportDashboard(
            race_type=race_type,
            target_city=target_city,
            target_districts=target_districts or SEOUL_DISTRICTS,
            campaign_action=CampaignAction(
                action_type=result.get("campaign_action", {}).get("action_type", "policy_clarification"),
                summary=result.get("campaign_action", {}).get("summary", campaign_action_brief or "Campaign action scenario"),
                target_districts=result.get("campaign_action", {}).get("target_districts", target_districts or SEOUL_DISTRICTS),
                expected_focus=result.get("campaign_action", {}).get("expected_focus", ["approval", "support"]),
            ),
            candidates=[
                CandidateShiftSummary(
                    candidate_name=item.get("candidate_name", candidates[0].name if candidates else "Candidate"),
                    party=item.get("party", candidates[0].party if candidates else ""),
                    citywide_approval_shift=item.get("citywide_approval_shift", "flat"),
                    citywide_favorability_shift=item.get("citywide_favorability_shift", "flat"),
                    citywide_vote_intent_shift=item.get("citywide_vote_intent_shift", "flat"),
                    citywide_swing_voter_shift=item.get("citywide_swing_voter_shift", "flat"),
                    strongest_districts=item.get("strongest_districts", []),
                    risk_districts=item.get("risk_districts", []),
                )
                for item in result.get("candidates", [])
            ],
            districts=[
                DistrictShiftSummary(
                    district=item.get("district", "Unknown"),
                    approval_shift=item.get("approval_shift", "flat"),
                    favorability_shift=item.get("favorability_shift", "flat"),
                    vote_intent_shift=item.get("vote_intent_shift", "flat"),
                    swing_voter_shift=item.get("swing_voter_shift", "flat"),
                    dominant_drivers=item.get("dominant_drivers", []),
                )
                for item in result.get("districts", [])
            ],
            blocs=[
                VoterBlocShiftSummary(
                    district=item.get("district", bloc.get("district", "Unknown")),
                    bloc_key=item.get("bloc_key", bloc.get("bloc_key", "bloc")),
                    bloc_label=item.get("bloc_label", bloc.get("bloc_label", "District bloc")),
                    party_lean=item.get("party_lean", bloc.get("party_lean", "swing")),
                    top_issues=item.get("top_issues", bloc.get("top_issues", [])),
                    approval_shift=item.get("approval_shift", "flat"),
                    favorability_shift=item.get("favorability_shift", "flat"),
                    vote_intent_shift=item.get("vote_intent_shift", "flat"),
                    swing_voter_shift=item.get("swing_voter_shift", "flat"),
                    likely_reaction=item.get("likely_reaction", "Mixed response"),
                )
                for item, bloc in zip(result.get("blocs", []), blocs)
            ],
            top_positive_drivers=result.get("top_positive_drivers", []),
            top_negative_drivers=result.get("top_negative_drivers", []),
            uncertainty_note=result.get(
                "uncertainty_note",
                "Directional scenario estimate only. Treat outputs as support pressure signals, not a literal vote forecast.",
            ),
        )

        if not dashboard.districts:
            dashboard.districts = [
                DistrictShiftSummary(
                    district=bloc["district"],
                    approval_shift="mixed",
                    favorability_shift="mixed",
                    vote_intent_shift="mixed",
                    swing_voter_shift="mixed",
                    dominant_drivers=bloc.get("top_issues", [])[:2],
                )
                for bloc in blocs[:8]
            ]

        if len(dashboard.blocs) < len(blocs):
            existing = len(dashboard.blocs)
            for bloc in blocs[existing:]:
                dashboard.blocs.append(
                    VoterBlocShiftSummary(
                        district=bloc["district"],
                        bloc_key=bloc["bloc_key"],
                        bloc_label=bloc["bloc_label"],
                        party_lean=bloc["party_lean"],
                        top_issues=bloc["top_issues"],
                        approval_shift="flat",
                        favorability_shift="flat",
                        vote_intent_shift="flat",
                        swing_voter_shift="mixed",
                        likely_reaction="Insufficient evidence; likely limited movement.",
                    )
                )
        return dashboard.to_dict()

    def _fallback_dashboard(
        self,
        race_type: str,
        target_city: str,
        target_districts: List[str],
        campaign_action_brief: str,
        candidates: List[CandidateProfile],
        blocs: List[Dict[str, Any]],
    ) -> SupportDashboard:
        return SupportDashboard(
            race_type=race_type,
            target_city=target_city,
            target_districts=target_districts or SEOUL_DISTRICTS,
            campaign_action=CampaignAction(
                action_type="policy_clarification",
                summary=campaign_action_brief or "Campaign action scenario",
                target_districts=target_districts or SEOUL_DISTRICTS,
                expected_focus=["approval", "support"],
            ),
            candidates=[],
            districts=[
                DistrictShiftSummary(
                    district=bloc["district"],
                    approval_shift="mixed",
                    favorability_shift="mixed",
                    vote_intent_shift="mixed",
                    swing_voter_shift="mixed",
                    dominant_drivers=bloc.get("top_issues", [])[:2],
                )
                for bloc in blocs[:8]
            ],
            blocs=[
                VoterBlocShiftSummary(
                    district=bloc["district"],
                    bloc_key=bloc["bloc_key"],
                    bloc_label=bloc["bloc_label"],
                    party_lean=bloc["party_lean"],
                    top_issues=bloc["top_issues"],
                    approval_shift="flat",
                    favorability_shift="flat",
                    vote_intent_shift="flat",
                    swing_voter_shift="mixed",
                    likely_reaction="Directional estimate unavailable; treat as a neutral baseline with district-specific sensitivity.",
                )
                for bloc in blocs
            ],
            top_positive_drivers=[
                "district-level issue matching highlights where Seoul blocs are most sensitive",
                "bloc modeling captures different reactions across homeowners, renters, commuters, and families",
            ],
            top_negative_drivers=[
                "without a declared candidate, trust and coalition effects remain under-specified",
                "outputs remain sensitive to media framing and implementation details in source material",
            ],
            uncertainty_note="Fallback directional estimate only. Use it to inspect citizen bloc sensitivity, not to forecast an election result.",
        )
