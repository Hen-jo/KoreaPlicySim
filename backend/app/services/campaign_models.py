"""
Campaign-domain models for the Seoul mayoral simulator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

from .seoul_civic_signals import enrich_bloc_quant_signals


SEOUL_DISTRICTS: List[str] = [
    "Gangnam",
    "Gangdong",
    "Gangbuk",
    "Gangseo",
    "Gwanak",
    "Gwangjin",
    "Guro",
    "Geumcheon",
    "Nowon",
    "Dobong",
    "Dongdaemun",
    "Dongjak",
    "Mapo",
    "Seodaemun",
    "Seocho",
    "Seongdong",
    "Seongbuk",
    "Songpa",
    "Yangcheon",
    "Yeongdeungpo",
    "Yongsan",
    "Eunpyeong",
    "Jongno",
    "Jung",
    "Jungnang",
]


DISTRICT_THEME_PROFILES: Dict[str, Dict[str, Any]] = {
    "Gangnam": {
        "anchor_bloc": "asset-focused homeowners",
        "swing_bloc": "high-income professionals",
        "anchor_lean": "center_right",
        "swing_lean": "swing",
        "anchor_issues": ["taxes", "redevelopment", "asset_values"],
        "swing_issues": ["education", "mobility", "competence"],
        "anchor_turnout": "high",
        "swing_turnout": "medium_high",
        "anchor_housing": "homeowner",
        "swing_housing": "mixed",
        "anchor_stability": "high",
        "swing_stability": "high",
    },
    "Gangdong": {
        "anchor_bloc": "family apartment owners",
        "swing_bloc": "commuting households",
        "anchor_lean": "swing_center_right",
        "swing_lean": "swing",
        "anchor_issues": ["schools", "housing_prices", "local_infrastructure"],
        "swing_issues": ["commute_time", "cost_of_living", "public_services"],
        "anchor_turnout": "medium_high",
        "swing_turnout": "medium",
        "anchor_housing": "homeowner",
        "swing_housing": "mixed",
        "anchor_stability": "medium_high",
        "swing_stability": "medium",
    },
    "Gangbuk": {
        "anchor_bloc": "long-term residential households",
        "swing_bloc": "aging mixed-income voters",
        "anchor_lean": "swing_center_left",
        "swing_lean": "swing",
        "anchor_issues": ["redevelopment", "welfare", "local_revival"],
        "swing_issues": ["aging", "healthcare", "public_safety"],
        "anchor_turnout": "medium_high",
        "swing_turnout": "medium_high",
        "anchor_housing": "mixed",
        "swing_housing": "mixed",
        "anchor_stability": "medium",
        "swing_stability": "medium_low",
    },
    "Gangseo": {
        "anchor_bloc": "family commuters",
        "swing_bloc": "airport corridor workers",
        "anchor_lean": "swing",
        "swing_lean": "swing_center_left",
        "anchor_issues": ["transport", "childcare", "housing"],
        "swing_issues": ["jobs", "noise", "cost_of_living"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium",
        "anchor_housing": "mixed",
        "swing_housing": "renters",
        "anchor_stability": "medium",
        "swing_stability": "medium_low",
    },
    "Gwanak": {
        "anchor_bloc": "young renters",
        "swing_bloc": "precarious workers",
        "anchor_lean": "swing_center_left",
        "swing_lean": "swing",
        "anchor_issues": ["rent", "jobs", "public_transport"],
        "swing_issues": ["welfare", "cost_of_living", "job_security"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium_low",
        "anchor_housing": "renters",
        "swing_housing": "renters",
        "anchor_stability": "low_medium",
        "swing_stability": "low",
    },
    "Gwangjin": {
        "anchor_bloc": "mixed urban families",
        "swing_bloc": "students and new workers",
        "anchor_lean": "swing",
        "swing_lean": "center_left",
        "anchor_issues": ["housing", "schools", "transport"],
        "swing_issues": ["rent", "jobs", "nightlife_regulation"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium_low",
        "anchor_housing": "mixed",
        "swing_housing": "renters",
        "anchor_stability": "medium",
        "swing_stability": "low_medium",
    },
    "Guro": {
        "anchor_bloc": "industrial working households",
        "swing_bloc": "digital complex workers",
        "anchor_lean": "swing_center_left",
        "swing_lean": "swing",
        "anchor_issues": ["jobs", "housing", "welfare"],
        "swing_issues": ["innovation", "commute_time", "cost_of_living"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium",
        "anchor_housing": "mixed",
        "swing_housing": "renters",
        "anchor_stability": "medium_low",
        "swing_stability": "medium",
    },
    "Geumcheon": {
        "anchor_bloc": "value-sensitive households",
        "swing_bloc": "logistics and service workers",
        "anchor_lean": "swing_center_left",
        "swing_lean": "swing",
        "anchor_issues": ["jobs", "welfare", "housing_cost"],
        "swing_issues": ["transport", "local_investment", "job_security"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium_low",
        "anchor_housing": "mixed",
        "swing_housing": "renters",
        "anchor_stability": "medium_low",
        "swing_stability": "low_medium",
    },
    "Nowon": {
        "anchor_bloc": "stable apartment households",
        "swing_bloc": "education-focused families",
        "anchor_lean": "swing",
        "swing_lean": "swing_center_left",
        "anchor_issues": ["cost_of_living", "schools", "transit"],
        "swing_issues": ["education", "housing", "public_services"],
        "anchor_turnout": "medium_high",
        "swing_turnout": "medium_high",
        "anchor_housing": "mixed",
        "swing_housing": "mixed",
        "anchor_stability": "medium",
        "swing_stability": "medium",
    },
    "Dobong": {
        "anchor_bloc": "older residential households",
        "swing_bloc": "price-sensitive family voters",
        "anchor_lean": "swing_center_left",
        "swing_lean": "swing",
        "anchor_issues": ["welfare", "healthcare", "redevelopment"],
        "swing_issues": ["housing", "schools", "cost_of_living"],
        "anchor_turnout": "medium_high",
        "swing_turnout": "medium",
        "anchor_housing": "mixed",
        "swing_housing": "mixed",
        "anchor_stability": "medium_low",
        "swing_stability": "medium",
    },
    "Dongdaemun": {
        "anchor_bloc": "traditional market households",
        "swing_bloc": "redevelopment-sensitive renters",
        "anchor_lean": "swing_center_left",
        "swing_lean": "swing",
        "anchor_issues": ["small_business", "redevelopment", "welfare"],
        "swing_issues": ["rent", "displacement", "local_services"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium_low",
        "anchor_housing": "mixed",
        "swing_housing": "renters",
        "anchor_stability": "medium_low",
        "swing_stability": "low_medium",
    },
    "Dongjak": {
        "anchor_bloc": "education-minded families",
        "swing_bloc": "public sector aspirants",
        "anchor_lean": "swing",
        "swing_lean": "swing_center_left",
        "anchor_issues": ["schools", "housing", "mobility"],
        "swing_issues": ["jobs", "fairness", "public_transport"],
        "anchor_turnout": "medium_high",
        "swing_turnout": "medium",
        "anchor_housing": "mixed",
        "swing_housing": "renters",
        "anchor_stability": "medium",
        "swing_stability": "medium_low",
    },
    "Mapo": {
        "anchor_bloc": "young professionals",
        "swing_bloc": "progressive families",
        "anchor_lean": "center_left",
        "swing_lean": "center_left",
        "anchor_issues": ["housing", "quality_of_life", "mobility"],
        "swing_issues": ["childcare", "schools", "local_services"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium_high",
        "anchor_housing": "renters",
        "swing_housing": "mixed",
        "anchor_stability": "medium",
        "swing_stability": "medium_high",
    },
    "Seodaemun": {
        "anchor_bloc": "student-adjacent renters",
        "swing_bloc": "middle-class family households",
        "anchor_lean": "center_left",
        "swing_lean": "swing",
        "anchor_issues": ["rent", "education", "public_transport"],
        "swing_issues": ["schools", "housing", "quality_of_life"],
        "anchor_turnout": "medium_low",
        "swing_turnout": "medium",
        "anchor_housing": "renters",
        "swing_housing": "mixed",
        "anchor_stability": "low_medium",
        "swing_stability": "medium",
    },
    "Seocho": {
        "anchor_bloc": "affluent homeowners",
        "swing_bloc": "professional parents",
        "anchor_lean": "center_right",
        "swing_lean": "swing_center_right",
        "anchor_issues": ["taxes", "redevelopment", "stability"],
        "swing_issues": ["education", "public_order", "mobility"],
        "anchor_turnout": "high",
        "swing_turnout": "medium_high",
        "anchor_housing": "homeowner",
        "swing_housing": "homeowner",
        "anchor_stability": "high",
        "swing_stability": "high",
    },
    "Seongdong": {
        "anchor_bloc": "urban redevelopment beneficiaries",
        "swing_bloc": "young apartment buyers",
        "anchor_lean": "swing",
        "swing_lean": "swing",
        "anchor_issues": ["redevelopment", "mobility", "asset_values"],
        "swing_issues": ["housing_affordability", "quality_of_life", "transport"],
        "anchor_turnout": "medium_high",
        "swing_turnout": "medium",
        "anchor_housing": "homeowner",
        "swing_housing": "mixed",
        "anchor_stability": "medium_high",
        "swing_stability": "medium",
    },
    "Seongbuk": {
        "anchor_bloc": "older mixed-income voters",
        "swing_bloc": "education-sensitive families",
        "anchor_lean": "swing_center_left",
        "swing_lean": "swing",
        "anchor_issues": ["welfare", "redevelopment", "public_services"],
        "swing_issues": ["schools", "housing", "cost_of_living"],
        "anchor_turnout": "medium_high",
        "swing_turnout": "medium",
        "anchor_housing": "mixed",
        "swing_housing": "mixed",
        "anchor_stability": "medium_low",
        "swing_stability": "medium",
    },
    "Songpa": {
        "anchor_bloc": "large apartment owners",
        "swing_bloc": "child-raising households",
        "anchor_lean": "swing_center_right",
        "swing_lean": "swing",
        "anchor_issues": ["asset_values", "redevelopment", "taxes"],
        "swing_issues": ["schools", "parks", "transport"],
        "anchor_turnout": "high",
        "swing_turnout": "medium_high",
        "anchor_housing": "homeowner",
        "swing_housing": "mixed",
        "anchor_stability": "high",
        "swing_stability": "medium_high",
    },
    "Yangcheon": {
        "anchor_bloc": "education-driven homeowners",
        "swing_bloc": "commuter family households",
        "anchor_lean": "swing_center_right",
        "swing_lean": "swing",
        "anchor_issues": ["education", "housing_values", "local_services"],
        "swing_issues": ["commute_time", "schools", "cost_of_living"],
        "anchor_turnout": "medium_high",
        "swing_turnout": "medium",
        "anchor_housing": "homeowner",
        "swing_housing": "mixed",
        "anchor_stability": "medium_high",
        "swing_stability": "medium",
    },
    "Yeongdeungpo": {
        "anchor_bloc": "office district professionals",
        "swing_bloc": "service and renter households",
        "anchor_lean": "swing",
        "swing_lean": "swing_center_left",
        "anchor_issues": ["economic_growth", "transport", "competence"],
        "swing_issues": ["housing", "welfare", "cost_of_living"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium_low",
        "anchor_housing": "mixed",
        "swing_housing": "renters",
        "anchor_stability": "medium_high",
        "swing_stability": "medium_low",
    },
    "Yongsan": {
        "anchor_bloc": "redevelopment-focused property voters",
        "swing_bloc": "young urban renters",
        "anchor_lean": "swing_center_right",
        "swing_lean": "swing",
        "anchor_issues": ["redevelopment", "business_district_growth", "transport"],
        "swing_issues": ["rent", "nightlife", "mobility"],
        "anchor_turnout": "medium_high",
        "swing_turnout": "medium",
        "anchor_housing": "homeowner",
        "swing_housing": "renters",
        "anchor_stability": "medium_high",
        "swing_stability": "medium",
    },
    "Eunpyeong": {
        "anchor_bloc": "stable family households",
        "swing_bloc": "commuting apartment renters",
        "anchor_lean": "swing_center_left",
        "swing_lean": "swing",
        "anchor_issues": ["housing", "welfare", "transport"],
        "swing_issues": ["commute_time", "schools", "cost_of_living"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium",
        "anchor_housing": "mixed",
        "swing_housing": "renters",
        "anchor_stability": "medium",
        "swing_stability": "medium_low",
    },
    "Jongno": {
        "anchor_bloc": "civic tradition voters",
        "swing_bloc": "heritage-business residents",
        "anchor_lean": "swing_center_left",
        "swing_lean": "swing",
        "anchor_issues": ["governance", "heritage", "public_order"],
        "swing_issues": ["tourism", "small_business", "quality_of_life"],
        "anchor_turnout": "high",
        "swing_turnout": "medium",
        "anchor_housing": "mixed",
        "swing_housing": "mixed",
        "anchor_stability": "medium",
        "swing_stability": "medium",
    },
    "Jung": {
        "anchor_bloc": "downtown business voters",
        "swing_bloc": "central-city service workers",
        "anchor_lean": "swing",
        "swing_lean": "swing_center_left",
        "anchor_issues": ["economic_activity", "tourism", "public_order"],
        "swing_issues": ["jobs", "transport", "housing_cost"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium_low",
        "anchor_housing": "mixed",
        "swing_housing": "renters",
        "anchor_stability": "medium_high",
        "swing_stability": "medium_low",
    },
    "Jungnang": {
        "anchor_bloc": "value-sensitive households",
        "swing_bloc": "commuting working families",
        "anchor_lean": "swing_center_left",
        "swing_lean": "swing",
        "anchor_issues": ["cost_of_living", "housing", "local_investment"],
        "swing_issues": ["commute_time", "schools", "welfare"],
        "anchor_turnout": "medium",
        "swing_turnout": "medium",
        "anchor_housing": "mixed",
        "swing_housing": "mixed",
        "anchor_stability": "medium_low",
        "swing_stability": "medium",
    },
}


def normalize_district_name(name: str) -> str:
    cleaned = (name or "").strip()
    if not cleaned:
        return ""

    lower_map = {district.lower(): district for district in SEOUL_DISTRICTS}
    suffix_trimmed = cleaned.replace("-gu", "").replace(" District", "").replace(" district", "").strip()
    suffix_trimmed = suffix_trimmed[:-1] if suffix_trimmed.endswith("구") else suffix_trimmed

    aliases = {
        "gangnamgu": "Gangnam",
        "gangdonggu": "Gangdong",
        "gangbukgu": "Gangbuk",
        "gangseogu": "Gangseo",
        "gwanakgu": "Gwanak",
        "gwangjingu": "Gwangjin",
        "gurogu": "Guro",
        "geumcheongu": "Geumcheon",
        "nowongu": "Nowon",
        "dobonggu": "Dobong",
        "dongdaemungu": "Dongdaemun",
        "dongjakgu": "Dongjak",
        "mapogu": "Mapo",
        "seodaemungu": "Seodaemun",
        "seochogu": "Seocho",
        "seongdonggu": "Seongdong",
        "seongbukgu": "Seongbuk",
        "songpagu": "Songpa",
        "yangcheongu": "Yangcheon",
        "yeongdeungpogu": "Yeongdeungpo",
        "yongsangu": "Yongsan",
        "eunpyeonggu": "Eunpyeong",
        "jongnogu": "Jongno",
        "junggu": "Jung",
        "jungnanggu": "Jungnang",
    }

    key = suffix_trimmed.replace(" ", "").lower()
    return aliases.get(key, lower_map.get(suffix_trimmed.lower(), cleaned))


def _slugify(value: str) -> str:
    return value.lower().replace(" ", "_").replace("-", "_")


def _build_blocs_for_district(district: str) -> List[Dict[str, Any]]:
    profile = DISTRICT_THEME_PROFILES.get(
        district,
        {
            "anchor_bloc": "core local households",
            "swing_bloc": "district swing voters",
            "anchor_lean": "base",
            "swing_lean": "swing",
            "anchor_issues": ["local_services", "stability", "housing"],
            "swing_issues": ["cost_of_living", "competence", "fairness"],
            "anchor_turnout": "medium_high",
            "swing_turnout": "medium",
            "anchor_housing": "mixed",
            "swing_housing": "mixed",
            "anchor_stability": "medium",
            "swing_stability": "medium",
        },
    )
    district_slug = _slugify(district)
    blocs = [
        {
            "bloc_key": f"{district_slug}_anchor",
            "bloc_label": f"{district} {profile['anchor_bloc']}",
            "life_stage": "settled_households",
            "housing_status": profile["anchor_housing"],
            "occupation_stability": profile["anchor_stability"],
            "party_lean": profile["anchor_lean"],
            "top_issues": profile["anchor_issues"],
            "turnout_tendency": profile["anchor_turnout"],
            "district": district,
        },
        {
            "bloc_key": f"{district_slug}_swing",
            "bloc_label": f"{district} {profile['swing_bloc']}",
            "life_stage": "mixed_working_age",
            "housing_status": profile["swing_housing"],
            "occupation_stability": profile["swing_stability"],
            "party_lean": profile["swing_lean"],
            "top_issues": profile["swing_issues"],
            "turnout_tendency": profile["swing_turnout"],
            "district": district,
        },
    ]
    return [enrich_bloc_quant_signals(district, bloc) for bloc in blocs]


SEOUL_DISTRICT_BLOC_LIBRARY: Dict[str, List[Dict[str, Any]]] = {
    district: _build_blocs_for_district(district) for district in SEOUL_DISTRICTS
}


@dataclass
class CampaignAction:
    action_type: str
    summary: str
    target_districts: List[str] = field(default_factory=list)
    expected_focus: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_type": self.action_type,
            "summary": self.summary,
            "target_districts": self.target_districts,
            "expected_focus": self.expected_focus,
        }


@dataclass
class CandidateProfile:
    name: str
    party: str = ""
    slogan: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "party": self.party,
            "slogan": self.slogan,
        }


@dataclass
class VoterBlocShiftSummary:
    district: str
    bloc_key: str
    bloc_label: str
    party_lean: str
    top_issues: List[str]
    approval_shift: str
    favorability_shift: str
    vote_intent_shift: str
    swing_voter_shift: str
    likely_reaction: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "district": self.district,
            "bloc_key": self.bloc_key,
            "bloc_label": self.bloc_label,
            "party_lean": self.party_lean,
            "top_issues": self.top_issues,
            "approval_shift": self.approval_shift,
            "favorability_shift": self.favorability_shift,
            "vote_intent_shift": self.vote_intent_shift,
            "swing_voter_shift": self.swing_voter_shift,
            "likely_reaction": self.likely_reaction,
        }


@dataclass
class DistrictShiftSummary:
    district: str
    approval_shift: str
    favorability_shift: str
    vote_intent_shift: str
    swing_voter_shift: str
    dominant_drivers: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "district": self.district,
            "approval_shift": self.approval_shift,
            "favorability_shift": self.favorability_shift,
            "vote_intent_shift": self.vote_intent_shift,
            "swing_voter_shift": self.swing_voter_shift,
            "dominant_drivers": self.dominant_drivers,
        }


@dataclass
class CandidateShiftSummary:
    candidate_name: str
    party: str
    citywide_approval_shift: str
    citywide_favorability_shift: str
    citywide_vote_intent_shift: str
    citywide_swing_voter_shift: str
    strongest_districts: List[str] = field(default_factory=list)
    risk_districts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_name": self.candidate_name,
            "party": self.party,
            "citywide_approval_shift": self.citywide_approval_shift,
            "citywide_favorability_shift": self.citywide_favorability_shift,
            "citywide_vote_intent_shift": self.citywide_vote_intent_shift,
            "citywide_swing_voter_shift": self.citywide_swing_voter_shift,
            "strongest_districts": self.strongest_districts,
            "risk_districts": self.risk_districts,
        }


@dataclass
class SupportDashboard:
    race_type: str
    target_city: str
    target_districts: List[str]
    campaign_action: CampaignAction
    candidates: List[CandidateShiftSummary]
    districts: List[DistrictShiftSummary]
    blocs: List[VoterBlocShiftSummary]
    top_positive_drivers: List[str]
    top_negative_drivers: List[str]
    uncertainty_note: str
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "race_type": self.race_type,
            "target_city": self.target_city,
            "target_districts": self.target_districts,
            "campaign_action": self.campaign_action.to_dict(),
            "candidates": [c.to_dict() for c in self.candidates],
            "districts": [d.to_dict() for d in self.districts],
            "blocs": [b.to_dict() for b in self.blocs],
            "top_positive_drivers": self.top_positive_drivers,
            "top_negative_drivers": self.top_negative_drivers,
            "uncertainty_note": self.uncertainty_note,
            "generated_at": self.generated_at,
        }


def starter_blocs_for_districts(target_districts: List[str]) -> List[Dict[str, Any]]:
    districts = [normalize_district_name(d) for d in target_districts if normalize_district_name(d)]
    if not districts:
        districts = SEOUL_DISTRICTS

    blocs: List[Dict[str, Any]] = []
    for district in districts:
        blocs.extend(SEOUL_DISTRICT_BLOC_LIBRARY.get(district, _build_blocs_for_district(district)))
    return blocs
