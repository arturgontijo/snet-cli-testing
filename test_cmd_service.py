import unittest

from io import StringIO

from snet_cli.config import conf
from snet_cli import arguments
from snet_cli.commands import ServiceCommand


class ServiceCommandTests(unittest.TestCase):
    def setUp(self):
        self.config = conf
        self.output_f = StringIO()

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
        argv = ["service", "publish"]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        service_cmd = ServiceCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        os.mak
        # Show session keys
        service_cmd.publish()

        response = self.output_f.getvalue().strip()
        # Response:
        #
        self.assertGreaterEqual(len(response.split("\n")), 1)


if __name__ == "__main__":
    unittest.main()