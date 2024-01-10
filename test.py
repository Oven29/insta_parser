from instaloader import ConnectionException, Instaloader
from sqlite3 import OperationalError, connect


# def import_session(cookiefile, sessionfile):
    # print(f"Using cookies from {cookiefile}.")
    # conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    # try:
    #     cookie_data = conn.execute(
    #         "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
    #     )
    # except OperationalError:
    #     cookie_data = conn.execute(
    #         "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
    #     )
    # instaloader = Instaloader(max_connection_attempts=1)
    # instaloader.context._session.cookies.update(cookie_data)
    # username = instaloader.test_login()
    # if not username:
    #     raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
    # print(f"Imported session cookie for {username}.")
    # instaloader.context.username = username
    # instaloader.save_session_to_file(sessionfile)

# L = Instaloader()
# L.login('claudie__mantuano__1414', 'K50kt7u4')
# print(L.save_session())
# IG-U-DS-USER-ID=64048778885;
# X-MID=ZZ6FMwABAAG7WF5ci0S2vy9w7bz1;
# IG-U-RUR=LDC,64048778885,1736423693:01f757d5b08579093d536f00c9b9598ff06ff3870421d51793994c9abfd63cdabbf17f97;
# X-IG-WWW-Claim:hmac.AR36pBrBpnaNnCr0FIhVhYKUj1uRl-l5KLCmy7WeJfbfgCsK;IG-INTENDED-USER-ID=64048778885;
# Authorization=Bearer IGT:2:eyJkc191c2VyX2lkIjoiNjQwNDg3Nzg4ODUiLCJzZXNzaW9uaWQiOiI2NDA0ODc3ODg4NSUzQW1pUFBBb3h3bnJhSVpTJTNBMCUzQUFZY3FGeHBBLUF0VjhMeFB1N09UTWNLWEF2NXd3dVFSdnduTjdWNVpiQSJ9
# import settings


# instagrapi==1.5.1

### instagrapi
from instagrapi import Client, types
login, password = 'kennedy_u8689:5uR2JW8fm'.split(':')
code = 'C1h_ojmsnp1'
client = Client(proxy='http://4V40x1:1NtRS8@168.196.237.230:9427')
# client = Client()
client.login(login, password)

media_pk = client.media_pk_from_code(code)
comments = client.media_comments(client.media_id(media_pk))
# likers = client.media_likers(client.media_id(media_pk))

# for user in likers:
#     print(type(user))
i = 0
for el in comments:
    i += 1
print(i)
