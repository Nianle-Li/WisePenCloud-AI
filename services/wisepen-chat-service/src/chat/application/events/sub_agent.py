from dataclasses import dataclass

from chat.application.events.base import StreamEvent


@dataclass(frozen=True)
class SubAgentStartEvent(StreamEvent):
    """
    子 Agent 开始执行。
    SubAgentRuntime.run() 进入 QueryLoopRuntime 循环前推送。
    """

    agent_id: str
    """子 Agent 实例 ID，由 create_sub_agent 工具生成（格式：sa_xxxxxxxx）。"""

    display_name: str
    """子 Agent 展示名，来自 create_sub_agent 的 display_name 参数或 description 兜底。"""


@dataclass(frozen=True)
class SubAgentStepEvent(StreamEvent):
    """
    子 Agent 产出增量文本。
    SubAgentRuntime 内部监听到 QueryLoopRuntime 的 TextDeltaEvent 时包装转发。
    """

    agent_id: str
    """来源子 Agent 实例 ID，用于多子 Agent 并行时区分来源。"""

    delta: str
    """文本增量片段，直接来自子 Agent LLM 输出的 TextDeltaEvent.delta。"""


@dataclass(frozen=True)
class SubAgentCompleteEvent(StreamEvent):
    """
    子 Agent 完成（成功或失败）。
    SubAgentRuntime.run() 循环结束后推送。
    """

    agent_id: str
    """来源子 Agent 实例 ID。"""

    result_summary: str
    """
    子 Agent 最终输出的摘要，截断至 500 字，仅用于前端进度展示。
    主 Agent 收到的完整 tool result 不做截断，由 CallSubAgentTool 直接返回。
    """

    success: bool
    """True 表示子 Agent 正常完成；False 表示内部出现异常或达到 max_iterations。"""
