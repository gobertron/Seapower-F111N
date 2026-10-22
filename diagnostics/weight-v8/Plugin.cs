// Optional BepInEx 5 monitor for the user's existing Anchor Chain installation.
// No Harmony patches, physics writes, game assembly replacement or network IO.
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Reflection;
using BepInEx;
using UnityEngine;

namespace RANF111N.WeightV8
{
    [BepInPlugin("com.gobertron.f111n.weight.v8", "RAN F-111N Weight Monitor Version 8", "8.0.0")]
    public sealed class Plugin : BaseUnityPlugin
    {
        StreamWriter writer;
        Type aircraftType;
        float nextSample;
        long sample;
        readonly HashSet<string> schemas = new HashSet<string>();
        bool stopped;
        const long MaximumBytes = 40L * 1024L * 1024L;
        static readonly CultureInfo Invariant = CultureInfo.InvariantCulture;

        void Awake()
        {
            try
            {
                string folder = Path.Combine(Paths.GameRootPath, "RAN-F111N-weight-V8");
                Directory.CreateDirectory(folder);
                string path = Path.Combine(folder, "weight-v8-" + DateTime.UtcNow.ToString("yyyyMMdd-HHmmss-fffffff", Invariant) + ".csv");
                writer = new StreamWriter(new FileStream(path, FileMode.CreateNew, FileAccess.Write, FileShare.Read));
                writer.WriteLine("sample,realtime_s,unit_key,aircraft_id,kind,name,value");
                writer.Flush();
                Logger.LogInfo("Version 8 read-only weight recording: " + path);
            }
            catch (Exception error) { stopped = true; Logger.LogError("Weight recording unavailable: " + error.Message); }
        }

        static string Csv(string value) { return "\"" + value.Replace("\"", "\"\"") + "\""; }

        void Update()
        {
            if (stopped || writer == null || Time.realtimeSinceStartup < nextSample) return;
            nextSample = Time.realtimeSinceStartup + 1f;
            try
            {
                if (aircraftType == null)
                    foreach (Assembly assembly in AppDomain.CurrentDomain.GetAssemblies())
                    {
                        aircraftType = assembly.GetType("SeaPower.Aircraft", false);
                        if (aircraftType != null) break;
                    }
                if (aircraftType == null) return;
                sample++;
                int count = 0;
                foreach (UnityEngine.Object candidate in Resources.FindObjectsOfTypeAll(aircraftType))
                {
                    Component aircraft = candidate as Component;
                    if (aircraft == null || !aircraft.gameObject.activeInHierarchy) continue;
                    object destroyed = WeightProbe.Get(aircraft, "IsDestroyed");
                    if (destroyed is bool && (bool)destroyed) continue;
                    string id = WeightProbe.Definition(aircraft);
                    if (!WeightProbe.IsNavalWing(id)) continue;
                    double uniqueId;
                    if (!WeightProbe.Number(WeightProbe.Get(aircraft, "UniqueID"), out uniqueId) || uniqueId <= 0) continue;
                    if (++count > 64) break;
                    string key = aircraft.GetInstanceID().ToString(Invariant) + ":" + uniqueId.ToString(Invariant);
                    object controller = WeightProbe.Get(aircraft, "Motioncontroller");
                    string schemaKey = id + ":" + (controller == null ? "none" : controller.GetType().FullName);
                    foreach (Reading value in WeightProbe.Read(aircraft, schemas.Add(schemaKey)))
                        writer.WriteLine(sample.ToString(Invariant) + "," + Time.realtimeSinceStartup.ToString("R", Invariant) + "," +
                            Csv(key) + "," + Csv(id) + "," + Csv(value.Kind) + "," + Csv(value.Name) + "," + value.Value.ToString("R", Invariant));
                }
                writer.Flush();
                if (writer.BaseStream.Position >= MaximumBytes)
                {
                    stopped = true;
                    Logger.LogWarning("Version 8 weight recording reached 40 MiB; restart for another recording.");
                    writer.Dispose(); writer = null;
                }
            }
            catch (Exception error)
            {
                stopped = true;
                Logger.LogError("Version 8 weight monitor stopped without changing game state: " + error);
                if (writer != null) { writer.Dispose(); writer = null; }
            }
        }

        void OnDestroy() { if (writer != null) { writer.Dispose(); writer = null; } }
    }
}
