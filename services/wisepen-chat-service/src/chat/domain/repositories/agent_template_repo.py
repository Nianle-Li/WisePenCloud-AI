from abc import ABC, abstractmethod
from typing import List, Optional

from chat.domain.entities.agent_template import AgentTemplate, AgentTemplateMeta


class AgentTemplateRepository(ABC):
    """
    AgentTemplate 的只读仓储接口（AI 服务侧 view）。

    本服务只消费已发布的模板；创建/编辑/删除由管理后台完成，不在此接口中定义。
    """

    @abstractmethod
    async def list_enabled_template_metas(self) -> List[AgentTemplateMeta]:
        """
        返回所有 enabled=True 的模板轻量元信息（不含完整 agent_config）。
        供 SkillAndAgentMatcher warmup 缓存，以及 ChatContextAssembler 构建模板清单。
        """
        ...

    @abstractmethod
    async def get_template(self, template_id: str) -> Optional[AgentTemplate]:
        """
        按 template_id 读取完整文档（含 agent_config）。
        ChatTurnCoordinator 在 create_sub_agent 使用 template_id 时调用。
        """
        ...
