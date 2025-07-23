from django.core.management.base import BaseCommand #base class from which all manage.py commands should run like 'py manage.py setup_permissions'
from jobs.models import Permission, RolePermission  
from users.choices import UserRoles 

class Command(BaseCommand):

    help = "Setup default dynamic role-based permissions" #help shows what the command does if someone types python manage.py help

    def handle(self, *args, **kwargs): #this fnc runs when you execute the command in the terminal
        permissions_map = {
            'job': {
                'employer': ['create', 'update', 'delete', 'list', 'retrieve'],
                'jobseeker': ['list', 'retrieve'],
                'admin': ['create', 'update', 'delete', 'list', 'retrieve']
            },
            'application': {
                'employer': ['list', 'retrieve', 'update'],  # update will be used for shortlisting
                'jobseeker': ['create', 'update', 'delete', 'list', 'retrieve'],
                'admin': ['create', 'update', 'delete', 'list', 'retrieve']
            },
            'jobcategory': {
                'employer': ['create', 'update', 'delete', 'list', 'retrieve'],
                'admin': ['create', 'update', 'delete', 'list', 'retrieve']
            }
        }

        for model_name, role_actions in permissions_map.items():
            for role, actions in role_actions.items():
                for action in actions:
                    code = f'{model_name}_{action}' #gen code like job_create
                

                    #Check if this permission already exists in the DB. If not, create it with a nice description like: "Can create job" or "Can list application".
                    perm, _ = Permission.objects.get_or_create(
                        code = code,
                        defaults = {'description': f'can_{action}_{model_name}'}
                    )

                    #now link this permission to a user role if not already linked
                    RolePermission.objects.get_or_create(
                        role = role,
                        permission = perm
                    )

        self.stdout.write(self.style.SUCCESS('Permissions and role bindings set up successfully.'))
        #print like command that appears in your terminal when you run management commands and it executes successfully
        #runs only for management commands inside the handle fnc, it is a property of BaseCommand class from Django

        # unlike print, it’s part of Django’s command system, so it:
        # Works well with command output redirection
        # Supports colored/styled text
        # Helps Django log the output properly if needed

        #Django has a few styles like:
        # self.style.SUCCESS("...") → Green text ✅
        # self.style.ERROR("...") → Red text ❌
        # self.style.WARNING("...") → Yellow text ⚠️
        # self.style.NOTICE("...") → Blueish/grey 📝


                