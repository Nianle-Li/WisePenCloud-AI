from dataclasses import dataclass
from typing import Any, Protocol

from chat.application.tools.core.definition import ToolPolicy, ToolParametersSchema
from chat.application.tools.core.llm.invocation import ToolInvocation


@dataclass(frozen=True)
class ToolPreflightResult:
    ok: bool
    message: str | None = None

class ToolPreflightHook(Protocol):
    name: str

    async def check(
        self,
        invocation: ToolInvocation,
        policy: ToolPolicy,
        parameters_schema: ToolParametersSchema,
        context: dict[str, Any],
    ) -> ToolPreflightResult:
        ...