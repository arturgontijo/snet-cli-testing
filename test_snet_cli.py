import unittest
import sys
from io import StringIO

from web3 import Web3, EthereumTesterProvider
from eth_tester import EthereumTester, MockBackend

from snet_cli.config import conf
from snet_cli import arguments
from snet_cli import identity
from snet_cli.commands import Command, OrganizationCommand

W3 = Web3(EthereumTesterProvider(EthereumTester(backend=MockBackend())))


class OrganizationCommandTests(unittest.TestCase):
    def init(self):
        self.config = conf
        self.args = None

    def test_org_list(self):
        self.init()

        argv = ["organization", "list"]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args)
        err = StringIO()
        org_cmd.err_f = err
        org_cmd.list()
        response = err.getvalue().strip()
        # Response:
        # [0] List of Organizations:
        # [1] - ORG_NAME_1
        # [2] - ORG_NAME_2
        # [n] - ORG_NAME_n
        self.assertGreaterEqual(len(response.split('\n')), 1)

    def test_org_info(self):
        self.init()

        org_name = "SNET_BH"
        argv = ["organization", "info", org_name]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args)
        err = StringIO()
        org_cmd.err_f = err
        org_cmd.info()
        response = err.getvalue().strip()
        # Response:
        # Owner:
        # - OWNER_ADDRESS
        #
        # Members:
        # - MEMBER_1_ADDRESS
        # - MEMBER_2_ADDRESS
        # - MEMBER_n_ADDRESS
        #
        # Services:
        # - SERVICE_NAME_1
        # - SERVICE_NAME_2
        # - SERVICE_NAME_n
        self.assertIn("Owner:", response)
        self.assertIn("Members", response)
        self.assertIn("Services:", response)

    def test_org_create(self):
        self.init()

        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        org_name = "NEW_ORG_TEST"

        member_1 = "0x0123456789012345678901234567890123456789"
        member_2 = "0x2222222222222222222222222222222222222222"
        member_3 = "0x3333333333333333333333333333333333333333"
        members = "{},{},{}".format(member_1, member_2, member_3)

        argv = ["organization", "create", no_confirm, gas_price_f, gas_price, org_name, members]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args)
        org_cmd.err_f = None
        # Create NEW_ORG_TEST
        org_cmd.create()

        err = StringIO()
        org_cmd.err_f = err
        # Try to create NEW_ORG_TEST again
        org_cmd.create()

        response = err.getvalue().strip()
        # Response (org already exists):
        # [0] NEW_ORG_TEST already exists!
        self.assertIn("NEW_ORG_TEST already exists", response)

    def test_org_delete_existent(self):
        self.init()

        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        org_name = "NEW_ORG_TEST"

        argv = ["organization", "delete", no_confirm, gas_price_f, gas_price, org_name]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args)

        err = StringIO()
        org_cmd.err_f = err
        # Delete NEW_ORG_TEST
        org_cmd.delete()

        response = err.getvalue().strip()
        # Response:
        # [0] Creating transaction to delete organization NEW_ORG_TEST...
        # [1] Submitting transaction...
        self.assertIn("Creating transaction to delete organization NEW_ORG_TEST...", response)

    def test_org_delete_nonexistent(self):
        self.init()

        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        org_name = "NEW_ORG_TEST"

        argv = ["organization", "delete", no_confirm, gas_price_f, gas_price, org_name]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args)

        err = StringIO()
        org_cmd.err_f = err
        # Delete NEW_ORG_TEST
        org_cmd.delete()

        response = err.getvalue().strip()
        # Response:
        # [0] NEW_ORG_TEST doesn't exist!
        self.assertIn("NEW_ORG_TEST doesn't exist!", response)

    def test_org_list_services(self):
        self.init()

        org_name = "SNET_BH"
        argv = ["organization", "list-services", org_name]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args)
        err = StringIO()
        org_cmd.err_f = err
        org_cmd.list_services()
        response = err.getvalue().strip()
        # Response:
        # [0] List of ORG_NAME's Services:
        # [1] - SERVICE_NAME_1
        # [2] - SERVICE_NAME_2
        # [n] - SERVICE_NAME_n
        self.assertGreaterEqual(len(response.split('\n')), 1)

    def test_org_change_owner(self):
        self.init()

        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        org_name = "NEW_ORG_TEST"

        new_owner = "0x7fA3FBCFAc5c56367cB33821968Fc8c086199989"

        argv = ["organization", "change-owner", no_confirm, gas_price_f, gas_price, org_name, new_owner]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args)

        err = StringIO()
        org_cmd.err_f = err
        # Change owner of NEW_ORG_TEST
        org_cmd.change_owner()

        response = err.getvalue().strip()
        # Response (org must exist):
        # [0] Creating transaction to change organization NEW_ORG_TEST's owner...
        self.assertIn("Creating transaction to change organization NEW_ORG_TEST's owner...", response)

    def test_org_add_members(self):
        self.init()

        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        org_name = "NEW_ORG_TEST"

        member_1 = "0x4444444444444444444444444444444444444444"
        member_2 = "0x5555555555555555555555555555555555555555"
        members = "{},{}".format(member_1, member_2)

        argv = ["organization", "add-members", no_confirm, gas_price_f, gas_price, org_name, members]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args)

        err = StringIO()
        org_cmd.err_f = err
        # Add members into NEW_ORG_TEST
        org_cmd.add_members()

        response = err.getvalue().strip()
        # Response (org must exists):
        # [0] Creating transaction to add [n] members into organization NEW_ORG_TEST...
        self.assertIn("Creating transaction to add", response)

    def test_org_rem_members(self):
        self.init()

        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        org_name = "NEW_ORG_TEST"

        member_1 = "0x4444444444444444444444444444444444444444"
        member_2 = "0x5555555555555555555555555555555555555555"
        members = "{},{}".format(member_1, member_2)

        argv = ["organization", "rem-members", no_confirm, gas_price_f, gas_price, org_name, members]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args)

        err = StringIO()
        org_cmd.err_f = err
        # Remove members from NEW_ORG_TEST
        org_cmd.rem_members()

        response = err.getvalue().strip()
        # Response (org must exists):
        # [0] Creating transaction to remove [n] members from organization NEW_ORG_TEST...
        self.assertIn("Creating transaction to remove", response)


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