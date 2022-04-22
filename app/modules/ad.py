import ldap3
from ldap3 import Server, Connection
import os
import json
from dotenv import load_dotenv


class pldap():
    '''class pldap was created to parse ldap information about user and return it in structure formats like json'''
    def __init__(self,AD_SERVER,AD_USER,AD_PASSWORD,AD_SEARCH_BASE,FILTER,ATTR=ldap3.ALL_ATTRIBUTES):
        '''Connection object, takes all nessasary information to load information from AD'''

        self.ad_server = AD_SERVER
        self.ad_user = AD_USER
        self.ad_password = AD_PASSWORD
        self.ad_search_base = AD_SEARCH_BASE
        self.filter = FILTER
        self.attr = ATTR
        self.json_data = None

    def load(self):
        '''Connect to the domain controller via ldap and load data to self.json_data
        return True in case of the success, otherwise False'''
        server = Server(self.ad_server)
        conn = Connection(server,user=self.ad_user,password=self.ad_password)
        if conn.bind():
            conn.search(self.ad_search_base,self.filter,attributes=self.attr)
            self.json_data = json.loads(conn.response_to_json())
            conn.unbind()
            return True
        else:
            raise Exception("No connection, please check credentials!!!!")
            conn.unbind()
            return False
    @property
    def get_json_data(self):
        return self.json_data
    def _get_user_from_dep(self):
        'The func takes the departament name and return the list of namedtuples of contacts from AD'
        data = self.raw_data
        list_users = []
        for raw in data:
            if raw['telephoneNumber']:
                user = {}
                user['first_name']=str(raw['givenName'])
                user['last_name']=str(raw['sn'])
                user['number']= str(raw['telephoneNumber'])
                list_users.append(user)
                #sorting users in the list by last_name
                list_users.sort(key= lambda user: user['last_name'])
        #getting Dep name from AD_SEARCH_DIR
        ou_Dep, *other = self.ad_search_dir.split(',')
        DepName, *other = ou_Dep.split('=')
        return {DepName:list_users}
    def get_all_users(self,Dep_List,AD_SEARCH_DIR_Temp,AD_SERVER,AD_USER,AD_PASSWORD,filter_all_users,attr):
        'The func takes the departament name and return the list of namedtuples of contacts from AD'
        result = {}
        for dep in Dep_List:
            AD_SEARCH_DIR = self.ad_search_dir_temp.format(dep)
            data = _get_ad_data(AD_SERVER,AD_USER,AD_PASSWORD,AD_SEARCH_DIR,filter_all_users,attr)
            list_users = []
            for raw in data:
                if raw['telephoneNumber']:
                    user = {}
                    user['first_name']=str(raw['givenName'])
                    user['last_name']=str(raw['sn'])
                    user['number']= str(raw['telephoneNumber'])
                    list_users.append(user)
                    #sorting users in the list by last_name
                    list_users.sort(key= lambda user: user['last_name'])
            #getting Dep name from AD_SEARCH_DIR
            ou_Dep, *other = AD_SEARCH_DIR.split(',')
            DepName, *other = ou_Dep.split('=')
            result[dep]=list_users
        return result



def main():
    load_dotenv()
    AD_SERVER = os.getenv('AD_SERVER')
    DEP_LIST = os.getenv('DEP_LIST')
    AD_SEARCH_BASE = os.getenv('AD_SEARCH_BASE')
    AD_USER = os.getenv('AD_USER')
    AD_PASSWORD = os.getenv("AD_PASSWORD")
    filter_all_users = os.getenv('filter_all_users')
    attr = os.getenv('attr')
    # attr=ldap3.ALL_ATTRIBUTES
    result = None
    ldap_query = pldap(AD_SERVER, AD_USER, AD_PASSWORD, AD_SEARCH_BASE, filter_all_users)
    if ldap_query.load():
        result = ldap_query.json_data
    else:
        result = {'entries':'error'}

if __name__=="__main__":
    main()
