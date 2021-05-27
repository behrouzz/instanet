from .insta_core import CoreInstagram
import pickle, os, glob
import networkx as nx
import matplotlib.pyplot as plt

class Instagram:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.adr = 'dataset/'+username+'/'
        self.logged = False
        
    def login(self):
        self.inst = CoreInstagram(self.username, self.password)
        self.username_id = self.inst.username_id
        self.followers, self.followings = self.get_friend(self.username)
        my_net = list(set(self.followers+self.followings))
        all_ids = [i[0] for i in my_net]
        all_users = [i[1] for i in my_net]
        self.user2id = {u:v for (u,v) in zip(all_users,all_ids)}
        self.logged = True

    def save_me(self):
        if not os.path.isdir(self.adr):
            os.makedirs(self.adr)
        with open(self.adr+'me.pickle','wb') as f:
            pickle.dump([self.followers, self.followings], f)   

    def get_friend(self, user):
        user_id = self.username_id if user==self.username else self.user2id[user]
        f_ers = self.inst.followers(user_id)
        f_ing = self.inst.followings(user_id)
        f_ers = [(i['pk'], i['username'], i['full_name'], i['is_private']) for i in f_ers]
        f_ing = [(i['pk'], i['username'], i['full_name'], i['is_private']) for i in f_ing]
        return [f_ers, f_ing]

    def get_friends(self, users_list):
        dc = {}
        for user in users_list:
            dc[user] = self.get_friend(user)
        return dc

    def save_friend(self, user):
        if not os.path.isdir(self.adr):
            os.makedirs(self.adr)
        friend_data = self.get_friend(user)
        with open(self.adr+user+'.pickle','wb') as f:
            pickle.dump(friend_data, f)

    def save_friends(self, users_list):
        for user in users_list:
            self.save_friend(user)

    def load_friend(self, user):
        with open(self.adr+user+'.pickle','rb') as f:
            data = pickle.load(f)
        return data

    def load_friends_dic(self, users_list=None):
        dc = {}
        adr = glob.glob(self.adr+'/*.pickle')
        adr = [i for i in adr if i.split('\\')[-1][:-7]!='me']
        users = [i.split('\\')[-1][:-7] for i in adr]
        if users_list is not None:
            users = [i for i in users if i in users_list]
        for i,user in enumerate(users):
            dc[user] = self.load_friend(user)
        return dc

    def load_friends_net_dic(self, users_list=None):
        dc = self.load_friends_dic(users_list)
        net_dc = {}
        for user in dc.keys():
            net_dc[user] = list(set(dc[user][0]+dc[user][1]))
        return net_dc

    def graph(self, users_list=None):
        net_dc = self.load_friends_net_dic(users_list)
        G = nx.Graph()
        nds = list(net_dc.keys())
        G.add_nodes_from(nds)
        for k,v in net_dc.items():
            eds = [(k, i[1]) for i in v if i[1] in nds]
            G.add_edges_from(eds)
        nx.draw(G, with_labels=True, font_size=7)
        plt.show()

