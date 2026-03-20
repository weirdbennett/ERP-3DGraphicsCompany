import json
from odoo import http
from odoo.http import request


class LeadRestController(http.Controller):

    @http.route(
        "/api/leads",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def create_lead(self, **kwargs):
        # Безпечний парсинг JSON (Odoo 19 friendly)
        try:
            raw_data = request.httprequest.data
            data = json.loads(raw_data.decode("utf-8")) if raw_data else {}
        except Exception as e:
            return request.make_response(
                json.dumps({"error": "Invalid JSON"}),
                headers=[("Content-Type", "application/json")],
                status=400,
            )

        if not data.get("name"):
            return request.make_response(
                json.dumps({"error": "Field 'name' is required"}),
                headers=[("Content-Type", "application/json")],
                status=400,
            )

        lead = request.env["crm.lead"].sudo().create({
            "name": data["name"],
            "email_from": data.get("email"),
            "phone": data.get("phone"),
        })

        return request.make_response(
            json.dumps({
                "status": "success",
                "lead_id": lead.id
            }),
            headers=[("Content-Type", "application/json")],
            status=200,
        )
