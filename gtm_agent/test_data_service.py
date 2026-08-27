import unittest
import importlib.util
import sys
import types
from pathlib import Path


package_root = Path(__file__).parent
package = types.ModuleType("gtm_agent")
package.__path__ = [str(package_root)]
sys.modules["gtm_agent"] = package

records_spec = importlib.util.spec_from_file_location(
    "gtm_agent.gtm_records", package_root / "gtm_records.py"
)
records_module = importlib.util.module_from_spec(records_spec)
sys.modules[records_spec.name] = records_module
records_spec.loader.exec_module(records_module)

data_service_spec = importlib.util.spec_from_file_location(
    "gtm_agent.data_service", package_root / "data_service.py"
)
data_service = importlib.util.module_from_spec(data_service_spec)
sys.modules[data_service_spec.name] = data_service
data_service_spec.loader.exec_module(data_service)


class UpdateProspectInfoTest(unittest.TestCase):
    def setUp(self):
        self.original_stack = list(data_service.PROSPECTS["LEAD-71001"]["tech_stack"])
        data_service._PROFILES.pop("LEAD-71001", None)

    def tearDown(self):
        data_service.PROSPECTS["LEAD-71001"]["tech_stack"] = self.original_stack
        data_service._PROFILES.pop("LEAD-71001", None)

    def test_update_persists_technology(self):
        data_service.update_prospect_info("LEAD-71001", "Kafka")

        self.assertIn("Kafka", data_service.fetch_tech_stack("LEAD-71001"))


if __name__ == "__main__":
    unittest.main()
