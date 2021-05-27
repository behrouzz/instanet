import uuid, hashlib, requests, json, hmac, urllib, base64
from .bs_settings import b
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def decode(string_b64):
    string_b64_byt = string_b64.encode("ascii")
    string_byt = base64.b64decode(string_b64_byt)
    return string_byt.decode("ascii")

b = b[::-1].split('.')

API_URL = decode(b[0])
USER_AGENT = decode(b[1])
IG_SIG_KEY = bytes(decode(b[2]), 'utf-8')
EXPERIMENTS = decode(b[3])
HDR_REQ_DC = json.loads(decode(b[4]))


class CoreInstagram:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.username_id = ''
        self._rank_token = ''
        self._s = None
        self.logged = self._login()
        

    def _signed(self, data):
        data_str = json.dumps(data)
        data_prs = urllib.parse.quote(data_str)
        hmc = hmac.new(IG_SIG_KEY, data_str.encode('utf-8'), hashlib.sha256)
        return 'ig_sig_key_version=4&signed_body='+hmc.hexdigest()+'.'+data_prs
        
    def _login(self):
        m = hashlib.md5()
        m.update(self.username.encode('utf-8') + self.password.encode('utf-8'))
        tmp = hashlib.md5()
        tmp.update(m.hexdigest().encode('utf-8') + b'12345')
        device_id = 'android-' + tmp.hexdigest()[:16]

        UUID = str(uuid.uuid4())

        self._s = requests.Session()

        tmp = 'si/fetch_headers/?challenge_type=signup&guid='
        tmp = tmp + str(uuid.uuid4()).replace('-', '')
        self._s.headers.update(HDR_REQ_DC)
        resp = self._s.get(API_URL+tmp, verify=False)

        data = {'phone_id': str(uuid.uuid4()),
                '_csrftoken': resp.cookies['csrftoken'],
                'username': self.username,
                'guid': UUID,
                'device_id': device_id,
                'password': self.password,
                'login_attempt_count': '0'}

        self._s.headers.update(HDR_REQ_DC)
        resp = self._s.post(API_URL+'accounts/login/', data=self._signed(data), verify=False)
        username_id = json.loads(resp.text)["logged_in_user"]["pk"]
        self.username_id = username_id
        
        self._rank_token = "%s_%s" % (username_id, UUID)
        token = resp.cookies["csrftoken"]

        sync_data = {'_uuid': UUID,
                     '_uid': username_id,
                     'id': username_id,
                     '_csrftoken': token,
                     'experiments': EXPERIMENTS}

        self._s.headers.update(HDR_REQ_DC)
        r = self._s.post(API_URL+'qe/sync/', data=self._signed(sync_data), verify=False)
        return True
    
    def _friends(self, user_id, frnd_type):
        url = 'friendships/'+str(user_id)+f'/{frnd_type}/?rank_token='+self._rank_token
        friends_list = []; next_max_id = ''
        while True:
            self._s.headers.update(HDR_REQ_DC)
            if next_max_id == '':
                r = self._s.get(API_URL+url, verify=False)
            else:
                r = self._s.get(API_URL+url+'&max_id='+str(next_max_id), verify=False)
            last_json = json.loads(r.text)

            for i in last_json["users"]:
                friends_list.append(i)

            if last_json["big_list"] is False:
                return friends_list
            next_max_id = last_json["next_max_id"]
        return friends_list

    def followings(self, user_id):
        return self._friends(user_id, 'following')

    def followers(self, user_id):
        return self._friends(user_id, 'followers')


