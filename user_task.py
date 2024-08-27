class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.created_tasks = 0
        self.completed_tasks = 0
        
    def create_task(self, num):
        self.created_tasks = num
        
    def complete_task(self):
        self.completed_tasks += 1
        if self.all_tasks_completed():
            self.delete_user_data()
        
    def all_tasks_completed(self):
        return self.completed_tasks == self.created_tasks
    
    def delete_user_data(self):
        del users_data[self.user_id]


class Users:
    def __init__(self):
        self.users_data = {}


    def add_user(self, user_id):
        if user_id not in self.users_data:
            self.users_data[user_id] = User(user_id)
        else:
            print(f"User with ID {user_id} already exists.")

    def create_task(self, user_id):
        if user_id in self.users_data:
            self.users_data[user_id].create_task()
        else:
            print(f"User with ID {user_id} not found.")

    def complete_task(self, user_id):
        if user_id in self.users_data:
            self.users_data[user_id].complete_task()
        else:
            print(f"User with ID {user_id} not found.")

    def check_all_users_tasks(self):
        for user_id, user_obj in list(self.users_data.items()):  # 使用list()复制一份items()以免在迭代时修改字典大小
            if user_obj.all_tasks_completed():
                print(f"User {user_id}: All tasks completed. Deleting user data.")
                del self.users_data[user_id]

# 示例运行
add_user("user123")
create_task("user123")
create_task("user123")
complete_task("user123")
check_all_users_tasks()
