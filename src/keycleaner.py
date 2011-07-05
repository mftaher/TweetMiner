# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Area51"
__date__ ="$Mar 9, 2011 4:10:58 AM$"

class KeyCleaner():
    def unset_tweet_keys(self,content):
        if content.has_key("retweeted_status"):
            content["retweeted_status"] = self.unset_tweet_keys(content["retweeted_status"])

        del content['contributors']
        del content['in_reply_to_screen_name']
        del content['in_reply_to_status_id']
        del content['in_reply_to_status_id_str']
        del content['in_reply_to_user_id_str']
        del content['in_reply_to_user_id']
        del content['retweeted']
        del content['truncated']
        del content['favorited']
        del content['id']
        del content['id_str']
        
        content['user'] = self.unset_user_keys(content['user'])

        return content

    def unset_user_keys(self,user):
        del user["contributors_enabled"]
        del user["follow_request_sent"]
        del user["id_str"]
        del user["is_translator"]
        del user["notifications"]
        del user["protected"]
        del user["show_all_inline_media"]
        del user["profile_background_image_url"]
        del user["profile_background_tile"]
        del user["profile_background_color"]
        del user["profile_image_url"]
        del user["profile_link_color"]
        del user["profile_sidebar_border_color"]
        del user["profile_sidebar_fill_color"]
        del user["profile_text_color"]
        del user["profile_use_background_image"]

        return user

    
