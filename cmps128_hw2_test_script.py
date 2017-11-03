#!/usr/bin/python

import unittest
import subprocess
import requests
import sys
import random
import time
import os


hostname = '127.0.0.1'  #Windows and Mac users can change this to the docker vm ip
sudo = ''
container = 'hw2:latest'

TEST_STATUS_CODES_ONLY = False

def start_nodes(sudo, hostname, container):
    exec_string_main  = sudo + " docker run -p 8083:8080 --net=mynet --ip=10.0.0.20 -e IP=10.0.0.20 -e PORT=8080 -d %s" % container
    exec_string_forw1 = sudo + " docker run -p 8084:8080 --net=mynet --ip=10.0.0.21 -e IP=10.0.0.21 -e PORT=8080 -e MAINIP=10.0.0.20:8080 -d %s" % container
    exec_string_forw2 = sudo + " docker run -p 8085:8080 --net=mynet --ip=10.0.0.22 -e IP=10.0.0.22 -e PORT=8080 -e MAINIP=10.0.0.20:8080 -d %s" % container
    node_ids = []
    print exec_string_main
    node_ids.append(subprocess.check_output(exec_string_main, shell=True).rstrip('\n'))
    print exec_string_forw1
    node_ids.append(subprocess.check_output(exec_string_forw1, shell=True).rstrip('\n'))
    print exec_string_forw2
    node_ids.append(subprocess.check_output(exec_string_forw2, shell=True).rstrip('\n'))
    node_address = ['http://' + hostname + ":" + x for x in ['8083', '8084', '8085']]
    return node_ids, node_address

class TestHW2(unittest.TestCase):

    '''
    Creating a subnet:
        sudo docker network create --subnet 10.0.0.0/16 mynet
    '''

    def __kill_node(self, idx):
        global sudo
        cmd_str = sudo + " docker kill %s" % self.node_ids[idx]
        print
        print cmd_str
        os.system(cmd_str)

    def __start_nodes():
        global sudo, hostname, container
        exec_string_main  = sudo + " docker run -p 8083:8080 --net=mynet --ip=10.0.0.20 -e IP=10.0.0.20 -e PORT=8080 -d %s" % container
        exec_string_forw1 = sudo + " docker run -p 8084:8080 --net=mynet --ip=10.0.0.21 -e MAINIP=10.0.0.20:8080 -e IP=10.0.0.21 -e PORT=8080 -d %s" % container
        exec_string_forw2 = sudo + " docker run -p 8085:8080 --net=mynet --ip=10.0.0.22 -e MAINIP=10.0.0.20:8080 -e IP-10.0.0.22 -e PORT=8080 -d %s" % container
        node_ids = []
        print exec_string_main
        node_ids.append(subprocess.check_output(exec_string_main, shell=True).rstrip('\n'))
        print exec_string_forw1
        node_ids.append(subprocess.check_output(exec_string_forw1, shell=True).rstrip('\n'))
        print exec_string_forw2
        node_ids.append(subprocess.check_output(exec_string_forw2, shell=True).rstrip('\n'))
        node_address = ['http://' + hostname + ":" + x for x in ['8083', '8084', '8085']]
        self.node_ids = node_ids
        self.node_address = node_address

    @classmethod
    def setUpClass(cls):
        global sudo, hostname, container
        cls.node_ids, cls.node_address = start_nodes(sudo, hostname, container)
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        global sudo
        print "Stopping all containers"
        os.system(sudo + " docker kill $(" + sudo + " docker ps -q)")

    def setUp(self):
        #within limit (199 chars)
        self.key1 = 'PgS5W3uzS7lKtY24ARgCEIcb4tEBYYtgct6WoTcwwL1JvYJV_5DKNkzblPEGCj3cavUZ8qi9NwtdpxkS_1YfoI0LETs2DEC7q8KiQlZI0RibE7dBJ9HLuppFjaEPdA4PY9uSlkjUbM0jopy9sin1vKA6A8ldxgEkU1kM4a7jdCo7mykYBrc_owJokxtTqw7DFyJlN_q'
        #at border (200 chars)
        self.key2 = 'n4P2bm7A0zNTHpr9VJs5yYL6zqCJgTBWEOAxDbOLhyVZnp2eTH55B0mZ0FhcyCuwZkulYdCHf_shthzk2RuHVG5QMrXJU1RSXHmyIjalfFEqWrW5fbOELdSuha4AMKF6HbMpq_aImVEzB7dDDDkliRoQhvCe6ICEM81vepjSRsZzACjGQbIubrMHN0pKXaqjS6TPhmQ0'
        #outside limit (201 chars)
        self.key3 = 'aKCG1zAFvXUWiIX75kU8Eq0ugVgz6dV7CItwQaA6oCczaJ_ScwhTSX87RchI9P9TgjDax56mcGWBWAtmUybG3OEh8kWfSTyAxsYyq0NQRQ4et1E4JCgwXq208zh3zpfG5lDyPBA0m5hMnpkSBB0PT0M8muLhmVwBVvYas8QO2CE7AGucjMeNEF4N1GbnRm03kNIRpOW41'
        self.val1 = 'aaaasjdhvksadjfbakdjs'
        self.val2 = 'asjdhvksadjfbakdjs'
        self.val3 = 'bknsdfnbKSKJDBVKpnkjgbsnk'

    def test_a_put_nonexistent_key(self):
        res = requests.put(self.node_address[0]+'/kv-store/foo',data = {'val':'bart'})
        print(res)
        self.assertTrue(res.status_code, [201, '201'])

        d = res.json()
        self.assertEqual(d['replaced'],'False')
        self.assertEqual(d['msg'],'New key created')
        if not TEST_STATUS_CODES_ONLY:
            print res
            print res.text

    def test_b_put_existing_key(self):
        res = requests.put(self.node_address[1]+'/kv-store/foo',data= {'val':'bart'})
        print("CONTENT:", res.content)
        print(res.json())
        print(res.json().keys())
        self.assertTrue(res.status_code, [200, '200'])
        d = res.json()
        self.assertEqual(d['replaced'],'True')
        self.assertEqual(d['msg'],'Value of existing key replaced')

    def test_c_get_nonexistent_key(self):
        res = requests.get(self.node_address[2]+'/kv-store/faa')
        print(res)
        self.assertTrue(res.status_code, [404, '404'])
        d = res.json()
        self.assertEqual(d['result'],'Error')
        self.assertEqual(d['msg'],'Key does not exist')

    def test_d_get_existing_key(self):
        res = requests.get(self.node_address[0]+'/kv-store/foo')
        print(res)
        self.assertTrue(res.status_code, [200, '200'])
        d = res.json()
        self.assertEqual(d['result'],'Success')
        self.assertEqual(d['value'],'bart')

    def test_e_del_nonexistent_key(self):
        res = requests.delete(self.node_address[1]+'/kv-store/faa')
        print(res)
        self.assertTrue(res.status_code,[404, '404'])
        d = res.json()
        self.assertEqual(d['result'],'Error')
        self.assertEqual(d['msg'],'Key does not exist')
#
    def test_f_del_existing_key(self):
        res = requests.delete(self.node_address[2]+'/kv-store/foo')
        print(res)
        self.assertTrue(res.status_code, [200, '200'])
        d = res.json()
        self.assertEqual(d['result'],'Success')
#
    def test_g_get_deleted_key(self):
        res = requests.get(self.node_address[0]+'/kv-store/foo')
        print(res)
        self.assertTrue(res.status_code,[ 404, '404'])
        d = res.json()
        self.assertEqual(d['result'],'Error')
        self.assertEqual(d['msg'],'Key does not exist')
#
    def test_h_put_deleted_key(self):
        res = requests.put(self.node_address[1]+'/kv-store/foo',data= {'val':'bart'})
        print(res)
        self.assertTrue(res.status_code, [201, '201'])
        d = res.json()
        self.assertEqual(d['replaced'],'False')
        self.assertEqual(d['msg'],'New key created')
#
    def test_i_put_nonexistent_key(self):
        res = requests.put(self.node_address[2]+'/kv-store/'+self.key1,data = {'val':self.val1})
        print(res)

        self.assertTrue(res.status_code, [201, '201'])
        d = res.json()
        self.assertEqual(d["replaced"], 'False')
        self.assertEqual(d['msg'],'New key created')
#
    def test_j_put_existing_key(self):
        res = requests.put(self.node_address[0]+'/kv-store/'+self.key1,data= {'val':self.val2})
        print(res)
        self.assertTrue(res.status_code, [200, '200'])
        d = res.json()
        self.assertEqual(d['replaced'],'True')
        self.assertEqual(d['msg'],'Value of existing key replaced')
#
    def test_k_get_nonexistent_key(self):
        res = requests.get(self.node_address[1]+'/kv-store/'+self.key2)
        print(res)
        self.assertTrue(res.status_code, [404, '404'])
        d = res.json()
        self.assertEqual(d['result'],'Error')
        self.assertEqual(d['msg'],'Key does not exist')

#
    def test_l_get_existing_key(self):
        res = requests.get(self.node_address[2]+'/kv-store/'+self.key1)
        print(res)
        self.assertTrue(res.status_code, [200, '200'])
        d = res.json()
        self.assertEqual(d['result'],'Success')
        self.assertEqual(d['value'],self.val2)
#
    def test_m_put_key_too_long(self):
        res = requests.put(self.node_address[2]+'/kv-store/'+self.key3,data= {'val':self.val2})
        print(res)
        self.assertTrue(res.status_code, [403, '403'])
        d = res.json()
        self.assertEqual(d['result'],'Error')
        self.assertEqual(d['msg'],'Key not valid')
#
    def test_n_del_existing_key(self):
        res = requests.delete(self.node_address[0]+'/kv-store/'+self.key1)
        print(res)
        self.assertTrue(res.status_code, [200, '200'])
        d = res.json()
        self.assertEqual(d['result'],'Success')
#
    def test_o_get_deleted_key(self):
        res = requests.get(self.node_address[1]+'/kv-store/'+self.key1)
        print(res)
        self.assertTrue(res.status_code, [404, '404'])
        d = res.json()
        self.assertEqual(d['result'],'Error')
        self.assertEqual(d['msg'],'Key does not exist')
#
    def test_p_put_deleted_key(self):
        res = requests.put(self.node_address[2]+'/kv-store/'+self.key1,data= {'val':self.val3})
        print(res)
        self.assertTrue(res.status_code, [201, '201'])
        d = res.json()
        self.assertEqual(d['replaced'],'False')
        self.assertEqual(d['msg'],'New key created')
#
    def test_q_put_key_without_value(self):
        res = requests.put(self.node_address[0]+'/kv-store/'+self.key2)
        print(res)
        self.assertTrue(res.status_code, [403, '403'])
        d = res.json()
        self.assertEqual(d['result'],'Error')
        self.assertEqual(d['msg'], 'No value provided')

    def test_r_put_key_kill_forwarder(self):
        self.__kill_node(2)
        time.sleep(3)
        res = requests.put(self.node_address[0]+'/kv-store/'+self.key1,data= {'val':'foo'})
        print(res)
        self.assertTrue(res.status_code, [200, '200'])
        d = res.json()
        self.assertEqual(d['replaced'],'True')
        self.assertEqual(d['msg'],'Value of existing key replaced')

    def test_s_put_key_kill_main(self):
        self.__kill_node(0)
        time.sleep(3)
        res = requests.put(self.node_address[1]+'/kv-store/'+self.key1,data= {'val':'foo'})
        print "res"
        print res
        print "res.text"
        print res.text
        print "res.content"
        print res.content
        self.assertTrue(res.status_code in [501, '501'])

        d = res.json()
        self.assertEqual(d['result'], 'Error')
        self.assertEqual(d['msg'], 'Server unavailable')

#'''

if __name__ == '__main__':
    unittest.main()
    #os.system(sudo + " docker kill $(" + sudo + " docker ps -q)")
