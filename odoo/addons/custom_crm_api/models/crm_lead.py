from odoo import models, api


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def send_weekly_greetings(self):
        template = self.env["mail.template"].search(
            [("name", "=", "Weekly Greeting")],
            limit=1
        )

        if not template:
            return

        leads = self.search([
            ("email_from", "!=", False),
        ])

        for lead in leads:
            template.send_mail(
                lead.id,
                force_send=True,
                email_values={
                    "email_to": lead.email_from,
                },
            )
