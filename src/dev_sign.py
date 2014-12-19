# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import jwt
import json
from collections import namedtuple
from ecdsa import SigningKey, NIST256p
from datetime import datetime, timedelta
import os.path
import optparse
import sys

ver = "0.1"
descr = """Utility to produce AWT signed device data"""


optparser = optparse.OptionParser(version=ver, description=descr)

sk_file = os.path.join(os.path.expanduser("~"), ".reg_sk.pem")
vk_file = os.path.join(os.path.expanduser("~"), ".reg_vk.pem")


DeviceRegister = namedtuple('DeviceRegister',
                            ['version', 'cryptoSerial', 'deviceSerial',
                             'pubKey'])

def reg_2_jwt(reg_data, priv_key):
    claims = {'iss': reg_data._asdict(), 'nbf': datetime.utcnow() }
    return jwt.encode(claims, priv_key, algorithm='ES256')

def gen_key():
    return SigningKey.generate(curve=NIST256p)

def getserial():
    # Extract serial from cpuinfo file
    # Taken from
    # http://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
    # Obviously, this needs to be generalized for those not on a Pi
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial

def get_crypto_serial():
    # For now just return the 18 char (72 bit) value of all zeros to
    # indicate software keys
    return '000000000000000000'

def build_dev_reg_data(get_pub_key_func):
    return DeviceRegister('1',
                          get_crypto_serial(), getserial(), get_pub_key_func())

def create_reg_keys():
    sk = gen_key()
    open(sk_file, 'w').write(sk.to_pem())

    vk = sk.get_verifying_key()
    open(vk_file, 'w').write(vk.to_pem())

    return sk,vk

def load_keys():
    if not os.path.isfile(sk_file):
        return create_reg_keys()

    sk = SigningKey.from_pem(open(sk_file).read())
    vk = sk.get_verifying_key()

    return sk,vk

def data_2_jwt(data_to_sign, reg_data, priv_key):
    td = timedelta(minutes=2)
    exp = datetime.utcnow() + td
    claims = {'data': data_to_sign, 'iss': reg_data._asdict(),
              'nbf': datetime.utcnow(),
              'exp':exp }
    return jwt.encode(claims, priv_key, algorithm='ES256')


if __name__ == "__main__":

    optparser.add_option("-r", "--register", action="store_true",
                         dest="register", help="Returns the registration data")
    optparser.set_defaults(register=False)

    opt, args = optparser.parse_args()

    sk,vk = load_keys()
    reg = build_dev_reg_data(lambda: vk.to_pem().rstrip())

    if opt.register:
        print reg_2_jwt(reg, sk)
    else:

        val = sys.stdin.readline().rstrip()
        print data_2_jwt(val, reg, sk)
