import unittest
from types import SimpleNamespace
from unittest.mock import patch

from gtm_agent.gtm_agent import send_prospect_email


class SendProspectEmailTest(unittest.TestCase):
    def setUp(self):
        self.runtime = SimpleNamespace(config={"metadata": {"user_id": "rep_sbrown"}})
        self.prospect = {
            "prospect_id": "LEAD-50003",
            "name": "Sofia Rossi",
            "email": "sofia.rossi@greenfieldnetworks.com",
        }

    @patch("gtm_agent.gtm_agent.data_service.get_prospect_record")
    def test_disqualified_prospect_is_blocked_without_message_id(self, get_prospect_record):
        get_prospect_record.return_value = {"disqualified": True}

        result = send_prospect_email.func(
            self.prospect, "Pricing Deck", "Hello", self.runtime
        )

        self.assertEqual(result["status"], "blocked")
        self.assertNotIn("message_id", result)

    @patch("gtm_agent.gtm_agent.data_service.get_rep")
    @patch("gtm_agent.gtm_agent.data_service.get_prospect_record")
    def test_qualified_prospect_is_sent(self, get_prospect_record, get_rep):
        get_prospect_record.return_value = {"disqualified": False}
        get_rep.return_value = {"email": "sara.brown@northpoint.com", "name": "Sara Brown"}

        result = send_prospect_email.func(
            self.prospect, "Pricing Deck", "Hello", self.runtime
        )

        self.assertEqual(result["status"], "sent")
        self.assertIn("message_id", result)


if __name__ == "__main__":
    unittest.main()
