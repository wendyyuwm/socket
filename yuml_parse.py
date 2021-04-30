import yaml

fname = 'oa8600_evb_local.yaml'
devdata = ''


def get_data():
    global devdata
    fp = open(fname, 'r')
    file_data = fp.read()
    config_data = yaml.load(file_data, Loader=yaml.FullLoader)
    if 'DUTs' in config_data.keys():
        # print(config_data)
        for dut in config_data['DUTs']:
            devdata = dut
            actions = dut['controls'][0]['actions']
            for i in actions:
                if i['name'] == 'set':
                    print(i)
                    return i
            # print(dut['controls'][0]['actions'])

def use():
    print(devdata['type'])


if __name__ == "__main__":
    get_data()
    # use()
