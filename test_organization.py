import unittest
from io import StringIO

from snet_cli.config import conf
from snet_cli import arguments
from snet_cli.commands import OrganizationCommand


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


if __name__ == '__main__':
    unittest.main()