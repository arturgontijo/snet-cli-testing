import unittest
import sys

from web3 import Web3, EthereumTesterProvider
from eth_tester import EthereumTester, MockBackend

from snet_cli.config import conf
from snet_cli import identity
from snet_cli.commands import Command

W3 = Web3(EthereumTesterProvider(EthereumTester(backend=MockBackend())))


# Test: Identity types
class IdentityTests(unittest.TestCase):
    def init(self):
        self.w3 = W3
        self.config = conf
        self.args = None
        self.txn = {
            'gasPrice': 1,
            'nonce': 0,
            'gas': 1
        }

        self.key_id_provider = None
        self.rpc_id_provider = None
        self.mnemonic_id_provider = None
        self.trezor_id_provider = None
        self.ledger_id_provider = None

        self.idx = 0
        self.private_key = None
        self.mnemonic = None

    def _get_id(self, id_type):
        if id_type == "key":
            try:
                return identity.KeyIdentityProvider(self.w3, self.private_key)
            except ValueError:
                return None
        elif id_type == "mnemonic":
            try:
                return identity.MnemonicIdentityProvider(self.w3, self.mnemonic, self.idx)
            except ValueError:
                return None
        elif id_type == "rpc":
            return identity.RpcIdentityProvider(self.w3, self.idx)
        elif id_type == "trezor":
            return identity.TrezorIdentityProvider(self.w3, self.idx)
        elif id_type == "ledger":
            return identity.LedgerIdentityProvider(self.w3, self.idx)
        else:
            return None

    def test_valid_key_id(self):
        self.init()

        self.private_key = "0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF"
        test_id = self._get_id("key")

        # First transaction (receipt must have 9 fields)
        receipt = test_id.transact(self.txn, out_f=sys.stdout)
        cmd = Command(self.config, None)
        cmd._pprint_receipt_and_events(receipt, [])
        self.assertEqual(len(receipt), 9)
        block_number_1 = int(receipt["blockNumber"])

        # First transaction (receipt must have 9 fields)
        receipt = test_id.transact(self.txn, out_f=sys.stdout)
        cmd._pprint_receipt_and_events(receipt, [])
        self.assertEqual(len(receipt), 9)
        block_number_2 = int(receipt["blockNumber"])

        # Is blockNumber increasing?
        self.assertEqual(block_number_1, block_number_2 - 1)

    def test_invalid_key_id(self):
        self.init()

        self. private_key = "INVALID"
        test_id = self._get_id("key")
        self.assertEqual(test_id, None)

    def test_valid_mnemonic_id(self):
        self.init()

        self.mnemonic = "gauge enact biology destroy normal tunnel slight slide wide sauce ladder produce"
        self.idx = 0
        test_id = self._get_id("mnemonic")

        # First transaction (receipt must have 9 fields)
        receipt = test_id.transact(self.txn, out_f=sys.stdout)
        cmd = Command(self.config, None)
        cmd._pprint_receipt_and_events(receipt, [])
        self.assertEqual(len(receipt), 9)
        block_number_1 = int(receipt["blockNumber"])

        # First transaction (receipt must have 9 fields)
        receipt = test_id.transact(self.txn, out_f=sys.stdout)
        cmd._pprint_receipt_and_events(receipt, [])
        self.assertEqual(len(receipt), 9)
        block_number_2 = int(receipt["blockNumber"])

        # Is blockNumber increasing?
        self.assertEqual(block_number_1, block_number_2 - 1)

    def test_invalid_mnemonic_id(self):
        self.init()
        self.mnemonic = "INVALID"
        test_id = self._get_id("mnemonic")

        receipt = test_id.transact(self.txn, out_f=sys.stdout)
        cmd = Command(self.config, None)
        cmd._pprint_receipt_and_events(receipt, [])


if __name__ == '__main__':
    unittest.main()