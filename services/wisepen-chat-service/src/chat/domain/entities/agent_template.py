from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from beanie import Document
from pydantic import Field
from pymongo import IndexModel, ASCENDING

from chat.domain.entities.agent_config import AgentConfig


class AgentTemplate(Document):
    """
    预制子 Agent 模板（MongoDB 文档）。

    与 Skill 的核心区别：
    - Skill 携带指令文档（content_markdown），由主 Agent LLM 读取后在自身上下文中执行；
    - AgentTemplate 携带 AgentConfig，由 SubAgentRuntime 驱动独立的 Action Loop 执行。

    激活方式：
    - AgentTemplate 不做关键词过滤，SkillAndAgentMatcher 每轮直接返回全部 enabled=True 的模板；
    - ChatContextAssembler 将可用模板清单注入 System Prompt，由 LLM 自主决定是否使用。
    """

    template_id: str = Field(
        ...,
        description="唯一 slug，如 'security-analyst'。全链路工具参数、日志只用这个。",
    )
    display_name: str = Field(
        ...,
        description="展示名，如 'Security Analyst'，用于 System Prompt 清单和 SSE 事件。",
    )
    description: str = Field(
        ...,
        description="一句话说明本模板的场景与目的，注入 System Prompt 供 LLM 判断是否使用。",
    )

    agent_config: AgentConfig = Field(
        ...,
        description="子 Agent 运行时配置，create_sub_agent 以此为基础（config 字段可覆盖）。",
    )

    is_system: bool = Field(
        default=False,
        description="是否为内置系统模板；True 时 owner_user_id 为空。",
    )
    owner_user_id: Optional[str] = Field(
        default=None,
        description="用户自建模板的归属用户 ID；系统模板为 None。",
    )
    enabled: bool = Field(
        default=True,
        description="启停开关；False 时 SkillAndAgentMatcher 不会返回本模板。",
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "wisepen_agent_templates"
        indexes = [
            # template_id 作为业务主键，保证唯一
            IndexModel([("template_id", ASCENDING)], unique=True),
            # SkillAndAgentMatcher warmup 只拉 enabled=True；is_system 用于管理后台过滤
            IndexModel([("enabled", ASCENDING), ("is_system", ASCENDING)]),
        ]


@dataclass(frozen=True)
class AgentTemplateMeta:
    """
    SkillAndAgentMatcher / ChatContextAssembler 使用的轻量元信息快照。

    只含向 LLM 呈现可用模板清单所需的字段，不含完整 agent_config。
    ChatTurnCoordinator 在需要完整配置时另行从 MongoDB 读取 AgentTemplate。
    """

    template_id: str
    display_name: str
    description: str
