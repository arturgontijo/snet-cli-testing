import unittest

from io import StringIO
import os
import shutil
import json

from snet_cli.config import conf
from snet_cli import arguments
from snet_cli.commands import ServiceCommand


class ServiceCommandTests(unittest.TestCase):
    def setUp(self):
        self.config = conf
        self.service_json = {
            "name":         "MyService",
            "service_spec": "service_spec/",
            "organization": "NEW_ORG_TEST",
            "path":         "",
            "price":        1,
            "endpoint":     "http://localhost:7000",
            "tags":         ["TAG1","TAG2","TAG3"],
            "metadata":     {
                "description": "My description."
                             }
        }
        self.output_f = StringIO()

    def _service_json(self, update=False, **kwargs):
        if update:
            with open("service.json", "r") as f:
                self.service_json = json.load(f)
            if kwargs.get("price"):
                self.service_json["price"] = kwargs.get("price")
            if kwargs.get("endpoint"):
                self.service_json["endpoint"] = kwargs.get("endpoint")
        with open("service.json", "w") as f:
            json.dump(self.service_json, f, indent=4, ensure_ascii=False)

    def test_1_service_init(self):
        # -y: accept defaults for any argument that is not provided
        argv = ["service", "init", "-y"]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        service_cmd = ServiceCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Init (create) a new service json file
        service_cmd.init()

        response = self.output_f.getvalue().strip()
        # Response:
        # {
        #     "name": "snet-cli-testing",
        #     "service_spec": "service_spec/",
        #     "organization": "",
        #     "path": "",
        #     "price": 0,
        #     "endpoint": "",
        #     "tags": [],
        #     "metadata": {
        #         "description": ""
        #     }
        # }
        self.assertIn("name", response)
        self.assertIn("service_spec", response)
        self.assertIn("organization", response)

    def test_2_service_publish(self):
        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        argv = ["service", "publish", no_confirm, gas_price_f, gas_price]

        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        service_cmd = ServiceCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        self._service_json()
        if not os.path.exists("service_spec/"):
            os.makedirs("service_spec/")

        # Publish the service on network
        service_cmd.publish()

        if os.path.exists("service_spec/"):
            shutil.rmtree("service_spec/")

        response = self.output_f.getvalue().strip()
        # Response:
        # Service published!
        self.assertIn("Service published!", response)

    def test_3_service_update(self):
        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        argv = ["service", "update", no_confirm, gas_price_f, gas_price]

        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        service_cmd = ServiceCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        self._service_json(update=True, price=2, endpoint="http://localhost:7777")
        if not os.path.exists("service_spec/"):
            os.makedirs("service_spec/")

        # Update a published service
        service_cmd.update()

        if os.path.exists("service_spec/"):
            shutil.rmtree("service_spec/")

        response = self.output_f.getvalue().strip()
        # Response:
        # Service is updated!
        self.assertIn("Service is updated!", response)

    def test_4_service_delete(self):
        no_confirm = "--no-confirm"
        gas_price_f = "--gas-price"
        gas_price = "1000000000"

        argv = ["service", "delete", no_confirm, gas_price_f, gas_price, self.service_json["organization"], self.service_json["name"]]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        service_cmd = ServiceCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Delete the service on network
        service_cmd.delete()

        response = self.output_f.getvalue().strip()
        # Response:
        # Removing current contract address from session...
        #
        # unset current_agent_at
        #
        # Service was deleted!
        self.assertIn("Service was deleted!", response)


if __name__ == "__main__":
    unittest.main()