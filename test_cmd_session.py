import unittest
from io import StringIO

from snet_cli.config import conf
from snet_cli import arguments
from snet_cli.commands import SessionCommand


class SessionCommandTests(unittest.TestCase):
    def setUp(self):
        self.config = conf
        self.output_f = StringIO()

    def test_1_session_show(self):
        argv = ["session"]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        session_cmd = SessionCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Show session keys
        session_cmd.show()

        response = self.output_f.getvalue().strip()
        # Response:
        # [0] session:
        #         default_eth_rpc_endpoint: https://kovan.infura.io
        #         default_gas_price: '1000000000'
        #         default_wallet_index: '0'
        #         identity_name: MY_ID
        self.assertGreaterEqual(len(response.split('\n')), 1)

    def test_2_session_set(self):
        argv = ["set", "current_agent_at", "0x2222222222222222222222222222222222222222"]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        session_cmd = SessionCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Set session key 'current_agent_at'
        session_cmd.set()

        response = self.output_f.getvalue().strip()
        # Response:
        # [0] set current_agent_at 0x2222222222222222222222222222222222222222
        self.assertEqual(" ".join(argv), response)

    def test_3_session_unset(self):
        argv = ["unset", "current_agent_at"]
        parser = arguments.get_root_parser(self.config)
        args = parser.parse_args(argv)

        session_cmd = SessionCommand(self.config, args, out_f=self.output_f, err_f=self.output_f)

        # Unset session key 'current_agent_at'
        session_cmd.unset()

        response = self.output_f.getvalue().strip()
        # Response (if current_agent_at is set):
        # [0] unset current_agent_at
        # Response (if current_agent_at is not set):
        # [0] (no output)
        self.assertEqual(" ".join(argv), response)


if __name__ == '__main__':
    unittest.main()