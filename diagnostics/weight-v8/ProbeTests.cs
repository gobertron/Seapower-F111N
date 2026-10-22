// Engine-free verification of reflection and inventory capture, not a flight test.
using System;
using System.Collections.Generic;
using RANF111N.WeightV8;

class Parameters { public string _objectIniName = "aircraft/ran_fb-111n_2003.ini"; public double _emptyMass = 26975; }
class AmmoParameters { public double _mass = 526; }
class Ammo { public AmmoParameters _ap = new AmmoParameters(); }
class Reactive { public float Value { get; set; } }
class Physics { public double Mass = 46595; public Reactive FuelMass = new Reactive { Value = 14897 }; }
class AircraftBase
{
    public Parameters _obp = new Parameters();
    public Physics Motioncontroller = new Physics();
    public Dictionary<string, int> AmmunitionAmountDictionary = new Dictionary<string, int> { { "ran_nw_harpoonl", 7 } };
    public Dictionary<string, Ammo> AmmunitionNameToAmmunitionDictionary = new Dictionary<string, Ammo> { { "ran_nw_harpoonl", new Ammo() } };
}
class FakeAircraft : AircraftBase { public double FuelMass { get { throw new Exception("Unavailable getter"); } } }

class ProbeTests
{
    static int checks;
    static void Assert(bool ok, string message) { checks++; if (!ok) throw new Exception(message); }
    static Reading Find(List<Reading> rows, string kind, string name) { return rows.Find(x => x.Kind == kind && x.Name == name); }
    static void Main()
    {
        var aircraft = new FakeAircraft();
        Assert(WeightProbe.Definition(aircraft) == "ran_fb-111n_2003", "Definition including path/extension");
        foreach (string role in new [] { "f", "fb", "rf", "ef" })
            foreach (string year in new [] { "", "_1985", "_1995", "_2003" })
                Assert(WeightProbe.IsNavalWing("ran_" + role + "-111n" + year), "All sixteen IDs");
        Assert(!WeightProbe.IsNavalWing("usn_f-14a"), "Do not monitor other aircraft");
        Assert(!WeightProbe.IsNavalWing("ran_fb-111n_2003_squadrons"), "Do not match squadron definitions");
        var before = WeightProbe.Read(aircraft);
        Assert(Find(before, "metric", "aircraft.Motioncontroller.Mass").Value == 46595, "Live controller mass");
        Assert(Find(before, "metric", "aircraft.Motioncontroller.FuelMass").Value == 14897, "Reactive fuel value");
        Assert(Find(before, "metric", "aircraft._obp._emptyMass").Value == 26975, "Separate static parameter");
        Assert(Find(before, "ammunition", "ran_nw_harpoonl").Value == 7, "Inventory count");
        Assert(Find(before, "ammunition_parameter", "ran_nw_harpoonl._mass").Value == 526, "Live store mass");
        Assert(WeightProbe.Read(aircraft, true).Exists(x => x.Kind == "schema" && x.Name.Contains("Motioncontroller")), "Field layout recorded on request");
        aircraft.AmmunitionAmountDictionary["ran_nw_harpoonl"] = 6;
        aircraft.Motioncontroller.Mass -= 536;
        aircraft.Motioncontroller.FuelMass.Value -= 10;
        var after = WeightProbe.Read(aircraft);
        Assert(Find(after, "metric", "aircraft.Motioncontroller.Mass").Value == 46059, "Fresh mass after release");
        Assert(Find(after, "ammunition", "ran_nw_harpoonl").Value == 6, "Fresh count after release");
        Assert(aircraft.Motioncontroller.Mass == 46059 && aircraft.AmmunitionAmountDictionary["ran_nw_harpoonl"] == 6, "No state writes");
        double number;
        Assert(!WeightProbe.Number(true, out number), "Ignore flags");
        Assert(!WeightProbe.Number(Double.NaN, out number), "Ignore invalid values");
        Assert(!WeightProbe.Number("526", out number), "Ignore strings");
        Console.WriteLine("Version 8 reflection checks passed: " + checks);
    }
}
