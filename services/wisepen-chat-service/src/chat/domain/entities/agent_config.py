from typing import List, Optional

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """
    Agent 运行时配置。

    主 Agent 会话配置（存于 ChatSession.agent_config）与子 Agent 配置（存于 Redis）共用同一类型。
    所有字段默认值均为保守策略，主 Agent 的实际默认值由 DEFAULT_MAIN_AGENT_CONFIG 常量设置。

    字段分组：
    - 模型控制：model_id
    - 提示词控制：system_prompt_override / system_prompt_append
    - 工具权限控制：allow_tool_names / deny_tool_names / expose_reserved_tool_names
    - Skill 控制：allowed_skill_ids / disable_skill_matching
    - 运行时策略：max_iterations / enable_long_term_memory
    """

    # ── 模型控制 ──────────────────────────────────────────────────────────────
    model_id: Optional[str] = Field(
        default=None,
        description=(
            "指定使用的模型 ID。"
            "为 None 时：子 Agent 继承主 Agent 的模型；主 Agent 使用系统默认模型。"
        ),
    )

    # ── 提示词控制 ────────────────────────────────────────────────────────────
    system_prompt_override: Optional[str] = Field(
        default=None,
        description=(
            "完全替换系统提示词。"
            "设置后将忽略默认 System Prompt，适合专用子 Agent。"
            "与 system_prompt_append 互斥，override 优先。"
        ),
    )
    system_prompt_append: Optional[str] = Field(
        default=None,
        description=(
            "在默认 System Prompt 末尾追加的内容。"
            "适合轻度扩展，不影响默认提示词主体。"
            "若 system_prompt_override 已设置，则本字段被忽略。"
        ),
    )

    # ── 工具权限控制（映射到 ToolRegistry.derive() 的同名参数）────────────────
    allow_tool_names: Optional[List[str]] = Field(
        default=None,
        description=(
            "工具白名单。"
            "为 None 时继承注册表全部非 reserved 工具；"
            "设置后只保留列表内的工具。"
        ),
    )
    deny_tool_names: Optional[List[str]] = Field(
        default=None,
        description=(
            "工具黑名单。"
            "为 None 时不屏蔽任何工具；"
            "列表内的工具名将被强制排除（优先级低于 allow_tool_names）。"
        ),
    )
    expose_reserved_tool_names: Optional[List[str]] = Field(
        default=None,
        description=(
            "需要解禁的 reserved 工具名列表（reserved 工具默认对 LLM 不可见）。"
            "主 Agent 可通过此字段将 create_sub_agent / call_sub_agent 暴露给 LLM（自由模式）。"
        ),
    )

    # ── Skill 控制 ────────────────────────────────────────────────────────────
    allowed_skill_ids: Optional[List[str]] = Field(
        default=None,
        description=(
            "本轮允许 LLM 加载的 Skill ID 白名单。"
            "为 None 时由 SkillMatcher 正常匹配决定；设置后 matcher 结果会被进一步过滤。"
        ),
    )
    disable_skill_matching: bool = Field(
        default=False,
        description=(
            "是否完全禁用 Skill 匹配。"
            "子 Agent 默认为 True（create_sub_agent 工具在未收到 config 时自动覆盖）；"
            "主 Agent 默认为 False。"
        ),
    )

    # ── 运行时策略 ────────────────────────────────────────────────────────────
    max_iterations: int = Field(
        default=10,
        ge=1,
        le=50,
        description="ReAct 循环最大迭代次数，防止无限循环。",
    )
    enable_long_term_memory: bool = Field(
        default=False,
        description="是否在本轮对话开始前检索 Mem0 长期记忆并注入上下文。",
    )


# 主 Agent 在 ChatSession.agent_config 为 None 时使用的默认配置。
# 与 AgentConfig 字段默认值有意区分：主 Agent 需要更多迭代次数和长期记忆支持。
DEFAULT_MAIN_AGENT_CONFIG = AgentConfig(
    enable_long_term_memory=True,
    max_iterations=20,
)
