import subprocess
import pprint as pp
from instaloader import Instaloader, Profile

username = "picklively_official"
password = "iamaganducoder"
dest_profile = "kohlikingofficial"


def download_sources(source_profiles, save_path):
    if save_path:
        L = Instaloader(dirname_pattern=save_path + "/" + dest_profile)
    else:
        L = Instaloader()
    L.login(username, password)

    for thisprofile in source_profiles:
        X_percentage = 10  # percentage of posts that should be downloaded
        MAX_DOWNLOAD = 100
        profile = Profile.from_username(L.context, thisprofile)
        print("get_followers:", *profile.get_followers())
        l = len(list(profile.get_posts()))
        print(l, "posts")

        if l < 100:
            print("Sorting Posts(by likes) of {} Started...".format(thisprofile))
            posts_in_action = sorted(
                profile.get_posts(), key=lambda p: -p.likes - 300 * p.comments
            )
            print(
                "Sorting Completed for {} posts...".format(len(list(posts_in_action)))
            )
            for post in islice(
                posts_in_action,
                min(ceil(profile.mediacount * X_percentage / 100), MAX_DOWNLOAD),
            ):
                print(post.shortcode)
                print(post.date)
                post_data = post._node
                likes = post_data["edge_media_preview_like"]["count"]
                comments = post_data["edge_media_to_comment"]["count"]
                caption = (
                    post_data["edge_media_to_caption"]["edges"][0]["node"]["text"]
                    if post_data["edge_media_to_caption"]["edges"]
                    else None
                )
                print("{} likes, {}, comments, {}".format(likes, comments, caption))
                L.download_post(post, thisprofile)
        else:
            pp.pprint(*profile.get_followers())
            print(
                len(list(profile.get_posts())), "posts, Too big to sort, lets filter",
            )
            posts_list = list(profile.get_posts())
            print(*posts_list[0])
            # posts_in_action = list(map(lambda x: {k:v for k, v in x.likes() if v > 2500000}, ))
            # print("{} posts left after posts_filtered_by_100_likes".format(len(posts_in_action)))
            # for post in islice(posts_in_action, min(ceil(len(list(profile.get_posts())) * X_percentage / 100), MAX_DOWNLOAD)):
            #     print(post.shortcode)
            #     print(post.date)
            #     post_data = post._node
            #     likes = post_data["edge_media_preview_like"]["count"]
            #     comments = post_data["edge_media_to_comment"]["count"]
            #     caption = post_data["edge_media_to_caption"]["edges"][0]["node"]["text"] if post_data["edge_media_to_caption"]["edges"] else None
            #     print("{} likes, {}, comments, {}".format(likes, comments, caption))
            #     L.download_post(post, thisprofile)


from pathlib import Path

MYUPLOADDIR = str(Path.home()) + "/Dropbox"
MYDATAPATH = "/".join(str(Path().absolute()).split("/")[:6]) + "/testdata"

source_profiles = [
    "virat.kohli",
    "18_viratkohli._18",
    "virat.kohli_018_",
    "virat_king_army",
    "virat_kohli_champ18",
    "viratkohli_addicted_",
    "viratmylife_",
    "_virat_lovers_for_.life_",
    "champ._kohli",
    "virat_gang_18",
    "viratkohli.clubfc",
]

print(MYUPLOADDIR)
print(MYDATAPATH)

download_sources(source_profiles=source_profiles, save_path=MYDATAPATH)
