



import json



def test_all():
    with open("json_dumps_test.json","r") as f:
        feat_dict_list = json.loads(f.read())
    check_percent_sum(feat_dict_list)

def check_percent_sum(feat_dict_list):
    percent_sum = 0
    for feat in feat_dict_list:
        percent_sum += feat['percentage']
    
    print(percent_sum)


def main():
    test_all()

main()

