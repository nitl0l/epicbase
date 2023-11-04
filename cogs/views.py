from discord import Color, Embed, InputTextStyle, Interaction, ui

from .models import Employee, Review

__all__ = ("ReviewInput",)


class ReviewInput(ui.Modal):
    def __init__(self) -> None:
        super().__init__(
            ui.InputText(
                label="Employee",
                placeholder="The name of your employee",
                style=InputTextStyle.singleline,
            ),
            ui.InputText(
                label="Rating",
                placeholder="Your rating on a 1-10 scale (e.g 9.5)",
                style=InputTextStyle.singleline,
            ),
            ui.InputText(
                label="Write your review",
                style=InputTextStyle.long,
            ),
            title="New Review",
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(invisible=True)
        employee_name, rating_raw, review = self.children
        employee_record, created = await Employee.get_or_create(
            name__iexact=employee_name.value, defaults={"name": employee_name.value}
        )
        try:
            rating_value = float(rating_raw.value.strip())
        except ValueError:
            return await interaction.followup.send(
                content=":x: Your rating must be a number (e.g 10 or 9.5)",
                ephemeral=True,
            )
        if (rating_value > 10) or (rating_value < 1):
            return await interaction.followup.send(
                content=":x: Your rating must be between 1-10", ephemeral=True
            )
        await Review.create(
            employee_id=employee_record.id,
            rating=rating_value,
            description=review.value,
        )
        embed = Embed(
            title="Thank you for your feedback!",
            description="Your feedback has been stored.",
            color=Color.green(),
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
