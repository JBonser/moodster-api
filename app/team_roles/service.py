from app.team_roles.model import TeamRole


def get_all_team_roles():
    return TeamRole.query.all()


def get_team_role_by_name(name):
    return TeamRole.query.filter_by(name=name).first()
