from discord.ext.commands import Context

from Methods import Emojis
from Bot import bot, admin_ids


@bot.command()
async def test(ctx: Context):
    for admin_id in admin_ids:
        user = await bot.fetch_user(admin_id)
        if ctx.message.author == user:
            await ctx.send("test")

@bot.tree.command(name = "emoji",
                description = "send the corresponding majiang emoji (for test purposes)")
async def emoji(interaction, name: str):
    await interaction.response.send_message(Emojis.get_emoji(bot, name))

@bot.command()
async def emoji(ctx, name: str):
    await ctx.send(Emojis.get_emoji(bot, name))