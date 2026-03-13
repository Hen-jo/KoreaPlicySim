"""
模拟预设定义
"""

from typing import Dict


DEFAULT_PRESET = "generic_social"
KOREA_PRESET = "korea_society_policy"


SIMULATION_PRESETS: Dict[str, Dict[str, str]] = {
    DEFAULT_PRESET: {
        "label": "通用社交模拟",
        "ontology_focus": (
            "聚焦可发声的个人、组织、媒体、平台与事件相关主体，"
            "适用于一般舆情传播与观点互动场景。"
        ),
        "profile_focus": (
            "生成符合社交媒体表达习惯的账号画像，突出立场、表达风格、"
            "影响力和互动偏好。"
        ),
        "config_focus": (
            "围绕线上话题扩散、立场冲突、权威回应、媒体放大等社媒过程"
            "配置时间节奏和行为强度。"
        ),
    },
    KOREA_PRESET: {
        "label": "韩国政治与政策反应模拟",
        "ontology_focus": (
            "聚焦韩国政治与政策传播场景中的选民群体、候选人、政党、地方政府、"
            "区级/市级行政主体、媒体、民间团体、平台与关键议题执行机构。优先"
            "保留能体现首尔、特定区、特定选区差异以及政策受益/受损差异的实体。"
        ),
        "profile_focus": (
            "生成人设或机构账号时强调居住地（首尔/특정 구/선거구）、年龄段、职业、"
            "阶层感受、媒体消费、政党倾向、议题优先级、政策得失感，以及对候选人、"
            "公约与行政绩效的敏感点。"
        ),
        "config_focus": (
            "以韩国政治议题、政策 발표、公约 비교、候选人 논쟁和民调波动为中心配置"
            "事件与行为，重点观察首尔内不同区/选区之间的反应差异、政策支持率变化、"
            "候选人好感度变化、媒体 framing 与线上扩散路径。"
        ),
    },
}


def normalize_preset(preset: str | None) -> str:
    if not preset:
        return DEFAULT_PRESET
    return preset if preset in SIMULATION_PRESETS else DEFAULT_PRESET


def get_preset_context(preset: str | None) -> Dict[str, str]:
    normalized = normalize_preset(preset)
    context = dict(SIMULATION_PRESETS[normalized])
    context["key"] = normalized
    return context
