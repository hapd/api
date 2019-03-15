from github import Github
import json

class GHFiles:
    def __init__(self, file_name):
        gh = Github("hapd", "mAJORPROJECT19")
        u = gh.get_user()
        repo = u.get_repo("database")
        db = repo.get_file_contents(str(file_name))
        temp = db.decoded_content.decode("utf-8")
        temp = temp.replace("\'", "\"").replace('\n', '').replace(' ','')
        temp = json.loads(temp)
        self.file_contents = temp
        self.db = db
        self.repo = repo
    
    def update(self, updatedFile, file_name):
        try:
            self.repo.update_file(self.db.path, "Update", updatedFile, self.db.sha)
            return True
        except:
            return False

