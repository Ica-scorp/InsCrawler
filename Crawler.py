import re
import time

import requests

import json

from convert_date import convertToDate
cookie = {
    'dpr': '1.5',
    'ig_did': '6BBEEB12-94A8-4927-BB6C-3992C3E6C9E4',
    'datr': 'pvAZZSne9xdHK0uZXEPbN8Sw',
    'mid': 'ZRnwpgALAAHSRKXs-sWEzoseg66t',
    'ig_nrcb': '1',
    'csrftoken': 'dsTcF2ZtNFmDx378bXR0wfFOEtFyK9kZ',
    'ds_user_id': '56526374820',
    'shbid': '13625,56526374820,1727734836:01f78959355f0b2c6de2414c596031d4037174650eb42f69d87a266484fe42d2e2b571a7',
    'shbts': '1696198836,56526374820,1727734836:01f7e5a96a297345260fccd7d538ff1a48a191bd334c0a707f1f786f2a0ae75924aa253d',
    'sessionid': '56526374820:OaAdyA4Sv3EXB7:0:AYeUDDKkCe3rrhT9lQ2miN267-7w8ejAPFe3lrrdJA',
    'rur': 'NCG,56526374820,1727811770:01f7869cb91aaed4f11c4a0e630bc1b38d7e69db21c3a9547b3303d3b99c861b6cb35f9f'
}


PARAMS = r'("app_id":\s*"[^"]+")|("claim":\s*"[^"]+")|("csrf_token":\s*"[^"]+")'

URLS = [
    'https://www.instagram.com/',
    'https://www.instagram.com/api/v1/users/web_profile_info/',
    'https://www.instagram.com/api/v1/feed/user',
    'https://www.instagram.com/api/v1/media/'
]


class Ins:
    def __init__(self, cookies: dict):
        self.cookies = cookies
        self.session = requests.Session()
        self.headers = {
            'authority': 'www.instagram.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="113.0.5672.63", "Chromium";v="113.0.5672.63", "Not-A.Brand";v="24.0.0.0"',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'viewport-width': '1536',
        }
        self.get_Header_params()

    def ajax_request(self, url: str, /, params=None):
        """
        do requests, the engine of class
        :param url: api url
        :param params: api params
        :return: json object
        """
        for _ in range(5):
            try:
                resp = self.session.get(url, headers=self.headers, params=params, cookies=self.cookies)
                return resp.json()
            except requests.exceptions.RequestException:
                time.sleep(15)
        else:
            return None

    def get_Header_params(self):
        """
        every time visit ins will change header params, this is to get the header params
        :return: None
        """
        try:
            response = self.session.get(URLS[0], cookies=self.cookies, headers=self.headers)
            matches = re.findall(PARAMS, response.text)
            result = [match[i] for match in matches for i in range(3) if match[i]]

            if len(result) >= 3:
                # get app_id
                app_id = result[0].split(":")[1].strip().strip('"')
                # get claim
                claim = result[1].split(":")[1].strip().strip('"')
                # get csrf_token, if lose cookies, cannot get this param, also cannot access to other apis
                csrf_token = result[2].split(":")[1].strip().strip('"')
                # set values to headers
                self.headers.update({'x-asbd-id': '198387', 'x-csrftoken': csrf_token,
                                     'x-ig-app-id': app_id, 'x-ig-www-claim': claim,
                                     'x-requested-with': 'XMLHttpRequest', })
            else:
                raise ValueError("Unexpected response structure from Instagram")

        except requests.exceptions.RequestException as e:
            raise ValueError(f'Request error: {e}. Please try again and check your Internet settings')

    def get_userInfo(self, userName: str):
        """
        get user info by username
        :param userName: name of user
        :return: dict of user info
        """
        params = {
            'username': userName,
        }
        resp = self.ajax_request(URLS[1], params=params)
        if resp:
            try:
                # to avoid exception? Internet went wrong may return wrong information
                data = resp['data']['user']
            except KeyError:
                raise 'Could not get user information...'
            return {
                'biography': data.get('biography'),
                'username': data.get('username'),
                'fbid': data.get('fbid'),
                'full_name': data.get('full_name'),
                'id': data.get('id'),
                'followed_by': data.get('edge_followed_by', {}).get('count'),
                'follow': data.get('edge_follow', {}).get('count'),
                'avatar': data.get('profile_pic_url_hd'),
                'noteCount': data.get('edge_owner_to_timeline_media', {}).get('count'),
                'is_private': data.get('is_private'),
                'is_verified': data.get('is_verified')
            } if data else 'unknown User'

    def get_userPosts(self, userName: str):
        """
        get all posts from the username
        :param userName:  name
        :return: generator
        """
        continuations = [{
            'count': '3',
        }]
        temp = userName + '/username/'
        while continuations:
            continuation = continuations.pop()
            # url will change when second request and later
            url = URLS[2] + f'/{temp}'
            resp = self.ajax_request(url, params=continuation)
            # no such user
            if not resp.get('user'):
                yield 'checking cookie or unknown/private User: {}'.format(userName)
            else:
                _items = resp.get('items')
                # simulate the mousedown
                if resp.get('more_available'):
                    continuations.append({'count': '3', 'max_id': resp.get('next_max_id')})
                    user = resp.get('user')
                    temp = user.get('pk_id') if user.get('pk_id') else user.get('pk')
                yield from self.extract_post(_items)

    def get_comments(self, id):
        """
        get comments by given post id
        :param id:
        :return: generator of comments
        """
        continuations = [{
            'can_support_threading': 'true',
            'permalink_enabled': 'false',
        }]
        # base url
        url = URLS[3] + f'{id}/comments/'
        while continuations:
            continuation = continuations.pop()
            resp = self.ajax_request(url, params=continuation)
            if resp.get('next_min_id'):
                continuations.append({
                    'can_support_threading': 'true',
                    'min_id': resp.get('next_min_id')
                })
            comments = resp.get('comments')
            if comments:
                for comment in comments:
                    yield {
                        'id': comment.get('pk'),
                        'user_name': comment.get('user', {}).get('username'),
                        'user_fullname': comment.get('user', {}).get('full_name'),
                        'text': comment.get('text'),
                        'created_at': comment.get('created_at'),
                        'comment_like_count': comment.get('comment_like_count'),
                        'reply_count': comment.get('child_comment_count')
                    }
                    if comment.get('child_comment_count') > 0:
                        yield from self.get_child_comment(id, comment.get('pk'))
            else:
                yield 'no comments or losing login cookies'

    def get_child_comment(self, main_id, id):
        """
        get child of the comment by comment_id, only used in function get_comments().
        :param main_id: post id
        :param id: comment_id
        :return: to comments generator
        """
        url = f'https://www.instagram.com/api/v1/media/{main_id}/comments/{id}/child_comments/'
        continuations = [{'max_id': ''}]
        while continuations:
            continuation = continuations.pop()
            resp = self.ajax_request(url, params=continuation)
            cursor = resp.get('next_max_child_cursor')
            if cursor:
                continuations.append({'max_id': cursor})
            comments = resp.get('child_comments')
            if comments:
                for comment in comments:
                    yield {
                        'id': comment.get('pk'),
                        'user_name': comment.get('user', {}).get('username'),
                        'user_fullname': comment.get('user', {}).get('full_name'),
                        'text': comment.get('text'),
                        'created_at': comment.get('created_at'),
                        'comment_like_count': comment.get('comment_like_count'),
                    }

    @staticmethod
    def extract_post(posts):
        """
        to extract a post from a list of posts
        :param posts: original instagram posts
        :return: dict of posts
        """
        for post in posts:
            caption = post.get('caption')
            item = {
                'code': post.get('code'),
                'id': post.get('pk'),
                'pk_id': post.get('id'),
                'comment_count': post.get('comment_count'),
                'like_count': post.get('like_count'),
                'text': caption.get('text') if caption else None,
                'created_at': caption.get('created_at') if caption else post.get('taken_at'),
            }
            # other type can be added by yourself
            types = post.get('media_type')
            item.update({
                'photo': [_.get('image_versions2', {}).get('candidates', [{}])[0].get('url') for _ in
                          post.get('carousel_media')]
            }) if types == 8 else None
            item.update({
                'video': post.get('video_versions', [{}])[0].get('url')
            }) if types == 2 else None
            item.update({
                'photo': post.get('image_versions2', {}).get('candidates', [{}])[0].get('url')
            }) if types == 1 else None
            yield item



def convertToText(photourl):
    url = 'https://api.ocr.space/parse/image'
    headers = {
        'apikey': 'K84270671188957',
    }

    payload = {
        'language': 'eng',
        'isOverlayRequired': 'false',
        'url': 'https://scontent-ord5-2.cdninstagram.com/v/t51.2885-15/370756379_1025149722260803_1282863242509454581_n.jpg?stp=dst-jpg_e35&_nc_ht=scontent-ord5-2.cdninstagram.com&_nc_cat=107&_nc_ohc=HNZeSQwbZvUAX_JCvIS&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MzE3OTUyNTUyNzQ2MTY5NjIyNQ%3D%3D.2-ccb7-5&oh=00_AfAqX_6wJE00STZvZvM_sBIF40FhSxmmt6hGSbo_fYIaRQ&oe=651E833B&_nc_sid=ee9879',
        'iscreatesearchablepdf': 'false',
        'issearchablepdfhidetextlayer': 'false',
    }
    payload['url']=photourl
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code==200:
        data = response.json()
        exitmsg=data["OCRExitCode"]
        errormsg=data["IsErroredOnProcessing"]
        if exitmsg==1 and errormsg==False: 
            # Print the response
            return (data["ParsedResults"][0]["ParsedText"])
        else:
            return ("Error occured")

if __name__ == '__main__':
    INS = Ins(cookie)
    items = INS.get_userPosts('washurobotics')
    # items = INS.get_comments('3092771276598639274')
    for item in items:
        # text_collection=[]
        if 'photo' in item:
            # for photo_url in item['photo']:
            text=convertToText(item['photo'][0])
        #         text_collection.append(text)
        #         print(photo_url)
        print(item)
        # print("This is the text collection:")
        # print(text_collection)
        # break
        timestamp=item['created_at']
        if convertToDate(timestamp)==False:
            break
    item = INS.get_userInfo('washurobotics')
    print(item)