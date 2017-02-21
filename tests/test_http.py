from utilities.HttpManager import HttpManager

cylon_url = "https://joulie-cylon.herokuapp.com"
http = HttpManager()


#
# Testing post of the HttpManage
#
def test_post():

    result = http.Get(cylon_url)

    assert result.status_code == 200