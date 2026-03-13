"""
Quantified civic signals for Seoul voter blocs.

This module separates directly cited citywide/district facts from modeled scores
derived from those facts and district theme profiles.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


SEOUL_SIGNAL_SOURCES: Dict[str, str] = {
    "one_person_household_share_pct": "https://mediahub.seoul.go.kr/archives/2014052",
    "walking_practice_rate_pct": "https://www.yna.co.kr/view/AKR20251213029800004",
    "isolated_household_support_count_2024": "https://mediahub.seoul.go.kr/archives/2012885",
    "youth_move_support_max_krw": "https://mediahub.seoul.go.kr/archives/2013986",
    "youth_rent_support_office_worker_pct": "https://mediahub.seoul.go.kr/archives/2002193",
    "youth_rent_support_unemployed_pct": "https://mediahub.seoul.go.kr/archives/2002193",
    "youth_rent_support_student_pct": "https://mediahub.seoul.go.kr/archives/2002193",
    "youth_rent_support_service_worker_pct": "https://mediahub.seoul.go.kr/archives/2002193",
    "youth_rent_support_average_income_krw": "https://mediahub.seoul.go.kr/archives/2002193",
    "youth_rent_support_average_monthly_rent_krw": "https://mediahub.seoul.go.kr/archives/2002193",
    "youth_rent_support_average_management_fee_krw": "https://mediahub.seoul.go.kr/archives/2002193",
    "youth_rent_support_average_surplus_krw": "https://mediahub.seoul.go.kr/archives/2002193",
    "poor_housing_environment_share_pct": "https://mediahub.seoul.go.kr/archives/2002193",
    "economic_reason_for_housing_choice_pct": "https://mediahub.seoul.go.kr/archives/2002193",
    "school_or_job_proximity_reason_pct": "https://mediahub.seoul.go.kr/archives/2002193",
    "family_support_share_pct": "https://mediahub.seoul.go.kr/archives/2002193",
    "digital_training_campuses": "https://mediahub.seoul.go.kr/archives/2015552",
    "digital_training_job_placement_pct": "https://mediahub.seoul.go.kr/archives/2015552",
    "gwanak_youth_population_share_pct": "https://mediahub.seoul.go.kr/archives/2001979",
    "jung_one_person_household_share_pct": "https://mediahub.seoul.go.kr/archives/2004982",
    "district_population_monitor_2024": "https://data.si.re.kr/smr2024/smr2024_01population.html",
    "district_housing_monitor_2024": "https://data.si.re.kr/smr2024/smr2024_02housing.html",
    "district_industry_monitor_2024": "https://data.si.re.kr/smr2024/smr2024_03indecon.html",
    "district_traffic_monitor_2024": "https://data.si.re.kr/smr2024/smr2024_05traffic.html",
    "district_safety_monitor_2024": "https://data.si.re.kr/smr2024/smr2024_06safety.html",
    "presidential_2022_seoul_district_result": "https://www.segye.com/newsView/20220310518247",
    "general_2024_seoul_exit_poll": "https://www.hankyung.com/article/202404101816i",
}


SEOUL_CITYWIDE_SIGNALS: Dict[str, Any] = {
    "one_person_household_share_pct": 39.3,
    "walking_practice_rate_pct": 69.0,
    "isolated_household_support_count_2024": 44923,
    "youth_move_support_max_krw": 400000,
    "youth_rent_support_office_worker_pct": 24.9,
    "youth_rent_support_unemployed_pct": 22.3,
    "youth_rent_support_student_pct": 19.5,
    "youth_rent_support_service_worker_pct": 15.1,
    "youth_rent_support_average_income_krw": 1112000,
    "youth_rent_support_average_monthly_rent_krw": 390000,
    "youth_rent_support_average_management_fee_krw": 60000,
    "youth_rent_support_average_surplus_krw": -62000,
    "poor_housing_environment_share_pct": 36.0,
    "economic_reason_for_housing_choice_pct": 49.5,
    "school_or_job_proximity_reason_pct": 36.8,
    "family_support_share_pct": 32.6,
    "digital_training_campuses": 22,
    "digital_training_job_placement_pct": 75.0,
}


DISTRICT_FACT_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "Gangnam": {
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "low",
            "housing_stock_profile": "high_value_apartment_owner",
            "economic_activity_tier": "very_high",
            "green_access_tier": "medium",
            "youth_presence_tier": "medium",
            "ranked_indicator_notes": [
                "강남구는 2021년 자치구 GRDP 상위권으로 나타난다.",
                "공동주택 비중과 자산 민감도가 높은 지역군으로 해석된다.",
            ],
        },
        "election_baseline": {
            "presidential_2022": "conservative_stronghold",
            "general_2024": "conservative_hold",
            "political_lean_score": 2,
            "swing_index": 1,
        },
        "district_notes": ["강남3구 핵심 보수 기반, 자산가치와 조세 이슈에 민감."],
        "source_keys": ["district_industry_monitor_2024", "district_housing_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Gangdong": {
        "population_density_per_ha": 337.6,
        "district_indicators": {
            "population_density_tier": "very_high",
            "aging_tier": "medium",
            "housing_stock_profile": "family_apartment",
            "economic_activity_tier": "medium",
            "green_access_tier": "medium",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "conservative_lean",
            "general_2024": "competitive",
            "political_lean_score": 1,
            "swing_index": 3,
        },
        "district_notes": ["가족형 주거지 비중이 높고 교통·생활비 이슈의 반응 탄성이 큰 지역."],
        "source_keys": ["district_population_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Gangbuk": {
        "older_population_share_pct": 23.2,
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "very_high",
            "housing_stock_profile": "low_rise_mixed",
            "economic_activity_tier": "low",
            "green_access_tier": "high",
            "youth_presence_tier": "low",
        },
        "election_baseline": {
            "presidential_2022": "progressive_lean",
            "general_2024": "progressive_lean",
            "political_lean_score": -1,
            "swing_index": 2,
        },
        "district_notes": ["고령 비중이 높고 복지·균형발전 메시지에 반응도가 큰 편."],
        "source_keys": ["district_population_monitor_2024", "district_safety_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Gangseo": {
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "medium",
            "housing_stock_profile": "large_apartment_mixed",
            "economic_activity_tier": "growth_high",
            "green_access_tier": "medium",
            "youth_presence_tier": "medium",
            "growth_note": "2015~2021 GRDP growth ranked among the highest in Seoul.",
        },
        "election_baseline": {
            "presidential_2022": "progressive_lean",
            "general_2024": "progressive_lean",
            "political_lean_score": -1,
            "swing_index": 3,
        },
        "district_notes": ["서남권 성장축과 가족형 주거가 겹쳐 생활비·교통 공약에 민감."],
        "source_keys": ["district_industry_monitor_2024", "district_housing_monitor_2024", "general_2024_seoul_exit_poll"],
    },
    "Gwanak": {
        "youth_population_share_pct": 40.5,
        "population_density_per_ha": 316.8,
        "district_indicators": {
            "population_density_tier": "very_high",
            "aging_tier": "low_medium",
            "housing_stock_profile": "young_renter_cluster",
            "economic_activity_tier": "low_medium",
            "green_access_tier": "medium",
            "youth_presence_tier": "very_high",
        },
        "election_baseline": {
            "presidential_2022": "progressive_stronghold",
            "general_2024": "progressive_stronghold",
            "political_lean_score": -2,
            "swing_index": 2,
        },
        "district_notes": [
            "청년 인구와 1인 가구 집중도가 높다.",
            "주거비, 정착, 심야 안전, 일자리 이슈가 반복적으로 부각된다.",
        ],
        "source_keys": ["gwanak_youth_population_share_pct", "district_population_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Gwangjin": {
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "low",
            "housing_stock_profile": "mixed_urban_family",
            "economic_activity_tier": "medium",
            "green_access_tier": "medium",
            "youth_presence_tier": "medium_high",
        },
        "election_baseline": {
            "presidential_2022": "conservative_lean",
            "general_2024": "competitive_democratic",
            "political_lean_score": 0,
            "swing_index": 4,
        },
        "district_notes": ["청년 유입과 가족형 거주가 섞인 한강벨트 경합지."],
        "source_keys": ["presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Guro": {
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "medium",
            "housing_stock_profile": "industrial_renter_mixed",
            "economic_activity_tier": "medium_high",
            "green_access_tier": "medium_low",
            "youth_presence_tier": "medium",
            "technology_adoption_note": "Electric vehicle pressure per charger ranked high.",
        },
        "election_baseline": {
            "presidential_2022": "progressive_stronghold",
            "general_2024": "progressive_lean",
            "political_lean_score": -2,
            "swing_index": 2,
        },
        "district_notes": ["디지털단지 종사자와 생활비 민감 가구가 공존하는 서남권 핵심 지역."],
        "source_keys": ["district_traffic_monitor_2024", "general_2024_seoul_exit_poll"],
    },
    "Geumcheon": {
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "medium",
            "housing_stock_profile": "value_sensitive_renter",
            "economic_activity_tier": "medium_low",
            "green_access_tier": "medium_low",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "progressive_lean",
            "general_2024": "progressive_lean",
            "political_lean_score": -1,
            "swing_index": 3,
        },
        "district_notes": ["주거비와 고용 안정성 공약이 직접적으로 파급되는 가격 민감 지역."],
        "source_keys": ["general_2024_seoul_exit_poll"],
    },
    "Nowon": {
        "population_density_per_ha": 345.2,
        "apartment_share_pct": 86.6,
        "district_indicators": {
            "population_density_tier": "very_high",
            "aging_tier": "medium_high",
            "housing_stock_profile": "large_apartment_cluster",
            "economic_activity_tier": "medium_low",
            "green_access_tier": "high",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "progressive_lean",
            "general_2024": "progressive_lean",
            "political_lean_score": -1,
            "swing_index": 3,
        },
        "district_notes": ["아파트 밀집과 교육·생활비 민감도가 함께 높은 북동권 대표 주거지."],
        "source_keys": ["district_population_monitor_2024", "district_housing_monitor_2024", "district_safety_monitor_2024"],
    },
    "Dobong": {
        "older_population_share_pct": 22.2,
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "very_high",
            "housing_stock_profile": "older_family_mixed",
            "economic_activity_tier": "low_medium",
            "green_access_tier": "medium",
            "youth_presence_tier": "low",
        },
        "election_baseline": {
            "presidential_2022": "progressive_lean",
            "general_2024": "progressive_lean",
            "political_lean_score": -1,
            "swing_index": 2,
        },
        "district_notes": ["고령층 비중이 높고 의료·복지·생활 안정 메시지에 반응도가 높다."],
        "source_keys": ["district_population_monitor_2024"],
    },
    "Dongdaemun": {
        "district_indicators": {
            "population_density_tier": "medium_high",
            "aging_tier": "medium",
            "housing_stock_profile": "redevelopment_lowrise_mix",
            "economic_activity_tier": "medium",
            "green_access_tier": "medium_low",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "conservative_lean",
            "general_2024": "competitive_democratic",
            "political_lean_score": 0,
            "swing_index": 4,
        },
        "district_notes": ["재개발과 세입자 이슈가 맞물린 경합 성격이 강하다."],
        "source_keys": ["presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Dongjak": {
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "medium",
            "housing_stock_profile": "education_family_mixed",
            "economic_activity_tier": "medium",
            "green_access_tier": "medium",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "conservative_lean",
            "general_2024": "competitive",
            "political_lean_score": 0,
            "swing_index": 5,
        },
        "district_notes": ["동작갑·을 모두 전략 메시지에 흔들리기 쉬운 대표 경합지 성격."],
        "source_keys": ["presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Mapo": {
        "park_walkable_area_per_capita_sqm": 11.6,
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "low",
            "housing_stock_profile": "young_professional_renter_mix",
            "economic_activity_tier": "high",
            "green_access_tier": "high",
            "youth_presence_tier": "high",
        },
        "election_baseline": {
            "presidential_2022": "conservative_lean",
            "general_2024": "progressive_lean",
            "political_lean_score": 0,
            "swing_index": 5,
        },
        "district_notes": ["청년 전문직과 진보 성향 가족층이 섞여 메시지 프레이밍의 영향이 큰 지역."],
        "source_keys": ["district_safety_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Seodaemun": {
        "population_density_per_ha": 203.9,
        "district_indicators": {
            "population_density_tier": "low",
            "aging_tier": "medium",
            "housing_stock_profile": "student_family_mix",
            "economic_activity_tier": "medium",
            "green_access_tier": "medium",
            "youth_presence_tier": "medium_high",
        },
        "election_baseline": {
            "presidential_2022": "progressive_lean",
            "general_2024": "progressive_lean",
            "political_lean_score": -1,
            "swing_index": 3,
        },
        "district_notes": ["대학가와 중산층 가족 주거가 섞여 교육·교통 이슈 반응이 빠르다."],
        "source_keys": ["district_population_monitor_2024", "general_2024_seoul_exit_poll"],
    },
    "Seocho": {
        "population_density_per_ha": 202.6,
        "park_area_per_capita_sqm": 36.6,
        "district_indicators": {
            "population_density_tier": "low",
            "aging_tier": "low",
            "housing_stock_profile": "affluent_homeowner_apartment",
            "economic_activity_tier": "very_high",
            "green_access_tier": "high",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "conservative_stronghold",
            "general_2024": "conservative_hold",
            "political_lean_score": 2,
            "swing_index": 1,
        },
        "district_notes": ["자산가치, 교육, 질서 이슈에 민감한 서울 대표 보수 강세지."],
        "source_keys": ["district_population_monitor_2024", "district_safety_monitor_2024", "district_industry_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Seongdong": {
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "medium_low",
            "housing_stock_profile": "redevelopment_beneficiary_mix",
            "economic_activity_tier": "growth_high",
            "green_access_tier": "medium",
            "youth_presence_tier": "high",
        },
        "election_baseline": {
            "presidential_2022": "conservative_lean",
            "general_2024": "competitive_democratic",
            "political_lean_score": 0,
            "swing_index": 4,
        },
        "district_notes": ["재개발 수혜 기대와 청년 유입이 공존하는 마용성 핵심 경합지."],
        "source_keys": ["district_industry_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Seongbuk": {
        "single_detached_houses_count": 21000,
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "medium_high",
            "housing_stock_profile": "mixed_lowrise_family",
            "economic_activity_tier": "medium_low",
            "green_access_tier": "medium",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "progressive_lean",
            "general_2024": "progressive_lean",
            "political_lean_score": -1,
            "swing_index": 3,
        },
        "district_notes": ["단독·저층 주거와 교육 민감 가족층이 겹쳐 생활 안정 공약에 반응."],
        "source_keys": ["district_housing_monitor_2024", "general_2024_seoul_exit_poll"],
    },
    "Songpa": {
        "district_indicators": {
            "population_density_tier": "high",
            "aging_tier": "low",
            "housing_stock_profile": "mega_apartment_owner",
            "economic_activity_tier": "high",
            "green_access_tier": "high",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "conservative_stronghold",
            "general_2024": "conservative_hold_mixed",
            "political_lean_score": 2,
            "swing_index": 2,
        },
        "district_notes": ["강남3구 중에서도 가족·교육·자산 이슈가 결합된 대형 표밭."],
        "source_keys": ["district_housing_monitor_2024", "district_industry_monitor_2024", "district_safety_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Yangcheon": {
        "population_density_per_ha": 327.2,
        "district_indicators": {
            "population_density_tier": "very_high",
            "aging_tier": "medium",
            "housing_stock_profile": "education_homeowner_cluster",
            "economic_activity_tier": "medium",
            "green_access_tier": "medium",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "conservative_lean",
            "general_2024": "competitive_right",
            "political_lean_score": 1,
            "swing_index": 3,
        },
        "district_notes": ["목동권 교육·재건축 이슈가 강하게 작동하는 준보수 경합지."],
        "source_keys": ["district_population_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Yeongdeungpo": {
        "grdp_trillion_krw": 39.7,
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "medium",
            "housing_stock_profile": "office_service_renter_mix",
            "economic_activity_tier": "very_high",
            "green_access_tier": "medium_low",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "conservative_lean",
            "general_2024": "competitive_democratic",
            "political_lean_score": 0,
            "swing_index": 4,
        },
        "district_notes": ["여의도 업무권역과 서민 주거지가 섞인 전략 메시지 민감 지역."],
        "source_keys": ["district_industry_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Yongsan": {
        "population_density_per_ha": 168.8,
        "district_indicators": {
            "population_density_tier": "low",
            "aging_tier": "medium",
            "housing_stock_profile": "redevelopment_affluent_mix",
            "economic_activity_tier": "growth_high",
            "green_access_tier": "medium",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "conservative_stronghold",
            "general_2024": "competitive_right",
            "political_lean_score": 2,
            "swing_index": 3,
        },
        "district_notes": ["보수 강세이지만 개발·용산정치 이슈에 따라 흔들릴 수 있는 핵심 경합 축."],
        "source_keys": ["district_population_monitor_2024", "district_industry_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Eunpyeong": {
        "district_indicators": {
            "population_density_tier": "medium",
            "aging_tier": "medium_high",
            "housing_stock_profile": "stable_family_mixed",
            "economic_activity_tier": "medium_low",
            "green_access_tier": "medium_high",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "progressive_lean",
            "general_2024": "progressive_lean",
            "political_lean_score": -1,
            "swing_index": 2,
        },
        "district_notes": ["주거 안정과 복지, 교통 균형발전 메시지가 강하게 작동하는 서북권."],
        "source_keys": ["general_2024_seoul_exit_poll"],
    },
    "Jongno": {
        "population_density_per_ha": 117.8,
        "park_area_per_capita_sqm": 76.0,
        "park_walkable_area_per_capita_sqm": 20.1,
        "single_detached_house_share_pct": 24.7,
        "district_indicators": {
            "population_density_tier": "very_low",
            "aging_tier": "medium",
            "housing_stock_profile": "heritage_lowrise_business_mix",
            "economic_activity_tier": "high",
            "green_access_tier": "very_high",
            "youth_presence_tier": "medium_low",
        },
        "election_baseline": {
            "presidential_2022": "conservative_lean",
            "general_2024": "competitive",
            "political_lean_score": 1,
            "swing_index": 4,
        },
        "district_notes": ["전통 도심 정서와 소상공인·공공성 이슈가 혼재하는 상징 지역."],
        "source_keys": ["district_population_monitor_2024", "district_housing_monitor_2024", "district_safety_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Jung": {
        "one_person_household_share_pct": 41.4,
        "older_population_share_pct": 20.7,
        "population_density_per_ha": 132.5,
        "grdp_trillion_krw": 58.6,
        "park_walkable_area_per_capita_sqm": 10.6,
        "district_indicators": {
            "population_density_tier": "low",
            "aging_tier": "high",
            "housing_stock_profile": "downtown_service_single_household",
            "economic_activity_tier": "very_high",
            "green_access_tier": "high",
            "youth_presence_tier": "medium",
        },
        "election_baseline": {
            "presidential_2022": "conservative_lean",
            "general_2024": "competitive",
            "political_lean_score": 1,
            "swing_index": 4,
        },
        "district_notes": [
            "1인 가구 비율이 높아 단신가구·도심 서비스 이용자 정서가 강하다.",
        ],
        "source_keys": ["jung_one_person_household_share_pct", "district_population_monitor_2024", "district_industry_monitor_2024", "district_safety_monitor_2024", "presidential_2022_seoul_district_result", "general_2024_seoul_exit_poll"],
    },
    "Jungnang": {
        "population_density_per_ha": 346.6,
        "older_population_share_pct": 20.0,
        "district_indicators": {
            "population_density_tier": "very_high",
            "aging_tier": "high",
            "housing_stock_profile": "value_sensitive_family_mix",
            "economic_activity_tier": "medium_low",
            "green_access_tier": "medium",
            "youth_presence_tier": "medium_low",
        },
        "election_baseline": {
            "presidential_2022": "progressive_lean",
            "general_2024": "progressive_lean",
            "political_lean_score": -1,
            "swing_index": 2,
        },
        "district_notes": ["고밀·생활비 민감 지역으로 공공서비스·교통 개선 메시지 반응이 크다."],
        "source_keys": ["district_population_monitor_2024", "general_2024_seoul_exit_poll"],
    },
}


HOUSING_STATUS_SCORE = {
    "renters": 4,
    "mixed": 3,
    "homeowner": 1,
}

OCCUPATION_STABILITY_SCORE = {
    "low": 5,
    "low_medium": 4,
    "medium_low": 4,
    "medium": 3,
    "medium_high": 2,
    "high": 1,
}

TURNOUT_SCORE = {
    "low": 2,
    "medium_low": 3,
    "medium": 4,
    "medium_high": 5,
    "high": 6,
}


ISSUE_SCORE_MAP = {
    "rent": {"housing_pressure_score": 2, "youth_issue_pressure_score": 2},
    "housing": {"housing_pressure_score": 1},
    "housing_cost": {"housing_pressure_score": 2},
    "housing_affordability": {"housing_pressure_score": 2},
    "redevelopment": {"asset_sensitivity_score": 2, "local_change_pressure_score": 1},
    "asset_values": {"asset_sensitivity_score": 2},
    "housing_values": {"asset_sensitivity_score": 2},
    "taxes": {"asset_sensitivity_score": 1},
    "jobs": {"employment_anxiety_score": 2, "youth_issue_pressure_score": 1},
    "job_security": {"employment_anxiety_score": 2},
    "innovation": {"digital_job_exposure_score": 2},
    "economic_growth": {"digital_job_exposure_score": 1},
    "business_district_growth": {"digital_job_exposure_score": 1},
    "transport": {"mobility_dependency_score": 2},
    "public_transport": {"mobility_dependency_score": 2},
    "commute_time": {"mobility_dependency_score": 2},
    "mobility": {"mobility_dependency_score": 1},
    "schools": {"family_service_pressure_score": 2},
    "childcare": {"family_service_pressure_score": 2},
    "parks": {"family_service_pressure_score": 1},
    "welfare": {"welfare_sensitivity_score": 2},
    "healthcare": {"health_activity_score": 1, "welfare_sensitivity_score": 1},
    "aging": {"isolation_risk_score": 2, "welfare_sensitivity_score": 1},
    "public_services": {"welfare_sensitivity_score": 1},
    "small_business": {"small_business_pressure_score": 2},
    "tourism": {"small_business_pressure_score": 1},
    "public_order": {"local_change_pressure_score": 1},
    "fairness": {"trust_volatility_score": 1},
    "competence": {"trust_volatility_score": 1},
    "quality_of_life": {"trust_volatility_score": 1},
}


def _clamp_score(value: int) -> int:
    return max(1, min(5, value))


def _base_modeled_scores(bloc: Dict[str, Any]) -> Dict[str, int]:
    scores = {
        "housing_pressure_score": 2 + HOUSING_STATUS_SCORE.get(bloc.get("housing_status", "mixed"), 3) // 2,
        "employment_anxiety_score": OCCUPATION_STABILITY_SCORE.get(bloc.get("occupation_stability", "medium"), 3),
        "mobility_dependency_score": 2,
        "digital_job_exposure_score": 2,
        "welfare_sensitivity_score": 2,
        "isolation_risk_score": 2,
        "health_activity_score": 3,
        "youth_issue_pressure_score": 2 if bloc.get("life_stage") == "mixed_working_age" else 1,
        "asset_sensitivity_score": 1 if bloc.get("housing_status") == "homeowner" else 2,
        "family_service_pressure_score": 2 if bloc.get("life_stage") == "settled_households" else 1,
        "small_business_pressure_score": 1,
        "trust_volatility_score": 2 if "swing" in bloc.get("party_lean", "") else 1,
        "local_change_pressure_score": 2,
        "turnout_energy_score": TURNOUT_SCORE.get(bloc.get("turnout_tendency", "medium"), 4) - 1,
    }

    for issue in bloc.get("top_issues", []):
        for key, delta in ISSUE_SCORE_MAP.get(issue, {}).items():
            scores[key] = scores.get(key, 1) + delta

    for key, value in list(scores.items()):
        scores[key] = _clamp_score(int(value))
    return scores


def enrich_bloc_quant_signals(district: str, bloc: Dict[str, Any]) -> Dict[str, Any]:
    enriched = deepcopy(bloc)
    district_facts = DISTRICT_FACT_OVERRIDES.get(district, {})

    official_signals = {
        key: district_facts.get(key, value)
        for key, value in SEOUL_CITYWIDE_SIGNALS.items()
    }
    for key, value in district_facts.items():
        if key not in {"district_notes", "source_keys", "district_indicators", "election_baseline"}:
            official_signals[key] = value

    modeled_scores = _base_modeled_scores(enriched)

    if official_signals.get("one_person_household_share_pct", 0) >= 40:
        modeled_scores["isolation_risk_score"] = _clamp_score(modeled_scores["isolation_risk_score"] + 1)
        modeled_scores["housing_pressure_score"] = _clamp_score(modeled_scores["housing_pressure_score"] + 1)

    if district == "Gwanak":
        modeled_scores["youth_issue_pressure_score"] = 5
        modeled_scores["housing_pressure_score"] = _clamp_score(modeled_scores["housing_pressure_score"] + 1)
        modeled_scores["mobility_dependency_score"] = _clamp_score(modeled_scores["mobility_dependency_score"] + 1)

    if bloc.get("housing_status") == "renters":
        modeled_scores["housing_pressure_score"] = _clamp_score(modeled_scores["housing_pressure_score"] + 1)
        modeled_scores["swing_sensitivity_score"] = 4
    else:
        modeled_scores["swing_sensitivity_score"] = 2 if bloc.get("housing_status") == "homeowner" else 3

    enriched["official_signals"] = official_signals
    enriched["district_indicators"] = deepcopy(district_facts.get("district_indicators", {}))
    enriched["election_baseline"] = deepcopy(
        district_facts.get(
            "election_baseline",
            {
                "presidential_2022": "competitive",
                "general_2024": "competitive",
                "political_lean_score": 0,
                "swing_index": 3,
            },
        )
    )
    enriched["modeled_scores"] = modeled_scores
    enriched["source_context"] = {
        "signal_basis": "official_city_or_public_news",
        "score_basis": "heuristic_modeling_from official signals + district theme profile + election baseline",
        "district_notes": district_facts.get("district_notes", []),
    }
    enriched["source_refs"] = [
        {"key": key, "url": url}
        for key, url in SEOUL_SIGNAL_SOURCES.items()
        if key in official_signals or key in district_facts.get("source_keys", [])
    ]
    return enriched
