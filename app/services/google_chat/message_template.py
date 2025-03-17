from app.utils import config, constants


def generate_report(payload):
    message = constants.REPORT_TEMPLATE.format(
        not_political=payload.get("not_political"),
        political=payload.get("political"),
        not_related_to_lk=payload.get("not_related_to_lk"),
        related_to_lk=payload.get("related_to_lk"),
        not_phishing=payload.get("not_phishing"),
        phishing=payload.get("phishing"),
        total_sites_scanned=payload.get("total_sites_scanned"),
        google_sheet_url=config.GOOGLE_SHEET_URL
    )

    return message
