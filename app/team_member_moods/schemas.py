from flask_restplus import fields, Model


team_member_mood_post_schema = Model(
    "team_member_mood_post",
    {
        "mood_id": fields.String(required=True, description="mood id"),
    },
)

team_member_mood_view_schema = Model(
    "team_member_mood_view",
    {
        "id": fields.String(attribute="public_id", description="team member mood id"),
        "team_member_id": fields.String(
            attribute="team_member.public_id", description="team member id"
        ),
        "mood_id": fields.String(attribute="mood.public_id", description="mood id"),
    },
)
