"""Discord.py UI view for paginating a list."""
from typing import Any, Callable, Coroutine, TypeVar

from discord import ButtonStyle, Interaction
from discord.ext.commands import Context
from discord.ui import Button, View


class Paginator(View):
    """View for paginating a list of items."""

    T = TypeVar('T')

    def __init__(
            self,
            ctx: Context,
            title: str,
            page_count: int,
            get_page: Callable[[int], Coroutine[Any, Any, list[T]]],
            formatter: Callable[[T], str]):
        """Create a new paginator view."""
        super().__init__(timeout=None)
        self.back_button = PaginatorButton(delta=-1, label='🠐')
        self.next_button = PaginatorButton(delta=1, label='🠒')
        self.add_item(self.back_button)
        self.add_item(self.next_button)
        self.ctx = ctx
        self.title = title
        self.page_count = page_count
        self.get_page = get_page
        self.formatter = formatter
        self.page = 0

    async def setup(self):
        """Send the view."""
        await self.ctx.send(content=await self.render(), view=self)

    async def render(self) -> str:
        """Render the current page."""
        self.back_button.disabled = self.page <= 0
        self.next_button.disabled = self.page >= self.page_count - 1
        lines = list(map(self.formatter, await self.get_page(self.page)))
        content = '\n'.join(lines) or "*There's nothing here.*"
        return (
            f'**{self.title}**\n\n{content}\n\n'
            f'Page {self.page + 1} of {self.page_count or 1}'
        )


class PaginatorButton(Button[Paginator]):
    """A button for moving a paginator forwards or backwards."""

    def __init__(self, delta: int, label: str):
        """Set up the button."""
        super().__init__(style=ButtonStyle.secondary, label=label)
        self.delta = delta

    async def callback(self, interaction: Interaction):
        """Handle the button being pressed."""
        if interaction.user.id != self.view.ctx.author.id:
            return
        self.view.page += self.delta
        if self.view.page < 0:
            self.view.page = 0
        if self.view.page >= self.view.page_count:
            self.view.page = self.view.page_count - 1
        await interaction.response.edit_message(
            content=await self.view.render(),
            view=self.view,
        )
