import unittest
import importlib.util
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def import_from_path(rel_path, module_name=None):
    full_path = os.path.join(ROOT_DIR, rel_path)
    if module_name is None:
        module_name = os.path.splitext(os.path.basename(rel_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Modülleri yükle
data_analyzer = import_from_path("software/python/data_analyzer.py")
cloud_cost = import_from_path("software/cloud/cloud_cost_calculator.py")
electrical_calc = import_from_path("automation-electronics/circuit-design/electrical_calculator.py")
modbus_sim = import_from_path("automation-electronics/plc-scada/modbus_simulator.py")
gcode_gen = import_from_path("mechanical-civil/cad-cam/gcode_generator.py")
cpm_calc = import_from_path("mechanical-civil/project-management/cpm_calculator.py")
beam_calc = import_from_path("mechanical-civil/structural-mechanics/beam_stress_calculator.py")
fluid_calc = import_from_path("chemical-process/process-engineering/fluid_thermal_calculator.py")
oee_calc = import_from_path("industrial-engineering/lean-six-sigma/oee_sigma_calculator.py")
carbon_calc = import_from_path("environment/sustainability-reports/carbon_footprint.py")
power_calc = import_from_path("energy-engineering/renewables/power_calculator.py")
bess_calc = import_from_path("energy-engineering/storage-grid/bess_storage_calculator.py")


class TestSoftwareTools(unittest.TestCase):
    def test_stats_calculation(self):
        data = [10.0, 20.0, 30.0, 40.0, 50.0]
        stats = data_analyzer.calculate_stats(data)
        self.assertEqual(stats["N"], 5)
        self.assertAlmostEqual(stats["Ortalama"], 30.0)
        self.assertAlmostEqual(stats["Medyan"], 30.0)
        self.assertAlmostEqual(stats["Min"], 10.0)
        self.assertAlmostEqual(stats["Max"], 50.0)
        self.assertAlmostEqual(stats["Standart Sapma"], 15.811388, places=4)

    def test_linear_regression(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        reg = data_analyzer.linear_regression(x, y)
        self.assertIsNotNone(reg)
        self.assertAlmostEqual(reg["egim (m)"], 2.0)
        self.assertAlmostEqual(reg["kesim (c)"], 0.0)
        self.assertAlmostEqual(reg["R_kare (R2)"], 1.0)

    def test_quadratic_regression(self):
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 9, 16, 25]  # y = x^2
        qreg = data_analyzer.quadratic_regression(x, y)
        self.assertIsNotNone(qreg)
        self.assertAlmostEqual(qreg["a (x^2)"], 1.0, places=4)
        self.assertAlmostEqual(qreg["b (x)"], 0.0, places=4)
        self.assertAlmostEqual(qreg["c (sabit)"], 0.0, places=4)

    def test_unit_conversions(self):
        self.assertAlmostEqual(data_analyzer.celsius_to_fahrenheit(0), 32.0)
        self.assertAlmostEqual(data_analyzer.fahrenheit_to_celsius(32), 0.0)
        self.assertAlmostEqual(data_analyzer.bar_to_psi(1.0), 14.5038, places=3)
        self.assertAlmostEqual(data_analyzer.psi_to_bar(14.5038), 1.0, places=3)
        self.assertAlmostEqual(data_analyzer.inch_to_mm(1.0), 25.4)
        self.assertAlmostEqual(data_analyzer.mm_to_inch(25.4), 1.0)
        self.assertAlmostEqual(data_analyzer.mps_to_kmh(10.0), 36.0)

    def test_cloud_cost_calculator(self):
        res, err = cloud_cost.estimate_cloud_cost(vcpu_count=4, ram_gb=16, storage_gb=200, egress_gb_month=50, running_hours_month=730)
        self.assertIsNone(err)
        self.assertGreater(res["Aylık On-Demand Maliyet ($)"], 0)
        self.assertGreater(res["Yıllık 1-Yıl Rezerv Tasarrufu ($)"], 0)
        self.assertGreater(res["Aylık Karbon Emisyonu (kg CO2e)"], 0)


class TestElectricalTools(unittest.TestCase):
    def test_voltage_drop_3phase(self):
        res, err = electrical_calc.calculate_voltage_drop(voltage=400, current=30, length_m=100, section_mm2=10, material="bakir", system_type="3phase")
        self.assertIsNone(err)
        self.assertGreater(res["Gerilim Düşümü (V)"], 0)
        self.assertLess(res["Gerilim Düşümü Oranı (%)"], 5.0)

    def test_voltage_drop_1phase(self):
        res, err = electrical_calc.calculate_voltage_drop(voltage=230, current=16, length_m=30, section_mm2=2.5, material="bakir", system_type="1phase")
        self.assertIsNone(err)
        self.assertGreater(res["Gerilim Düşümü (V)"], 0)

    def test_filter_resonance(self):
        r = 1000.0  # 1k Ohm
        c = 1e-6    # 1 uF
        l = 0.1     # 100 mH
        res = electrical_calc.calculate_filter_resonance(r, l, c)
        self.assertIn("RC Kesim Frekansı (Cutoff fc - Hz)", res)
        self.assertIn("RLC Rezonans Frekansı (f0 - Hz)", res)
        self.assertAlmostEqual(res["RLC Rezonans Frekansı (f0 - Hz)"], 503.29, delta=1.0)

    def test_power_factor_compensation(self):
        res, err = electrical_calc.calculate_power_factor_compensation(active_power_kw=100, current_cos_phi=0.75, target_cos_phi=0.98)
        self.assertIsNone(err)
        self.assertGreater(res["Gereken Kondansatör Gücü (kVAR)"], 0)
        self.assertGreater(res["Şebekeden Çekilen Güç Tasarrufu (kVA)"], 0)


class TestAutomationTools(unittest.TestCase):
    def test_modbus_simulator_scan(self):
        plc = modbus_sim.PLCSimulator()
        self.assertEqual(plc.coils[1], False)
        plc.coils[1] = True
        plc.scan_cycle()
        self.assertGreater(plc.input_registers[3003], 0)

    def test_modbus_emergency_stop(self):
        plc = modbus_sim.PLCSimulator()
        plc.coils[1] = True
        plc.scan_cycle()
        plc.discrete_inputs[101] = True
        plc.scan_cycle()
        self.assertEqual(plc.coils[1], False)
        self.assertEqual(plc.input_registers[3003], 0)
        self.assertEqual(plc.coils[3], True)


class TestMechanicalTools(unittest.TestCase):
    def test_gcode_generation(self):
        rect_gcode = gcode_gen.generate_rectangular_gcode(50, 80, -2, 5, 800, 3000, 6, "dummy.nc")
        self.assertIn("G21", rect_gcode)
        self.assertIn("M03 S3000", rect_gcode)
        self.assertIn("M30", rect_gcode)

        circ_gcode = gcode_gen.generate_circular_gcode(60, -2, 5, 600, 2500, 6, "dummy.nc")
        self.assertIn("G02", circ_gcode)

    def test_cpm_critical_path(self):
        tasks = {
            "A": cpm_calc.Task("A", 2, 2, 2, []),
            "B": cpm_calc.Task("B", 3, 3, 3, ["A"]),
            "C": cpm_calc.Task("C", 4, 4, 4, ["A"]),
            "D": cpm_calc.Task("D", 2, 2, 2, ["B", "C"])
        }
        topo_order, duration = cpm_calc.solve_cpm(tasks)
        self.assertIsNotNone(topo_order)
        # Kritik yol elemanlarını tespit et
        critical_path = [u for u in topo_order if abs(tasks[u].slack) < 0.0001]
        self.assertEqual(critical_path, ["A", "C", "D"])
        self.assertAlmostEqual(duration, 8.0)

    def test_beam_mechanics(self):
        sec, err = beam_calc.calculate_section_properties("rectangle", b=50, h=100)
        self.assertIsNone(err)
        self.assertAlmostEqual(sec["Atalet Momenti Ix (mm⁴)"], (50 * 100**3) / 12.0)
        
        bm, err2 = beam_calc.calculate_beam_mechanics(1, 5000, 2.0, sec["Atalet Momenti Ix (mm⁴)"], sec["Mukavemet Momenti Wx (mm³)"], 210.0, 235.0)
        self.assertIsNone(err2)
        self.assertIn("Maksimum Eğilme Momenti", bm)
        self.assertIn("GÜVENLİ", bm["Gerilme Emniyeti"])


class TestChemicalProcessTools(unittest.TestCase):
    def test_pipe_friction_laminar(self):
        res, err = fluid_calc.calculate_pipe_friction(flow_rate_m3h=0.1, inner_dia_mm=50, pipe_length_m=10)
        self.assertIsNone(err)
        self.assertEqual(res["Akış Rejimi"], "Laminer Akış")
        self.assertAlmostEqual(res["Darcy Sürtünme Katsayısı (f)"], 64.0 / res["Reynolds Sayısı (Re)"], places=4)

    def test_pipe_friction_turbulent(self):
        res, err = fluid_calc.calculate_pipe_friction(flow_rate_m3h=20.0, inner_dia_mm=50, pipe_length_m=100)
        self.assertIsNone(err)
        self.assertEqual(res["Akış Rejimi"], "Türbülanslı Akış")
        self.assertGreater(res["Basınç Kaybı (Bar)"], 0)

    def test_heat_exchanger_lmtd(self):
        res, err = fluid_calc.calculate_heat_exchanger_lmtd(th_in=90, th_out=60, tc_in=20, tc_out=50, u_coeff=1000, flow_type="counter")
        self.assertIsNone(err)
        self.assertAlmostEqual(res["LMTD (°C)"], 40.0, places=2)

    def test_solution_dilution(self):
        res, err = fluid_calc.calculate_solution_dilution(c1=30, v1=10, c2=0, target_c=10)
        self.assertIsNone(err)
        self.assertAlmostEqual(res["Eklenmesi Gereken Çözücü Miktarı"], 20.0)


class TestIndustrialAndQualityTools(unittest.TestCase):
    def test_oee_calculation(self):
        res, err = oee_calc.calculate_oee(planned_time=480, planned_down=30, unplanned_down=30, ideal_cycle=1.0, total_units=20000, reject_units=500)
        self.assertIsNone(err)
        self.assertGreater(res["OEE %"], 0)
        self.assertLessEqual(res["OEE %"], 100.0)

    def test_six_sigma_calculation(self):
        res, err = oee_calc.calculate_six_sigma(n_units=1000, opportunities=10, n_defects=34)
        self.assertIsNone(err)
        self.assertAlmostEqual(res["DPMO (Hata/Milyon Fırsat)"], 3400.0)
        self.assertGreater(res["Sigma Seviyesi (1.5 Shift dahil)"], 4.0)

    def test_takt_time(self):
        takt, err = oee_calc.calculate_takt_time(available_time_sec=28800, demand=720)
        self.assertIsNone(err)
        self.assertAlmostEqual(takt, 40.0)

    def test_probit(self):
        self.assertAlmostEqual(oee_calc.probit(0.5), 0.0, places=2)


class TestEnvironmentAndEnergyTools(unittest.TestCase):
    def test_carbon_footprint(self):
        res = carbon_calc.calculate_footprint(nat_gas=1000, diesel=500, petrol=200, electricity=5000, flight_km=10000, commute_km=20000)
        self.assertGreater(res["Toplam Karbon Ayak İzi tCO2e"], 0)
        self.assertGreater(res["Scope 1 (Doğrudan) tCO2e"], 0)
        self.assertGreater(res["Scope 2 (Dolaylı Enerji) tCO2e"], 0)
        self.assertGreater(res["Scope 3 (Diğer Dolaylı) tCO2e"], 0)

    def test_bess_sizing(self):
        res, err = bess_calc.calculate_bess_sizing(daily_consumption_kwh=20.0, autonomy_days=1.0, system_voltage_v=48.0, chemistry="lifepo4")
        self.assertIsNone(err)
        self.assertGreater(res["Gereken Nominal Depolama Kapasitesi (kWh)"], 20.0)
        self.assertGreater(res["Gereken Toplam Kapasite (Ah)"], 0)

    def test_lcos(self):
        res, err = bess_calc.calculate_lcos(capex_usd=10000, opex_annual_usd=150, nominal_kwh=25.0, chemistry="lifepo4")
        self.assertIsNone(err)
        self.assertGreater(res["Düzleştirilmiş Depolama Maliyeti (LCOS $/kWh)"], 0)


if __name__ == "__main__":
    unittest.main()
