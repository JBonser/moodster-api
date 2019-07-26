from app import create_app
from app.teams.service import create_team_in_db
from app.users.service import create_user_in_db
from app.team_members.service import create_membership_in_db
from app.team_roles.service import get_team_role_by_name

app = create_app("dev")
app.app_context().push()

admin_user = create_user_in_db("admin", "password")
member_user = create_user_in_db("member", "password")
team = create_team_in_db("default_team")
member_role = get_team_role_by_name("Member")
admin_role = get_team_role_by_name("Admin")

create_membership_in_db(team, member_user, member_role)
create_membership_in_db(team, admin_user, admin_role)
