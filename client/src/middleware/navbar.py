from flask import session


def register_navbar(app):

    @app.context_processor
    def inject_navbar():

        user = session.get("user", {})

        is_admin = user.get("is_admin", False)

        if is_admin:
            links = {
                "dashboard": "/admin",
                "analysis": "/admin/analysis",
                "analysis_name": "Analysis"
            }
        else:
            links = {
                "dashboard": "/dashboard",
                "analysis": "/analysis",
                "analysis_name": "Usage"
            }

        return {
            "nav_links": links
        }