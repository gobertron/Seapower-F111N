#!/usr/bin/env python3
"""Exercise stale Majestic lift references on representative native layouts.

The user's actual RAN source definitions are unavailable. These fixtures
reproduce the reported Elevator3/Elevator4 failures without inventing lifts.
"""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from carrier_compatibility import compatible, parse, put


def two_elevator_conversion(missing, donor="usn_cvn_nimitz.ini"):
    text = (ROOT / "authoring/reference_carriers" / donor).read_text()
    text = re.sub(r"(?ms)^\[Elevator[34]\][^\n]*\n.*?(?=^\[|\Z)", "", text)
    return put(text, "RecoveryPoint1", "AssociatedElevators", str(missing))


class ElevatorRepairTests(unittest.TestCase):
    def assert_valid_graph(self, data):
        paths = {s: p for s, p in data.items() if re.fullmatch(r"TaxiPath\d+", s)}
        count = int(data["FlightDeck"]["NumberOfTaxiPaths"])
        self.assertEqual(set(paths), {"TaxiPath" + str(i) for i in range(1, count + 1)})
        for section, path in paths.items():
            for endpoint in ("From", "To"):
                self.assertIn(path[endpoint], data, section + "/" + endpoint)
        for section, point in data.items():
            if re.fullmatch(r"RecoveryPoint\d+", section):
                for lift in point["AssociatedElevators"].split(","):
                    self.assertIn("Elevator" + lift, data, section)
            if re.fullmatch(r"LaunchPoint\d+", section):
                for route in filter(None, point.get("TaxiPath", "").split(",")):
                    composite = re.fullmatch(r"(Elevator\d+)(LaunchPoint\d+)", route)
                    if composite:
                        self.assertIn(composite[1], data)
                        self.assertEqual(composite[2], section)
                    else:
                        self.assertIn(route, paths)
                        self.assertEqual(paths[route]["To"], section)

    def test_both_reported_missing_lifts_use_existing_geometry(self):
        for name, missing, donor in [
            ("ran_cv_majestic1968", 3, "usn_cvn_nimitz.ini"),
            ("ran_majestic_59", 4, "usn_cv_forrestal_75.ini"),
        ]:
            with self.subTest(name=name):
                source = two_elevator_conversion(missing, donor)
                before = parse(source)
                output, report = compatible(source, name)
                after = parse(output)
                self.assert_valid_graph(after)
                self.assertEqual(after["RecoveryPoint1"]["AssociatedElevators"], "1")
                self.assertEqual(after["FlightDeck"]["NumberOfElevators"], "2")
                self.assertTrue(report["elevator_repairs"])
                self.assertTrue(report["disabled_invalid_taxi_paths"])
                self.assertEqual(compatible(output, name)[0], output)
                self.assertEqual({s for s in after if re.fullmatch(r"Elevator\d+", s)}, {"Elevator1", "Elevator2"})
                for repair in report["elevator_repairs"]:
                    if repair["section"].startswith("RecoveryPoint"):
                        for lift in repair["replacement"].split(","):
                            self.assertTrue(any(p.get("From") == repair["section"] and p.get("To") == "Elevator" + lift
                                                for s, p in after.items() if re.fullmatch(r"TaxiPath\d+", s)))
                for section, values in before.items():
                    if re.fullmatch(r"Elevator\d+", section):
                        for key, value in values.items():
                            if key != "AssociatedLaunchPoints":
                                self.assertEqual(after[section][key], value)
                    elif not section.startswith(("FlightDeck", "RecoveryPoint", "LaunchPoint", "TaxiPath")):
                        self.assertEqual(after[section], values)
                for key in ("Position", "Rotation", "AllowedType", "CircuitWaypoints", "HelicopterCircuitWaypoints"):
                    self.assertEqual(after["RecoveryPoint2"].get(key), before["RecoveryPoint2"].get(key))

    def test_existing_recovery_route_has_priority(self):
        source = put(two_elevator_conversion(3), "TaxiPath1", "To", "Elevator2")
        source = put(source, "Elevator2", "Unused", "False")
        output, _ = compatible(source, "ran_cv_majestic1968")
        data = parse(output)
        self.assertEqual(data["RecoveryPoint1"]["AssociatedElevators"], "2")
        self.assert_valid_graph(data)

    def test_valid_association_is_retained_when_other_lift_is_missing(self):
        source = put(two_elevator_conversion(3), "RecoveryPoint1", "AssociatedElevators", "2,4")
        output, _ = compatible(source, "ran_majestic_59")
        data = parse(output)
        self.assertEqual(data["RecoveryPoint1"]["AssociatedElevators"], "2")
        self.assert_valid_graph(data)

    def test_removed_path_indices_do_not_select_renumbered_routes(self):
        source = put(two_elevator_conversion(4), "LaunchPoint1", "TaxiPath", "TaxiPath2,TaxiPath3")
        source = put(source, "LaunchPoint3", "TaxiPath", "TaxiPath5")
        output, _ = compatible(source, "ran_majestic_59")
        data = parse(output)
        self.assertEqual(data["LaunchPoint1"]["TaxiPath"], "TaxiPath2")
        self.assertEqual(data["TaxiPath2"]["From"], "Elevator1")
        self.assertEqual(data["TaxiPath2"]["To"], "LaunchPoint1")
        self.assertRegex(data["LaunchPoint3"]["TaxiPath"], r"^Elevator[12]LaunchPoint3$")
        self.assert_valid_graph(data)
        self.assertEqual(compatible(output, "ran_majestic_59")[0], output)

    def test_missing_geometry_is_not_fabricated(self):
        source = two_elevator_conversion(3)
        source = re.sub(r"(?ms)^\[Elevator[12]\][^\n]*\n.*?(?=^\[|\Z)", "", source)
        with self.assertRaisesRegex(ValueError, "no usable defined elevator"):
            compatible(source, "ran_cv_majestic1968")

    def test_last_duplicate_association_is_repaired(self):
        source = two_elevator_conversion(3).replace("AssociatedElevators=3", "AssociatedElevators=1\nAssociatedElevators=3")
        output, report = compatible(source, "ran_cv_majestic1968")
        data = parse(output)
        self.assertEqual(data["RecoveryPoint1"]["AssociatedElevators"], "1")
        self.assertEqual(report["elevator_repairs"][0]["previous"], "3")
        self.assert_valid_graph(data)
        self.assertEqual(compatible(output, "ran_cv_majestic1968")[0], output)


if __name__ == "__main__":
    unittest.main()
