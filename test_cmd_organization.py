import unittest
from io import StringIO

from snet_cli.config import conf
from snet_cli import arguments
from snet_cli.commands import OrganizationCommand


class OrganizationCommandTests(unittest.TestCase):
    def setUp(self):
        self.config = conf
        self.output_f = StringIO()

    def test_1_org_list(self):
        argv = ["organization", "list"]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # List all registered Organizations
        org_cmd.list()

        response = self.output_f.getvalue().strip()
        # Response:
        # [0] List of Organizations:
        # [1] - ORG_NAME_1
        # [2] - ORG_NAME_2
        # [n] - ORG_NAME_n
        self.assertGreaterEqual(len(response.split('\n')), 1)

    def test_2_org_info(self):
        org_name = "SNET_BH"
        argv = ["organization", "info", org_name]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Get information about an Organization
        org_cmd.info()

        response = self.output_f.getvalue().strip()
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

    def test_3_org_create(self):
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

        org_cmd = OrganizationCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Create NEW_ORG_TEST
        org_cmd.create()

        # Try to create NEW_ORG_TEST again
        org_cmd.create()

        response = self.output_f.getvalue().strip()
        # Response (org already exists):
        # [0] NEW_ORG_TEST already exists!
        self.assertIn("NEW_ORG_TEST already exists", response)

    def test_4_org_list_services(self):
        org_name = "SNET_BH"
        argv = ["organization", "list-services", org_name]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # List all organization's services
        org_cmd.list_services()

        response = self.output_f.getvalue().strip()
        # Response:
        # [0] List of ORG_NAME's Services:
        # [1] - SERVICE_NAME_1
        # [2] - SERVICE_NAME_2
        # [n] - SERVICE_NAME_n
        self.assertGreaterEqual(len(response.split('\n')), 1)

    def test_5_org_add_members(self):
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

        org_cmd = OrganizationCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Add members into NEW_ORG_TEST
        org_cmd.add_members()

        response = self.output_f.getvalue().strip()
        # Response (org must exists):
        # [0] Creating transaction to add [n] members into organization NEW_ORG_TEST...
        self.assertIn("Creating transaction to add", response)

    def test_6_org_rem_members(self):
        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        org_name = "NEW_ORG_TEST"

        member_1 = "0x2222222222222222222222222222222222222222"
        member_2 = "0x3333333333333333333333333333333333333333"
        members = "{},{}".format(member_1, member_2)

        argv = ["organization", "rem-members", no_confirm, gas_price_f, gas_price, org_name, members]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Remove members from NEW_ORG_TEST
        org_cmd.rem_members()

        response = self.output_f.getvalue().strip()
        # Response (org must exists):
        # [0] Creating transaction to remove [n] members from organization NEW_ORG_TEST...
        self.assertIn("Creating transaction to remove", response)

    def test_7_org_delete_existent(self):
        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        org_name = "NEW_ORG_TEST"

        argv = ["organization", "delete", no_confirm, gas_price_f, gas_price, org_name]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Delete NEW_ORG_TEST
        org_cmd.delete()

        response = self.output_f.getvalue().strip()
        # Response:
        # [0] Creating transaction to delete organization NEW_ORG_TEST...
        # [1] Submitting transaction...
        self.assertIn("Creating transaction to delete organization NEW_ORG_TEST...", response)

    def test_8_org_delete_nonexistent(self):
        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        org_name = "NEW_ORG_TEST"

        argv = ["organization", "delete", no_confirm, gas_price_f, gas_price, org_name]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Delete NEW_ORG_TEST
        org_cmd.delete()

        response = self.output_f.getvalue().strip()
        # Response:
        # [0] NEW_ORG_TEST doesn't exist!
        self.assertIn("NEW_ORG_TEST doesn't exist!", response)

    def test_9_org_change_owner(self):
        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        org_name = "NEW_ORG_TEST"

        new_owner = "0x7fA3FBCFAc5c56367cB33821968Fc8c086199989"

        argv = ["organization", "change-owner", no_confirm, gas_price_f, gas_price, org_name, new_owner]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        org_cmd = OrganizationCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Change owner of NEW_ORG_TEST (doesn't exist anymore...)
        # If you change the NEW_ORG_TEST's owner you'll have to change your
        # session private_key (new owner) to keep interacting with it.
        org_cmd.change_owner()

        response = self.output_f.getvalue().strip()
        # Response (org must exist):
        # [0] Creating transaction to change organization NEW_ORG_TEST's owner...
        # [-] But: NEW_ORG_TEST doesn't exist!
        self.assertIn("NEW_ORG_TEST doesn't exist!", response)


if __name__ == '__main__':
    unittest.main()