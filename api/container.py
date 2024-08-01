from api.dao.task import TaskDAO
from api.dao.user import UserDAO
from api.dao.redis import RedisDAO
from api.services.task import TaskService
from api.services.user import UserService
from api.services.authentication import AuthenticationService


user_dao = UserDAO()
user_service = UserService(user_dao)

task_dao = TaskDAO()
task_service = TaskService(task_dao)

redis_dao = RedisDAO()
auth_service = AuthenticationService(redis_dao)
