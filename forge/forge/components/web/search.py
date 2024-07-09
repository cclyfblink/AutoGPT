import json
import logging
import time
from typing import Iterator, Optional

from duckduckgo_search import DDGS
from pydantic import BaseModel, SecretStr

from forge.agent.components import ConfigurableComponent
from forge.agent.protocols import CommandProvider, DirectiveProvider
from forge.command import Command, command
from forge.models.config import UserConfigurable
from forge.models.json_schema import JSONSchema
from forge.utils.exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class WebSearchConfiguration(BaseModel):
    google_api_key: Optional[SecretStr] = UserConfigurable(
        None, from_env="GOOGLE_API_KEY", exclude=True
    )
    google_custom_search_engine_id: Optional[SecretStr] = UserConfigurable(
        None, from_env="GOOGLE_CUSTOM_SEARCH_ENGINE_ID", exclude=True
    )
    duckduckgo_max_attempts: int = 3



import json
from typing import Iterator, Optional

from forge.agent.components import ConfigurableComponent
from forge.agent.protocols import CommandProvider, DirectiveProvider
from forge.command import Command, command
from forge.models.config import UserConfigurable
from forge.models.json_schema import JSONSchema

from baidu_search import search as baidu_search

logger = logging.getLogger(__name__)


class BaiduSearchConfiguration:
    pass


class BaiduSearchComponent(
    DirectiveProvider, CommandProvider, ConfigurableComponent[BaiduSearchConfiguration]
):
    """Provides commands to search the web using Baidu."""

    config_class = BaiduSearchConfiguration

    def __init__(self, config: Optional[BaiduSearchConfiguration] = None):
        pass

    def get_resources(self) -> Iterator[str]:
        yield "Internet access for searches and information gathering."

    def get_commands(self) -> Iterator[Command]:
        yield self.web_search

    @command(
        ["web_search", "search"],
        "Searches the web",
        {
            "query": JSONSchema(
                type=JSONSchema.Type.STRING,
                description="The search query",
                required=True,
            ),
            "num_results": JSONSchema(
                type=JSONSchema.Type.INTEGER,
                description="The number of results to return",
                minimum=1,
                maximum=10,
                required=False,
            ),
        },
    )
    def web_search(self, query: str, num_results: int = 8) -> str:
        """
        Return the results of a Baidu search.

        Args:
            query (str): The search query.
            num_results (int): The number of results to return.

        Returns:
            str: The results of the search.
        """
        search_results = baidu_search(query, num_results)

        # Convert the search results to the expected format
        formatted_results = ["## Search results\n"]
        for rank, result in enumerate(search_results, start=1):
            title = result.get("title", "N/A")
            url = result.get("url", "N/A")
            abstract = result.get("abstract", "N/A")
            formatted_results.append(f"### {title}\n")
            formatted_results.append(f"**URL:** {url}\n")
            formatted_results.append(f"**Excerpt:** {abstract}\n")

        return """\n""".join(formatted_results)
