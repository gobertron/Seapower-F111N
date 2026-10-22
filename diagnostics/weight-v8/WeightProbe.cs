// Original Version 8 diagnostic code. Reads game state; never changes it.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Reflection;

namespace RANF111N.WeightV8
{
    public sealed class Reading
    {
        public string Kind, Name;
        public double Value;
        public Reading(string kind, string name, double value)
        { Kind = kind; Name = name; Value = value; }
    }

    public static class WeightProbe
    {
        const BindingFlags Flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;
        public static object Get(object instance, string name)
        {
            if (instance == null) return null;
            for (Type t = instance.GetType(); t != null; t = t.BaseType)
            {
                try
                {
                    FieldInfo f = t.GetField(name, Flags);
                    if (f != null) return f.GetValue(instance);
                    PropertyInfo p = t.GetProperty(name, Flags);
                    if (p != null && p.GetIndexParameters().Length == 0 && p.GetGetMethod(true) != null)
                        return p.GetValue(instance, null);
                }
                catch { return null; }
            }
            return null;
        }

        public static bool Number(object value, out double number)
        {
            number = 0;
            if (value == null || value is bool || value is char || value is string || value.GetType().IsEnum) return false;
            if (!(value is IConvertible)) value = Get(value, "Value"); // UniRx numeric property
            if (value == null || value is bool || value is char || value is string || !(value is IConvertible) || value.GetType().IsEnum) return false;
            try { number = Convert.ToDouble(value, CultureInfo.InvariantCulture); }
            catch { return false; }
            return !Double.IsNaN(number) && !Double.IsInfinity(number);
        }

        public static string Definition(object aircraft)
        {
            object parameters = Get(aircraft, "_obp");
            string path = Convert.ToString(Get(parameters, "_objectIniName"), CultureInfo.InvariantCulture).Replace('\\', '/');
            int slash = path.LastIndexOf('/');
            if (slash >= 0) path = path.Substring(slash + 1);
            if (path.EndsWith(".ini", StringComparison.OrdinalIgnoreCase)) path = path.Substring(0, path.Length - 4);
            return path;
        }

        public static bool IsNavalWing(string id)
        {
            foreach (string role in new [] { "f", "fb", "rf", "ef" })
            {
                string root = "ran_" + role + "-111n";
                if (id == root || id == root + "_1985" || id == root + "_1995" || id == root + "_2003") return true;
            }
            return false;
        }

        static bool Metric(string name)
        {
            string n = name.ToLowerInvariant();
            return n.Contains("mass") || n.Contains("weight") || n.Contains("fuel") || n == "rangeinkm" || n == "actualrangeinkm";
        }

        static bool Branch(string name)
        {
            string n = name.ToLowerInvariant();
            return n == "_obp" || n == "_ap" || n == "_fp" || n.Contains("motioncontroller") ||
                   n.Contains("flightmodel") || n.Contains("flightphysics") || n.Contains("parameters") || n == "performance";
        }

        static bool BranchType(Type type)
        {
            string name = type.FullName ?? "";
            return name.StartsWith("SeaPower.", StringComparison.Ordinal) &&
                   (name.Contains("Parameters") || name.Contains("Physics") || name.Contains("Controller") || name.Contains("FlightModel"));
        }

        static void Scan(object owner, string path, int depth, List<Reading> output, HashSet<object> seen, bool schema = false)
        {
            if (owner == null || depth > 3 || !seen.Add(owner)) return;
            var names = new Dictionary<string, Type>();
            for (Type t = owner.GetType(); t != null; t = t.BaseType)
            {
                foreach (FieldInfo field in t.GetFields(Flags))
                    if (!names.ContainsKey(field.Name)) names.Add(field.Name, field.FieldType);
                foreach (PropertyInfo property in t.GetProperties(Flags))
                    if (property.GetIndexParameters().Length == 0 && !names.ContainsKey(property.Name)) names.Add(property.Name, property.PropertyType);
            }
            foreach (string name in names.Keys)
            {
                if (schema) output.Add(new Reading("schema", path + "." + name + ":" + names[name].FullName, 0));
                bool branch = Branch(name) || BranchType(names[name]);
                if (!Metric(name) && !branch) continue;
                object value = Get(owner, name);
                double number;
                if (Metric(name) && Number(value, out number)) output.Add(new Reading("metric", path + "." + name, number));
                else if (branch && value != null && !(value is string) && !(value is IEnumerable))
                    Scan(value, path + "." + name, depth + 1, output, seen, schema);
            }
        }

        public static List<Reading> Read(object aircraft, bool schema = false)
        {
            var result = new List<Reading>();
            Scan(aircraft, "aircraft", 0, result, new HashSet<object>(), schema);
            // This is the same ammunition total the game's weapon panel displays.
            IEnumerable inventory = Get(aircraft, "AmmunitionAmountDictionary") as IEnumerable;
            result.Add(new Reading("status", "inventory_available", inventory != null ? 1 : 0));
            if (inventory != null)
                foreach (object pair in inventory)
                {
                    string name = Convert.ToString(Get(pair, "Key"), CultureInfo.InvariantCulture);
                    double count;
                    if (!String.IsNullOrEmpty(name) && Number(Get(pair, "Value"), out count))
                        result.Add(new Reading("ammunition", name, count));
                }
            // Record the game's loaded ammunition parameters separately from the
            // release catalogue, including any overrides from another enabled mod.
            IEnumerable ammunition = Get(aircraft, "AmmunitionNameToAmmunitionDictionary") as IEnumerable;
            if (ammunition != null)
                foreach (object pair in ammunition)
                {
                    string name = Convert.ToString(Get(pair, "Key"), CultureInfo.InvariantCulture);
                    object parameters = Get(Get(pair, "Value"), "_ap");
                    if (parameters == null || String.IsNullOrEmpty(name)) continue;
                    var metrics = new List<Reading>();
                    Scan(parameters, name, 3, metrics, new HashSet<object>());
                    foreach (Reading metric in metrics) result.Add(new Reading("ammunition_parameter", metric.Name, metric.Value));
                }
            result.Sort((a, b) => String.CompareOrdinal(a.Kind + a.Name, b.Kind + b.Name));
            return result;
        }
    }
}
