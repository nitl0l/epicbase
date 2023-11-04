import discord
from discord import ApplicationContext, Cog, Color, Embed
from discord.ext import pages

from .models import Employee, Review
from .views import ReviewInput


class CoreCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="reviews", description="See reviews for an employee.")
    @discord.option(name="employee", type=str, description="The name of your employee.")
    async def search_reviews(self, ctx: ApplicationContext, employee: str):
        await ctx.defer(ephemeral=True)
        employee_record = await Employee.filter(name__iexact=employee).first()
        if employee_record:
            employee_id = employee_record.id
            review_embeds = []
            reviews = await Review.filter(employee_id=employee_id).all()
            average_rating = sum([review.rating for review in reviews]) / len(reviews)
            overview_embed = Embed(title="Overview", color=Color.green())
            overview_embed.add_field(
                name="Employee Name", value=employee_record.name.upper()
            )
            overview_embed.add_field(
                name="Average Rating",
                value="{rating:.1f}/10".format(rating=average_rating),
            )
            review_embeds.append([overview_embed])
            for review in reviews:
                review_embed = Embed(title="Review", color=Color.dark_green())
                review_embed.add_field(
                    name="Rating", value="{rating:.1f}/10".format(rating=review.rating)
                )
                review_embed.add_field(
                    name="Description",
                    value="```\n{review_text}\n```".format(
                        review_text=review.description
                    ),
                    inline=False,
                )
                review_embeds.append([review_embed])
            paginator = pages.Paginator(pages=review_embeds)
            await paginator.respond(
                ctx.interaction,
                ephemeral=True,
                target_message="Reviews for `{employee_name}`".format(
                    employee_name=employee_record.name.upper()
                ),
            )
        else:
            await ctx.respond(
                "Sorry, we do not have any records for `{employee_name}`. Feel free to leave a review with {review_command}".format(
                    employee_name=employee, review_command=self.leave_review.mention
                )
            )

    @discord.slash_command(
        name="newreview", description="Leave feedback for an employee."
    )
    async def leave_review(self, ctx: ApplicationContext):
        await ctx.send_modal(ReviewInput())


def setup(bot):
    bot.add_cog(CoreCommands(bot))
